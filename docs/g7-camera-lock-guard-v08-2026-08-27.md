# G7 Photo Sphere v0.8 相机锁死保护回执（2026-08-27）

## 状态

**v0.8 已在 Pixel 10 Pro XL 完成首次冷启动实时取景，并连续通过三轮“Photo Sphere 留在后台 → 系统 Pixel Camera 取景并退出 → 恢复原 Photo Sphere 任务”的热恢复实机验证。** 第二、三轮均真实触发 2 秒信号量保护，随后成功启动取景流，没有复现旧 ANR；热恢复闸门为 3/3 PASS。用户随后在断开 USB 的自然环境中完成完整 360° 球形全景，详见 G8。

安装前，目标机上的 v0.7 已被精确强行停止。v0.8 安装后 `com.shamim.cam` 仍为 `stopped=true`、无进程，CameraService 活动客户端为空。系统 Pixel Camera `com.google.android.GoogleCamera` 未被停止。后续启动与交接均由用户在手机上手动完成，ADB 只读取状态与日志。

## 真实故障

复现顺序为：先使用系统 Pixel Camera，退出到后台后再恢复已有的 Photo Sphere 任务。系统 Pixel Camera 在 Photo Sphere 恢复前约 13 秒已经断开 camera 0，因此它不是持续占用摄像头的直接原因。

Android 在 2026-08-27 16:57:33 记录唯一一次 `data_app_anr`：

```text
Input dispatching timed out
Waited 5003ms for FocusEvent(hasFocus=true)
```

ANR 中的等待链为：

```text
main
  bmj.b(...)                         waiting for bmj monitor

Camera-Ex
  ajy.run(...)
  bmj.h()                            holds bmj monitor
  bmj.n(...)
  Semaphore.acquire()               waits indefinitely
```

`bmj` 的日志身份是 `com/google/android/apps/camera/app/LegacyCameraController`。CameraService 同时显示第一次 Photo Sphere camera 0 连接已经成功；第二个相机请求却在持有控制器 monitor 时再次等待零许可的信号量，而第一次连接的完成回调必须取得同一 monitor。由此形成应用内部互等。

后续多次“PhotoSphere 没有响应”弹窗没有产生新的 `am_anr`；它们是同一旧 ANR 对话框在点击“等待”后反复恢复。当前新进程的 Input Dispatcher 通道当时仍标记为 `responsive=true`。

## 最小修复

可复现补丁：`patches/0005-bound-legacy-camera-semaphore-wait.patch`。

仅修改 `smali_classes2/bmj.smali`：

- 把无期限的 `Semaphore.acquire()` 改为最长 2 秒的 `tryAcquire(2000, MILLISECONDS)`；
- 超时后跳过本次重复相机请求并释放 `bmj` monitor；
- 不强制释放信号量，不尝试并行打开第二个相机会话；
- 不修改 Photo Sphere 采集、LightCycle 拼接、保存、类型菜单、包名、权限或系统相机。

2 秒上限低于 Android 此处 5 秒的输入分发超时。根据已捕获的故障链，monitor 释放后，第一次已成功连接的相机回调应能继续完成。若超时发生时其实没有可完成的首次连接，最坏预期从永久 ANR 收敛为取景失败但 UI 仍可响应；这仍需要真机验证。

## 产物

- 文件：`dist/Photo-Sphere-v0.8-camera-lock-guard.apk`
- 大小：`172531844` 字节
- SHA-256：`b9f6a41c3c5f4506666fde1b23b3d2e196d399e2def6b75227b05e51c5ed38e2`
- 包名：`com.shamim.cam`（由与 v0.7 逐字一致的 Manifest 证明）
- 显示名：`Photo Sphere`（Manifest/资源未变）
- 版本：`8.5.300.450594193.08` / versionCode `65075803`（未变）
- 签名证书 SHA-256：`79d76eb4ae694dc4b1b4d7ec064eec6f52998879b1658f1aa40bc7f1b806db76`
- 签名：APK Signature Scheme v2、v3；zipalign PASS
- ZIP：完整性 PASS；仅包含 `classes.dex`、`classes2.dex`、`classes3.dex`

与 v0.7 的 ZIP 内容逐项比较后，除签名元数据外仅有：

- `classes2.dex`：包含本次控制器补丁；
- `pinlist.meta`：因 DEX 长度变化而自动重算的文件偏移索引。

Manifest、资源、`classes.dex`、`classes3.dex` 和全部原生库逐字一致。

## 安装回执与验证边界

2026-08-27 17:30:36，`adb install -r` 返回 `Success`。安装后回执：

