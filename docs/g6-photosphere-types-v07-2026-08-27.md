# G6 Photo Sphere v0.7 类型菜单恢复回执（2026-08-27）

## 问题

v0.6 虽然直接启动了 LightCycle Photo Sphere 模块，但顶部选项控制器仍把当前模式读成普通 `PHOTO`。因此 Photo Sphere 自带的类型选择被可见性条件隐藏，展开菜单时反而出现普通相机的 HDR+、脸部修复、定时器和比例等选项。

五种类型的底层代码与资源没有被删除；最终 v0.6 APK 中的 `fcx.smali` 与原包逐字一致，仍包含：

- 360 / Photo Sphere
- Horizontal
- Vertical
- Wide angle
- Fish eye

## 修复

在这款单用途应用的 OptionsBarController 中，将当前模式固定报告为 `PHOTO_SPHERE`。这样只改变选项的可见性判定，不改 LightCycle 采集、拼接和保存链路，也不恢复普通拍照、运动模式、前后摄切换或变焦入口。

可复现补丁：`patches/0004-photo-sphere-type-menu.patch`。

## 产物

- 文件：`dist/Photo-Sphere-v0.7-photosphere-types.apk`
- 大小：`172531844` 字节
- SHA-256：`d4e6d55237ed66655b89a7668205f11c4473242251ba319343e311acbc7c3c0c`
- 包名：`com.shamim.cam`
- 显示名：`Photo Sphere`
- 签名证书 SHA-256：`79d76eb4ae694dc4b1b4d7ec064eec6f52998879b1658f1aa40bc7f1b806db76`
- 验证：APK Signature Scheme v3、zipalign、ZIP 完整性通过；仅包含 `classes.dex`、`classes2.dex`、`classes3.dex`

v0.7 已在 Pixel 10 Pro XL `mustang` 上原位安装，没有清除应用数据，也没有覆盖系统 Pixel Camera。

## 真机结果

用户亲自打开 `Photo Sphere` 并展开顶部箭头，确认出现 `Type`，其中包含五个选项。这构成“Photo Sphere 内部类型菜单恢复”的真机 PASS。

本回执只确认菜单存在；五种类型尚未逐一拍摄、拼接和保存，因此不能据此宣称五种类型均已兼容 Pixel 10 Pro XL。

## 剩余验证

- 先用默认 360 类型完成完整球面并在 Google Photos 中验证 viewer；
- 再分别低风险试拍 Wide angle 与 Fish eye；
- 连续完成至少 3 次目标类型拍摄。
