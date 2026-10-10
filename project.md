# Photo Sphere Revival 项目日志

> 本文件记录项目决策、验证边界与交付状态。使用说明见 `README.md`，发布摘要见 `docs/releases/`。

## 当前状态

- 当前目标：维持 Pixel 10 Pro XL v0.9 无变焦稳定版，不再推进主摄变焦。
- 当前实机版本：v0.9 已于 2026-10-11 00:03:20（Asia/Shanghai）按 Alice 决策原位恢复；首次安装时间保持不变，设备端 APK SHA-256 与此前验收包一致。回退后的首次启动仍待确认。
- 最新公开版本：v0.9，发布 commit `006c1040bb51cbf7e476078a6d16e37667670293`，annotated tag `v0.9`；GitHub Release 于 2026-10-11 00:12:37（Asia/Shanghai）发布：`https://github.com/isalicema/pixel-sphere-revival/releases/tag/v0.9`。
- 当前支持构建：v0.9；只应用 `0001`–`0006` 六个稳定补丁，不包含变焦。已安装 APK 大小 `172782348` bytes，SHA-256 `61c37c3ff900e0dd80d882c23bc63a1867e4e4a66ae8fe88ac5b26e55ea5b9af`。
- 发布前重建：2026-10-11 全量构建、zipalign、v3 签名与证书连续性 PASS；新包 SHA-256 为 `32cf9206024611ba302603b950ceafa90736f3e74a7cb8ba468a9201f62a4f93`。与设备已验收包逐一比较 3069 个 ZIP 条目，内容差异为 0；归一化内容 SHA-256 均为 `df41ea58bfb76abbba05fd6a1b2e23a079dfb5f8b1674e8c51c5e06708b1b31f`。整体 APK 哈希差异来自 ZIP/签名元数据，不宣称字节级可复现。
- 已生效边界：v0.8 隐藏变焦、前后镜头切换和其他不兼容入口；完整 360° 拍摄、拼接、Fish eye / Sphere 查看及系统相机热恢复 3/3 已有 Pixel 10 Pro XL 实机证据。
- 已接受方案：Alice 于 2026-10-10 最终确认 blue wrap v6；彩色图标使用钴蓝圆盘、深蓝球面环与半透明白色 360° 横带，主题图标使用原生 Photo Sphere 单色蒙版。主摄变焦实验已于 2026-10-11 被 Alice 明确放弃，支持版本保持默认焦段。

## 未完成事项

1. 打开已恢复的 v0.9，确认正常取景；必要时再做一张少量点合成的轻量回归。
2. 继续维持默认焦段；不要恢复 `0007/0008` 变焦实验。
3. 五种 Type、Android 主题图标与系统相机热恢复沿用既有分项证据，不扩写为本轮重新验证；Samsung 等其他品牌设备仍未验证。

## 证据入口

- v0.8 状态与构建：`README.md`、`docs/build.md`
- 控制面收敛与隐藏变焦：`docs/g5-clean-controls-v06-2026-08-27.md`、`patches/0003-clean-controls-and-startup.patch`
- 类型菜单恢复：`docs/g6-photosphere-types-v07-2026-08-27.md`
- 相机热恢复：`docs/g7-camera-lock-guard-v08-2026-08-27.md`
- 完整 360° 实拍：`docs/g8-full-360-field-validation-2026-08-27.md`
- 主摄数码变焦候选：`docs/g10-main-camera-digital-zoom-v10-2026-10-10.md`、`patches/0007-photo-sphere-main-camera-digital-zoom.patch`
- 双指触摸路由热修复：`docs/g11-pinch-routing-hotfix-v101-2026-10-10.md`、`patches/0008-photo-sphere-pinch-routing-hotfix.patch`
- 发布状态：`docs/releases/v0.9.md`、`https://github.com/isalicema/pixel-sphere-revival/releases/tag/v0.9`

## 历史记录

### PSR-001 — 2026-10-09（Asia/Shanghai）— 补建项目日志并评估图标与变焦

