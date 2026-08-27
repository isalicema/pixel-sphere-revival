# G8 v0.8 完整 360° 自然场景回执（2026-08-27）

## 结论

**Pixel 10 Pro XL 上的 Photo Sphere 核心移植成功。**

在 v0.8 已完成冷启动取景和系统相机热恢复 3/3 PASS 后，用户拔掉 USB 线，在真实自然环境中亲自完成了一张完整 360° 球形全景。采集、引导、合成与成片均可用；用户同时确认 Fish eye 与 Sphere 两种呈现均正常。

这补齐了此前 G3 只有 9 帧局部序列、不能证明完整球面闭环的关键缺口。结合既有静态与真机证据，当前已经证明：

- `Photo Sphere` 作为独立应用与系统 Pixel Camera 共存；
- 启动直接进入 Photo Sphere，普通相机危险入口已收敛；
- 完整 360° 引导采集与 LightCycle 合成链能在 Pixel 10 Pro XL `mustang` 上完成；
- Fish eye 与 Sphere 呈现可用；
- 系统 Pixel Camera 与 Photo Sphere 之间的热恢复连续三轮成功，后两轮由 v0.8 的 2 秒保护真实救回；
- 用户可以脱离电脑和 ADB 独立完成目标拍摄。

因此，项目最初的核心产品目标——在 Pixel 10 Pro XL 上恢复一款可独立使用的 Photo Sphere 相机——判定为 **PASS**。

## 证据边界

本轮在 USB 已断开的自然使用环境中完成，结果来自用户现场目视确认，没有同步 ADB 日志或重新读取本轮 JPEG 的 GPano XMP。因此本回执不额外声称本轮具体输出尺寸、源帧数或 `UsePanoramaViewer` 字段值。

此前 G3 已对同一保存链的局部输出验证 `IsPhotosphere=True`、`ProjectionType=equirectangular`、完整球面坐标与源帧计数；本轮则补充完整 360° 的真实使用证明。两者合并构成当前端到端判断，但不是对同一张文件的双重验证。

## 后续硬化（不阻塞核心移植成功）

- 连续完成至少三次完整自然场景拍摄，验证长时间稳定性；
- 补测 Horizontal、Vertical、Wide angle 三种 Type；
- 方便时重新连接设备，对本轮或下一轮完整 360° JPEG 读取 GPano XMP，并明确记录 Google Photos panorama viewer 行为；
- 保留 v0.8 APK、SHA-256、签名证书与补丁作为可恢复基线。
