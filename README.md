# [<img src="https://assets.testapp.io/logo/blue.svg" alt="TestApp.io"/>](https://testapp.io/) Github Action

### Current version: v4.0-BETA

> This is in BETA mode. Your feedback is highly appreciated!

[![Workflow to upload apk and ipa to TestApp.io app distribution](https://github.com/testappio/github-action/actions/workflows/main.yml/badge.svg)](https://github.com/testappio/github-action/actions/workflows/main.yml)

This action uploads artifacts (.apk or .ipa) to TestApp.io and notifying your team members about it.

### Inputs

> api_token: can be claimed from https://portal.testapp.io/settings/api-credentials

> app_id: can be found from your app page menu

> file: artifact to upload (.apk or .ipa)

> release_notes: manually add the release notes to be displayed for the testers

> git_release_notes: collect release notes from the the git commit message to be displayed for the testers

> include_git_commit_id: include the last git commit ID in the release notes (works with both release notes option)

> notify: notify your team members via a push notification in TestApp.io mobile app

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

Join our [Slack](https://join.slack.com/t/testappio/shared_invite/zt-pvpoj3l2-epGYwGTaV3~3~0f7udNWoA) channel for feedback and support or you can contact us at support@testapp.io and we'll gladly help you out!

---

Happy releasing 🎉
