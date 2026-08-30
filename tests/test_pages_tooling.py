from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
BUILD = REPO / "scripts" / "build-pages.sh"
VALIDATE = REPO / "scripts" / "validate-pages.py"


class PagesToolingTests(unittest.TestCase):
    def run_command(self, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(args, cwd=cwd or REPO, text=True, capture_output=True, check=False)

    def minimal_artifact(self, root: Path, *, html: str = "<!doctype html><title>test</title>") -> None:
        (root / "examples" / "third-party-api-change-monitoring").mkdir(parents=True)
        (root / "index.html").write_text(html, encoding="utf-8")
        (root / "tokens.css").write_text(":root {}", encoding="utf-8")
        (root / ".nojekyll").touch()
        (root / "examples" / "README.zh-TW.md").write_text("# Cases", encoding="utf-8")
        (root / "examples" / "third-party-api-change-monitoring" / "index.html").write_text(
            "<!doctype html><title>case</title>", encoding="utf-8"
        )

    def test_build_rejects_output_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "target"
            target.mkdir()
            output = root / "artifact"
            output.symlink_to(target, target_is_directory=True)
            result = self.run_command(str(BUILD), str(output))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must not be a symlink", result.stderr)
            self.assertEqual(list(target.iterdir()), [])

    def test_build_rejects_symlinked_required_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "scripts").mkdir()
            (root / "site").mkdir()
            (root / "examples").mkdir()
            shutil.copy2(BUILD, root / "scripts" / "build-pages.sh")
            outside = root / "outside.txt"
            outside.write_text("private", encoding="utf-8")
            (root / "site" / "index.html").symlink_to(outside)
            (root / "site" / "tokens.css").write_text(":root {}", encoding="utf-8")
            (root / "examples" / "README.zh-TW.md").write_text("# Cases", encoding="utf-8")
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            result = self.run_command(str(root / "scripts" / "build-pages.sh"), str(root / "output"), cwd=root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("regular non-symlink file", result.stderr)

    def test_build_rejects_untracked_required_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(REPO, root / "repo", symlinks=True, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            repo = root / "repo"
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "rm", "--cached", "site/index.html"], cwd=repo, check=True, capture_output=True)
            result = self.run_command(str(repo / "scripts" / "build-pages.sh"), str(root / "artifact"), cwd=repo)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("required publish source must be tracked", result.stderr)

    def test_build_excludes_untracked_matching_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(REPO, root / "repo", symlinks=True, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            repo = root / "repo"
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            untracked = repo / "docs" / "private-untracked.md"
            untracked.write_text("private", encoding="utf-8")
            output = root / "artifact"
            result = self.run_command(str(repo / "scripts" / "build-pages.sh"), str(output), cwd=repo)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((output / "docs" / "private-untracked.md").exists())

    def test_build_includes_tracked_path_with_spaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(REPO, root / "repo", symlinks=True, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            repo = root / "repo"
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            tracked = repo / "docs" / "path with spaces.md"
            tracked.write_text("# Tracked\n", encoding="utf-8")
            subprocess.run(["git", "add", str(tracked.relative_to(repo))], cwd=repo, check=True)
            output = root / "artifact"
            result = self.run_command(str(repo / "scripts" / "build-pages.sh"), str(output), cwd=repo)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / "docs" / "path with spaces.md").is_file())

    def test_build_rejects_tracked_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(REPO, root / "repo", symlinks=True, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            repo = root / "repo"
            outside = root / "outside.txt"
            outside.write_text("private", encoding="utf-8")
            link = repo / "docs" / "tracked-link.md"
            link.symlink_to(outside)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            result = self.run_command(str(repo / "scripts" / "build-pages.sh"), str(root / "artifact"), cwd=repo)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsafe publish path", result.stderr)

    def test_validator_rejects_artifact_root_escape(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "artifact"
            root.mkdir()
            (root.parent / "outside.txt").write_text("outside", encoding="utf-8")
            self.minimal_artifact(root, html='<a href="../outside.txt">outside</a>')
            result = self.run_command("python3", str(VALIDATE), str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("escapes artifact root", result.stderr)

    def test_validator_rejects_missing_html_resource(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.minimal_artifact(root, html='<link rel="stylesheet" href="missing.css">')
            result = self.run_command("python3", str(VALIDATE), str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing missing.css", result.stderr)

    def test_validator_rejects_missing_markdown_link(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.minimal_artifact(root)
            (root / "examples" / "README.zh-TW.md").write_text("[missing](missing.md)", encoding="utf-8")
            result = self.run_command("python3", str(VALIDATE), str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing missing.md", result.stderr)

    def test_validator_rejects_missing_markdown_image(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.minimal_artifact(root)
            (root / "examples" / "README.zh-TW.md").write_text("![missing](missing.png)", encoding="utf-8")
            result = self.run_command("python3", str(VALIDATE), str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing missing.png", result.stderr)

    def test_validator_rejects_missing_html_poster_and_object(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.minimal_artifact(root, html='<video poster="missing-poster.webp"></video><object data="missing.pdf"></object>')
            result = self.run_command("python3", str(VALIDATE), str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing missing-poster.webp", result.stderr)
            self.assertIn("missing missing.pdf", result.stderr)

    def test_validator_rejects_missing_css_url(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.minimal_artifact(root)
            (root / "tokens.css").write_text("@font-face { src: url(missing.woff2); }", encoding="utf-8")
            result = self.run_command("python3", str(VALIDATE), str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing missing.woff2", result.stderr)

    def test_validator_rejects_missing_quoted_css_imports(self) -> None:
        for quote in ('"', "'"):
            with self.subTest(quote=quote), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.minimal_artifact(root)
                (root / "tokens.css").write_text(f"@import {quote}missing.css{quote};", encoding="utf-8")
                result = self.run_command("python3", str(VALIDATE), str(root))
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("missing missing.css", result.stderr)


if __name__ == "__main__":
    unittest.main()
