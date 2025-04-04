# Simple script to create placeholder payment icons

from PIL import Image, ImageDraw, ImageFont
import os

def create_payment_icon(name, color, size=(120, 70)):
    # Create a new image with white background
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw colored rectangle
    draw.rectangle([5, 5, size[0]-5, size[1]-5], fill=color)
    
    # Try to add text
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        # Use default font if Arial is not available
        font = ImageFont.load_default()
    
    # Calculate text position
    text_width = draw.textlength(name, font=font)
    text_position = ((size[0] - text_width) / 2, (size[1] - font.size) / 2)
    
    # Draw text
    draw.text(text_position, name, fill='white', font=font)
    
    # Ensure directory exists
    os.makedirs('static/images', exist_ok=True)
    
    # Save image
    file_path = f'static/images/{name.lower()}.png'
    img.save(file_path)
    print(f"Created {file_path}")

# Create payment icons
create_payment_icon('Visa', '#1A1F71')  # Visa blue
create_payment_icon('Mastercard', '#EB001B')  # Mastercard red
create_payment_icon('PayPal', '#003087')  # PayPal blue
create_payment_icon('OXXO', '#ED1C2E')  # OXXO red

print("All payment icons created successfully")