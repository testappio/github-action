# [<img src="https://assets.testapp.io/logo/blue.svg" alt="TestApp.io"/>](https://testapp.io/) Github Action

### Current version: v4.0-BETA

> This is in BETA mode. Your feedback is highly appreciated!

[![Workflow to upload apk and ipa to TestApp.io app distribution](https://github.com/testappio/github-action/actions/workflows/main.yml/badge.svg)](https://github.com/testappio/github-action/actions/workflows/main.yml)

This action uploads artifacts (.apk or .ipa) to TestApp.io and notifying your team members about it.

## Configuration


| Key               | Description                                                                                             | Env Var(s)                  | Default |
| ----------------- | ------------------------------------------------------------------------------------------------------- | --------------------------- | ------- |
| api_token         | You can get it from https://portal.testapp.io/settings/api-credentials                                  | TESTAPPIO_API_TOKEN         |         |
| app_id            | You can get it from your app page at [https://portal.testapp.io/apps](https://portal.testapp.io/apps?select-for-integrations)                                       | TESTAPPIO_APP_ID            |         |
| release           | It can be either both or Android or iOS                                                                 | TESTAPPIO_RELEASE           |         |
| apk_file          | Path to the Android APK file                                                                            | TESTAPPIO_ANDROID_PATH      |         |
| ipa_file          | Path to the iOS IPA file                                                                                | TESTAPPIO_IOS_PATH          |         |
| release_notes     | Manually add the release notes to be displayed for the testers                                          | TESTAPPIO_RELEASE_NOTES     |         |
| git_release_notes | Collect release notes from the latest git commit message to be displayed for the testers: true or false | TESTAPPIO_GIT_RELEASE_NOTES | true    |
| git_commit_id     | Include the last commit ID in the release notes (works with both release notes options): true or false   | TESTAPPIO_GIT_COMMIT_ID     | false   |
| notify            | Send notifications to your team members about this release: true or false                               | TESTAPPIO_NOTIFY            | false   |

## Requirements

This action will **execute on runners with a Ubuntu & macOS operating systems**.

## Sample usage for Android

```
name: Android adhoc
on:
  push:
    branches:
      - code-sign

jobs:
  export_android:

    runs-on: ubuntu-latest

    steps:

    - name: Checkout repository
    - uses: actions/checkout@v2

    - name: Set up JDK 1.8
      uses: actions/setup-java@v1
      with:
        java-version: 1.8

    - name: Build release
      run: ./gradlew assembleRelease


    - name: Upload artifact to TestApp.io
      uses: testappio/github-action@v4
      with:
        api_token: ${{secrets.TESTAPPIO_API_TOKEN}}
        app_id: ${{secrets.TESTAPPIO_APP_ID}}
        file: app/build/outputs/apk/release/app-release-unsigned.apk
        release_notes: ""
        git_release_notes: true
        include_git_commit_id: true
        notify: true
```

## Sample usage for iOS

```
name: iOS adhoc
on:
  push:
    branches:
      - code-sign

jobs:
  export_ios_with_signing:
    runs-on: macos-11

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Build and export iOS
        uses: yukiarrr/ios-build-action@v1.4.0
        with:
          project-path: ios/testappio.xcodeproj
          workspace-path: ios/testappio.xcworkspace
          scheme: testappio
          export-method: ad-hoc
          configuration: Release
          output-path: artifacts/output.ipa
          p12-base64: ${{ secrets.P12_BASE64 }}
          certificate-password: ${{ secrets.P12_PASSWORD }}
          mobileprovision-base64: ${{ secrets.ADHOC_MOBILEPROVISION_BASE64 }}
          code-signing-identity: ${{ secrets.CODE_SIGNING_IDENTITY }}
          team-id: ${{ secrets.TEAM_ID }}

      - name: Upload artifact to TestApp.io
        uses: testappio/github-action@v4
        with:
          api_token: ${{ secrets.TESTAPPIO_API_TOKEN }}
          app_id: ${{ secrets.TESTAPPIO_APP_ID }}
          file: artifacts/output.ipa
          release_notes: "Testing manual release notes..."
          git_release_notes: false
          include_git_commit_id: false
          notify: true
```

---

## Feedback & Support

Developers built [TestApp.io](https://testapp.io) to solve the pain of app distribution for mobile app development teams.

Join our [Slack](https://join.slack.com/t/testappio/shared_invite/zt-pvpoj3l2-epGYwGTaV3~3~0f7udNWoA) channel for feedback and support.

Happy releasing 🎉
