from PIL import Image, ImageDraw, ImageFont

import os

from src.PathHelper import *

def generate_images(pruebas, series, options, debug):
    IG_data = options["image_generation"]
    # original image over which we write, only needed for size
    base = Image.open(P_IMAGES + IG_data["base_image"]).convert("RGBA")
    b_fnt = ImageFont.truetype(P_FONTS + IG_data["font_file"], IG_data["BIG_FONT_SIZE"])
    m_fnt = ImageFont.truetype(P_FONTS + IG_data["font_file"], IG_data["MEDIUM_FONT_SIZE"])
    s_fnt = ImageFont.truetype(P_FONTS + IG_data["font_file"], IG_data["SMALL_FONT_SIZE"])

    prueba_index = 0
    series_number = IG_data["IMAGES_PER_FOLDER"] + 1
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

            d.text((IG_data["RACE_NAME_X"], IG_data["RACE_NAME_Y"]),
                   ' ' * int(IG_data["RACE_NAME_CH_LENGTH"] - len(race_name) / 2) + race_name,
                   font=s_fnt, fill=(255, 255, 255, 255))

            for lane in range(1, 7):
                # draw lane number
                d.text((IG_data["LANE_X"], IG_data["START_LANE_Y"] + IG_data["LANE_HEIGHT"] * lane),
                       str(lane),
                       font=b_fnt, fill=(255, 255, 255, 255))
                # draw swimmer name
                if serie[lane-1] is not None :
                    d.text((IG_data["SWIMMER_X"], IG_data["START_SWIMMER_Y"] + IG_data["LANE_HEIGHT"] * lane),
                           serie[lane-1]["nombre"] + " " + serie[lane-1]["apellidos"], font=m_fnt,
                           fill=(255, 255, 255, 255))
            result = Image.alpha_composite(base, image)
            series_number = series_number + 1
            if series_number > IG_data["IMAGES_PER_FOLDER"]:
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
