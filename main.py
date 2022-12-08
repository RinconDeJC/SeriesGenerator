from src.ImageGenerator import generate_images

from src.start_list_reader import start_list, process_list_events, process_series

from src.PathHelper import *

import json
def execute(name="", debug=False):
    """

    Parameters
    ----------
    name : string
        name of the file to be processed withou ".pdf". If it is "" the default
        file in options.json will be processed.
    Returns
    -------
    Hopefully no errors
    """
    with open(P_OPTIONS + 'options.json') as options_json:
        options = json.load(options_json)
    if name == "":
        file_name = options["file_name"]
    else:
        file_name = name
    redo_parse = False
    try:
        with open(P_PDFS + 'intermedio.json') as aux_json:
            data = json.load(aux_json)
            if file_name != data["parsed_pdf"]:
                aux_json.close()
                redo_parse = True
            else:
                [pruebas, series] = [data["pruebas"], data["series"]]
                aux_json.close()
    except FileNotFoundError:
        redo_parse = True

    if redo_parse:
        # parse file
        pruebas, series,_,_ = start_list(file_name + ".pdf", debug)

        # create json and save
        json_data = {"parsed_pdf": file_name, "pruebas": pruebas, "series": series}
        save_file = open(P_PDFS + 'intermedio.json', "w")
        json.dump(json_data, save_file, indent=4, sort_keys=True)
        save_file.close()

    generate_images(pruebas, series, debug)

def debug_parse(input_file, output_file):
    """
    Outputs the text used before parsing swimmers and events into two .txt files
    whose names start with output_file in the Debug folder.
    This function is meant to be used in a python interactive console or to simply 
    check with the heck things are going sideways with the parsing
    
    To recover original objects:
        Events:
            1. Open de file Debug\\<output_file>_events.txt
            2. Read the whole file into a single string with >>> data = file.read()
            3. Separate with given separator >>> list_events = data.split('===')
        Series:
            1. Open de file Debug\\<output_file>_seires.txt
            2. Read the whole file into a single string with >>> data = file.read()
            3. Separate with given separator >>> series = [text.split('===') for text in data.split('|||')]
    Parameters
    ----------
    input_file : string
        file_name without .pdf to be parsed. This file should be a pdf located in 
        P_PDFS folder
    output_file : string
        start of name of output files
    Return
    ----------
    Hopefully no errors
    """
    _,_,text_events,text_series = start_list(input_file + ".pdf", True)
    with open(P_DEBUG + output_file + "_events.txt", "w", encoding="utf8") as file:
        for line in text_events:
            file.write(line)
            file.write("===")
        file.close()
    with open(P_DEBUG + output_file + "_series.txt", "w", encoding="utf8") as file:
        for list_ in text_series:
            for line in list_:
                file.write(line)
                file.write("===")
            file.write("|||")
        file.close()

def generate_from_manual_txt(file_name):
    """
    Combined with the previous function you can generate the txt, edit it 
    manually and then call this function the same way. This way, one is able 
    to fix reading errors manually in times of need. I hope you won't need it
    """
    with open(P_OPTIONS + 'options.json') as options_json:
        options = json.load(options_json)
    with open(P_DEBUG + file_name + '_events.txt', encoding="utf8") as events_text:
        data = events_text.read()
    list_events = data.split('===')
    with open(P_DEBUG + file_name + '_series.txt', encoding="utf8") as series_text:
        data = series_text.read()
    series = [text.split('===') for text in data.split('|||')]
    events_p, series_p = process_list_events(list_events, options), process_series(series, options)
    generate_images(events_p, series_p, True)

if __name__ == '__main__':
    print("doing nothing :)\n")
    #execute("trofeo22", True)

