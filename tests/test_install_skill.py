from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
INSTALLER = REPO / "scripts" / "install-skill.sh"
VALIDATOR = REPO / "scripts" / "validate-skill.py"
SOURCE_SKILL = REPO / ".agents" / "skills" / "fde-project-work"


class SkillInstallerTests(unittest.TestCase):
    def make_repo(self, root: Path, name: str = "target") -> Path:
        target = root / name
        target.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=target, check=True)
        (target / "README.md").write_text("keep me\n", encoding="utf-8")
        return target

    def install(
        self, target: Path, agent: str, *, cwd: Path = REPO
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(INSTALLER), "--target", str(target), "--agent", agent],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def assert_skill_copy(self, installed: Path) -> None:
        source_files = sorted(path.relative_to(SOURCE_SKILL) for path in SOURCE_SKILL.rglob("*") if path.is_file())
        installed_files = sorted(path.relative_to(installed) for path in installed.rglob("*") if path.is_file())
        self.assertEqual(installed_files, source_files)
        for relative_path in source_files:
            self.assertEqual((installed / relative_path).read_bytes(), (SOURCE_SKILL / relative_path).read_bytes())
        self.assertFalse(installed.is_symlink())
        self.assertTrue(os.access(installed / "scripts" / "validate-scenario.sh", os.X_OK))

    def test_installs_codex_skill_without_touching_other_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_repo(Path(temporary))
            result = self.install(target, "codex")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_skill_copy(target / ".agents" / "skills" / "fde-project-work")
            self.assertEqual((target / "README.md").read_text(encoding="utf-8"), "keep me\n")
            self.assertFalse((target / ".claude").exists())

    def test_installs_claude_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_repo(Path(temporary))
            result = self.install(target, "claude")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_skill_copy(target / ".claude" / "skills" / "fde-project-work")
            self.assertFalse((target / ".agents").exists())

    def test_installs_both_skill_copies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_repo(Path(temporary))
            result = self.install(target, "both")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_skill_copy(target / ".agents" / "skills" / "fde-project-work")
            self.assert_skill_copy(target / ".claude" / "skills" / "fde-project-work")

    def test_refuses_to_overwrite_existing_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_repo(Path(temporary))
            existing = target / ".agents" / "skills" / "fde-project-work"
            existing.mkdir(parents=True)
            sentinel = existing / "local.txt"
            sentinel.write_text("unchanged\n", encoding="utf-8")
            result = self.install(target, "codex")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Skill already exists", result.stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "unchanged\n")

    def test_refuses_dangerous_targets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            not_a_repo = Path(temporary) / "not-a-repo"
            not_a_repo.mkdir()
            for target in (Path("/"), Path.home(), not_a_repo):
                with self.subTest(target=target):
                    result = self.install(target, "codex")
                    self.assertNotEqual(result.returncode, 0)

    def test_refuses_symlinked_destination_ancestor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = self.make_repo(root)
            outside = root / "outside"
            outside.mkdir()
            (target / ".agents").symlink_to(outside, target_is_directory=True)
            result = self.install(target, "codex")
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(list(outside.iterdir()), [])

    def test_installs_into_repository_path_with_spaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = self.make_repo(root, "target repository")
            result = self.install(Path(target.name), "codex", cwd=root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_skill_copy(target / ".agents" / "skills" / "fde-project-work")

    def test_installed_skill_contains_skill_references_and_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_repo(Path(temporary))
            result = self.install(target, "codex")
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = target / ".agents" / "skills" / "fde-project-work"
            self.assertTrue((installed / "SKILL.md").is_file())
            self.assertEqual(len(list((installed / "references").glob("*.md"))), 6)
            self.assertTrue((installed / "schemas" / "fde-scenario.schema.json").is_file())
            self.assertTrue((installed / "scripts" / "validate-scenario.sh").is_file())

    def test_installed_skill_passes_structure_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_repo(Path(temporary))
            result = self.install(target, "codex")
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = target / ".agents" / "skills" / "fde-project-work"
            validation = subprocess.run(
                [sys.executable, str(VALIDATOR), str(installed)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(validation.returncode, 0, validation.stderr)

    def test_installed_scenario_validator_is_self_contained(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_repo(Path(temporary))
            result = self.install(target, "codex")
            self.assertEqual(result.returncode, 0, result.stderr)
            scenario = target / "scenario.json"
            shutil.copy2(REPO / "examples" / "account-reconciliation" / "scenario.json", scenario)
            validator = target / ".agents" / "skills" / "fde-project-work" / "scripts" / "validate-scenario.sh"
            validation = subprocess.run(
                [str(validator), str(scenario)],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertFalse((target / "pyproject.toml").exists())
            self.assertFalse((target / "schemas").exists())
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)


if __name__ == "__main__":
    unittest.main()
