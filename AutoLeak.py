import requests
import json
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import urllib.request
import time
import os
import glob
from math import ceil, floor

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
    layer = Image.open(f'./assets/{allItems["rarity"]["value"]}.png')
    image = Image.open(f'./cache/{allItems["id"]}.png').convert("RGBA")
    blackitem = Image.open("./assets/blackitem.png")
    if allItems["type"]["value"] == "outfit" or "emote" or "backpack":
        image1 = image.resize((361, 370))
        layer.paste(image1, (20, 15), image1)
    BurbankBold = ImageFont.truetype(
        "./assets/BurbankBigCondensed-Bold.otf", 15)
    BurbankBlack = ImageFont.truetype(
        "./assets/BurbankBigCondensed-Black.otf", 30)
    layer.paste(blackitem, (0, 0), blackitem)
    canvas = ImageDraw.Draw(layer)
    canvas.text((50, 300), f'{allItems["name"].upper()}',
                font=BurbankBlack, fill=(255, 255, 255))
    canvas.text((50, 340), f'{allItems["description"]}',
                font=BurbankBold, fill=(255, 255, 255))
    canvas.text((20, 370), f'{allItems["type"]["displayValue"]}',
                font=BurbankBold, fill=(255, 255, 255))

    layer.save(f'./images/{allItems["id"]}.png', "PNG")

print(bcolors.OKGREEN + "¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡")
print(bcolors.OKGREEN + "AutoLeaker Completed")
print(bcolors.OKGREEN + "¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡")
print(bcolors.HEADER + "Execution time %s seconds" %
      (time.time() - start_time))


PATH = r"path of folder imagges"

frame_width = 1920
images_per_row = 10
padding = 0

os.chdir(PATH)

images = glob.glob("*.png")
images = images[:100]

img_width, img_height = Image.open(images[0]).size
sf = (frame_width-(images_per_row-1)*padding) / \
    (images_per_row*img_width)
scaled_img_width = ceil(img_width*sf)
scaled_img_height = ceil(img_height*sf)

number_of_rows = ceil(len(images)/images_per_row)
frame_height = ceil(sf*img_height*number_of_rows)

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
new_im.save("./merge/all.jpg", "JPEG", quality=80,
            optimize=True, progressive=True)
