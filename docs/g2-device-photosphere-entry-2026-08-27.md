# G2 Photo Sphere 真机入口回执（2026-08-27）

## 手动入口

在 Pixel 10 Pro XL `mustang` 上，从默认黑屏的普通 Photo 页面进入“模式”，点击第二项“全景照片”（资源键 `mode_photosphere`）。

用户目视结果：

- 成功进入“全景照片”；
- 出现可见取景框；
- 应用没有闪退；
- 首次按快门前尚未出现白点/圆点引导。

设备侧仍显示前台 Activity 为：

```text
com.shamim.cam/com.android.camera.CameraLauncher
```

进程 PID 仍为 `22913`。切换前已经清空 logcat；进入模式后按 PID 抓取的缓冲为空，没有 `FATAL`，但也没有可用于证明 `liblightcycle.so` 或 LightCycle pipeline 已初始化的日志。因此“入口可见、取景框可见”只是入口级进展，不是功能 PASS。

## 下一探针

经典 Photo Sphere 交互通常在首次按快门后开始采集并显示下一帧的对准点。下一步只采集第一帧：

1. 对准无隐私、静态、光线稳定的场景；
2. 保持手机不动并按一次快门；
3. 暂不继续转动或完成整圈；
4. 观察是否出现白点/圆形对准引导、是否黑屏、是否闪退；
5. 随后立即采集隔离日志。

只有首帧引导出现，才能继续测试多帧采集；只有 `FinishCapture → stitching → JPEG → GPano XMP` 完整通过，才能判定 Photo Sphere 复活。

## 首帧探针结果：PASS

用户在无敏感内容的测试场景中按下快门一次：

- 白点与圆形对准引导立即出现；
- 用户没有继续转动或采集其他点；
- 随后退出本次采集；
- 应用进程保持存活。

隔离日志保存于 `evidence/g2-first-frame-20260827-1548/`。其中出现了 LightCycle 对齐器的真实首帧调用：

```text
alignment_estimator.cc: Camera input to AddImage() has different width (3264)
than specified image_match_width_ (1600), scaling to image_match_width_
```

这条记录确认图像已经进入 `AddImage()`，而不仅是 UI 模拟了引导。3264→1600 的宽度差被算法显式自动缩放，目前是需要监测成像质量的 warning，不是本轮失败。同期：

- 未发现应用进程级 `FATAL`、`SIGSEGV` 或 `SIGABRT`；
- CameraService `Camera error traces (0)`；
- 采集退出后应用仍在前台并持有 camera 0。

本轮因用户在首帧后退出，没有触发或证明 `FinishCapture`、stitching、JPEG 保存与 GPano XMP。下一闸门为 3–5 帧短序列后主动停止并观察处理/保存。
