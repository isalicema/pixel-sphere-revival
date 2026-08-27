# 可复现构建说明

`scripts/build-local.sh` 是 v0.8 的唯一支持构建入口。它只接受哈希完全匹配的标准 SGCAM V24 APK。

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

脚本按文件名排序应用所有补丁；任何补丁拒绝、输入哈希变化或工具哈希变化都会中止。

## 本地签名

首次构建会在 `.local/signing/` 生成 JKS 和随机密码属性文件，权限设为仅当前用户可读。它们不会进入 Git。

同一个包名的 Android 更新必须由同一证书签名。因此：

- 请备份整个 `.local/signing/`；
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
