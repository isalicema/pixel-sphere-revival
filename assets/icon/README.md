# Photo Sphere 专属图标

`photosphere-icon-source.png` 是 v0.9 图标 v1 的高分辨率透明原稿。它没有复用 Pixel Camera 的图标资产，但 Alice 于 2026-10-09 判断它更像“星球”而不是“球形全景相机”，因此已否决，不应进入最终版本。

`photosphere-icon-camera-v2.png` 是按该反馈生成的 v2 透明原稿，`photosphere-icon-camera-v2-launcher-preview.png` 是深海军蓝桌面背景预览。v2 已被后续反馈替代，未接入 Android 构建资源。

Alice 随后要求去掉青蓝色，改用相机常见的黑、白、灰，并允许红色快门。`photosphere-icon-camera-v3-monochrome.png` 是 v3 透明原稿，`photosphere-icon-camera-v3-monochrome-preview.png` 是浅灰桌面背景预览。v3 已被后续反馈替代，未接入 Android 构建资源。

Alice 进一步指出 v3 的经纬网像地球仪，整体结构过于复杂，并要求参考应用内 Type 菜单的五种全景图标。`photosphere-icon-v4-minimal.svg` 与 `photosphere-icon-v4-minimal-preview.png` 是 v4 原稿，`photosphere-icon-v4-minimal-launcher-preview.png` 是桌面尺寸预览。v4 仍属于重绘方案，已在 2026-10-10 被“直接使用第一枚 Photo Sphere 图形”的决定替代。

## 此前已构建：内置 Photo Sphere 图形

- 源图：标准基础 APK 的 `drawable-xxxhdpi/quantum_ic_panorama_photosphere_white_24.png`；
- 源图 SHA-256：`a0bf96ec92437c4aec8e7c97bb9741fc08ca319cafac3ab037131e944e997b94`；
- 图形身份：Google Material Icons `panorama_photosphere`，按 Apache License 2.0 使用并在仓库 `NOTICE.md` 标注；
- 处理边界：只等比缩放、透明留白和纯黑 `#151515` 背景合成，不修改原始轮廓；
- 生成脚本：`scripts/render-native-photosphere-icon.py`；
- 桌面预览：`photosphere-icon-native-preview.png`；
- 历史桌面预览：`photosphere-icon-native-preview.png`。

该纯黑底版本曾进入 v0.9 构建，后被 Alice 于 2026-10-10 确认的 blue wrap v6 替代。内置图形继续作为 Android 13+ themed icon 的单色 alpha 蒙版使用。

## Depth v2 候选（折角已否决）

Alice 于 2026-10-10 要求在内置图形基础上继续放大，并加入阴影与折角。`scripts/render-native-photosphere-icon-depth.py` 保留源图外轮廓，做以下确定性处理：

- 主体由 216 px 放大到 272 px，相对 432 px adaptive canvas 占比由 50% 提升到约 63%；
- 整体增加向下 12 px、Gaussian blur 14 px 的柔和黑色阴影；
- 在中间全景画幅左右收口内加入浅灰和深灰折面，所有折面均由源图 alpha 裁切；
- 输出 `photosphere-icon-native-depth-v2-foreground.png`、`photosphere-icon-native-depth-v2-launcher.png` 和 `photosphere-icon-native-depth-v2-preview.png`。

该候选的折角于 2026-10-10 被 Alice 否决，尚未覆盖 `assets/android/res/`。

## Gradient v3 候选（已被配色反馈替代）

Alice 要求取消折角，并把整个白色前景改成多彩渐变。`scripts/render-native-photosphere-icon-gradient.py` 做以下确定性处理：

- 保留 272 px 放大尺寸和向下柔和阴影；
- 完全移除 depth v2 的四个灰色折面；
- 以原始 Photo Sphere alpha 为唯一形状遮罩；
- 使用珊瑚红、琥珀橙、洋红、紫罗兰和少量钴蓝构成斜向连续渐变；
- 输出 `photosphere-icon-native-gradient-v3-foreground.png`、`photosphere-icon-native-gradient-v3-launcher.png` 和 `photosphere-icon-native-gradient-v3-preview.png`。

Alice 于 2026-10-10 认为该候选颜色观感奇怪，并提供新的蓝色圆盘风格参考。该候选未覆盖 `assets/android/res/`；在该轮结束时，已构建 APK 仍使用上一版纯白前景图形，后来已由 blue wrap v6 构建替代。

## Blue orb v4 候选（已被半透明材质试验替代）