- Alice 提出：v0.8 在数日高频实用中保持稳定；希望用不同图标更快找到应用，并重新评估取景变焦，以便在人群密集场景中不靠物理移动完成构图。
- 星子建议：图标是资源层的低风险改动，可单独进入 v0.9；变焦需要区分主摄数码裁切与 0.6× / 2× 物理镜头切换。优先研究前者，不直接恢复旧入口，不允许采集中途改变焦段。
- 实际修改：补建本日志；没有修改 APK 补丁、构建脚本或发布文件。
- 决策依据：现有 v0.8 已经长期实用验证；`ZoomUi` 曾被运行时重新显示且 0.6× / 2× 与镜头切换不可用。Photo Sphere 的引导和拼接依赖一组照片保持一致的视场角，因此不能把“显示按钮”等同于“变焦兼容”。
- 验证结果：完成仓库静态检查；确认 Manifest 仍引用 Pixel Camera 图标资源，确认变焦 UI 在布局和 `ZoomUi.setVisibility` 两层被强制隐藏。未反编译新工作树，未构建、未安装、未做设备测试。
- 状态边界：图标 v0.9 与变焦实验均为建议，尚未获 Alice 实施授权；没有 commit、push 或发布。
- 来源说明：早期状态从本仓库 v0.8 文档回填；本日长期使用情况来自 Alice 当轮回执。未回填缺失的使用次数或未留存的测试细节。

### PSR-002 — 2026-10-09（Asia/Shanghai）— v0.9 专属图标候选

- Alice 提出：同意“图标先行、变焦独立研究”的方案，并授权开始推进专属图标。
- 星子建议与实现：采用青蓝球体、经纬线、轨道与珊瑚色采集点；新增普通、自适应和 monochrome 主题资源；新增 `0006-photo-sphere-icon.patch`，覆盖 application 与所有 launcher alias；构建脚本升级到 v0.9 并复制图标资源。
- 决策依据：图标必须与 Pixel Camera 视觉区分，但不能触碰 v0.8 相机链路。Android launcher 实际使用启用的 activity alias，因此 application 与 alias 必须一起替换。
- 失败与更正：初次脚本编辑被补丁数量保护中止；随后静态回读发现 alias 仍覆盖旧图标；一份中间 APK 又使用了与 v0.8 不同的 `.local/signing` 证书。三者均未安装。最终脚本优先复用 `.signing/`，并通过 `certificate_sha256` 强制校验 v0.8 的 `79d7…` 证书。
- 验证结果：六补丁完整构建 PASS；XML PASS；zipalign PASS；APK Signature Scheme v3 PASS；签名后反解确认 application、启用/备用 launcher alias 均引用 `@mipmap/photosphere_launcher`。最终 APK SHA-256 为 `95b954e8335cab5033704799a425d3744ae7cc79ffa4ce09f07423e26f003809`。
- 状态边界：最新候选为 v0.9；当前实机仍为 v0.8。尚未安装、目视验证图标或回归 Photo Sphere 拍摄。本轮没有 commit、push 或发布。
- 证据：`assets/icon/README.md`、`patches/0006-photo-sphere-icon.patch`、`docs/g9-dedicated-icon-v09-2026-10-09.md`、`.local/output/Photo-Sphere-v0.9-dedicated-icon.apk`（忽略目录）。

### PSR-003 — 2026-10-09（Asia/Shanghai）— v1 视觉否决与 v2 相机语义草案

- Alice 纠正：v1 与“拍照”关系不明显，相比“球形全景”更像“星球”。
- 星子判断：轨道、发光球体和独立经纬网共同造成了行星语义；接受纠正，不以技术构建通过替代视觉验收。
- 实际修改：保留 v1 作为被否决历史；使用内置图像编辑生成 v2，改为相机机身、球形经纬网镜头、实体快门键和四角取景框；保存透明原稿和桌面背景预览。没有把 v2 覆盖进 Android 构建资源，也没有重建或安装 APK。
- 验证结果：v2 在 48 px 预览中仍能辨认相机轮廓、球形镜头和珊瑚色快门键；视觉是否合格仍由 Alice 确认。
- 状态边界：v1 APK 不应安装；v2 仅为视觉草案。本轮没有 commit、push、发布或设备变更。
- 证据：`assets/icon/photosphere-icon-camera-v2.png`、`assets/icon/photosphere-icon-camera-v2-launcher-preview.png`、`assets/icon/README.md`。

### PSR-004 — 2026-10-09（Asia/Shanghai）— v3 黑白灰相机配色

- Alice 提出：不喜欢青蓝色；希望改用相机常见的黑白灰，快门可以使用红色。
- 实际修改：以 v2 为编辑目标，保留相机机身、球形经纬网镜头和四角取景框；机身改为哑光黑/深灰，镜头圈与网格改为银白，快门改为红色；生成透明原稿、浅灰桌面预览和 48 px 检查图。
- 决策依据：只纠正配色，不重新改变已经更清楚的“拍照＋球形全景”结构；红色只用于快门，形成单一视觉焦点。
- 验证结果：透明通道存在；48 px 预览仍可辨认相机轮廓、球形镜头与红色快门。最终视觉仍待 Alice 确认。
- 状态边界：v3 尚未覆盖 Android 构建资源，没有重建或安装 APK；当前实机仍为 v0.8。本轮没有 commit、push 或发布。
- 证据：`assets/icon/photosphere-icon-camera-v3-monochrome.png`、`assets/icon/photosphere-icon-camera-v3-monochrome-preview.png`、`assets/icon/README.md`。

