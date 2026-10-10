# Photo Sphere Revival

把 Shamim 的 `SGCAM_8.5.300.XX.10_STABLE_V24` 收敛成一款独立安装、启动即进入 Photo Sphere 的单用途相机。

> **本仓库不提供 APK。** Google Camera / SGCam 及其原生库属于各自权利人；本仓库只发布互操作补丁、构建脚本和真机验证记录。请从原发布页自行取得基础 APK，并在本机完成构建与签名。

## 当前状态

- **Pixel 10 Pro XL (`mustang`) / Android 17：真机 PASS。** 已完成完整 360° 自然场景拍摄、合成、Fish eye 与 Sphere 查看，以及系统相机 → Photo Sphere 热恢复 3/3。
- **当前支持版本与实机版本均为 v0.9。** 该版本此前已通过专属图标、冷启动取景和新照片产出冒烟验收；2026-10-11 又以相同 APK 哈希原位恢复到 Pixel 10 Pro XL，本次回退后的首次启动仍待确认。
- **v1.0/v1.0.1 变焦实验已放弃。** v1.0 双指会崩溃；v1.0.1 修复崩溃并能出现变焦，但 Alice 实机判断交互鸡肋，决定不纳入产品。
- **Samsung：未验证。** 安装成功、出现取景和 Camera2 等级都不能证明 LightCycle 采集与拼接可用；请先看 [Samsung 兼容性与低风险试机流程](docs/compatibility.md)。
- 应用显示名为 **Photo Sphere**，包名仍为 `com.shamim.cam`，不会覆盖 Pixel 原生相机或 Google Photos；会与其他同包名 SGCam 冲突。

![Photo Sphere v0.9 蓝色环绕图标预览](assets/icon/photosphere-icon-approved-v6-android-preview.png)

## 这个版本做了什么

- 冷启动直接进入 Photo Sphere。
- 使用独立的球形全景启动图标，不再复用 Pixel Camera 图标。
- 只保留 Photo Sphere 路径，隐藏会崩溃的普通拍照、视频、前后镜头切换和原多镜头变焦入口。
- 不提供变焦；使用经长期拍摄验证的默认焦段。
- 保留顶部 `Type` 菜单的五种采集/呈现类型。
- 移除“管理所有文件”权限声明、Telegram 首启弹层和应用内更新检查。
- 把旧相机信号量的无限等待改成 2 秒有界等待，修复 Pixel 10 Pro XL 上与系统相机交替使用时的黑屏/ANR。

## 本地构建

### 1. 准备

需要 macOS 或 Linux、Bash、JDK（建议 17）、`curl`、`patch` 和 `openssl`。

从 [Shamim V24 发布页](https://www.celsoazevedo.com/files/android/google-camera/dev-shamim/f/dl79/) 下载第一项标准包：

```text
SGCAM_8.5.300.XX.10_STABLE_V24.apk
package: com.shamim.cam
size:    172438524 bytes
sha256:  5627913aadbda11a0d7abf77b670802335995f2c635ef9af5fee5161a615f76c
```

不要把 `RULER`、`SCAN3D` 或其他包名变体交给 v0.9 脚本；这些变体尚未应用和验证本补丁链。

### 2. 运行

```bash
./scripts/build-local.sh /绝对路径/SGCAM_8.5.300.XX.10_STABLE_V24.apk
```

脚本会：

1. 验证基础 APK 的 SHA-256；
2. 下载并校验固定版本的 apktool 2.12.0 与 uber-apk-signer 1.3.0；
3. 依次应用稳定补丁 `patches/0001` 到 `0006`，并复制 `assets/android/res/` 中的专属图标资源；变焦实验补丁 `0007/0008` 不进入默认构建；
4. 优先复用完整的 `.signing/`；否则在 `.local/signing/` 生成并保留你自己的本地签名；
5. 输出 `.local/output/Photo-Sphere-v0.9-dedicated-icon.apk`。

`.local/` 已被 Git 忽略。**请备份其中的签名文件**：以后升级同一安装包必须使用同一证书；换签名后 Android 会拒绝原位更新。

如果 Java 不在 `PATH`，可显式指定：

```bash
JAVA_BIN=/path/to/java KEYTOOL_BIN=/path/to/keytool \
  ./scripts/build-local.sh /path/to/SGCAM_8.5.300.XX.10_STABLE_V24.apk
```

### 3. 安装

```bash
adb install -r .local/output/Photo-Sphere-v0.9-dedicated-icon.apk
```

默认构建包含 Alice 确认的蓝色环绕图标，不包含主摄变焦实验。2026-10-11 的全量重建、zipalign、v3 签名与证书连续性均通过；重建包与设备上此前验收的 v0.9 包共 3069 个 ZIP 条目逐文件内容完全一致。两者整体 APK 哈希因 ZIP/签名元数据不同而不同，因此本仓库不把“整体哈希相同”冒充为源码可复现性证据。

若手机已有另一个签名的 `com.shamim.cam`，Android 会提示签名不匹配。先确认那是不是要保留的 SGCam；卸载旧包会清除它的应用数据。

## 首次使用

- 仅按实际需要授予相机、麦克风和照片/媒体权限。
- 不需要“管理所有文件”权限；v0.8 已移除该声明。
- v0.9 不提供双指变焦，保持默认焦段；不要依赖被放弃的 v1.0/v1.0.1 实验交互。
- 首次试拍先按快门、拍少量引导点并停止，确认能合成 JPEG，再进行完整 360°。
- 不要尝试前后镜头切换、原 `.6× / 2× / 5×` 镜头按钮或隐藏的其他模式；它们仍不在支持范围内。

## 安全与边界

- 不需要 root，不替换系统相机，不冒充 Google 签名。
- 这是社区互操作实验，不是 Google、Samsung 或 Shamim 的官方产品，也不提供保修。
- 相机兼容性取决于具体手机型号、SoC、Android/One UI 构建、相机 HAL 与厂商对第三方包的摄像头访问策略。
- 遇到黑屏、持续无响应或相机被占用时，关闭 Photo Sphere 与系统相机；不要反复强制启动，更不要在主力机上盲目改系统设置。

详细记录见 [v0.8 相机锁保护](docs/g7-camera-lock-guard-v08-2026-08-27.md)、[完整 360° 实拍验证](docs/g8-full-360-field-validation-2026-08-27.md)、[v0.9 专属图标](docs/g9-dedicated-icon-v09-2026-10-09.md)，以及已放弃的 [v1.0 主摄数码变焦实验](docs/g10-main-camera-digital-zoom-v10-2026-10-10.md) 和 [v1.0.1 双指路由热修复](docs/g11-pinch-routing-hotfix-v101-2026-10-10.md)。

## Credits

- Google Camera 与 LightCycle：Google。
- SGCam 基础版本：Shamim。
- Pixel 10 先行补丁思路：[`elbrutalo/gcam-pixel10`](https://github.com/elbrutalo/gcam-pixel10)。
- 本仓库：v0.8 单用途产品收敛、类型菜单恢复、权限/弹层清理、Pixel 10 Pro XL 相机热恢复保护与实机验证，v0.9 专属图标，以及已放弃的 v1.0/v1.0.1 主摄数码变焦实验记录。

详见 [NOTICE.md](NOTICE.md)。
