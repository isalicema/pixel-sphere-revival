# G2 Photo Sphere 静态模块地图

审计输入：`SGCAM_8.5.300.XX.10_STABLE_V24.apk`
状态：**静态可达 PASS；目标机硬件门 PASS；`lightcycle_enabled` 与端到端动态可达 HOLD**

## 已确认的主链

```text
CameraLauncher alias
  → CameraActivity
  → bju.d(Intent) 选择初始模式
  → heb.e = PHOTO_SPHERE
  → gvj / gwq 注册并激活模式栏项目
  → dsh.gF 的 mode → provider 映射
  → dsh.de / cys provider 构造 PhotoSphere agent
  → emn 宿主模块 + dws LightCycleController
  → dwv.ProcessFrame / AddImage
  → eml.FinishCapture
  → dxs 后台线程
  → dxh LightCycleStitchTask
  → dxx 写 JPEG / GPano XMP 并进入媒体处理链
```

这条链不是根据资源名称猜测出来的：模式枚举、provider 字符串、JNI 声明、帧处理、拼接任务和 XMP 字段在 DEX/smali 中都能闭合。

## 入口与模式注册

| 节点 | 静态证据 | 含义 |
|---|---|---|
| `smali/heb.smali` | `e` 的枚举名是 `PHOTO_SPHERE`，ordinal 为 4 | 证明社区补丁中的 `Lheb;->e` 不是猜测 |
| `smali_classes2/bju.smali` | 静态默认值原为 `Lheb;->b`（PHOTO） | 最小改动可让普通 `ACTION_MAIN` 默认选择 sphere |
| `smali/gvj.smali` | 构造逻辑列表并用 `gwq.j(mode)` 注册实际视图 | 只改默认值、不注册 sphere 会在 UI 激活时失败 |
| `smali/gwk.smali` | `l(Lheb;)` 创建 `MORE_MODES` 项 | 单用途 UI 需单独处理 More 入口 |
| `smali_classes2/dsh.smali` | `heb.e → dsh.de` 被写入模块 provider map | Photo Sphere 已在依赖图中注册，不需凭空创建新 Module |

## 真正的模块门控

`dsh.de` 最终由 `smali_classes2/cys.smali` 的 provider 构造。它在返回 Photo Sphere agent 前明确检查三项：

1. `clb.b`：配置键 `lightcycle_enabled` 必须为真；
2. `SensorManager.getSensorList(4)`：设备至少有一个 type 4 gyroscope；
3. `ActivityManager.isLowRamDevice()`：必须为假。

满足后 provider 返回包含 `Lest` agent 的 optional；否则返回空的 `Lldm.a`。目标机只读基线已确认约 16 GB RAM、`ro.config.low_ram` 未启用，并存在 ICM45631 type-4 gyroscope，因此后两项通过。首要动态疑点只剩 `lightcycle_enabled` 在这个 mod 的 `mustang` 配置里最终解析成什么。

## 捕获与拼接

- `smali/dwn.smali` 封装 `LightCycleNative.ResetForPhotoSphereCapture`、目标数量/命中、陀螺仪校准、撤销和渲染会话。
- `smali/dwv.smali` 将预览帧送入 `LightCycleNative.ProcessFrame`，命中目标后调用 `AddImage`。
- `smali_classes2/eml.smali` 在结束捕获时调用 `LightCycleNative.FinishCapture`，然后启动 `dxs` 线程。
- `smali_classes2/dxs.smali` 创建并提交 `dxh`（日志名 `LightCycleStitchTask`）。
- `smali_classes2/dxh.smali` 驱动 native 渲染、生成 `.jpg`，再调用 `dxx.c(...)` 写入元数据并完成媒体链交接。
- `smali_classes2/dxx.smali` 写入 `UsePanoramaViewer`、`CroppedAreaImageWidthPixels` 等 GPano/XMP 字段；`smali/jfr.smali` 注册 `GPano` namespace。
- JNI 类 `com/google/android/apps/lightcycle/panorama/LightCycleNative` 的实现由 `liblightcycle.so` 提供。

因此“能看到圆点引导”只证明链路走到 controller；“完成捕获”仍没有证明 `FinishCapture → stitch → XMP → MediaStore` 成功。

## 对社区补丁的代码审阅

固定对照：`elbrutalo/gcam-pixel10@5c84dc588ab5391c7b8eb80fc7c0b78e477d4c54`。

可复用的部分：

- `bju.patch`：把普通启动默认模式改成 sphere；
- `gvj.patch`：同时修正逻辑模式列表和实际 TextView 注册；
- `gwk.patch`：减少 More modes 入口；
- `Bye.smali`：延迟确认进程不可见后结束进程，规避 LightCycle warm-start 黑屏。

不能直接照搬的部分：

- `Dev.smali` / `Ask.smali` 为“自动、完整、精简”三套 UI 服务；本项目目标固定为单用途，不需要增加首启德语对话框、静态 Activity Context 和额外偏好状态。
- `gvj.z(I)` 被社区补丁全局改成 no-op，等于移除了所有 `indexOf()` 不变量检查。它可能掩盖其他模式状态偷偷进入，而不是只解决 sphere；在真机证据出现前不接受这项广域改动。
- 社区补丁没有收缩 Manifest 的外部拍照/录像 alias、远控、开机接收器或调试 Provider，因此它是“模式栏精简版”，不是完整的单用途安全边界。
- `Bye` 会让仍在后台渲染的全景丢失。只有验证保存回调和进程重要性时序后，才能决定保留、加长延迟或改成“渲染结束后退出”。

## G1/G2 真机观测点

目标机接入后依次确认：

1. `getconf PAGE_SIZE` 与 16 KB backcompat 属性；
2. `sensorservice` 中 type 4 gyroscope，以及 `ro.config.low_ram`；
3. 原包冷启动是否到达宿主 UI，首个 Java/native fatal 在哪一层；
4. 是否能从原有 More modes 手动进入 Photo Sphere；
5. 日志中 `PhotoSphereModule#providePhotoSphereAgent`、linker、LightCycle 与 camera session 事件；
6. `ProcessFrame / AddImage` 是否真实采到帧；
7. `FinishCapture` 后是否出现临时 mosaic、`LightCycleStitchTask`、JPEG 与 GPano XMP；
8. 退出重进是否触发黑取景器，再决定是否引入进程退出 workaround。

只有第 7 项闭环，才能进入单用途补丁与 Manifest 收敛。