Alice 提供的参考图采用钴蓝圆盘、中央淡紫柔光、深色后层与白色前层。blue orb v4 只提取这些风格特征，内容仍为 Photo Sphere 图形：

- 钴蓝/皇家蓝圆盘，边缘较深，中心为淡紫柔光；
- 上下两段深海军蓝球面弧明确分离，不构成完整圆环；
- 中间是一条收窄的白色全景带，仅在中心保留克制的粉紫高光；
- 不复制参考图的钟表指针和底部圆点，也不加入经纬线、相机机身、星球或轨道；
- 第一份内部草稿因白带过厚、后层接近完整圆环而像 VR 头显，已在同轮自检中替换，未作为项目候选保留。

输出文件为 `photosphere-icon-native-blue-orb-v4.png`（1254 px 透明原稿）和 `photosphere-icon-native-blue-orb-v4-preview.png`（144 px 小尺寸预览）。该候选没有覆盖 `assets/android/res/`，也没有触发 APK 重建或设备安装。

## Blue glass v5 候选（已被环绕形态试验替代）

Alice 认可蓝色圆盘方向后，重新附上带深蓝圆环和中央纯白横带的版本，并要求只修改中央白色部分：

- 中央横带改为均匀的半透明白色，让蓝紫背景和深蓝圆环可见；
- 移除厚度、倒角、投影、亮边和内部体积渐变，保持扁平；
- 保留附件里的蓝色圆盘、中央柔光、深蓝圆环、横带轮廓和构图；
- 不增加新物件或文字。

输出文件为 `photosphere-icon-native-blue-glass-v5.png`（1254 px 透明原稿）和 `photosphere-icon-native-blue-glass-v5-preview.png`（144 px 小尺寸预览）。该候选没有覆盖 `assets/android/res/`，也没有触发 APK 重建或设备安装。

## 当前采用：Blue wrap v6

Alice 指出 v5 的横带仍像贴在正面的半透明图形，缺少环绕一周的感觉。v6 只调整横带路径：

- 正面横带略带椭圆弧度，并保持均匀的半透明白色；
- 左右两端收窄、向后转折，以短小的背面延续表现同一条带子绕到球体背后；
- 只用轮廓与遮挡表达 360° 环绕，不添加倒角、厚度、投影、亮边或体积渐变；
- 不在球体外增加独立轨道，蓝色圆盘和深蓝圆环保持不变。

Alice 于 2026-10-10 确认该版本“已经足够有辨识度”，授权正式采用。输出与构建边界如下：

- 原稿：`photosphere-icon-native-blue-wrap-v6.png`，1254×1254 RGBA，SHA-256 `c1a911c74c19e7a77fabd3f6955ae1226d6f57fa35c3793090203e192192bc3c`；
- 资源脚本：`scripts/render-approved-icon-v6.py`，固定校验彩色原稿与 monochrome source 哈希；
- 普通/adaptive 资源：432×432 RGBA，并用圆形 alpha mask 清理生成图外围的零散透明像素；
- adaptive background：`#0B70FA`；
- Android 13+ themed icon：`photosphere-icon-monochrome-source.png` 的单色 alpha 轮廓，由系统着色；
- Android 预览：`photosphere-icon-approved-v6-android-preview.png`。

该版本已覆盖 `assets/android/res/` 并进入 v0.9 构建；普通桌面图标、冷启动取景和新照片产出已在 Pixel 10 Pro XL 上通过冒烟验收。2026-10-11，设备又以同一 APK 哈希原位恢复到 v0.9。

## v1 视觉含义（已否决）

- 青蓝色球体与经纬线：360° 球形全景；
- 环绕轨道：围绕拍摄者完成一整圈采集；
- 珊瑚色圆点：Photo Sphere 的白点/圆形拍摄引导；
- 深海军蓝底色：与 Pixel Camera 的白底彩色镜头图标明显区分。

否决原因：球体、轨道与发光质感组合后，第一视觉语义是“星球”，拍照与多张拼接的线索不足。

## 生成说明

v1 原稿于 2026-10-09 使用 Codex 内置图像生成工具生成，随后只做了确定性的缩放、透明留白和纯色背景合成。它曾短暂进入 `assets/android/res/`，但当前 Android 资源已经替换为上方记录的内置 Photo Sphere 图形。

生成提示词：

