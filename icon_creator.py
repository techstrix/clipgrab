from PIL import Image, ImageDraw

# Create a new 64x64 image with a white background
icon_size = 64
image = Image.new('RGBA', (icon_size, icon_size), (255, 255, 255, 0))  # Transparent background
draw = ImageDraw.Draw(image)

# Draw a simple clipboard (rectangle) and arrow
# Clipboard body
draw.rectangle([(10, 10), (54, 40)], fill=(0, 0, 255, 255))  # Blue rectangle
draw.rectangle([(10, 5), (20, 10)], fill=(0, 0, 255, 255))   # Top clip

# Arrow (downward)
draw.polygon([(27, 45), (37, 45), (32, 55)], fill=(255, 255, 255, 255))  # White triangle

# Save as .ico
image.save('clipboard_monitor.ico', format='ICO')

print("Icon saved as clipboard_monitor.ico")