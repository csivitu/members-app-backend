"""Generates certificates for the user
"""

from django.conf import settings
from PIL import Image, ImageFont, ImageDraw


def cert_gen(name, reg_no, year, of=""):
    year = str(year)[2:4] + " " + str(year + 1)[2:4]
    img = Image.open(settings.BASE_DIR + "/cert/base.jpg")

    # Load fonts
    font = ImageFont.truetype(settings.BASE_DIR + "/cert/font.ttf", 84)
    font_small = ImageFont.truetype(settings.BASE_DIR + "/cert/font.ttf", 64)

    # Write information
    draw = ImageDraw.Draw(img)
    draw.text((1400, 960), name, (0, 0, 0), font=font)
    draw.text((2800, 980), reg_no, (0, 0, 0), font=font_small)
    draw.text((500, 1100), of, (0, 0, 0), font=font)
    draw.text((3040, 1115), year, (0, 0, 0), font=font_small)

    return img
