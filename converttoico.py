from PIL import Image

# افتح صورة PNG
img = Image.open("icons/thrawa.png")

# غيّر حجمها إلى 512x512 (أفضل حجم للأيقونات)
img = img.resize((512, 512))

# خزّنها كـ ICO
img.save("thrawa.ico", format="ICO")
