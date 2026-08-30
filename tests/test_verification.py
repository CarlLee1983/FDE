from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


@unittest.skipIf(
    os.environ.get("FDE_VERIFY_INTEGRATION_CHILD") == "1",
    "avoid recursively running verification integration tests",
)
class VerificationOrchestrationTests(unittest.TestCase):
    def run_make(
        self, repo: Path, target: str, *, env: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        child_env = os.environ.copy()
        child_env["FDE_VERIFY_INTEGRATION_CHILD"] = "1"
        if env:
            child_env.update(env)
        return subprocess.run(
            ["make", target],
            cwd=repo,
            env=child_env,
            text=True,
            capture_output=True,
            check=False,
            timeout=180,
        )

    def copy_repo(self, root: Path) -> Path:
        repo = root / "repo"
        shutil.copytree(
            REPO,
            repo,
            symlinks=True,
            ignore=shutil.ignore_patterns(".git", ".pytest_cache", ".venv", "__pycache__"),
        )
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        return repo

    def test_valid_repository_runs_the_complete_verify_chain(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.copy_repo(Path(temporary))
            result = self.run_make(repo, "verify")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("tracked scenarios", result.stdout)
            self.assertIn("Pages and Skill valid", result.stdout)

    def test_invalid_tracked_scenario_fails_verify(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.copy_repo(Path(temporary))
            scenario = next((repo / "examples").glob("*/scenario.json"))
            scenario.write_text("{}\n", encoding="utf-8")
            result = self.run_make(repo, "verify")
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Verification passed", result.stdout)

    def test_untracked_scenario_is_not_release_validation_input(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.copy_repo(Path(temporary))
            scenario = repo / "examples" / "untracked case" / "scenario.json"
            scenario.parent.mkdir()
            scenario.write_text("{}\n", encoding="utf-8")
            result = self.run_make(repo, "validate-scenarios")
            tracked = subprocess.run(
                ["git", "ls-files", "examples/**/scenario.json"],
                cwd=repo,
                text=True,
                capture_output=True,
                check=True,
            ).stdout.splitlines()
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn(f"{len(tracked)} tracked records", result.stdout)

    def test_tracked_scenario_path_with_spaces_is_validated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.copy_repo(Path(temporary))
            scenario = repo / "examples" / "tracked case" / "scenario.json"
            scenario.parent.mkdir()
            shutil.copy2(repo / "examples" / "account-reconciliation" / "scenario.json", scenario)
            subprocess.run(["git", "add", str(scenario.relative_to(repo))], cwd=repo, check=True)
            result = self.run_make(repo, "validate-scenarios")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_tracked_scenario_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = self.copy_repo(root)
            scenario = next((repo / "examples").glob("*/scenario.json"))
            outside = root / "outside.json"
            outside.write_text("{}\n", encoding="utf-8")
            scenario.unlink()
            scenario.symlink_to(outside)
            subprocess.run(["git", "add", str(scenario.relative_to(repo))], cwd=repo, check=True)
            result = self.run_make(repo, "validate-scenarios")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("regular non-symlink file", result.stderr)

    def test_pages_validation_excludes_untracked_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repo = self.copy_repo(Path(temporary))
            (repo / "docs" / "private-untracked.md").write_text(
                "[missing](not-published.md)\n", encoding="utf-8"
            )
            result = self.run_make(repo, "validate-pages")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_tool_has_clear_error(self) -> None:
        result = self.run_make(REPO, "verify", env={"UV": "missing-uv-for-test"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required tool not found: missing-uv-for-test", result.stderr)

    def test_temporary_output_is_cleaned(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temp_root = Path(temporary)
            result = self.run_make(REPO, "validate-pages", env={"TMPDIR": temporary})
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(list(temp_root.iterdir()), [])
