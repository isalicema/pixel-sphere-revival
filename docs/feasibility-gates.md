# 可行性闸门

## G0：输入可信且可复现

记录 APK 的来源说明、SHA-256、包名、版本、签名证书摘要、`minSdk` / `targetSdk`、ABI 和所有 `.so` 文件。任何改动都从这份不可变输入重新生成。

通过条件：团队能准确回答“我们修改的是哪一个字节级版本”。

## G1：安装与进程启动

先测试原 APK，不改 smali。采集：

- Package Manager 安装结果；
- Android linker / native library 错误；
- 首次启动的完整 fatal exception；
- 权限授予前后差异；
- 设备页面大小与 APK 中原生库的 ELF/ZIP 对齐。

如果失败发生在原生库加载或 ABI/页面对齐层，`CameraActivity` 路由补丁不会产生帮助。旧预编译 `.so` 若本身不兼容 16 KB 页面，单靠 apktool 不能把它重新编译成兼容版本。

通过条件：应用进程能稳定进入宿主相机 UI，或已得到可修复的第一处 Java/smali 级失败。

## G2：Photo Sphere 模块可达

建立这条调用链的静态与动态证据：

```text
Launcher / Intent
  → CameraActivity 宿主初始化
  → mode registry / device gate
  → Photo Sphere module creation
  → camera ID + capture session
  → frame guidance / sensor tracking
  → stitching / finalization
  → MediaStore + GPano metadata
```

优先寻找已有的模式 ID、Intent extra、SharedPreferences、远程配置或设备白名单。只有证明宿主初始化与模块构造顺序后，才考虑强制路由。

通过条件：Pixel 10 Pro XL 能进入 Photo Sphere 取景界面，并能采集至少一个有效帧。Pixel 10 Pro 或其他同系列设备的结果只能作为旁证，不能替代该目标机验证。

## G3：端到端成片

在自然场景完成整套圆点引导，等待拼接结束，确认：

- 输出文件存在且像素尺寸合理；
- 没有后台 native crash / ANR；
- XMP 中存在正确的 GPano 元数据；
- Google Photos 能按 360° 图像打开；
- 退出、重进后还能再次拍摄。

通过条件：至少 1 张完整球形全景成功；这才是“技术可行”的第一个结论。

## G4：单用途产品化

在 G3 之后才做：

- 默认路由到 Photo Sphere；
- 隐藏或移除其他模式入口；
- 处理返回键、权限、设置页和相册入口；
- 采用独立包名与自有固定签名（若重命名不会破坏内部 provider/authority）；
- 连续 3 次拍摄、冷启动、系统重启回归。

通过条件：达到 README 中的五条完成标准。

## 失败分流

| 首个硬失败 | 判断 | 下一步 |
|---|---|---|
| 仅模式被机型/配置门控 | 高可修复性 | 最小化 patch 门控，保留宿主初始化 |
| 新 camera ID / stream config 不被旧代码接受 | 中等可修复性 | 追踪 `CameraCharacteristics` 与镜头选择映射 |
| Java API / 权限行为变化 | 中等可修复性 | 按异常点做兼容 shim |
| 旧 `.so` 无法加载或拼接器 native crash | 高风险 | 判断是否有兼容二进制；否则转向开源拼接内核 |
| 依赖 Google 私有签名/privileged permission | 高风险 | 不绕过平台安全；寻找无需该能力的独立实现 |
| 只能启动，无法拼接/保存 | 尚未复活 | 继续沿 finalization 与 MediaStore 链路取证 |

## 对最初方案的修正

“先改默认入口、再隐藏会崩的模式”把 UI 当成了根因。更稳妥的顺序是先跑原样基线、抓第一处失败、证明 Photo Sphere 端到端，再收敛 UI。其他模式崩溃与否不是本项目的决定性问题，只要它们最终不可达即可。
