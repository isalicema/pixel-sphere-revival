# G1 label-only 构建与安装回执（2026-08-27）

## 目标

消除原 SGCAM 与系统 Pixel Camera 在 launcher 中同名为“相机”的歧义。本候选只修改应用显示名，不修改包名、入口或 Photo Sphere 逻辑。

## 构建身份

- 输入：`artifacts/input/SGCAM_8.5.300.XX.10_STABLE_V24.apk`
- 输入 SHA-256：`5627913aadbda11a0d7abf77b670802335995f2c635ef9af5fee5161a615f76c`
- 唯一功能改动：`AndroidManifest.xml` 的 application label 从 `@string/app_name` 改为字面量 `Photo Sphere`
- 输出：`dist/Photo-Sphere-G1-label-only.apk`
- 输出 SHA-256：`6b8dd875d65ba697871986be59ac8c56a7ff5aa637e9a5fd9e99434a1b2cd403`
- 包名：`com.shamim.cam`
- 版本：`8.5.300.450594193.08`（versionCode `65075803`）

签名后的 APK 已重新反解确认：

```text
package="com.shamim.cam"
android:label="Photo Sphere"
```

ZIP 完整性、zipalign 与 APK Signature Scheme v3 均验证通过。候选使用本项目专属的本地 RSA-4096 密钥；证书 SHA-256 为：

```text
79d76eb4ae694dc4b1b4d7ec064eec6f52998879b1658f1aa40bc7f1b806db76
```

签名材料位于被忽略的 `.signing/`，不得分发；后续同包名升级必须保留这把密钥。

## 设备替换回执

目标机：Pixel 10 Pro XL `mustang`（公开记录已移除设备序列号）。

替换前重新确认：

- 飞行模式开启；
- Wi-Fi 关闭；
- 系统 Pixel Camera `com.google.android.GoogleCamera` 存在；
- 原 SGCAM `com.shamim.cam` 存在。

随后停止并卸载原 SGCAM，安装 label-only 候选。ADB 的卸载与安装均返回 `Success`。替换后：

- `com.google.android.GoogleCamera` 仍存在，未被修改；
- `com.shamim.cam` 已安装；
- 新包处于 `stopped=true notLaunched=true`，尚未启动；
- 危险运行时权限因全新安装而全部重置。

## 尚未证明

- launcher 实机可见名称仍需用户目视确认；
- 权限硬门后的真实相机 UI 尚未确认；
- Photo Sphere 菜单/默认路由、LightCycle 初始化、完整采集、拼接、JPEG 保存与 GPano XMP 均未验证。

因此本回执只证明“独立包已以 Photo Sphere 名称构建并安装”，不构成 Photo Sphere 功能 PASS。

## 首次启动动态回执

用户从 launcher 打开 `Photo Sphere` 并授予本轮运行所需权限后：

- 前台仍为 `com.shamim.cam/com.android.camera.CameraLauncher`；
- 应用进程 PID 为 `22913`，未出现进程级 `FATAL`；
- SGCAM 首启展示了三个 Telegram 社区推广入口；它们不是 Photo Sphere 功能的一部分，当前前台 Activity 也没有跳出应用；
- 相机、麦克风、照片/视频权限已授予；位置权限也被授予为 one-time，测试结束后应撤回；
- 进程日志已保存到 `evidence/g1-label-only-20260827-1534/app-logcat-after-permissions.txt`。

首个可归因的运行时失败为默认普通 Photo 路径：

```text
CAM_A: OneCamera failed to open, closing lifetime.
java.lang.NullPointerException: Attempt to invoke virtual method
'void com.google.googlex.gcam.Gcam.d(...)' on a null object reference
```

这证明普通 Photo 默认入口不能作为 Pixel 10 Pro XL 的宿主成功标准，也为“绕过普通 Photo、直接路由到 Photo Sphere”提供了真机依据。但该错误尚不能证明 LightCycle/Photo Sphere 自身失败；下一步必须先关闭推广提示并手动探测 Photo Sphere 入口。

### 用户目视与权限补充

用户拒绝了后续出现的“管理所有文件”特殊权限。设备侧 `appops` 回执为：

```text
MANAGE_EXTERNAL_STORAGE: default; rejectTime=...
```

返回默认相机界面后，用户观察到黑屏；点击“模式”后取景内容可见，并出现“全景”“全景照片”“智能镜头”三个入口；再次返回默认相机则恢复黑屏。这与普通 Photo 路径的 `OneCamera failed to open` 一致，同时说明相机基础取景并非在所有 UI 状态下整体失效。

反编译简体中文资源确认：

```text
mode_panorama = 全景
mode_photosphere = 全景照片
mode_lens = 智能镜头
```

因此下一探针应点击第二项“全景照片”，而不是第一项普通“全景”。点击前已清空 logcat，以隔离 LightCycle/Photo Sphere 初始化记录。
