from PIL import Image, ImageDraw, ImageFont
import textwrap

def get_wallpaper(quote):
    # image_width
    if len(quote) <= 100:
        image = Image.new('RGB', (500, 300), color=(10, 133, 209))
        text_start_height = 40
    elif len(quote) <=150:          
        image = Image.new('RGB', (500, 400), color=(10, 133, 209))
        text_start_height = 70
    else:
        image = Image.new('RGB', (500, 500), color=(10, 133, 209))
        text_start_height = 100
    font = ImageFont.truetype("Arial.ttf", 40)
    text1 = quote
    text_color = (255, 255, 255)
    
    draw_text_on_image(image, text1, font, text_color, text_start_height)
    image.save('created_image.png')
 
def draw_text_on_image(image, text, font, text_color, text_start_height):
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=25)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text),line, font=font, fill=text_color)
        y_text += line_height