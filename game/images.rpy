# ============================================================
# images.rpy —— 占位图像资源
# ------------------------------------------------------------
# 第一阶段不依赖美术资源：背景用纯色代替，保证工程可运行、可测试。
# 后续接入正式美术时，只需把 Solid(...) 换成对应的 PNG/WebP 路径，例如：
#     image bg throne = "images/backgrounds/throne.png"
# ============================================================

image bg throne = Solid("#141b28")
image bg hall = Solid("#1b2231")
image bg study = Solid("#161a20")
image bg border = Solid("#2a1c1c")
image bg night = Solid("#0b0e14")
