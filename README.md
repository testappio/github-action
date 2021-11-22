# [<img src="https://assets.testapp.io/logo/blue.svg" alt="TestApp.io"/>](https://testapp.io/) Github Action

> This is in BETA mode. Your feedback is highly appreciated!

[![Workflow to upload apk and ipa to TestApp.io app distribution](https://github.com/testappio/github-action/actions/workflows/main.yml/badge.svg)](https://github.com/testappio/github-action/actions/workflows/main.yml)

This action uploads artifacts (.apk or .ipa) to TestApp.io and notifying your team members about it.

### Inputs

> api_token: can be claimed from https://portal.testapp.io/settings/api-credentials

> app_id: can be found from your app page menu

> file: artifact to upload (.apk or .ipa)

> notify: **yes** or **no** - to notify your team members in TestApp.io via push notification

## Requirements

This action is a docker-based and it will **execute on runners with a Linux operating system**.

Read more in Github Actions [documentation](https://docs.github.com/en/actions/creating-actions/about-actions#docker-container-actions) for more info.

## Sample usage

```
name: Build, code quality, tests

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v1
    - name: set up JDK 1.8
      uses: actions/setup-java@v1
      with:
        java-version: 1.8
    - name: build release
      run: ./gradlew assembleRelease
    - name: upload artefact to TestApp.io
      uses: testappio/github-action@v1
      with:
        api_token: ${{secrets.TESTAPPIO_API_TOKEN}}
        app_id: ${{secrets.TESTAPPIO_APP_ID}}
        file: app/build/outputs/apk/release/app-release-unsigned.apk
        notify: yes
        debug: false
```
