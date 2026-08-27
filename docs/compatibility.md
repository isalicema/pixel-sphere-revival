# 兼容性与 Samsung 试机

## 已知矩阵

| 设备 | 系统 | 状态 | 证据边界 |
| --- | --- | --- | --- |
| Pixel 10 Pro XL (`mustang`) | Android 17 / `CP2A.260805.005` | **PASS** | 完整 360° 采集与合成；Fish eye、Sphere；系统相机热恢复 3/3 |
| Pixel 10 Pro | 未固定 | 未由本项目验证 | 有上游社区作品，但不能替代本项目真机回执 |
| 其他 Pixel | 未固定 | 未验证 | 可能可用，不作承诺 |
| Samsung Galaxy | 型号/SoC/One UI 未知 | **未验证** | 必须按具体型号测试；目前没有 Samsung 端到端成片证据 |

`Camera2 FULL`、64 位 ARM、陀螺仪和足够内存只是筛选条件，不是 Photo Sphere 成功保证。真正的通过标准必须包括：取景、引导点采集、结束拍摄、LightCycle 合成、JPEG 保存和 360° 元数据/查看全链路。

## 为什么 Samsung 需要单独验证

Shamim V24 下载页提供标准、`RULER`（`com.samsung.android.ruler`）和 `SCAN3D`（`com.samsung.android.scan3d`）等包名变体。这通常与 Samsung 对辅助镜头或相机客户端身份的访问策略有关，但**不能推出 Photo Sphere 或 LightCycle 一定兼容**。

v0.8 的五个补丁只对以下标准输入做过逐字节哈希锁定和构建验证：

```text
SGCAM_8.5.300.XX.10_STABLE_V24.apk
com.shamim.cam
sha256 5627913aadbda11a0d7abf77b670802335995f2c635ef9af5fee5161a615f76c
```

不要把 Samsung 包名变体直接交给当前脚本。即使文件内容相近，补丁上下文、权限和相机 ID 行为也可能不同。

## 需要朋友提供的信息

判断成功概率至少需要：

- 完整型号（例如 `SM-S9280`，不能只写 “S24 Ultra”）；
- Snapdragon 或 Exynos；
- Android 版本、One UI 版本与构建号；
- 是否已安装其他 `com.shamim.cam`；
- 可选：Camera2 Probe 的后摄 hardware level 与 camera ID 列表。

这些信息仍不能代替试拍，但能排除明显不匹配的路径。

## 低风险试机顺序

1. 先确认系统相机工作正常，并关闭其后台取景页面。
2. 安装由本仓库标准输入构建的 APK。它不会覆盖 Samsung 系统相机，但可能与其他 `com.shamim.cam` 冲突。
3. 首次只授予相机、麦克风与照片/媒体权限；不要授予“管理所有文件”。
4. 确认 Photo Sphere 有稳定后摄取景；不要点前摄切换、变焦或其他模式。
5. 按快门后只采集少量引导点，主动停止，等待合成并确认 JPEG 可打开。
6. 上一步成功后，再在非关键场景完成一轮 360°；确认 Google Photos 或兼容 viewer 能识别球形全景。
7. 最后测试“系统相机取景 → 回桌面 → Photo Sphere 取景”，重复三轮。

## 立即停止的信号

- 连续黑屏或多次“没有响应”；
- 系统相机也无法重新取得摄像头；
- 设备明显发热、合成长期不结束；
- 保存失败或输出损坏。

遇到这些情况，先关闭两个相机应用并重启手机。不要 root、不要改系统相机权限数据库，也不要反复安装不同包名变体碰运气。提交兼容性报告时，请使用 GitHub issue 模板，并在日志中删除设备序列号、账号与照片路径等隐私信息。
