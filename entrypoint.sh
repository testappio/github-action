#!/bin/sh

APK_PATH=""
IPA_PATH=""
RELEASE=""
FILE="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"$INPUT_FILE
FILE_EXT=${INPUT_FILE##*.}

if [ "$FILE_EXT" = "apk" ]; then
        RELEASE="android"
        APK_PATH=$FILE
fi

if [ "$FILE_EXT" = "ipa" ]; then
        RELEASE="ios"
        IPA_PATH=$FILE
fi

ta-cli publish --api_token="$INPUT_API_TOKEN" --app_id="$INPUT_APP_ID" --release="$RELEASE" --apk="$APK_PATH" --ipa="$IPA_PATH" --notify="$INPUT_NOTIFY"
