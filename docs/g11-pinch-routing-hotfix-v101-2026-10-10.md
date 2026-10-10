# G11：双指触摸路由热修复 v1.0.1

日期：2026-10-10（Asia/Shanghai）

## 问题

v1.0 安装后可以进入取景，但 Pixel 10 Pro XL 第一次双指缩放即让 `com.shamim.cam` 主进程崩溃。Alice 同时看到系统的“所有文件访问权限”应用设置页面；该页面外观不能单独证明应用重新请求了权限。

ADB crash buffer 给出直接原因：

```text
10-10 23:49:05.864 AndroidRuntime: FATAL EXCEPTION: main
java.lang.IllegalArgumentException: min zoom value hasn't been initialized properly
at hdq.onScaleBegin(...)
at hiu.onScaleBegin(...)
at android.view.ScaleGestureDetector.onTouchEvent(...)
at com.google.android.apps.camera.ui.wirers.PreviewOverlay.onTouchEvent(...)
```

v1.0.1 的反编译结果中没有 `MANAGE_EXTERNAL_STORAGE` 声明，也没有全文件访问设置 Action。可确认的因果链是双指事件进入通用相机缩放检测器并崩溃；没有证据把这次崩溃归因于 Photo Sphere 重新申请全文件权限。

## 原因与修复

专版从 v0.8 起隐藏并禁用了原 `.6× / 2× / 5×` 控件，通用相机缩放控制器没有完成最小倍率初始化。`PreviewOverlay` 原先先执行该通用检测器，只有绕过这一分支后才会继续调用模块级 `OnTouchListener`；因此 v1.0 新增的 Photo Sphere 变焦代码尚未收到事件，应用已先崩溃。

`0008-photo-sphere-pinch-routing-hotfix.patch` 在专版 `PreviewOverlay` 可触摸时直接进入模块监听器分支：

- 跳过通用 `hix/hiu/hdq` 缩放检测器；
- 保留既有 GestureDetector 与模块 `OnTouchListener`；
- 让 Photo Sphere 的 `bpt → dwv → dws` 链路接收双指事件；
- 不改 Camera1 裁切、LightCycle FOV、采集锁定、Type 菜单或相机热恢复逻辑。

该改动按单用途产品边界生效：此 APK 只支持 Photo Sphere，不承诺被隐藏的普通相机模式仍使用通用缩放手势。

## 本地验证

- 固定基础 APK 上八补丁完整应用：PASS；无 `.rej` / `.orig`。
- apktool 完整重建：PASS。
- 输出反编译回读：`PreviewOverlay` 在可触摸状态下跳转到模块监听器分支，PASS。
- `MANAGE_EXTERNAL_STORAGE` 与全文件访问设置 Action 扫描：无匹配。
- zipalign：PASS。
- APK Signature Scheme v3：PASS。
- 签名证书连续性：`79d76eb4ae694dc4b1b4d7ec064eec6f52998879b1658f1aa40bc7f1b806db76`，PASS。
- APK：`.local/output/Photo-Sphere-v1.0.1-main-camera-zoom-hotfix.apk`
- 大小：`172782348` bytes。
- SHA-256：`086357e2eb2b9b5d47ca8479f33e8a60f6ce89d21ac28774de9f9768e56fabdb`。

## 安装状态与验证边界

Alice 明确授权后，v1.0.1 已于 2026-10-10 23:56:10（Asia/Shanghai）通过 `adb install -r` 原位安装到 `mustang / Pixel 10 Pro XL`。首次安装时间保持不变；设备端 `base.apk` SHA-256 与本地候选一致；启动入口仍为 `com.shamim.cam/com.android.camera.CameraLauncher`。

Alice 随后确认变焦已经出现，证明 v1.0.1 至少通过了“不再于手势开始时崩溃并出现缩放效果”的首项验证；没有继续验证倍率精度、采集锁定或 2× 拼接。Alice 判断这一交互体验价值不足，于 2026-10-11 明确放弃变焦并要求回到 v0.9。本热修复不进入支持版本，只作为实验记录保留。
