#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(cd "${script_dir}/.." && pwd)"
timestamp="$(date '+%Y%m%d-%H%M%S')"
output_dir="${1:-${project_root}/evidence/device-baseline-${timestamp}}"

if ! command -v adb >/dev/null 2>&1; then
  echo "adb is required" >&2
  exit 1
fi

adb start-server >/dev/null
device_serial="$(adb devices | awk 'NR > 1 && $2 == "device" { print $1; exit }')"

if [[ -z "${device_serial}" ]]; then
  echo "No authorized Android device found. Connect the phone, unlock it, and accept USB debugging." >&2
  exit 2
fi

mkdir -p "${output_dir}"

{
  echo "captured_at=$(date '+%Y-%m-%dT%H:%M:%S%z')"
  echo "model=$(adb -s "${device_serial}" shell getprop ro.product.model | tr -d '\r')"
  echo "device=$(adb -s "${device_serial}" shell getprop ro.product.device | tr -d '\r')"
  echo "product=$(adb -s "${device_serial}" shell getprop ro.build.product | tr -d '\r')"
  echo "hardware=$(adb -s "${device_serial}" shell getprop ro.hardware | tr -d '\r')"
  echo "hardware_sku=$(adb -s "${device_serial}" shell getprop ro.boot.hardware.sku | tr -d '\r')"
  echo "low_ram_config=$(adb -s "${device_serial}" shell getprop ro.config.low_ram | tr -d '\r')"
  echo "android_release=$(adb -s "${device_serial}" shell getprop ro.build.version.release | tr -d '\r')"
  echo "sdk=$(adb -s "${device_serial}" shell getprop ro.build.version.sdk | tr -d '\r')"
  echo "build_id=$(adb -s "${device_serial}" shell getprop ro.build.id | tr -d '\r')"
  echo "security_patch=$(adb -s "${device_serial}" shell getprop ro.build.version.security_patch | tr -d '\r')"
  echo "build_fingerprint=$(adb -s "${device_serial}" shell getprop ro.build.fingerprint | tr -d '\r')"
  echo "supported_abis=$(adb -s "${device_serial}" shell getprop ro.product.cpu.abilist | tr -d '\r')"
  echo "page_size=$(adb -s "${device_serial}" shell getconf PAGE_SIZE 2>/dev/null | tr -d '\r')"
  echo "linker_16kb_backcompat=$(adb -s "${device_serial}" shell getprop bionic.linker.16kb.app_compat.enabled | tr -d '\r')"
  echo "pm_16kb_backcompat_disabled=$(adb -s "${device_serial}" shell getprop pm.16kb.app_compat.disabled | tr -d '\r')"
} > "${output_dir}/device.txt"

adb -s "${device_serial}" shell dumpsys package com.google.android.GoogleCamera \
  > "${output_dir}/pixel-stock-camera-package.txt" 2>&1 || true
adb -s "${device_serial}" shell pm path com.google.android.GoogleCamera \
  > "${output_dir}/pixel-stock-camera-paths.txt" 2>&1 || true
adb -s "${device_serial}" shell dumpsys package com.sec.android.app.camera \
  > "${output_dir}/samsung-stock-camera-package.txt" 2>&1 || true
adb -s "${device_serial}" shell pm path com.sec.android.app.camera \
  > "${output_dir}/samsung-stock-camera-paths.txt" 2>&1 || true
adb -s "${device_serial}" shell pm list features \
  > "${output_dir}/device-features.txt" 2>&1 || true
adb -s "${device_serial}" shell cat /proc/meminfo \
  > "${output_dir}/memory-info.txt" 2>&1 || true
adb -s "${device_serial}" shell dumpsys sensorservice \
  > "${output_dir}/sensor-service.txt" 2>&1 || true
adb -s "${device_serial}" shell dumpsys media.camera \
  > "${output_dir}/camera-service.txt" 2>&1 || true
adb -s "${device_serial}" shell pm path com.shamim.cam \
  > "${output_dir}/sgcam-package-paths.txt" 2>&1 || true

echo "Baseline saved to ${output_dir}"
