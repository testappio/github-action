#!/bin/sh

if [ -z "${TESTAPPIO_API_TOKEN-}" ]; then
  printf 'api_token is required.\n' >&2
  exit 1
fi
if [ -z "${INPUT_APP_ID-}" ]; then
  printf 'app_id is required.\n' >&2
  exit 1
fi
unset API_TOKEN

case "$INPUT_FILE" in
  *.[Aa][Pp][Kk]) set -- --release=android "--apk=$INPUT_FILE" ;;
  *.[Ii][Pp][Aa]) set -- --release=ios "--ipa=$INPUT_FILE" ;;
  *)
    printf 'file must end in .apk or .ipa.\n' >&2
    exit 1
    ;;
esac

for input in "git_release_notes=${INPUT_GIT_RELEASE_NOTES-}" \
             "include_git_commit_id=${INPUT_INCLUDE_GIT_COMMIT_ID-}" \
             "notify=${INPUT_NOTIFY-}"; do
  name=${input%%=*}
  value=${input#*=}
  case "$value" in
    '') continue ;;
    1|[Tt]|[Tt][Rr][Uu][Ee]) value=true ;;
    0|[Ff]|[Ff][Aa][Ll][Ss][Ee]) value=false ;;
    *)
      printf '%s must be true or false.\n' "$name" >&2
      exit 1
      ;;
  esac
  if [ "$name" = include_git_commit_id ]; then
    name=git_commit_id
  fi
  set -- "$@" "--$name=$value"
done

if [ -n "${INPUT_RELEASE_NOTES-}" ]; then
  set -- "$@" "--release_notes=$INPUT_RELEASE_NOTES"
fi

exec ta-cli publish --app_id="$INPUT_APP_ID" --source="Github Action" "$@"
