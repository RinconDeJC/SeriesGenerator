from PIL import Image, ImageDraw, ImageFont

import os

from src.PathHelper import *

# constants
FONT_FILE = "lmmonocaps10-regular.otf"
BIG_FONT_SIZE = 40
MEDIUM_FONT_SIZE = 32
SMALL_FONT_SIZE = 28

# coordinates
RACE_NAME_X = 200
RACE_NAME_Y = 507
RACE_NAME_CH_LENGTH = 16

LANE_X = 95
START_LANE_Y = 45

SWIMMER_X = 160
START_SWIMMER_Y = 53

LANE_HEIGHT = 66


IMAGES_PER_FOLDER = 20


def generate_images(pruebas, series, debug):

    # original image over which we write, only needed for size
    base = Image.open(P_IMAGES + "MarcoSeries.png").convert("RGBA")

    b_fnt = ImageFont.truetype(P_FONTS + FONT_FILE, BIG_FONT_SIZE)
    m_fnt = ImageFont.truetype(P_FONTS + FONT_FILE, MEDIUM_FONT_SIZE)
    s_fnt = ImageFont.truetype(P_FONTS + FONT_FILE, SMALL_FONT_SIZE)

    prueba_index = 0
    series_number = IMAGES_PER_FOLDER + 1
    folder = 0
    for prueba in series:
        for serie in prueba:
            if all(lane is None for lane in serie):
                continue
            # for every series there is
            image = Image.new("RGBA", base.size, (255, 255, 255, 0))
            # get a drawing context
            d = ImageDraw.Draw(image)

            race_name = pruebas[prueba_index]

            d.text((RACE_NAME_X, RACE_NAME_Y),
                   ' ' * int(RACE_NAME_CH_LENGTH - len(race_name) / 2) + race_name,
                   font=s_fnt, fill=(255, 255, 255, 255))

            for lane in range(1, 7):
                # draw lane number
                d.text((LANE_X, START_LANE_Y + LANE_HEIGHT * lane),
                       str(lane),
                       font=b_fnt, fill=(255, 255, 255, 255))
                # draw swimmer name
                if serie[lane-1] is not None :
                    d.text((SWIMMER_X, START_SWIMMER_Y + LANE_HEIGHT * lane),
                           serie[lane-1]["nombre"] + " " + serie[lane-1]["apellidos"], font=m_fnt,
                           fill=(255, 255, 255, 255))
            result = Image.alpha_composite(base, image)
            series_number = series_number + 1
            if series_number > IMAGES_PER_FOLDER:
                series_number = 1
                folder = folder + 1
                if not os.path.exists(P_GALLERY_CHECKING + str(folder)):
                    os.makedirs(P_GALLERY_CHECKING + str(folder))
                if not os.path.exists(P_GALLERY + str(folder)):
                    os.makedirs(P_GALLERY + str(folder))
            save_file_name = str(series_number)
            if series_number < 10:
                save_file_name = '00' + save_file_name
            elif series_number < 100:
                save_file_name = '0' + save_file_name
            result.save(P_GALLERY_CHECKING + str(folder) + '\\' + save_file_name + ".png", format='png')
            image.save(P_GALLERY + str(folder) + '\\' + save_file_name + ".png", format='png')

        prueba_index = prueba_index + 1


# Ideas:
# Añadir el logo del club a la izquierda del nombre en chiquitito
# Añadir tiempos en imagenes que roten
# acortar nombres para que quepa mejor el resto, poniendo iniciales. apellidos
