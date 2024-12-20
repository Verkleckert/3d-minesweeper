from PIL import Image, ImageDraw, ImageFont
import os
from colorsys import hsv_to_rgb

# Path to the base background image
base_image_path = "assets/base.png"  # Replace with the actual path to your base image

# Folder to save the output images
output_folder = "assets/numbers"  # Replace with the actual path to your output folder
os.makedirs(output_folder, exist_ok=True)

# Define font settings
font_size = 65  # Adjusted size
font_path = "assets/font/dejavu-sans-bold.ttf"  # Adjust to the font available on your system

# Load the font
font = ImageFont.truetype(font_path, font_size)

# Load the base image
base_image = Image.open(base_image_path)

# Generate images with numbers 1 to 26
for number in range(1, 27):
    # Create a copy of the base image
    img = base_image.copy()
    draw = ImageDraw.Draw(img)

    # Define the text and calculate its position
    text = str(number)
    text_bbox = draw.textbbox((0, 0), text, font=font)  # Get the bounding box of the text
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    position = ((img.width - text_width) // 2, (img.height - text_height) // 2)

    # Adjust for perfect vertical centering
    position = (position[0], position[1] - text_bbox[1])

    # Calculate a color along the color spectrum
    hue = (number - 1) / 26  # Spread hues evenly across the range
    rgb = hsv_to_rgb(hue, 1.0, 1.0)  # Convert HSV to RGB
    color = tuple(int(c * 255) for c in rgb)  # Scale to 0-255 range

    # Draw the number on the image
    draw.text(position, text, font=font, fill=color)

    # Save the image to the output folder
    img.save(os.path.join(output_folder, f"{number}.png"))

print(f"Images saved in folder: {output_folder}")
