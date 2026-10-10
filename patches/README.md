# Patch sets

## Stable v0.9

`scripts/build-local.sh` 只应用以下六个稳定补丁：

1. `0001-photo-sphere-label.patch`
2. `0002-photo-sphere-dedicated-mode.patch`
3. `0003-clean-controls-and-startup.patch`
4. `0004-photo-sphere-type-menu.patch`
5. `0005-bound-legacy-camera-semaphore-wait.patch`
6. `0006-photo-sphere-icon.patch`

## Abandoned zoom experiment

`0007-photo-sphere-main-camera-digital-zoom.patch` 与 `0008-photo-sphere-pinch-routing-hotfix.patch` 是 v1.0/v1.0.1 实验记录，不进入默认构建。v1.0 的通用缩放监听器会在手势开始时崩溃；v1.0.1 修复该崩溃并能出现变焦，但实机体验价值不足，项目于 2026-10-11 决定继续使用 v0.9 默认焦段。
