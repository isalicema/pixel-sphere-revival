# G0 输入与安装前审计回执

审计日期：2026-08-25
目标机：Pixel 10 Pro XL
状态：**字节级输入可复现 PASS；来源信任与真机兼容性 CONDITIONAL**

## 不可变输入

| 项目 | 结果 |
|---|---|
| 来源 | Shamim V24 发布页第一项标准包 |
| 文件名 | `SGCAM_8.5.300.XX.10_STABLE_V24.apk` |
| 大小 | `172438524` 字节 |
| SHA-256 | `5627913aadbda11a0d7abf77b670802335995f2c635ef9af5fee5161a615f76c` |
| ZIP 完整性 | PASS |
| 包名 | `com.shamim.cam` |
| 原始包声明 | `com.android.camera2` |
| versionName | `8.5.300.450594193.08` |
| versionCode | `65075803` |
| minSdk / targetSdk | `29 / 29` |
| ABI | 仅 `arm64-v8a` |
| DEX | `classes.dex`、`classes2.dex`、`classes3.dex` |

## 签名

- APK 同时含 v1 条目以及 APK Signature Scheme v2、v3 Signing Block；签名工具以最高方案 v3 验证通过。
- 签名证书：自签名 `CN=editor`，RSA 2048。
- 证书 SHA-256：`6215f00baa4bf18bab5792fc796bfc5555917240f14f7c7e672d956888d75c96`。
- 有效期：2016-01-10 至 2115-12-17。
- 本项目不会复用或冒充该私钥。重签名候选包将拥有不同安装证书；与其他签名的 SGCam 不能覆盖升级。

## 保护链与信任边界

外层应用入口是 `com.pairip.application.Application`。继承链同时触发两套完整性机制：

```text
com.pairip.application.Application
  → PairIP SignatureCheck.verifyIntegrity(...)
  → CameraApp → eav → bin.mt.signature.KillerApplication
  → SignatureKiller hook PackageManager 签名与 APK 文件访问
  → assets/SignatureKiller/origin.apk
```

`SignatureKiller` 会通过反射和原生 hook 让应用看到预期的签名与“原始 APK”视图，从而使第三方重签名包继续通过 PairIP 检查。这解释了为什么社区版本能用不同证书重签，但也扩大了安装前必须审计的范围。它本身不是恶意行为的充分证据，也不是安全背书。

内嵌 `origin.apk` 的结果：

- 大小 `4885507` 字节，SHA-256 `6eb17085c9de26e9846ca4e67033581cec5d7b1ddc212b2bf226663533f2f685`；
- ZIP 完整，无 APK Signing Block，无 `classes*.dex`；
- 包名为 `com.google.android.GoogleCamera`，`minSdk / targetSdk = 31 / 31`；
- 包含清单、资源、12 个原生库和 source-stamp 摘要，更符合供 hook 使用的原包视图，而不是第二个独立相机应用。

精确外层 SHA-256 未检索到公开索引结果；本轮没有把私有下载文件上传给第三方扫描服务。因此当前结论不能替代恶意代码分析或动态网络审计。

## 权限与组件暴露面

原包清单包含：

- 29 个 `uses-permission`；
- 70 个 Activity / alias / receiver / service / provider；
- 29 个显式 `android:exported="true"` 组件。

其中包括 `INTERNET`、位置、录音、开机广播、改 Wi-Fi、改系统设置、媒体/外部存储和 `MANAGE_EXTERNAL_STORAGE`，以及外部拍照/录像 Intent、远控服务、调试 Provider、后台接收器等。很多来自旧版 Google Camera 或 SGCam 的通用能力，并非 Photo Sphere 必需。

社区 SGCam360 补丁只收缩模式栏，没有收缩这组 Manifest 入口。项目最终候选版必须把 UI 收敛与组件/权限收敛分开验证，不能把“看不见按钮”当成“路径不可达”。

## Photo Sphere 与原生库

- `liblightcycle.so` 存在，且 smali 中可见 Photo Sphere、水平/垂直/广角/鱼眼等 LightCycle 捕获路径。
- 社区固定提交所修改的 `bju.smali`、`gvj.smali`、`gwk.smali` 和 `CameraActivity.smali` 在本输入中全部存在。
- 外层共有 21 个 `arm64-v8a` 原生库；20 个库的 ELF `LOAD` 对齐为 `2**12`（4 KB），只有 `libyuv-decoder.so` 为 `2**16`。
- 关键的 `liblightcycle.so`、`libSignatureKiller.so`、`libpairipcore.so` 均为 4 KB ELF LOAD 对齐。
- 外层 APK 将 `.so` 压缩存储且未设置 `extractNativeLibs=false`，安装时会解压；这避免了未压缩库的 APK 内 16 KB ZIP 偏移要求，但不能修复 ELF 段本身的 4 KB 对齐。

如果 Pixel 10 Pro XL 的 `adb shell getconf PAGE_SIZE` 返回 `16384`，Android 可能对这类库启用 16 KB backcompat mode；兼容模式只能作为动态实验条件，不能作为可靠支持结论。若返回 `4096`，该风险分支暂不触发。两种情况都仍需实际跑完拼接和保存。

## 工具链复现

- `apktool 2.12.0` 官方 JAR SHA-256：`effb69dab2f93806cafc0d232f6be32c2551b8d51c67650f575e46c016908fdd`，本地匹配。
- `uber-apk-signer 1.3.0` 官方 JAR SHA-256：`e1299fd6fcf4da527dd53735b56127e8ea922a321128123b9c32d619bba1d835`，本地匹配官方 Release 清单。
- apktool 解包完成；零改动回编译完成，生成结构有效的 unsigned APK，ZIP 完整性 PASS。
- 本轮未给回编译产物签名，也未安装到设备。

## G0 处置

1. **可复现性 PASS**：修改对象已精确到字节级版本，工具与输出链可重复。
2. **来源信任 CONDITIONAL**：它是第三方闭源 mod，并带签名/文件访问 hook；只允许进入受控真机基线，不作为可信日常相机直接安装。
3. **目标机构建的页面兼容 PASS**：Pixel 10 Pro XL / Android 17 构建 `CP2A.260805.005` 实测 `PAGE_SIZE=4096`，与 20 个旧原生库的 4 KB ELF LOAD 对齐匹配；本机不需要依赖 16 KB backcompat。系统更新后仍应重新测量。
4. **下一闸门**：只读设备基线已完成；原包 G1 安装与启动测试等待用户单独授权。获批后应在飞行模式、无敏感素材的条件下进行，并只授予测试所必需权限。
