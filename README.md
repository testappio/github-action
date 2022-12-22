# [<img src="https://assets.testapp.io/logo/blue.svg" alt="TestApp.io"/>](https://testapp.io/) Github Action

### Current version: v5

> BETA mode. Your feedback is highly appreciated!

[![Workflow to upload APK and IPA to TestApp.io app distribution](https://github.com/testappio/github-action/actions/workflows/main.yml/badge.svg)](https://github.com/testappio/github-action/actions/workflows/main.yml)

This action uploads artifacts (.apk or .ipa) to TestApp.io and notifies your team members about it.

## Configuration

_More info here: [https://help.testapp.io/ta-cli](https://help.testapp.io/ta-cli/)_

| Key               | Description                                                                                                                          | Env Var(s)                  | Default |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------ | --------------------------- | ------- |
| api_token         | You can get it from https://portal.testapp.io/settings/api-credentials                                                               | TESTAPPIO_API_TOKEN         |         |
| app_id            | You can get it from your app page at [https://portal.testapp.io/apps](https://portal.testapp.io/apps?action=select-for-integrations) | TESTAPPIO_APP_ID            |         |
| release           | It can be either both or Android or iOS                                                                                              | TESTAPPIO_RELEASE           |         |
| file              | Path to the either Android .APK file or iOS .IPA file                                                                                | TESTAPPIO_FILE_PATH         |         |
| release_notes     | Manually add the release notes to be displayed for the testers                                                                       | TESTAPPIO_RELEASE_NOTES     |         |
| git_release_notes | Collect release notes from the latest git commit message to be displayed for the testers: true or false                              | TESTAPPIO_GIT_RELEASE_NOTES | true    |
| git_commit_id     | Include the last commit ID in the release notes (works with both release notes options): true or false                               | TESTAPPIO_GIT_COMMIT_ID     | false   |
| notify            | Send notifications to your team members about this release: true or false                                                            | TESTAPPIO_NOTIFY            | false   |

## Requirements

This action will **execute on runners with Ubuntu & macOS operating systems**.

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

    - name: Upload IPA to TestApp.io
      uses: testappio/github-action@v5
      with:
        api_token: ${{secrets.TESTAPPIO_API_TOKEN}}
        app_id: ${{secrets.TESTAPPIO_APP_ID}}
        file: app/build/outputs/apk/release/app-release-unsigned.apk
        release_notes: "Testing manual release notes..."
        git_release_notes: true
        include_git_commit_id: false
        notify: true
```

If you want a debug version, replace the following:

`run: ./gradlew assembleDebug`

`file: app/build/outputs/apk/debug/app-debug.apk`

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

      - name: Upload APK to TestApp.io
        uses: testappio/github-action@v5
        with:
          api_token: ${{ secrets.TESTAPPIO_API_TOKEN }}
          app_id: ${{ secrets.TESTAPPIO_APP_ID }}
          file: artifacts/output.ipa
          release_notes: "Testing manual release notes..."
          git_release_notes: true
          include_git_commit_id: false
          notify: true
```

---

## Feedback & Support

Developers built [TestApp.io](https://testapp.io) to solve the pain of app distribution & feedback for mobile app development teams.

Join our [community](https://help.testapp.io/faq/join-our-community/) for feedback and support.

Check out our [Help Center](https://help.testapp.io/) for more info and other integrations.

Happy releasing 🎉
