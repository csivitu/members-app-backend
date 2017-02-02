from PIL import Image,ImageFont,ImageDraw
import os
from django.conf import settings


def cert_gen(name,regno,year,of=""):
	year=str(year)[2:4]+" "+str(year+1)[2:4]
	img = Image.open(settings.BASE_DIR+"/cert/base.jpg")
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype(settings.BASE_DIR+"/cert/font.ttf", 84)
	font_SM = ImageFont.truetype(settings.BASE_DIR+"/cert/font.ttf", 64)
	draw.text((1400, 960),name,(0,0,0),font=font)
	draw.text((2800, 980),regno,(0,0,0),font=font_SM)
	draw.text((500, 1100),of,(0,0,0),font=font)
	draw.text((3040, 1115),year,(0,0,0),font=font_SM)
	return img

