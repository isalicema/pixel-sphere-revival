# 可复现构建说明

`scripts/build-local.sh` 是稳定 v0.9 的唯一支持构建入口。它只接受哈希完全匹配的标准 SGCAM V24 APK。

## 固定依赖

| 工具 | 版本 | SHA-256 |
| --- | --- | --- |
| apktool | 2.12.0 | `effb69dab2f93806cafc0d232f6be32c2551b8d51c67650f575e46c016908fdd` |
| uber-apk-signer | 1.3.0 | `e1299fd6fcf4da527dd53735b56127e8ea922a321128123b9c32d619bba1d835` |

脚本把工具下载到 `.local/tools/`，把 apktool framework 固定在 `.local/framework/`，避免隐式写入用户主目录。

## 补丁顺序

1. `0001-photo-sphere-label.patch`：应用显示名改为 Photo Sphere。
2. `0002-photo-sphere-dedicated-mode.patch`：Photo Sphere 默认路由、单模式 UI、移除全文件权限与首启推广弹层。
3. `0003-clean-controls-and-startup.patch`：隐藏不兼容控制，移除 OTA/脏安装检查。
4. `0004-photo-sphere-type-menu.patch`：固定 Photo Sphere 设置上下文，恢复五种 Type。
5. `0005-bound-legacy-camera-semaphore-wait.patch`：把旧相机信号量无限等待改成 2 秒超时。
6. `0006-photo-sphere-icon.patch`：让 application 和两个 launcher alias 都引用 Photo Sphere 专属图标。

`0007-photo-sphere-main-camera-digital-zoom.patch` 与 `0008-photo-sphere-pinch-routing-hotfix.patch` 属于已放弃的 v1.0/v1.0.1 实验，只保留用于追溯，不进入默认构建。Alice 于 2026-10-11 实机确认变焦能够出现后，决定其体验价值不足，产品继续使用默认焦段。

脚本按文件名排序只应用 `0001`–`0006` 六个稳定补丁；任何补丁拒绝、输入哈希变化或工具哈希变化都会中止。

补丁应用后，脚本会把 `assets/android/res/` 合并到反编译资源目录。资源包括普通 PNG、自适应图标以及 Android 13+ 的 monochrome 主题图标。普通与自适应图标使用 Alice 确认的 blue wrap v6 彩色原稿；主题图标单独复用基础 APK 的 `quantum_ic_panorama_photosphere_white_24` alpha 轮廓，避免整颗蓝色圆盘在主题模式下变成实心圆。来源、历史草案与固定哈希重建方式记录在 `assets/icon/README.md`，资源可用 `python3 scripts/render-approved-icon-v6.py` 重建。

## 本地签名

如果项目内已有完整的 `.signing/photo-sphere-local.jks` 与 `.signing/keystore.properties`，脚本会优先复用它们；这用于给既有安装包原位升级。否则，首次构建会在 `.local/signing/` 生成 JKS 和随机密码属性文件。两处均被 Git 忽略，权限应保持为仅当前用户可读。

`keystore.properties` 可以额外提供 `certificate_sha256=`。存在时，签名器必须验证输出证书与该指纹一致，否则构建失败。也可以用 `SIGNING_DIR` 显式选择其他完整签名目录。

同一个包名的 Android 更新必须由同一证书签名。因此：

- 请备份实际使用的 `.signing/` 或 `.local/signing/`；
- 不要把 JKS 或密码提交到 issue、网盘或公开仓库；
- 不同朋友各自构建时会得到不同证书，彼此的 APK 不能直接覆盖安装；
- 删除本地签名后重新构建，会被 Android 视为另一个签名来源。

## 高级覆盖

在离线或已有工具的环境中，可指定已校验的 JAR：

```bash
APKTOOL_JAR=/path/to/apktool_2.12.0.jar \
UBER_APK_SIGNER_JAR=/path/to/uber-apk-signer-1.3.0.jar \
JAVA_BIN=/path/to/java \
KEYTOOL_BIN=/path/to/keytool \
./scripts/build-local.sh /path/to/SGCAM_8.5.300.XX.10_STABLE_V24.apk
```

即使使用覆盖路径，脚本仍会校验两个 JAR 的 SHA-256。
