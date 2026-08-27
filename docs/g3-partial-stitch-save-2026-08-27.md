# G3 局部 Photo Sphere 合成与保存回执（2026-08-27）

## 用户结果

用户在 Pixel 10 Pro XL 上手动进入“全景照片”，完成一轮短序列后主动停止：

- 采集过程正常；
- 出现处理状态；
- 生成缩略图；
- 合成照片完成；
- 用户目视确认成片可用。

## 运行日志

隔离日志保存在 `evidence/g3-short-stitch-20260827-1556/`。系统相机管线记录了 9 次 3264×2448、quality 100 的 JPEG 帧压缩；随后 MediaStore 发出新媒体事件，SGCAM 以 `android.provider.action.REVIEW` 将输出 URI 交给 Google Photos。同期 CameraService 的 error trace 为 0，未发现当前采集进程的 `FATAL`、`SIGSEGV` 或 `SIGABRT`。

设备历史记录显示此前一次退出采集后旧 PID `22913` 的 camera client 发生 binder died，应用随后以 PID `24076` 恢复并完成本轮短序列。当前尚不能把该进程更替归因为崩溃或设计内重启；后续冷启动/连续采集回归需继续监测。

## MediaStore 与 XMP

本轮测试时段唯一新增图片：

```text
_id=6192
_display_name=SGCAM_20260827_154058615.PHOTOSPHERE.jpg
mime_type=image/jpeg
width=3120
height=5850
relative_path=DCIM/Camera/
```

验证只流式扫描该测试文件的 XMP 文本字段，没有保存、显示或分析图像画面。关键 GPano 字段：

```text
GPano:UsePanoramaViewer="False"
GPano:IsPhotosphere="True"
GPano:ProjectionType="equirectangular"
GPano:CroppedAreaImageHeightPixels="5850"
GPano:CroppedAreaImageWidthPixels="3120"
GPano:FullPanoHeightPixels="8086"
GPano:FullPanoWidthPixels="16172"
GPano:CroppedAreaTopPixels="1326"
GPano:CroppedAreaLeftPixels="5828"
GPano:SourcePhotosCount="9"
GPano:PoseHeadingDegrees="84.0"
```

`IsPhotosphere=True`、等距柱状投影、9 张源照片与完整球面/裁剪区域坐标证明 JPEG+GPano 输出链成立。由于这是故意提前停止的局部测试，`UsePanoramaViewer=False` 且裁剪区域小于完整球面；因此它构成“局部 Photo Sphere 端到端 PASS”，不构成完整 360° panorama viewer PASS。

## 下一闸门

完成一轮所有白点/圆点引导，等待合成并重新验证：

- `UsePanoramaViewer=True`（或 Google Photos 实际进入可拖动的 360 viewer）；
- 完整球面覆盖与合理尺寸；
- 应用在长采集和拼接阶段无 OOM/native crash；
- 成片保存后冷启动仍可再次进入 Photo Sphere。