### PSR-005 — 2026-10-09（Asia/Shanghai）— 参考原生 Type 图标并收敛为 v4

- Alice 纠正：v3 的球形镜头仍过于具体，带经纬线后像地球仪；相机机身、镜头和取景框叠加也不够直观，希望参考 Photo Sphere 内部五种全景类型图标的画法。
- 星子检查：从本地反编译工作区确认 Type 菜单依次使用 Photo Sphere、Horizontal、Vertical、Wide angle 和 Fish eye 五枚图标；它们共同使用单色、单轮廓和投影形变表达范围，没有相机机身、镜头材质或装饰性网格。
- 实际修改：新增可复现的 v4 SVG、PNG 和桌面尺寸预览；v4 只保留黑色底、白色球面轮廓及一条弯曲全景画幅。早期内部草稿曾加入灰色下弧和红点，缩小后容易像 VR 头显，已在同轮自检中移除。生成对比表保存在忽略目录 `.local/review/`，不作为公开资产。
- 决策依据：此轮优先与应用自身的视觉词汇保持一致；Alice 允许红色快门不代表必须加入，任何无法提高小尺寸识别度的元素都应删除。
- 验证结果：v4 已在 144 px 桌面预览中检查；轮廓可读且不再含经纬线、相机机身或取景框。最终视觉仍待 Alice 确认。
- 状态边界：v4 尚未覆盖 Android 构建资源，没有重建、安装或实机回归；当前实机仍为 v0.8。本轮没有 commit、push 或发布。
- 证据：`assets/icon/photosphere-icon-v4-minimal.svg`、`assets/icon/photosphere-icon-v4-minimal-preview.png`、`assets/icon/photosphere-icon-v4-minimal-launcher-preview.png`、`scripts/render-icon-v4.py`。

### PSR-006 — 2026-10-10（Asia/Shanghai）— 直接采用内置 Photo Sphere 图形并构建 v0.9

- Alice 决策：不再继续重绘，直接使用对比表第一枚、Type 菜单内置的 Photo Sphere 图形作为启动图标。
- 实际修改：从标准基础 APK 的 `drawable-xxxhdpi/quantum_ic_panorama_photosphere_white_24.png` 取得原图，只做等比尺寸适配和纯黑底合成；替换普通与 adaptive foreground 资源，并让 Android 13+ monochrome 图标复用同一透明轮廓。新增 `scripts/render-native-photosphere-icon.py`，固定校验源图 SHA-256 `a0bf96ec…e997b94` 后才允许重建资源。
- 决策依据：直接复用应用自身已经验证的 Photo Sphere 视觉词汇，避免再次引入地球仪、相机机身或 VR 头显等额外语义。该图形对应 Google Material Icons 的 `panorama_photosphere`，公开说明按 Material Icons 的 Apache License 2.0 标注来源。
- 构建与验证：六补丁完整构建 PASS；XML、Python 编译与 `git diff --check` PASS；zipalign、APK Signature Scheme v3 与既有证书 `79d76e…db76` 校验 PASS。签名后 APK 中 foreground PNG 为 432×432，逐像素回读与构建输入完全一致；application 与全部 launcher alias 仍引用 `@mipmap/photosphere_launcher`。
- 构建产物：`.local/output/Photo-Sphere-v0.9-dedicated-icon.apk`，大小 `172561063` bytes，SHA-256 `6fc14e2d9d166bacbaa3a5bdda0c5b54519e8aa741f97d6356a9bb67c0547d08`。
- 状态边界：当前实机仍为 v0.8；v0.9 没有安装，桌面图标、主题图标、冷启动、360° 拍摄和相机热恢复均未做本轮实机验证。没有 commit、push 或发布。
- 临时依赖：本机缺少 JDK，使用经官方 API 解析且 SHA-256 校验通过的 Eclipse Temurin 17.0.20.1 临时包完成构建；约 177 MB 压缩包、解压目录与 API 回执随后均已从 `/private/tmp` 删除。
- 证据：`assets/icon/photosphere-icon-native-preview.png`、`assets/android/res/`、`scripts/render-native-photosphere-icon.py`、`docs/g9-dedicated-icon-v09-2026-10-09.md`。

### PSR-007 — 2026-10-10（Asia/Shanghai）— 放大、阴影与折角视觉候选

