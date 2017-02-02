from PIL import Image,ImageFont,ImageDraw
import os
from django.conf import settings

def get_school(reg):
	code=reg[2:5]
	if(code in ['BCE','BCS','MIS','BCB']):
		return 'SCOPE'
	elif(code in ['BPI','BEM','BME']):
		return 'SMEC'
	elif(code in ['BIT','PHD']):
		return 'SITE'
	elif(code in ['BEC']):
		return 'SENSE'
	elif(code in ['BEI','BEE']):
		return 'SELECT'
	elif(code in ['BCM']):
		return 'SCALE'
	else:
		return ""
def cert_gen(name,regno,year):
	school=get_school(regno)
	year=str(year)[2:4]+" "+str(year+1)[2:4]
	img = Image.open(settings.BASE_DIR+"/cert/base.jpg")
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype(settings.BASE_DIR+"/cert/font.ttf", 84)
	font_SM = ImageFont.truetype(settings.BASE_DIR+"/cert/font.ttf", 64)
	draw.text((1400, 905),name,(0,0,0),font=font)
	draw.text((2800, 930),regno,(0,0,0),font=font_SM)
	draw.text((500, 1040),of,(0,0,0),font=font)
	draw.text((3028, 1060),year,(0,0,0),font=font_SM)
	return img

