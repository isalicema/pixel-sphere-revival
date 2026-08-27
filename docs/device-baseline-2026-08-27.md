# Pixel 10 Pro XL 只读设备基线

采集时间：2026-08-27 15:08:21 +0800
证据目录：`evidence/device-baseline-20260827-150821/`
操作边界：仅 ADB 读取；未安装、卸载、启动第三方 APK，未改系统设置或设备文件。

## 身份与系统

| 项目 | 实测值 |
|---|---|
| 型号 | Pixel 10 Pro XL |
| device / product / hardware | `mustang` |
| hardware SKU | `G45RY` |
| Android / SDK | Android 17 / API 37 |
| build ID | `CP2A.260805.005` |
| 安全补丁 | 2026-08-05 |
| ABI | `arm64-v8a` |
| 页面大小 | `4096` |
| MemTotal | `15949056 kB` |

## Photo Sphere 前置条件

- `PAGE_SIZE=4096`：匹配 SGCam V24 中关键 LightCycle/PairIP/SignatureKiller 库的 4 KB ELF LOAD 对齐，当前构建不依赖 16 KB backcompat。
- `ro.config.low_ram` 未设置，且物理内存约 16 GB：与 `ActivityManager.isLowRamDevice() == false` 一致。
- ICM45631 Gyroscope 存在，类型为 `android.sensor.gyroscope(4)`；另有 AOSP corrected gyroscope。
- PackageManager 声明 `android.hardware.camera.level.full`、RAW、manual sensor/post-processing、concurrent camera 等能力。
- CameraService 报告两个逻辑 camera device；静态入口使用旧式 0/1 映射的基础条件存在，具体 stream configuration 仍须进程启动验证。

## 安装身份

- 系统 Pixel Camera 当前包：`com.google.android.GoogleCamera`，用户侧版本 `10.4.117.936816638.14`。
- 系统相机包含 `split_lightcycle_asset_module.apk`，但这不证明当前 UI 或代码仍开放 Photo Sphere。
- `pm path com.shamim.cam` 无输出：目标机目前没有同包名 SGCam，未来侧载不会覆盖 Pixel Camera 或 Google Photos，也不存在 SGCam 同包冲突。

## 闸门处置

1. 页面大小风险：PASS（仅针对当前系统构建）。
2. 陀螺仪门：PASS。
3. low-RAM 门：PASS。
4. 包名并存：PASS。
5. `lightcycle_enabled`、旧相机 API/stream 配置、native 初始化、拼接与保存：HOLD，必须由原包 G1/G2 动态测试证明。

下一步会改变手机状态：安装原始 SGCam V24。没有用户单独明确授权，不执行。