- 设备端 `base.apk` SHA-256 与本地产物完全一致：`b9f6a41c3c5f4506666fde1b23b3d2e196d399e2def6b75227b05e51c5ed38e2`；
- versionCode、versionName 与 v3 签名身份保持不变；
- `ceDataInode=1047522` 与安装前一致，证明原位更新没有卸载或清除应用数据；
- `com.shamim.cam` 为 `stopped=true` 且无进程，证明安装后没有自动启动；
- CameraService 活动客户端为空；
- 系统 Pixel Camera 仍为 `stopped=false`；
- 前台页面仍是 Pixel Launcher。

## 首次冷启动回执

安装后由用户亲自从 Pixel Launcher 点击 `Photo Sphere`。用户确认出现实时取景。只读设备证据：

- 2026-08-27 17:34:03，CameraService 记录 camera 0 连接到 `com.shamim.cam` PID 17568；
- `CameraLauncher` 为 top resumed activity 与当前焦点窗口；
- ActivityTaskManager 的 CameraStateMonitor 记录同一 camera 0 / PID 17568；
- 当次日志没有新的 ANR、FATAL EXCEPTION 或“等待相机信号量超时”记录。

这构成 v0.8 “安装后首次冷启动并取得实时取景”的真机 PASS；尚未拍摄。

## 系统相机交接与热恢复回执

用户按 Home 将 Photo Sphere 留在最近任务，没有划掉进程。随后手动打开系统 Pixel Camera，确认取景，再按 Home 回桌面；最后从桌面重新打开 Photo Sphere。用户确认恢复后出现实时取景。只读设备证据形成完整闭环：

- Photo Sphere 的 PID 17568 与 task 11943 在整个测试中保持不变；它不是被杀后冷启动的新进程；
- 系统 Pixel Camera 于 2026-08-27 17:56:44 连接 camera 0，并于 17:56:49 正常断开；交接前 camera 0 无活动客户端；
- 2026-08-27 18:04:30，系统对原 Photo Sphere PID 17568 执行 `am_unfreeze` 并恢复原 task 11943；同一时刻 CameraService 将 camera 0 重新连接到 `com.shamim.cam`；
- 18:04:33，CameraService 记录 `Start camera streaming for com.shamim.cam (PID 17568, UID 10488)`；用户同时确认屏幕已有取景；
- 本轮没有新增 `am_anr`、`am_crash`、进程死亡或 `FATAL EXCEPTION`；
- 本轮没有出现 `doRequestCamera: timed out waiting for camera semaphore; skip duplicate request`，说明补丁的 2 秒超时分支未被触发。这一轮证明 v0.8 在真实热恢复路径上没有回归并成功完成交接，但单轮成功不能单独证明旧竞态已被彻底消除。

第二轮由用户重复同一操作序列。Photo Sphere 仍使用原 PID 17568：

- 2026-08-27 18:07:03，Photo Sphere 正常断开 camera 0；
- 18:07:05，系统 Pixel Camera PID 1884 连接 camera 0，并于 18:07:11 正常断开；
- 18:07:37，原 Photo Sphere PID 17568 重新连接 camera 0；
- 18:07:39.205，日志出现 `doRequestCamera: timed out waiting for camera semaphore; skip duplicate request`，证明 v0.8 的 2 秒保护分支被真实执行；
- 18:07:39.321，CameraService 记录 `Start camera streaming for com.shamim.cam (PID 17568, UID 10488)`，距保护分支释放控制器 monitor 仅 116 毫秒；
- 用户确认屏幕已有取景，系统没有新增 ANR、崩溃或进程死亡。

第二轮形成了补丁的动态因果证据：与旧 ANR 相同的重复请求不再永久持有 `bmj` monitor，而是在 2 秒后退出；已有相机会话随即完成回调并开始取景。

第三轮再次重复相同操作序列，并复现相同的安全恢复结果：

- 2026-08-27 18:09:34，Photo Sphere PID 17568 正常断开 camera 0；
- 18:09:35，系统 Pixel Camera PID 1884 连接 camera 0，并于 18:09:41 正常断开；
- 18:09:43，原 Photo Sphere PID 17568 重新连接 camera 0；
- 18:09:45.241，2 秒保护分支再次记录跳过重复请求；
- 18:09:45.360，CameraService 启动 Photo Sphere 取景流，距保护分支 119 毫秒；
- 用户确认屏幕已有取景，系统没有新增 ANR、崩溃或进程死亡。

因此，G7 的“系统 Pixel Camera → 原 Photo Sphere 任务热恢复”真机闸门为 **PASS（3/3）**。其中两轮真实命中原竞态入口并由补丁恢复，形成可重复的动态修复证据。

后续真机硬化顺序：

1. 连续完成至少三次完整自然场景拍摄；
2. 补测尚未覆盖的 Type，并读取完整球面 JPEG 的 GPano XMP；
3. 明确记录 Google Photos panorama viewer 行为。
