#!/usr/bin/env bash
set -euo pipefail

readonly release_version="v0.9"
readonly expected_base_sha256="5627913aadbda11a0d7abf77b670802335995f2c635ef9af5fee5161a615f76c"
readonly apktool_sha256="effb69dab2f93806cafc0d232f6be32c2551b8d51c67650f575e46c016908fdd"
readonly signer_sha256="e1299fd6fcf4da527dd53735b56127e8ea922a321128123b9c32d619bba1d835"
readonly apktool_url="https://github.com/iBotPeaches/Apktool/releases/download/v2.12.0/apktool_2.12.0.jar"
readonly signer_url="https://github.com/patrickfav/uber-apk-signer/releases/download/v1.3.0/uber-apk-signer-1.3.0.jar"

fail() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

hash_file() {
  local target="$1"
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$target" | awk '{print $1}'
  elif command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$target" | awk '{print $1}'
  else
    fail "shasum or sha256sum is required"
  fi
}

verify_hash() {
  local target="$1"
  local expected="$2"
  local actual
  actual="$(hash_file "$target")"
  [[ "$actual" == "$expected" ]] || fail "SHA-256 mismatch for $target (got $actual)"
}

resolve_java() {
  if [[ -n "${JAVA_BIN:-}" ]]; then
    [[ -x "$JAVA_BIN" ]] || fail "JAVA_BIN is not executable: $JAVA_BIN"
    java_bin="$JAVA_BIN"
  elif command -v java >/dev/null 2>&1 && java -version >/dev/null 2>&1; then
    java_bin="$(command -v java)"
  else
    fail "a working JDK is required; install JDK 17 or set JAVA_BIN and KEYTOOL_BIN"
  fi

  if [[ -n "${KEYTOOL_BIN:-}" ]]; then
    [[ -x "$KEYTOOL_BIN" ]] || fail "KEYTOOL_BIN is not executable: $KEYTOOL_BIN"
    keytool_bin="$KEYTOOL_BIN"
  elif [[ -x "$(dirname "$java_bin")/keytool" ]]; then
    keytool_bin="$(dirname "$java_bin")/keytool"
  elif command -v keytool >/dev/null 2>&1; then
    keytool_bin="$(command -v keytool)"
  else
    fail "keytool is required; use a full JDK rather than a JRE"
  fi
}

resolve_tool() {
  local label="$1"
  local override="$2"
  local target="$3"
  local url="$4"
  local expected="$5"

  if [[ -n "$override" ]]; then
    [[ -f "$override" ]] || fail "$label override does not exist: $override"
    verify_hash "$override" "$expected"
    resolved_tool="$override"
    return
  fi

  if [[ ! -f "$target" ]]; then
    command -v curl >/dev/null 2>&1 || fail "curl is required to download $label"
    printf 'Downloading %s...\n' "$label"
    curl --fail --location --retry 3 --output "$target.download" "$url"
    verify_hash "$target.download" "$expected"
    mv "$target.download" "$target"
  fi

  verify_hash "$target" "$expected"
  resolved_tool="$target"
}

