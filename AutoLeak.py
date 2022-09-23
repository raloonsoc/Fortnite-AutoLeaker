import requests
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np
import urllib.request
import time
import os
import glob
from math import ceil, floor
import textwrap

start_time = time.time()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(bcolors.WARNING + "Generating rarities..")
print(bcolors.WARNING + "Obtaining the data...")
print(bcolors.WARNING + "Restructuring the data...")
print(bcolors.WARNING + "Starting...")
r = requests.get("https://fortnite-api.com/v2/cosmetics/br/new",
                 params={'language': 'en'})
newItems = json.loads(r.text)
for allItems in newItems["data"]["items"]:
    if (allItems["images"]["featured"]):
        imageicon = allItems["images"]["featured"]
    else:
        imageicon = allItems["images"]["icon"]
        imageIcon = allItems["images"]["smallIcon"]
    if(imageicon):
        urllib.request.urlretrieve(imageicon, f'./cache/{allItems["id"]}.png')
    if (imageicon == "null"):
        urllib.request.urlretrieve(imageIcon, f'./cache/{allItems["id"]}.png')
    rarityy = allItems["rarity"]["value"];
    layer = Image.open(f'./Assets/rarities/{rarityy.capitalize()}.png')
    image = Image.open(f'./cache/{allItems["id"]}.png').convert("RGBA")
    blackitem = Image.open(f"./Assets/rarities/{rarityy.capitalize()}Down.png")
    if allItems["type"]["value"] == "outfit" or "emote" or "backpack":
        image1 = image.resize((512, 512))
        layer.paste(image1, (0, 0), image1)
    image12 = blackitem.resize((512, 512))
    layer.paste(image12, (0, 0), image12)
    canvas = ImageDraw.Draw(layer)
    text_size = 32;
    text = allItems["name"].upper()
    font = ImageFont.truetype(f'Assets/fonts/BurbankBigRegularBlack.otf', size=text_size)
    text_width, text_height = font.getsize(text)
    x = (512 - text_width) / 2
    while text_width > 512 - 4:
        text_size = text_size - 1
        font = ImageFont.truetype(f'Assets/fonts/BurbankBigRegularBlack.otf', size=text_size)
        text_width, text_height = font.getsize(text)
        x = (512 - text_width) / 2
    y = 420
    canvas.text((x, y), text ,(255, 255, 255),font=font,align='center',stroke_width=1,stroke_fill=(0, 0, 0))
    text_sizes = 14
    texts = allItems["description"]
    texts = texts.upper()

    fonts = ImageFont.truetype(f'Assets/fonts/BurbankBigRegularBlack.otf', size=text_sizes)
    if len(texts) > 50:
            
            new_text = ""
            for des in textwrap.wrap(texts, width=100):
                new_text += f'{des}\n'
            texts = new_text  # Split the Description
            text_widths, text_heights = fonts.getsize(texts)
            
            
            while text_widths / 2 > 512 - 4:
                text_sizes = text_sizes - 1
                fonts = ImageFont.truetype(f'Assets/fonts/BurbankBigRegularBlack.otf', size=text_sizes)
                text_widths, text_heights = font.getsize(texts)

            if len(texts.split('\n')) > 2:
                text_widths = text_widths / 2

                xs = (512 - text_widths) / 2
                ys = 465 - text_heights

                canvas.multiline_text((xs, ys), texts, fill='white', align='center', font=fonts)  
    else:
        text_widths, text_heights = font.getsize(texts)
        xs = (512 - text_widths) / 2
        while text_widths > 512 - 4:
            text_sizes = text_sizes - 1
            fonts = ImageFont.truetype(f'Assets/fonts/BurbankBigRegularBlack.otf', size=text_sizes)
            text_widths, text_heights = fonts.getsize(texts)
            xs = (512 - text_widths) / 2
        ys = 455

            
    canvas.text((xs, ys),text=texts,fill='white',font=fonts)

    

    layer.save(f'./images/{allItems["id"]}.png', "PNG")

print(bcolors.OKGREEN + "¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡")
print(bcolors.OKGREEN + "AutoLeaker Completed")
print(bcolors.OKGREEN + "¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡")
print(bcolors.HEADER + "Execution time %s seconds" %
      (time.time() - start_time))


PATH = r"Your images path"

frame_width = 1920
images_per_row = 10
padding = 0

os.chdir(PATH)

images = glob.glob("*.png")
images = images[:100]

img_widthss, img_heightss = Image.open(images[0]).size
sf = (frame_width-(images_per_row-1)*padding) / \
    (images_per_row*img_widthss)
scaled_img_width = ceil(img_widthss*sf)
scaled_img_height = ceil(img_heightss*sf)

number_of_rows = ceil(len(images)/images_per_row)
frame_height = ceil(sf*img_heightss*number_of_rows)

new_im = Image.new('RGB', (frame_width, frame_height))

i, j = 0, 0
for num, im in enumerate(images):
    if num % images_per_row == 0:
        i = 0
    im = Image.open(im)
    im.thumbnail((scaled_img_width, scaled_img_height))
    y_cord = (j//images_per_row)*scaled_img_height
    new_im.paste(im, (i, y_cord))
    i = (i+scaled_img_width)+padding
    j += 1

new_im.show()
new_im.save("./merger/all.jpg", "JPEG", quality=80,
            optimize=True, progressive=True)
