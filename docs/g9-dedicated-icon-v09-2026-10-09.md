# G9 Photo Sphere v0.9 专属图标候选（2026-10-09）

> 2026-10-10 状态更新：Alice 最终确认 blue wrap v6：钴蓝圆盘、深蓝球面环与扁平半透明白色 360° 横带。该方案已经接入普通、自适应和主题图标，完成 v0.9 构建并原位安装到 Pixel 10 Pro XL；普通桌面图标、冷启动取景和新照片产出已获 Alice 实机确认。

## 目标

把 Photo Sphere 与 Pixel 原生相机在桌面上清楚区分，同时不改动 v0.8 已验证的 Photo Sphere、LightCycle 或相机热恢复逻辑。

## 设计与资源

- 彩色图形：`assets/icon/photosphere-icon-native-blue-wrap-v6.png`，源图 SHA-256 `c1a911c74c19e7a77fabd3f6955ae1226d6f57fa35c3793090203e192192bc3c`；
- 背景：钴蓝圆盘及 adaptive background `#0B70FA`，与 Pixel Camera 的白底彩色镜头图标明显区分；
- 资源：普通 PNG、Android adaptive icon、圆形图标入口和 Android 13+ monochrome 主题图标；
- 主题图标：使用基础 APK 内置 `quantum_ic_panorama_photosphere_white_24` 的单色 alpha 轮廓；
- 资源重建脚本：`scripts/render-approved-icon-v6.py`；
- 历史草案与来源说明：`assets/icon/README.md`；
- Android 资源：`assets/android/res/`。

普通和 adaptive 图标使用本项目最终确认的彩色原稿，不复用 Pixel Camera 的彩色镜头/光圈启动图标。Android 13+ themed icon 的单色蒙版对应 Google Material Icons `panorama_photosphere`，按 Apache License 2.0 标注来源。

## 补丁边界

`patches/0006-photo-sphere-icon.patch` 同时替换：

1. `<application android:icon>`；
2. `<application android:roundIcon>`；
3. 启用的 `com.android.camera.CameraLauncher` alias 图标；
4. 备用的 `com.android.camera.CameraLauncher1` alias 图标；
5. 两个 alias 的 SEND/SEND_MULTIPLE intent-filter 图标。

只改 application 图标不足：该 APK 的 launcher alias 原本单独指定 Pixel Camera 图标，会覆盖 application 图标。

## 构建与静态验证

- 输入 APK SHA-256：`5627913aadbda11a0d7abf77b670802335995f2c635ef9af5fee5161a615f76c`
- 输出：`.local/output/Photo-Sphere-v0.9-dedicated-icon.apk`
- 输出大小：`172782348` bytes
- 首次实机验收/当前设备 APK SHA-256：`61c37c3ff900e0dd80d882c23bc63a1867e4e4a66ae8fe88ac5b26e55ea5b9af`
- 2026-10-11 发布前全量重建 APK SHA-256：`32cf9206024611ba302603b950ceafa90736f3e74a7cb8ba468a9201f62a4f93`
- 签名证书 SHA-256：`79d76eb4ae694dc4b1b4d7ec064eec6f52998879b1658f1aa40bc7f1b806db76`
- 签名验证：APK Signature Scheme v3 PASS；zipalign PASS；证书指纹强制校验 PASS。

构建输入确认 application、启用 launcher alias 和备用 launcher alias 均引用 `@mipmap/photosphere_launcher`；签名后 APK 同时包含普通、自适应与 monochrome 图标资源。签名后 APK 内的 432×432 彩色 foreground、legacy launcher 与 monochrome mask 均已逐像素回读，与构建输入完全一致。apktool 会重新编码 PNG，因此文件字节哈希不同，但 RGBA 像素差异为空。

XML 资源通过 `xmllint`，完整六补丁构建通过，无 `.rej` 或 `.orig` 残留。

发布前重新构建会因为 ZIP/签名时间元数据产生不同的整体 APK 哈希。为排除代码或资源漂移，项目从设备只读拉取已验收 APK，与新构建包逐一解压并比较全部 3069 个 ZIP 条目；内容差异为 0，两者按“条目名＋解压内容哈希”归一化后的 SHA-256 均为 `df41ea58bfb76abbba05fd6a1b2e23a079dfb5f8b1674e8c51c5e06708b1b31f`。临时设备 APK 比较副本已删除，未进入 Git。

## 开发中发现并纠正的问题

1. 首次脚本更新没有正确替换补丁数量，保护检查在第六个补丁后主动中止；没有生成 APK。修正后从原始 APK 重新构建。
2. 第一份图标 APK 暴露 launcher alias 仍覆盖为 Pixel Camera 图标；该候选未安装，补丁补齐所有 alias 后重新构建。
3. 一份中间候选误用了 `.local/signing/` 的另一证书（`5997…`），不能覆盖实机 v0.8；该候选未安装且被最终输出覆盖。构建脚本现会优先使用保留的 `.signing/`，并强制校验 v0.8 证书 `79d7…`。

## 当前验证边界

- 本地资源、固定原稿哈希、透明噪点裁切、完整构建、zipalign、v3 签名、证书连续性与签名后资源逐像素回读：PASS。
- Pixel 10 Pro XL 安装/原位升级：PASS；`adb install -r` 返回 `Success`，`firstInstallTime` 保持 `2026-08-27 15:28:47`，`lastUpdateTime` 更新为 `2026-10-10 23:22:11`。
- 普通桌面图标目视：PASS，Alice 确认图标已更新；Android 主题图标：未验证。
- 冷启动取景与新照片产出：PASS；本轮没有足够证据把该照片标记为完整 360°，Type 菜单、Fish eye / Sphere 与系统相机热恢复也未复测。
- 当前实机已安装 v0.9，且通过图标/取景/拍摄冒烟验收；专项回归项目仍按上方边界保留。

> 2026-10-11 状态更新：主摄变焦实验被产品决策放弃后，Pixel 10 Pro XL 已再次通过 `adb install -r` 原位恢复上述 v0.9 APK。设备端 SHA-256 与本页记录一致，首次安装时间未变化；本次回退后的首次启动尚未重新观察。