- Alice 提出：在直接采用第一枚 Photo Sphere 图形的基础上，把图形再放大，并加入一些阴影和折角。
- 星子实现：保留原始图形轮廓，将主体从 216 px 放大到 272 px（相对 432 px adaptive canvas）；增加向下偏移的柔和黑色投影；在全景画幅左右端点内，以浅灰/深灰四个裁切折面形成折角。折面严格裁切在原图 alpha 内，不扩张或重画外轮廓。
- 决策依据：折角放在中间全景画幅的收口处，使其更像一条折叠的全景胶片；不修改图标外框，避免重新增加星球、相机或 VR 头显语义。图像技能规则判断此类项目内图标应采用确定性本地处理，因此没有调用生成式图像工具。
- 验证结果：已生成 432 px foreground/launcher 候选及 144 px 桌面尺寸预览；透明通道与尺寸检查 PASS。阴影在放大图中清晰、桌面尺寸中克制；最终视觉待 Alice 确认。
- 状态边界：depth v2 仅位于 `assets/icon/`，尚未覆盖 `assets/android/res/`，没有重建、安装、commit、push 或发布；当前可安装 APK 仍是 PSR-006 的无折角版本。
- 证据：`assets/icon/photosphere-icon-native-depth-v2-foreground.png`、`assets/icon/photosphere-icon-native-depth-v2-launcher.png`、`assets/icon/photosphere-icon-native-depth-v2-preview.png`、`scripts/render-native-photosphere-icon-depth.py`。

### PSR-008 — 2026-10-10（Asia/Shanghai）— 取消折角并改用多彩渐变

- Alice 纠正：depth v2 的折角不好看，要求取消；希望把整个前景图形的白色改成多彩渐变。
- 实际修改：新增 gradient v3 视觉候选；保留 272 px 放大尺寸与柔和向下阴影，完全移除四个灰色折面；以源图 alpha 作为唯一形状遮罩，将所有原白色前景替换为连续的珊瑚红、琥珀橙、洋红、紫罗兰和少量钴蓝斜向渐变。
- 决策依据：以暖色为主，避免重新回到 Alice 已否决的大面积青蓝；颜色只改变填充，不改变 Photo Sphere 原始轮廓。图像技能规则仍要求采用确定性本地处理，因此没有调用生成式图像工具。
- 验证结果：已生成 432 px foreground/launcher 候选及 144 px 桌面尺寸预览；透明通道、尺寸与 Python 编译检查 PASS。最终视觉待 Alice 确认。
- 状态边界：gradient v3 仅位于 `assets/icon/`，尚未覆盖 `assets/android/res/`，没有重建、安装、commit、push 或发布；当前可安装 APK 仍是 PSR-006 的纯白前景版本。
- 证据：`assets/icon/photosphere-icon-native-gradient-v3-foreground.png`、`assets/icon/photosphere-icon-native-gradient-v3-launcher.png`、`assets/icon/photosphere-icon-native-gradient-v3-preview.png`、`scripts/render-native-photosphere-icon-gradient.py`。

### PSR-009 — 2026-10-10（Asia/Shanghai）— 蓝色圆盘风格候选

- Alice 纠正：gradient v3 的颜色观感奇怪；提供一枚蓝色圆盘图标作为风格参考，希望 Photo Sphere 图标采用类似的视觉语言。
- 星子判断：参考图只用于颜色、材质和层次，不复制其中的钟表指针或底部圆点；主体继续沿用已确认的 Photo Sphere 球形全景符号。
- 实际修改：使用内置图像生成工具，将钴蓝圆盘、中央淡紫柔光、深海军蓝后层与白色前层应用到 Photo Sphere 图形；第一份内部草稿的小尺寸白带过厚，易误读为 VR 头显，因此同轮收窄白色全景带，并把后层改为上下分离的两段弧线。保存 1254 px 透明原稿与 144 px 小尺寸预览。
- 决策依据：蓝色圆盘直接回应 Alice 的新参考；上下分离弧线与窄全景带保留应用内 Photo Sphere 图形的关键结构，同时避免此前已经排除的地球仪、星球和 VR 头显语义。
- 验证结果：原稿与预览尺寸分别为 1254×1254、144×144，均带 alpha 通道；144 px 回读可辨认上下弧和中央全景带。最终视觉仍待 Alice 确认。
- 状态边界：blue orb v4 仅位于 `assets/icon/`，尚未覆盖 `assets/android/res/`，没有重建、安装、commit、push 或发布；当前可安装 APK 仍是 PSR-006 的纯白前景版本。
- 证据：`assets/icon/photosphere-icon-native-blue-orb-v4.png`、`assets/icon/photosphere-icon-native-blue-orb-v4-preview.png`。

