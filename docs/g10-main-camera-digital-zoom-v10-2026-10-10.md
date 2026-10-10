# G10：Photo Sphere 主摄数码变焦 v1.0

日期：2026-10-10（Asia/Shanghai）

## 目标与边界

v1.0 只为 Photo Sphere 增加当前主摄的数码裁切，不恢复原 SGCam 的 `.6× / 2× / 5×` 多镜头按钮，不开放前摄，也不允许在一组球形照片的采集中途改变倍率。

交互采用 Photo Sphere 原本已经注册的双指手势：按快门前可在 1.0×–2.0× 范围内缩放，松手后以短 Toast 显示实际 Camera1 倍率；进入白点采集后，预览触摸层拒绝缩放。

## 实现链路

基础 APK 的手势代码原本只调整 `dwv` 的 OpenGL 投影视场角，没有把倍率写入相机参数，因此它不是可交付的拍摄变焦。`0007-photo-sphere-main-camera-digital-zoom.patch` 补齐以下链路：

1. 手势结束时读取 Photo Sphere 当前 Camera1 设置并更新 `Laum.p`；
2. 通过既有 `Latu.m(Laum)` / `Camera.Parameters.setZoom()` 路径应用主摄数码裁切；
3. 将请求值限制在 1.0×–2.0× 以及设备实际最大倍率的较小者，并回读驱动实际采用的倍率；
4. 用 `2 * atan(tan(baseFov / 2) / zoom)` 修正交给 LightCycle 的水平视场角；
5. 仅在采集尚未开始时重置当前 Type 的 LightCycle 引导，使白点密度、取景投影与相机裁切使用同一视场角；
6. `Lemn.l` 进入采集态后锁住双指手势，避免同一球形照片中途改变视场角。

## 本地验证

- 七补丁从固定哈希基础 APK 全量应用：PASS；无 `.rej` / `.orig`。
- apktool 完整重建：PASS。
- zipalign：PASS。
- APK Signature Scheme v3：PASS。
- 签名证书连续性：`79d76eb4ae694dc4b1b4d7ec064eec6f52998879b1658f1aa40bc7f1b806db76`，PASS。
- APK：`.local/output/Photo-Sphere-v1.0-main-camera-zoom.apk`
- 大小：`172782348` bytes。
- SHA-256：`2dc2b7b2127403674dac5ec9a1b4de3ed35100c19add39a0a85080766f206f2f`。

## 安装与实机失败结果

Alice 授权后，v1.0 已于 2026-10-10 23:42:55（Asia/Shanghai）通过 `adb install -r` 原位安装到 `mustang / Pixel 10 Pro XL`。首次安装时间保持不变，设备端 `base.apk` 哈希与本地候选一致。

Alice 随后确认普通取景可进入，但第一次双指缩放即失败。ADB crash buffer 精确记录 `23:49:05.864` 主线程崩溃：`IllegalArgumentException: min zoom value hasn't been initialized properly`，调用链来自通用 `PreviewOverlay` 缩放监听器。v1.0 双指变焦验收因此为 FAIL；倍率变化、Toast、采集中锁定与 2× 拼接均未进入可验证阶段。

修复方案另见 [v1.0.1 双指触摸路由热修复](g11-pinch-routing-hotfix-v101-2026-10-10.md)。

## 最终产品决策

2026-10-11（Asia/Shanghai），Alice 在 v1.0.1 上确认变焦已经出现，但认为实际体验“很鸡肋”，明确决定回到 v0.9 并取消变焦。该功能不进入支持版本；本文件和补丁仅作为实验历史保留。
