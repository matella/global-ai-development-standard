import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA = "3f786850e387550fdab836ed7e6dc881de23001b"


def generate(out, *args):
    # --only keeps the report from re-running this test suite.
    command = [sys.executable, str(ROOT / "scripts/release_report.py"), "--output", str(out),
               "--commit", SHA, "--only", "manifest-verification", *args]
    subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(out.read_text(encoding="utf-8"))


def gate(path):
    return subprocess.run([sys.executable, str(ROOT / "scripts/release_gate.py"), str(path)],
                          capture_output=True, text=True).returncode


class ReleaseReportTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.out = Path(self._tmp.name) / "report.json"

    def tearDown(self):
        self._tmp.cleanup()

    def test_report_records_real_results(self):
        report = generate(self.out, "--approver", "release owner")
        self.assertEqual(report["checks"], [{"name": "manifest-verification", "status": "passed",
                                             "command": "scripts/verify_manifest.py"}])
        self.assertEqual(report["version"], (ROOT / "VERSION").read_text(encoding="utf-8").strip())
        self.assertEqual(gate(self.out), 0)

    def test_missing_approver_fails_gate(self):
        generate(self.out)
        self.assertEqual(gate(self.out), 1)


class ToolLaunchTests(unittest.TestCase):
    def test_tools_found_on_path_are_launched(self):
        # npm tools are .cmd files on Windows; launching them by bare name fails there.
        import importlib.util
        import os
        from unittest import mock

        spec = importlib.util.spec_from_file_location("release_report", ROOT / "scripts/release_report.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as tmp:
            if os.name == "nt":
                (Path(tmp) / "gads-fake-tool.cmd").write_text("@exit /b 0\r\n", encoding="utf-8")
            else:
                tool = Path(tmp) / "gads-fake-tool"
                tool.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
                tool.chmod(0o755)
            path = tmp + os.pathsep + os.environ.get("PATH", "")
            with mock.patch.dict(os.environ, {"PATH": path}), \
                    mock.patch.object(module, "CHECKS", [("fake", ["gads-fake-tool", "--check"])]):
                checks, skipped = module.run_checks()
        self.assertEqual(skipped, [])
        self.assertEqual(checks, [{"name": "fake", "status": "passed", "command": "gads-fake-tool --check"}])


if __name__ == "__main__":
    unittest.main()
