"""Exercise the repository checker against isolated valid and broken documents."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_repo


class RepositoryChecks(unittest.TestCase):
    def check_documents(self, documents):
        with tempfile.TemporaryDirectory(prefix="cv-link-check-") as directory:
            root = Path(directory).resolve()
            for name, content in documents.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            listed = "\0".join(documents).encode("utf-8") + b"\0"
            output = StringIO()
            with patch.object(check_repo, "ROOT", root), patch.object(
                check_repo.subprocess, "run"
            ) as git, redirect_stdout(output):
                git.return_value.stdout = listed
                failed = check_repo.main()
            return failed, output.getvalue()

    def test_relative_unicode_links_and_code_examples(self):
        failed, output = self.check_documents({
            "README.md": "[Evidence](knowledge/projects.md#säätiedot--own-work)\n"
                         "```md\n[Example](not-a-real-file.md)\n```\n",
            "knowledge/projects.md": "# Säätiedot — own work\n[Back](../README.md)\n",
        })
        self.assertFalse(failed, output)
        self.assertIn("2 repository links", output)

    def test_broken_files_fragments_and_escaping_paths_fail(self):
        failed, output = self.check_documents({
            "README.md": "# Start\n[Missing](missing.md)\n"
                         "[Heading](README.md#missing)\n[Outside](../outside.md)\n",
        })
        self.assertTrue(failed)
        for expected in ("missing target", "missing heading", "escapes repository"):
            self.assertIn(expected, output)

    def test_machine_paths_only_tolerated_in_historical_sources(self):
        failed, output = self.check_documents({
            "README.md": "[Not portable](C:/private/report.md)\n",
            "sources/original.md": "[Historical](C:/private/report.md)\n",
        })
        self.assertTrue(failed)
        self.assertIn("README.md:1: machine-specific link", output)
        self.assertNotIn("ERROR sources/", output)

    def test_merge_markers_and_encoding_damage_fail(self):
        failed, output = self.check_documents({
            "README.md": "# Heading\n<<<<<<< HEAD\nDamage: \ufffd\n",
        })
        self.assertTrue(failed)
        self.assertIn("FAIL: 2 issue(s)", output)


if __name__ == "__main__":
    unittest.main()