```text
Use case: logo-brand
Asset type: Android adaptive app icon foreground for an app named Photo Sphere
Primary request: create a distinctive, instantly recognizable spherical panorama symbol: a luminous cyan-to-teal globe made from three elegant curved longitude/latitude arcs, surrounded by one subtle orbit ring, with a small warm coral capture dot as an accent
Scene/backdrop: genuinely transparent background
Style/medium: clean geometric vector-like icon, premium modern Android app icon, bold simple silhouette, crisp smooth edges, minimal detail
Composition/framing: centered square composition; symbol fills about 68% of the canvas; generous transparent safe area on all sides for Android adaptive icon masking; balanced at tiny launcher size
Color palette: cyan, turquoise, deep teal, one small coral-orange accent; no Google four-color palette
Constraints: no text, no letters, no camera-lens aperture blades, no Pixel Camera resemblance, no phone mockup, no outer rounded-square container, no shadow outside the symbol, no watermark; transparent background; readable at 48 px
```

## v2 相机语义草案（待确认）

- 相机机身和实体快门键：直接建立拍照语义；
- 镜头内部的球形经纬网：表达 Photo Sphere，而不是单独的星球；
- 四角取景框：表达取景与多张采集；
- 完全去除轨道、卫星路径和星空元素。

v2 使用 Codex 内置图像编辑模式生成，编辑目标为 v1，完整提示词如下：

```text
Use case: logo-brand
Asset type: revised Android adaptive app icon foreground for Photo Sphere
Input image: the current generated icon is the edit target; retain only its cyan/teal plus small coral accent palette, but replace the concept
Primary request: redesign the mark so it reads immediately as photography plus spherical panorama, not as a planet. Create a compact modern camera silhouette with a rounded rectangular camera body and a small shutter button; make the central camera lens a clearly visible 360-degree spherical panorama grid with curved longitude and latitude lines, as if the globe is inside the lens. Add four subtle viewfinder corner marks or two small overlapping photo-frame edges to suggest multi-shot stitching.
Style/medium: clean geometric vector-like Android icon, flatter and simpler than the original, bold silhouette, crisp edges, minimal gradients, professional and friendly
Composition/framing: centered square composition, fills about 68% of the canvas, generous transparent adaptive-icon safe area, legible at 48 px
Color palette: cyan, turquoise, deep teal, small coral shutter accent
Constraints: genuinely transparent background; no text; no letters; no orbit ring; no satellite path; no stars; no standalone planet; no outer rounded-square container; no Pixel Camera or Google four-color resemblance; no aperture-blade logo; no watermark
```

## v3 黑白灰相机草案（待确认）

- 保留 v2 的相机、球形镜头和取景框结构；
- 相机机身改为哑光黑和深灰；
- 镜头圈与经纬网改为银白；
- 快门按钮使用摄影红；
- 背景预览改为浅灰，完全移除青、蓝、绿配色。

v3 使用 Codex 内置图像编辑模式对 v2 定向改色，完整提示词如下：

```text
Use case: logo-brand
Asset type: color revision of the Photo Sphere Android adaptive icon foreground
Input image: the current cyan camera icon is the edit target
Primary request: change only the color and material language to a classic camera palette. Make the camera body matte black and charcoal gray, the lens rim metallic silver and white, and the spherical longitude/latitude grid bright white and light gray. Keep the shutter button a clear photographic red. Preserve the exact camera silhouette, central spherical-grid lens, four viewfinder corners, proportions, layout, and transparent background.
Style/medium: clean geometric vector-like Android icon, restrained black/white/gray photography aesthetic, high contrast, minimal subtle metallic highlight, readable at 48 px
Color palette: matte black, charcoal, neutral gray, silver, white; one red shutter-button accent only
Constraints: genuinely transparent background; remove every cyan, teal, turquoise, blue, aqua, and coral color; do not alter the composition or add objects; no text; no letters; no orbit; no stars; no Pixel Camera or Google four-color resemblance; no watermark
```

## v4 原生图标语言重绘草案（已替代）

- 参考 Photo Sphere、Horizontal、Vertical、Wide angle、Fish eye 五枚 Type 图标的共同规则：单色、单轮廓、用边界形变表达投影范围；
- 删除相机机身、镜头材质、经纬线、取景框、渐变与装饰；
- 用一条弯曲画幅带穿过抽象球面，表达“球形全景”，不是地球；
- 使用 `scripts/render-icon-v4.py` 从确定性几何重绘 PNG，避免生成式图像在小尺寸产生多余细节；
- 该草案没有成为 Android 构建输入；最终改为直接使用内置图形。