### PSR-010 — 2026-10-10（Asia/Shanghai）— 半透明白色扁平前景候选

- Alice 反馈：蓝色圆盘方向“好很多”；重新附上蓝色圆盘与深蓝圆环版本，要求把中央纯白部分改成白色半透明图形，并去掉立体感。
- 实际修改：使用 Alice 附件作为精确编辑目标，只改变中央白色全景带；让蓝紫背景与深蓝圆环能够透过约半透明的白色覆盖层，并移除原先的厚度、倒角、投影、亮边和体积渐变。蓝色圆盘、中央柔光、深蓝圆环与构图保持不变。
- 决策依据：此轮是对明确附件的局部材质编辑，不把上一轮的其他几何调整混入，便于 Alice 单独判断“半透明、无立体感”是否成立。
- 验证结果：保存 1254×1254 透明原稿和 144×144 预览，均带 alpha 通道；小尺寸回读中白色横带仍可识别，蓝紫底色与深蓝圆环能透过横带。视觉接受仍待 Alice 确认。
- 状态边界：blue glass v5 仅位于 `assets/icon/`，尚未覆盖 `assets/android/res/`，没有重建、安装、commit、push 或发布；当前可安装 APK 仍是 PSR-006 的纯白前景版本。
- 证据：`assets/icon/photosphere-icon-native-blue-glass-v5.png`、`assets/icon/photosphere-icon-native-blue-glass-v5-preview.png`。

### PSR-011 — 2026-10-10（Asia/Shanghai）— 半透明横带环绕候选

- Alice 纠正：blue glass v5 的半透明方向成立，但横带仍缺少环绕球体一周的感觉。
- 实际修改：保留扁平半透明白色材质，把横带改为略带椭圆弧度的连续腰带；正面横跨球体，两端在左右收窄并向后转折，以短小的背面延续和遮挡关系表达完整 360° 环绕。没有在球体外新增独立轨道。
- 决策依据：使用轮廓路径和前后遮挡表达空间关系，而不靠倒角、厚度、阴影或高光恢复立体材质，兼顾 Alice 对“环绕一周”和“不要有立体感”的两项要求。
- 验证结果：保存 1254×1254 透明原稿和 144×144 预览，均带 alpha 通道；小尺寸回读仍能看到左右端向后包裹的短段，半透明白带与深蓝圆环保持可区分。视觉接受仍待 Alice 确认。
- 状态边界：blue wrap v6 仅位于 `assets/icon/`，尚未覆盖 `assets/android/res/`，没有重建、安装、commit、push 或发布；当前可安装 APK 仍是 PSR-006 的纯白前景版本。
- 证据：`assets/icon/photosphere-icon-native-blue-wrap-v6.png`、`assets/icon/photosphere-icon-native-blue-wrap-v6-preview.png`。

### PSR-012 — 2026-10-10（Asia/Shanghai）— blue wrap v6 正式接入并重建 v0.9

- Alice 验收：确认 blue wrap v6“已经足够有辨识度”，授权正式采用。
- 实际修改：将 1254 px v6 原稿固定为彩色图标源；新增 `scripts/render-approved-icon-v6.py`，校验原稿与单色蒙版源文件哈希，缩放为 432 px，并用圆形 alpha mask 清除生成图外围透明噪点。普通与 adaptive foreground 使用 v6，adaptive background 改为 `#0B70FA`；Android 13+ themed icon 单独使用原生 Photo Sphere alpha 蒙版，避免主题模式下变成实心圆。同步更新 README、构建说明、NOTICE 与 G9 记录。
- 决策依据：视觉批准只授权采用 v6，不应牺牲 Android 主题图标可读性；彩色图标和 themed mask 分离，既保留桌面辨识度，又符合 monochrome 图标的单色渲染方式。
- 构建与验证：原稿哈希、Python 编译、XML、完整六补丁构建、zipalign、APK Signature Scheme v3 与证书连续性 `79d76e…db76` 均 PASS。签名后 APK 反解确认 application、两个 launcher alias 仍引用 `@mipmap/photosphere_launcher`；彩色 foreground、legacy launcher 与 monochrome mask 的 432×432 RGBA 像素均与构建输入完全一致。
- 构建产物：`.local/output/Photo-Sphere-v0.9-dedicated-icon.apk`，大小 `172782348` bytes，SHA-256 `61c37c3ff900e0dd80d882c23bc63a1867e4e4a66ae8fe88ac5b26e55ea5b9af`。
- 状态边界：资源接入和本地构建已完成；当前实机仍为 v0.8，v0.9 尚未安装，普通/主题图标目视与相机功能回归均未执行。本轮没有 commit、push 或发布。
- 证据：`assets/icon/photosphere-icon-approved-v6-android-preview.png`、`assets/android/res/`、`scripts/render-approved-icon-v6.py`、`docs/g9-dedicated-icon-v09-2026-10-09.md`、`.local/verify/v0.9-selected-icon-61c37c3f/`（忽略目录）。

