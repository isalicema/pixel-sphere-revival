# G5 Photo Sphere v0.6 单用途控制面收敛回执（2026-08-27）

## 目标

在已经真机可拍、可拼接、可保存的 Photo Sphere 路径上，移除 Pixel 10 Pro XL 当前不可用或会进入未验证代码路径的控制：变焦切换、前后摄切换，以及 SGCAM 注入的六个顶部快捷按钮。

这一步采用“隐藏危险入口、保留已验证链路”的产品策略，不把未工作的按钮伪装成已经修复。

## 用户观察与静态定位

- 变焦按钮无法完成 0.6x / 2x 切换。
- 前后摄切换会导致应用退出；本轮没有取得该次退出的完整 crash stack，因此不对根因作超出证据的判断。
- 顶部六个缩写来自 SGCAM 的扩展控制。根据资源名和控件绑定，它们分别是：`SHAD`（shading）、`UPSC`（upscaling）、`AWB`（自动白平衡）、`HDNT`（HDRnet 开关）、`WMK`（watermark）、`PRFL`（profile）。这些都不是 LightCycle Photo Sphere 完成采集与拼接所必需的入口。

## v0.6 补丁

1. 将 `CameraSwitchButton` 设为不可见、不可点击且尺寸为 0。
2. 将所有 SGCAM 顶部扩展控件的容器设为不可见且尺寸为 0；保留节点本身，避免宿主初始化因 `findViewById` 找不到控件而出错。
3. 在布局中禁用 `ZoomUi`，并覆写其 `setVisibility(int)`：无论运行时如何重新请求显示，都强制保持 `GONE`。仅改 XML 在 v0.5 真机上不足，运行时仍会重新显示变焦条，因此需要这一层约束。
4. 移除 CameraActivity 启动时的 SGCAM OTA 检查和 dirty-install reset 检查，避免再次出现更新联网路径或 `Reset Required` 数据清除提示。
5. 延续 v0.3 的单模式路由、Telegram 弹层抑制、`MANAGE_EXTERNAL_STORAGE` 删除和独立应用身份。

可复现差异为依次应用：

```text
patches/0001-photo-sphere-label.patch
patches/0002-photo-sphere-dedicated-mode.patch
patches/0003-clean-controls-and-startup.patch
```

三个补丁均已对原始 apktool 反编译树完成 dry-run；第三个补丁包含资源层隐藏、ZoomUi 运行时约束和启动清理。

## 构建完整性

首次 v0.6 回编译候选因 apktool 缓存和空的重复反编译目录产生了额外 ghost dex，体积异常，未安装到手机。清理缓存和四个空重复目录后重新构建；最终 APK 只包含标准的：

```text
classes.dex
classes2.dex
classes3.dex
```

最终产物：

- 文件：`dist/Photo-Sphere-v0.6-single-purpose.apk`
- 大小：`172531844` 字节
- SHA-256：`018d27e5bc0ed19ac37acfde24b21b61442f2d047367258b9d24bcd565868e92`
- 包名：`com.shamim.cam`
- 显示名：`Photo Sphere`
- 签名证书 SHA-256：`79d76eb4ae694dc4b1b4d7ec064eec6f52998879b1658f1aa40bc7f1b806db76`
- 验证：APK Signature Scheme v3、zipalign、ZIP 完整性通过

包名仍与系统 Pixel Camera 的 `com.google.android.GoogleCamera` 不同，原位升级没有覆盖系统相机。

## Pixel 10 Pro XL 真机回执

v0.6 已在飞行模式下原位安装到 `mustang` 并冷启动：

```text
Status: ok
Activity: com.shamim.cam/com.google.android.apps.camera.legacy.app.activity.main.CameraActivity
TotalTime: 363 ms
```

UI hierarchy 结果：

- 仍直接进入唯一模式“全景照片”；
- 不再存在 ZoomUi 节点；
- 不再存在前后摄切换节点；
- 六个 SGCAM 顶部扩展控件均不存在于可访问界面；
- 顶部只保留设置齿轮及其展开箭头；
- 底部只保留快门和缩略图入口。

CameraService 同时记录应用进程使用后摄 camera 0，状态为 `PREVIEW`；观察窗口内没有应用进程的 Fatal，也没有 Reset、Telegram 或“管理所有文件”弹窗。日志中的一次 `AndroidRuntime: Shutting down VM` 属于 UI 自动化进程，不是 Photo Sphere 应用进程。

这构成“单用途控制面收敛 + 冷启动预览”的真机 PASS。它不等于完整 360° 成片已经在 v0.6 上复验。

## 剩余最终闸门

- 拔掉 USB 后完成全部白点/圆点引导并等待合成；
- 在 Google Photos 中验证可拖动的 360° viewer，或取得满足 viewer 条件的完整 GPano XMP；
- 连续完成至少 3 次自然场景拍摄；
- 再次冷启动后仍能拍摄、拼接和保存。
