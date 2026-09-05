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
VALID_SCENARIO = REPO / "examples" / "account-reconciliation" / "scenario.json"
INVALID_SCENARIO = '{"title": "missing required fields"}\n'


def installed_skill(target: Path, agent: str) -> Path:
    return target / f".{agent}" / "skills" / "fde-project-work"


class SkillInstallerTests(unittest.TestCase):
    def make_repo(self, root: Path, name: str = "target") -> Path:
        target = root / name
        target.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=target, check=True)
        (target / "README.md").write_text("keep me\n", encoding="utf-8")
        return target

    def install(
        self, target: Path, agent: str, *, cwd: Path = REPO, installer: Path = INSTALLER
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(installer), "--target", str(target), "--agent", agent],
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

    def test_installs_portable_skill_for_every_requested_host(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            for mode, hosts in (("codex", ("agents",)), ("claude", ("claude",)), ("both", ("agents", "claude"))):
                with self.subTest(mode=mode), tempfile.TemporaryDirectory(dir=temporary) as child:
                    target = self.make_repo(Path(child))
                    (target / "CONTEXT.md").write_text("target context\n", encoding="utf-8")
                    (target / "docs").mkdir()
                    (target / "docs" / "README.md").write_text("target docs\n", encoding="utf-8")
                    result = self.install(target, mode)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    for host in hosts:
                        installed = installed_skill(target, host)
                        self.assert_skill_copy(installed)
                        self.assertTrue((installed / "references" / "canonical" / "CONTEXT.md").is_file())
                        self.assertTrue((installed / "references" / "canonical" / "FDE-Scenario-to-Action-Method.md").is_file())
                        self.assertTrue((installed / "references" / "canonical" / "docs" / "fde-ontology" / "07-capability-map-and-implementation-strategy.md").is_file())
                    self.assertEqual((target / "README.md").read_text(encoding="utf-8"), "keep me\n")
                    self.assertEqual((target / "CONTEXT.md").read_text(encoding="utf-8"), "target context\n")
                    for absent_host in {"agents", "claude"} - set(hosts):
                        self.assertFalse((target / f".{absent_host}").exists())

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

    def test_validation_rejects_missing_packaged_reference_with_source_and_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_repo(Path(temporary))
            self.assertEqual(self.install(target, "codex").returncode, 0)
            installed = installed_skill(target, "agents")
            missing = installed / "references" / "canonical" / "FDE-Scenario-to-Action-Method.md"
            missing.unlink()
            validation = subprocess.run(
                [sys.executable, str(VALIDATOR), str(installed)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(validation.returncode, 0)
            self.assertIn("references/source-map.md", validation.stderr)
            self.assertIn("FDE-Scenario-to-Action-Method.md", validation.stderr)

    def test_installed_scenario_validator_is_self_contained_for_every_host(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            distribution = root / "distribution"
            shutil.copytree(SOURCE_SKILL, distribution / ".agents" / "skills" / "fde-project-work")
            (distribution / "scripts").mkdir()
            installer = distribution / "scripts" / "install-skill.sh"
            shutil.copy2(INSTALLER, installer)
            installer.chmod(0o755)
            target = self.make_repo(root)
            result = self.install(target, "both", installer=installer)
            self.assertEqual(result.returncode, 0, result.stderr)
            shutil.rmtree(distribution)
            scenario = target / "scenario.json"
            shutil.copy2(VALID_SCENARIO, scenario)
            self.assertFalse((target / "pyproject.toml").exists())
            self.assertFalse((target / "schemas").exists())
            for host in ("agents", "claude"):
                with self.subTest(host=host):
                    installed = installed_skill(target, host)
                    validation = subprocess.run(
                        ["./scripts/validate-scenario.sh", str(scenario)],
                        cwd=installed,
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
                    scenario.write_text(INVALID_SCENARIO, encoding="utf-8")
                    invalid = subprocess.run(
                        ["./scripts/validate-scenario.sh", str(scenario)],
                        cwd=installed,
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertNotEqual(invalid.returncode, 0)
                    shutil.copy2(VALID_SCENARIO, scenario)

    def test_installed_validator_reports_missing_uv(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = self.make_repo(Path(temporary))
            self.assertEqual(self.install(target, "claude").returncode, 0)
            scenario = target / "scenario.json"
            shutil.copy2(VALID_SCENARIO, scenario)
            result = subprocess.run(
                ["./scripts/validate-scenario.sh", str(scenario)],
                cwd=installed_skill(target, "claude"),
                env={"PATH": "/usr/bin:/bin"},
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 69)
            self.assertIn("required tool not found: uv", result.stderr)


if __name__ == "__main__":
    unittest.main()