### PSR-013 — 2026-10-10（Asia/Shanghai）— v0.9 安装授权与 ADB 阻塞

- Alice 授权：明确允许安装 v0.9。
- 实际检查：电脑 USB 层识别到设备序列号，但 `adb devices -l` 返回 `unauthorized`；等待约 30 秒并复查后状态未改变。
- 安全边界：没有执行卸载、清除数据或安装命令；v0.9 尚未写入设备，当前实机版本仍为 v0.8。
- 下一步：Alice 在手机 USB 调试弹窗中允许此电脑后，重新核对设备代号/型号，再执行 `adb install -r` 原位升级并做安装后回读。

### PSR-014 — 2026-10-10（Asia/Shanghai）— v0.9 原位安装成功

- Alice 操作：在 Pixel 10 Pro XL 上允许了本电脑的 USB 调试授权。
- 安装前核对：ADB 状态为 `device`；产品代号 `mustang`，型号 `Pixel 10 Pro XL`；现有 `com.shamim.cam` 的 `firstInstallTime` 为 `2026-08-27 15:28:47`，`lastUpdateTime` 为 `2026-08-27 17:30:36`。
- 实际执行：对 `.local/output/Photo-Sphere-v0.9-dedicated-icon.apk` 运行 `adb install -r`，返回 `Performing Streamed Install` / `Success`；未卸载应用、未清除数据。
- 安装后回读：`firstInstallTime` 保持不变，`lastUpdateTime` 更新为 `2026-10-10 23:22:11`；包路径存在，MAIN/LAUNCHER 解析到 `com.shamim.cam/com.android.camera.CameraLauncher`。
- 状态边界：v0.9 已安装，但尚未打开应用；普通/主题图标目视、冷启动取景、Type 菜单、完整 360°、Fish eye / Sphere 和系统相机热恢复均未做本轮验证。没有 commit、push 或发布。

### PSR-015 — 2026-10-10（Asia/Shanghai）— v0.9 实机冒烟验收

- Alice 验收回执：“没问题！图标已更新，正常取景，也拍出了新照片”。
- 验证结果：Pixel 10 Pro XL 普通桌面图标目视 PASS；Photo Sphere 冷启动取景 PASS；新照片产出 PASS。
- 证据边界：Alice 没有在本轮说明启用了 Android themed icon，也没有明确说明新照片是完整 360° 球形全景；Type 菜单、Fish eye / Sphere 和系统相机热恢复也未单独复测，因此这些项目不从 v0.8 历史证据自动推定为 v0.9 PASS。
- 状态边界：v0.9 已完成安装与基础实机冒烟验收；没有 commit、push 或发布。

### PSR-016 — 2026-10-10（Asia/Shanghai）— v1.0 主摄数码变焦候选

- Alice 提出：在 v0.9 图标与拍照冒烟通过后，下一步推进主摄数码变焦。
- 星子建议与实现：不恢复旧 `.6× / 2× / 5×` 多镜头控件，不碰前摄；复用 Photo Sphere 已注册的双指手势。静态逆向确认旧代码只调整 OpenGL 取景投影，并未写入拍照参数；新增 `0007` 补丁，把手势接入 Camera1 `Laum.p` / `Camera.Parameters.setZoom()`，限制在 1×–2×并回读实际倍率。
- 拼接一致性：新增独立 `zoomRatio` 状态，以精确透视公式修正 LightCycle 水平视场角；倍率变化后仅在采集前重置当前 Type 引导。进入 `Lemn.l` 采集态后锁住触摸缩放，避免一组照片使用不同视场角。手势结束时短暂显示实际倍率。
- 构建与验证：固定基础 APK 上七补丁完整应用，无 reject/orig；apktool 重建、zipalign、APK Signature Scheme v3 和既有证书 `79d76e…db76` 连续性均 PASS。输出 `.local/output/Photo-Sphere-v1.0-main-camera-zoom.apk`，大小 `172782348` bytes，SHA-256 `2dc2b7b2127403674dac5ec9a1b4de3ed35100c19add39a0a85080766f206f2f`。ADB 只读核对设备仍为 `mustang / Pixel 10 Pro XL`，当前包 `lastUpdateTime` 仍为 `2026-10-10 23:22:11`，证明 v1.0 尚未安装。
- 决策来源：主摄变焦目标由 Alice 提出；双指 1×–2×、采集锁定与不恢复多镜头按钮是星子的最小风险实现方案，尚待 Alice 实机接受。
- 状态边界：v1.0 仅完成本地候选构建与签名；未安装、未启动、未拍摄。当前实机仍为 v0.9。没有 commit、push 或发布。
- 证据：`patches/0007-photo-sphere-main-camera-digital-zoom.patch`、`docs/g10-main-camera-digital-zoom-v10-2026-10-10.md`、`.local/output/Photo-Sphere-v1.0-main-camera-zoom.apk`（忽略目录）。

