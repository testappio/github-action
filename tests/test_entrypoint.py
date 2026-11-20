import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import uuid


ACTION_DIRECTORY = Path(__file__).resolve().parents[1]
ENTRYPOINT = ACTION_DIRECTORY / "entrypoint.sh"


class InstallerTest(unittest.TestCase):
    def test_empty_http_error_stops_the_installer_step(self):
        action = (ACTION_DIRECTORY / "action.yml").read_text(encoding="utf-8")
        installer = next(line.split("run: ", 1)[1] for line in action.splitlines() if line.lstrip().startswith("- run: curl "))
        with tempfile.TemporaryDirectory() as directory:
            curl = Path(directory) / "curl"
            # An empty HTTP error response succeeds unless curl's fail option is set.
            curl.write_text("#!/bin/sh\ncase \"$1\" in -*f*) exit 22 ;; esac\nexit 0\n", encoding="utf-8")
            curl.chmod(0o700)

            result = subprocess.run(
                ["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", installer],
                env={"PATH": f"{directory}:/usr/bin:/bin"},
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 22)


class EntrypointTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.workspace = Path(self.directory.name)
        self.token = uuid.uuid4().hex
        self.capture = self.workspace / "invocation.json"
        stub = self.workspace / "ta-cli"
        stub.write_text(
            """#!/usr/bin/env python3
import json
import os
import sys

token = os.environ['FIXTURE_TOKEN']
with open(os.environ['FIXTURE_CAPTURE'], 'w') as capture:
    json.dump({
        'has_token_in_environment': os.environ.get('TESTAPPIO_API_TOKEN') == token,
        'has_legacy_token_in_environment': 'API_TOKEN' in os.environ,
        'has_token_argument': any(arg == '--api_token' or arg.startswith('--api_token=') or token in arg for arg in sys.argv[1:]),
        'argv': [arg for arg in sys.argv[1:] if token not in arg],
    }, capture)
sys.exit(int(os.environ.get('FIXTURE_EXIT_STATUS', '0')))
""",
            encoding="utf-8",
        )
        stub.chmod(0o700)

    def run_entrypoint(self, file, **inputs):
        env = {
            "PATH": f"{self.workspace}:{os.environ['PATH']}",
            "FIXTURE_TOKEN": self.token,
            "FIXTURE_CAPTURE": str(self.capture),
            "TESTAPPIO_API_TOKEN": self.token,
            "INPUT_APP_ID": "sample-app",
            "INPUT_FILE": str(file),
            "INPUT_RELEASE_NOTES": 'Notes with "quotes" and $ & *',
            **inputs,
        }
        return subprocess.run(
            ["sh", ENTRYPOINT], cwd=self.workspace, env=env, capture_output=True, text=True
        )

    def invocation(self):
        return json.loads(self.capture.read_text(encoding="utf-8"))

    def test_absolute_apk_is_passed_as_one_argument(self):
        file = self.workspace / "with spaces [copy] & more.apk"
        file.touch()
        self.assertEqual(self.run_entrypoint(file).returncode, 0)
        argv = self.invocation()["argv"]
        self.assertIn(f"--apk={file}", argv)
        self.assertIn("--release=android", argv)
        self.assertIn('--release_notes=Notes with "quotes" and $ & *', argv)

    def test_relative_ipa_is_passed_as_one_argument(self):
        file = Path("relative output.ipa")
        (self.workspace / file).touch()
        self.assertEqual(self.run_entrypoint(file).returncode, 0)
        argv = self.invocation()["argv"]
        self.assertIn(f"--ipa={file}", argv)
        self.assertIn("--release=ios", argv)

    def test_uppercase_artifact_extension_is_accepted(self):
        file = self.workspace / "output.IPA"
        file.touch()
        self.assertEqual(self.run_entrypoint(file).returncode, 0)
        self.assertIn(f"--ipa={file}", self.invocation()["argv"])

    def test_token_is_in_child_environment_and_absent_from_arguments(self):
        self.assertEqual(self.run_entrypoint("app.apk", API_TOKEN=self.token).returncode, 0)
        invocation = self.invocation()
        self.assertTrue(invocation["has_token_in_environment"])
        self.assertFalse(invocation["has_legacy_token_in_environment"])
        self.assertFalse(invocation["has_token_argument"])

    def test_empty_required_inputs_stop_before_cli_or_ambient_fallback(self):
        required_inputs = (
            ("api_token", "TESTAPPIO_API_TOKEN", "API_TOKEN", self.token),
            ("app_id", "INPUT_APP_ID", "APP_ID", "ambient-app"),
        )
        for name, input_var, legacy_var, legacy_value in required_inputs:
            with self.subTest(name=name):
                self.capture.unlink(missing_ok=True)
                result = self.run_entrypoint("app.apk", **{input_var: "", legacy_var: legacy_value})
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(name in result.stderr and legacy_value not in result.stderr + result.stdout)
                self.assertFalse(self.capture.exists())

    def test_empty_booleans_are_omitted(self):
        self.assertEqual(self.run_entrypoint("app.apk", INPUT_NOTIFY="").returncode, 0)
        argv = self.invocation()["argv"]
        for flag in ("git_release_notes", "git_commit_id", "notify"):
            with self.subTest(flag=flag):
                self.assertFalse(any(arg.startswith(f"--{flag}=") for arg in argv))

    def test_empty_release_notes_are_omitted(self):
        self.assertEqual(self.run_entrypoint("app.apk", INPUT_RELEASE_NOTES="").returncode, 0)
        self.assertFalse(any(arg.startswith("--release_notes=") for arg in self.invocation()["argv"]))

    def test_explicit_booleans_are_passed(self):
        result = self.run_entrypoint(
            "app.apk", INPUT_GIT_RELEASE_NOTES="true", INPUT_INCLUDE_GIT_COMMIT_ID="false", INPUT_NOTIFY="TRUE"
        )
        self.assertEqual(result.returncode, 0)
        argv = self.invocation()["argv"]
        self.assertIn("--git_release_notes=true", argv)
        self.assertIn("--git_commit_id=false", argv)
        self.assertIn("--notify=true", argv)

    def test_mixed_case_booleans_are_normalized(self):
        result = self.run_entrypoint("app.apk", INPUT_NOTIFY="tRuE", INPUT_GIT_RELEASE_NOTES="fAlSe")
        self.assertEqual(result.returncode, 0)
        args = self.invocation()["argv"]
        self.assertIn("--notify=true", args)
        self.assertIn("--git_release_notes=false", args)

    def test_each_invalid_boolean_stops_before_invoking_cli(self):
        for name in ("git_release_notes", "include_git_commit_id", "notify"):
            with self.subTest(name=name):
                result = self.run_entrypoint("app.apk", **{f"INPUT_{name.upper()}": "false --unexpected-argument *"})
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(name, result.stderr)
                self.assertNotIn("--unexpected-argument", result.stderr)
                self.assertFalse(self.capture.exists())

    def test_cli_failure_is_propagated(self):
        self.assertEqual(self.run_entrypoint("app.ipa", FIXTURE_EXIT_STATUS="23").returncode, 23)

    def test_unsupported_extension_stops_before_invoking_cli(self):
        result = self.run_entrypoint("app.zip")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(".apk or .ipa", result.stderr)
        self.assertFalse(self.capture.exists())


if __name__ == "__main__":
    unittest.main()
