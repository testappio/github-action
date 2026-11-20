from pathlib import Path
import re
import unittest


WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/main.yml'


class WorkflowTest(unittest.TestCase):
    def test_manual_and_main_push_sample_uploads(self):
        workflow = WORKFLOW.read_text(encoding='utf-8')
        self.assertRegex(workflow, r'(?m)^on:\n  workflow_dispatch:\n  push:\n    branches: \[main\]\n\njobs:$')
        base = 'https://github.com/testappio/fastlane-plugin-testappio/raw/main/fastlane/sample'
        for job, extension in [('linux', 'apk'), ('macos', 'apk')]:
            with self.subTest(job=job):
                match = re.search(rf'(?ms)^  {job}:\n(.*?)(?=^  [a-z]+:|\Z)', workflow)
                self.assertIsNotNone(match)
                steps = match.group(1)
                self.assertIn('uses: actions/checkout@v4', steps)
                self.assertIn(f'run: curl -fsSL --max-time 60 -o sample-app.{extension} {base}/sample-app.{extension}', steps)
                self.assertIn(f'file: sample-app.{extension}', steps)
                self.assertRegex(steps, r'(?m)^          notify: false$')
                self.assertRegex(steps, r'(?m)^          release_notes: ["\']?Action CI test["\']?$')
                self.assertIn('api_token: ${{secrets.TESTAPPIO_API_TOKEN}}', steps)
                self.assertIn('app_id: ${{secrets.TESTAPPIO_APP_ID}}', steps)


if __name__ == '__main__':
    unittest.main()