### PSR-017 — 2026-10-10（Asia/Shanghai）— v1.0 原位安装成功

- Alice 授权：明确回复“允许安装 v1.0”。
- 安装前核对：ADB 为 `device`；目标为 `mustang / Pixel 10 Pro XL`；当前包 `firstInstallTime=2026-08-27 15:28:47`、`lastUpdateTime=2026-10-10 23:22:11`。
- 实际执行：对 `.local/output/Photo-Sphere-v1.0-main-camera-zoom.apk` 执行 `adb install -r`，返回 `Performing Streamed Install` / `Success`；没有卸载或清除应用数据。
- 安装后回读：`firstInstallTime` 保持不变，`lastUpdateTime` 更新为 `2026-10-10 23:42:55`；启动入口仍为 `com.shamim.cam/com.android.camera.CameraLauncher`。设备端 `base.apk` SHA-256 为 `2dc2b7b2127403674dac5ec9a1b4de3ed35100c19add39a0a85080766f206f2f`，与本地候选一致。
- 状态边界：v1.0 已安装但尚未启动；不能据此宣称取景、倍率提示、实际裁切、采集锁定或拼接通过。没有 commit、push 或发布。

### PSR-018 — 2026-10-10（Asia/Shanghai）— v1.0 双指崩溃定位与 v1.0.1 热修复候选

- Alice 实机反馈：双指放大取景没有产生变焦，反而看到了“所有文件访问权限”的应用设置页面。
- 现场证据：ADB crash buffer 在 `23:49:05.864` 记录 `com.shamim.cam` 主线程于 `ScaleGestureDetector.onScaleBegin` 崩溃，异常为 `IllegalArgumentException: min zoom value hasn't been initialized properly`；调用链来自通用 `PreviewOverlay` 的 `hdq/hlz` 缩放路径，不是 Photo Sphere 的 `bpt/dws` 手势路径。
- 原因判断：v0.8 起隐藏并禁用了原 `.6× / 2× / 5×` 变焦 UI，通用相机缩放控制器因而没有有效最小倍率；v1.0 没有隔离这层监听器，它先于 Photo Sphere 模块收到双指事件并崩溃。v1.0.1 反编译结果中不存在 `MANAGE_EXTERNAL_STORAGE` 声明或全文件访问设置 Action；本次日志证明的是手势崩溃，不能把设置页外观当作权限请求链路的证据。
- 实际修改：新增 `0008-photo-sphere-pinch-routing-hotfix.patch`，让专版 `PreviewOverlay` 在可触摸状态下跳过通用 `hix/hdq` 缩放检测器，继续执行其 GestureDetector 与 Photo Sphere 模块 `OnTouchListener`；不改变 v1.0 的 Camera1 裁切、FOV 修正、采集锁定或五种 Type。
- 构建验证：固定基础 APK 上八补丁全部应用，无 `.rej` / `.orig`；apktool 重建、zipalign、APK Signature Scheme v3 和既有证书 `79d76e…db76` 连续性均 PASS。输出 `.local/output/Photo-Sphere-v1.0.1-main-camera-zoom-hotfix.apk`，大小 `172782348` bytes，SHA-256 `086357e2eb2b9b5d47ca8479f33e8a60f6ce89d21ac28774de9f9768e56fabdb`。
- 状态边界：v1.0 的双指变焦验收为 FAIL；v1.0.1 仅完成本地构建与静态验证，尚未安装、启动或拍摄。没有 commit、push 或发布。

### PSR-019 — 2026-10-10（Asia/Shanghai）— v1.0.1 原位安装成功