[[ $# -eq 1 ]] || fail "usage: $0 /path/to/SGCAM_8.5.300.XX.10_STABLE_V24.apk"

base_apk="$1"
[[ -f "$base_apk" ]] || fail "base APK not found: $base_apk"
command -v patch >/dev/null 2>&1 || fail "patch is required"
command -v openssl >/dev/null 2>&1 || fail "openssl is required for local signing-key generation"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
project_root="$(cd "$script_dir/.." && pwd -P)"
local_root="$project_root/.local"
tools_dir="$local_root/tools"
framework_dir="$local_root/framework"
work_dir="$local_root/work/$release_version"
decode_dir="$work_dir/decompiled"
signed_dir="$work_dir/signed"
signing_dir="$local_root/signing"
output_dir="$local_root/output"
output_apk="$output_dir/Photo-Sphere-v0.9-dedicated-icon.apk"

preserved_signing_dir="$project_root/.signing"
if [[ -n "${SIGNING_DIR:-}" ]]; then
  signing_dir="$SIGNING_DIR"
elif [[ -e "$preserved_signing_dir/photo-sphere-local.jks" || -e "$preserved_signing_dir/keystore.properties" ]]; then
  signing_dir="$preserved_signing_dir"
fi

case "$work_dir" in
  "$project_root"/.local/work/*) ;;
  *) fail "refusing unsafe work directory: $work_dir" ;;
esac

printf 'Verifying base APK...\n'
verify_hash "$base_apk" "$expected_base_sha256"
resolve_java

mkdir -p "$tools_dir" "$framework_dir" "$signing_dir" "$output_dir"
resolve_tool "apktool 2.12.0" "${APKTOOL_JAR:-}" "$tools_dir/apktool_2.12.0.jar" "$apktool_url" "$apktool_sha256"
apktool_jar="$resolved_tool"
resolve_tool "uber-apk-signer 1.3.0" "${UBER_APK_SIGNER_JAR:-}" "$tools_dir/uber-apk-signer-1.3.0.jar" "$signer_url" "$signer_sha256"
signer_jar="$resolved_tool"

rm -rf -- "$work_dir"
mkdir -p "$decode_dir" "$signed_dir"

printf 'Decoding base APK...\n'
"$java_bin" -jar "$apktool_jar" d -q -f -p "$framework_dir" "$base_apk" -o "$decode_dir"

printf 'Applying stable v0.9 patch series...\n'
patch_count=0
for patch_file in "$project_root"/patches/000[1-6]-*.patch; do
  [[ -f "$patch_file" ]] || fail "no patches found"
  printf '  %s\n' "$(basename "$patch_file")"
  patch -d "$decode_dir" -p1 --forward --batch < "$patch_file"
  patch_count=$((patch_count + 1))
done
[[ "$patch_count" -eq 6 ]] || fail "expected 6 stable patches, found $patch_count"

reject_file="$(find "$decode_dir" -type f -name '*.rej' -print -quit)"
[[ -z "$reject_file" ]] || fail "patch rejection found: $reject_file"
find "$decode_dir" -type f -name '*.orig' -delete

icon_res_dir="$project_root/assets/android/res"
[[ -d "$icon_res_dir" ]] || fail "Android icon resources not found: $icon_res_dir"
printf 'Installing Photo Sphere launcher icon resources...\n'
cp -R "$icon_res_dir"/. "$decode_dir/res/"

printf 'Rebuilding APK...\n'
unsigned_apk="$work_dir/Photo-Sphere-v0.9-unsigned.apk"
"$java_bin" -jar "$apktool_jar" b -q -p "$framework_dir" "$decode_dir" -o "$unsigned_apk"

keystore="$signing_dir/photo-sphere-local.jks"
properties="$signing_dir/keystore.properties"
if [[ ! -f "$keystore" && ! -f "$properties" ]]; then
  printf 'Generating a private local signing key...\n'
  umask 077
  signing_password="$(openssl rand -hex 24)"
  signing_alias="photosphere-local"
  "$keytool_bin" -genkeypair -noprompt \
    -keystore "$keystore" -storetype JKS \
    -storepass "$signing_password" -keypass "$signing_password" \
    -alias "$signing_alias" -keyalg RSA -keysize 3072 -validity 10000 \
    -dname "CN=Photo Sphere Local Build, O=Local Build"
  {
    printf 'alias=%s\n' "$signing_alias"
    printf 'store_password=%s\n' "$signing_password"
    printf 'key_password=%s\n' "$signing_password"
  } > "$properties"
  chmod 600 "$keystore" "$properties"
elif [[ ! -f "$keystore" || ! -f "$properties" ]]; then
  fail "incomplete signing state in $signing_dir; restore both files from backup"
fi

signing_alias="$(awk -F= '$1 == "alias" {print substr($0, index($0, "=") + 1)}' "$properties")"
store_password="$(awk -F= '$1 == "store_password" {print substr($0, index($0, "=") + 1)}' "$properties")"
key_password="$(awk -F= '$1 == "key_password" {print substr($0, index($0, "=") + 1)}' "$properties")"
expected_certificate="$(awk -F= '$1 == "certificate_sha256" {print substr($0, index($0, "=") + 1)}' "$properties")"
[[ -n "$signing_alias" && -n "$store_password" && -n "$key_password" ]] || fail "invalid signing properties"

printf 'Signing and zip-aligning APK...\n'
signer_args=(
  --apks "$unsigned_apk" --out "$signed_dir" \
  --ks "$keystore" --ksAlias "$signing_alias" \
  --ksPass "$store_password" --ksKeyPass "$key_password"
)
if [[ -n "$expected_certificate" ]]; then
  signer_args+=(--verifySha256 "$expected_certificate")
fi
"$java_bin" -jar "$signer_jar" "${signer_args[@]}"

signed_apks=("$signed_dir"/*.apk)
[[ -f "${signed_apks[0]}" && ${#signed_apks[@]} -eq 1 ]] || fail "expected exactly one signed APK in $signed_dir"
cp "${signed_apks[0]}" "$output_apk"
"$java_bin" -jar "$signer_jar" --apks "$output_apk" --onlyVerify >/dev/null

printf '\nBuild complete.\n'
printf 'APK:    %s\n' "$output_apk"
printf 'SHA256: %s\n' "$(hash_file "$output_apk")"
printf 'Signing key: %s (back up this directory; never publish it)\n' "$signing_dir"