- Alice 授权：明确回复“允许安装 v1.0.1”。
- 安装前核对：ADB 为 `device`；目标为 `mustang / Pixel 10 Pro XL`；当前包 `firstInstallTime=2026-08-27 15:28:47`、`lastUpdateTime=2026-10-10 23:42:55`，对应已安装的失败候选 v1.0。
- 实际执行：对 `.local/output/Photo-Sphere-v1.0.1-main-camera-zoom-hotfix.apk` 执行 `adb install -r`，返回 `Performing Streamed Install` / `Success`；没有卸载或清除应用数据。
- 安装后回读：`firstInstallTime` 保持不变，`lastUpdateTime` 更新为 `2026-10-10 23:56:10`；启动入口仍为 `com.shamim.cam/com.android.camera.CameraLauncher`。设备端 `base.apk` SHA-256 为 `086357e2eb2b9b5d47ca8479f33e8a60f6ce89d21ac28774de9f9768e56fabdb`，与本地候选一致。
- 状态边界：v1.0.1 已安装但尚未启动；不能据此宣称双指不崩溃、实际倍率、取景裁切、采集锁定或拼接通过。没有 commit、push 或发布。

### PSR-020 — 2026-10-11（Asia/Shanghai）— 放弃变焦并原位恢复 v0.9

- Alice 实机反馈与决策：v1.0.1 的变焦“出现了”，说明热修复后双指不再立即崩溃并出现缩放效果；但 Alice 认为该功能“很鸡肋”，明确要求回到 v0.9，不再提供变焦。
- 产品决定：接受 Alice 的体验判断；v1.0/v1.0.1 不进入支持版本。`0007/0008` 与 G10/G11 仅保留为实验和失败修复历史；默认构建脚本恢复为只应用 `0001`–`0006` 的 v0.9。
- 回退前核对：ADB 为 `device`，目标为 `mustang / Pixel 10 Pro XL`；v0.9 本地 APK SHA-256 为 `61c37c3ff900e0dd80d882c23bc63a1867e4e4a66ae8fe88ac5b26e55ea5b9af`。
- 实际执行：对 `.local/output/Photo-Sphere-v0.9-dedicated-icon.apk` 执行 `adb install -r`，返回 `Performing Streamed Install` / `Success`；没有卸载或清除应用数据。
- 安装后回读：`firstInstallTime` 仍为 `2026-08-27 15:28:47`，`lastUpdateTime` 更新为 `2026-10-11 00:03:20`；启动入口仍为 `com.shamim.cam/com.android.camera.CameraLauncher`。设备端 `base.apk` SHA-256 为 `61c37c3ff900e0dd80d882c23bc63a1867e4e4a66ae8fe88ac5b26e55ea5b9af`，与此前验收过的 v0.9 输出一致。
- 状态边界：回退安装与文件一致性 PASS；回退后的首次启动尚未观察。没有 commit、push 或发布。

### PSR-021 — 2026-10-11（Asia/Shanghai）— v0.9 GitHub Release

- Alice 授权：明确要求更新 GitHub 仓库并把 v0.9 设为新的 Release；该授权包括为本轮 v0.9 源码范围创建提交、推送、标签和 GitHub Release。
- 发布范围：只发布补丁、构建脚本、图标资源与公开验证记录，不附带基础 APK、派生 APK、签名材料、设备序列号或私人绝对路径。稳定构建只应用 `0001`–`0006`；`0007/0008` 明确标为已放弃实验且不进入默认构建。
- 凭据与工具边界：遵循仓库通用规则，push 使用原生 Git；Release 使用 GitHub 官方 API；不以沙箱内 `gh auth status` 判断登录状态，不启动浏览器授权。
- 发布前验证：公开范围与敏感信息扫描 PASS；稳定六补丁全量重建、zipalign、APK Signature Scheme v3、既有证书连续性及与设备已验收包的 3069 个 ZIP 条目逐项内容比较均 PASS。实验补丁 `0007/0008` 的 dry-run 也可应用，但不进入默认构建。
- 实际交付：使用 Alice Ma 的既有 Git author / committer 身份创建发布 commit `006c1040bb51cbf7e476078a6d16e37667670293`，并附 `Co-authored-by: Codex <codex@openai.com>` trailer；原生 Git 已将 `main` 和 annotated tag `v0.9` 推送到 `origin`，远端 peeled tag 与发布 commit 一致。
- GitHub Release：通过 GitHub 官方 API 创建 `Photo Sphere Revival v0.9`，`draft=false`、`prerelease=false`，发布时间为 2026-10-11 00:12:37（Asia/Shanghai），URL 为 `https://github.com/isalicema/pixel-sphere-revival/releases/tag/v0.9`。Release 附件数为 0；没有上传基础 APK、派生 APK 或签名材料。
- 状态边界：仓库 commit、远端 push、tag 与 Release 均已完成并回读；本条日志的发布后证据回写将作为后续 `main` 文档提交，不移动 `v0.9` 标签。Pixel 10 Pro XL 既有实机验收保持有效；Samsung 与其他品牌兼容性仍未验证。
