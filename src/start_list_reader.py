# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 09:15:26 2021

@author: sredo
"""

# pip install PyPDF2  # IMPORTANTE CARGAR EL PAQUETE ANTES DE IMPORTARLO!!!

import PyPDF2 as pdf
from math import log10, floor
import json
from src.PathHelper import *


# returns list<str>, list<list<dict*>>
def start_list(file_name, debug):
    """
    Given a file name parses it and outputs the events and series

    Parameters
    ----------
    name : string
        name of the file to be processed withou ".pdf"
    Returns
    -------
    TODO:
    For debuging propouses:
    text_series : [[string]]
        the list of lists of strings used to output the series
    text_events : [string]
        the list of strings used to output the list of events
    """

    with open(P_OPTIONS + 'options.json') as options_json:
        options = json.load(options_json)

    file = open(P_PDFS + file_name, 'rb')
    
    reader = pdf.PdfFileReader(file)
    
    npag = reader.getNumPages()

    if not options["range"]["until_end"]:
        npag = options["range"]["end"]
    
    txt = ''
    
    for i in range(options["range"]["start"], npag):
        
        tx = reader.getPage(i).extractText()
        txt = txt + tx

    if debug:
        file = open(P_DEBUG + "pdf_raw.txt", "w")
        file.write(txt)
        file.close()

    events = txt.split(options["parsing_data"]['EVENT_SPLITTER']) # -> [String]
    events = events[1:]

    if debug:
        file = open(P_DEBUG + "pdf_after_split_event.txt", "w")
        for text in events:
            file.write(text)
            file.write("\n")
        file.close()
    
    events_ordered = [] # -> [String]
    counter = 1
    for i in events:
        ini = i.split(',')[0]
        if len(ini) < 4:
            events_ordered[-1] = events_ordered[-1] + i
        else:
            events_ordered.append(i)
        counter = counter + 1  

    list_events = [] # -> [String]
    
    for i in events_ordered:
        list_events.append(i.split('/')[0][0:-2])

    series = [] # -> [[String]]
    
    for i in events_ordered:
        series.append(i.split(options["parsing_data"]["SERIES_SPLITTER"])[1:])

    # eliminate TRASH_to_eol (end of line)
    for i in range(len(series)):
        for trash in options["parsing_data"]["EOL_TRASH"]:
            for j in range(len(series[i])):
                position = series[i][j].find(trash)
                if position >= 0:
                    series[i][j] = series[i][j][0:position]

    if debug:
        file = open(P_DEBUG + "pdf_list_events.txt", "w")
        for text in list_events:
            file.write(text)
            file.write("\n")
        file.close()
        file = open(P_DEBUG + "pdf_series.txt", "w")
        i = 0
        for array1 in series:
            file.write("Serie " + str(i) + ":")
            file.write("[")
            file.write("\n")
            for text in array1:
                file.write("{\n")
                file.write(text)
                file.write("\n}\n")
            i = i + 1
            file.write("]\n")
        file.close()

    return process_list_events(list_events, options), process_series(series, options), list_events, series


def process_list_events(list_events, options):
    """
    Parses a list of events into simple format to be printed on images.

    DISCLAIMER: Function hasn't been tested in events with relays in option.json file

    Parameters
    ----------
    list_events : [string]
        list of the events (non parsed)
    options : json
        json object with the information in options.json file
    Returns
    -------
    ret_list_events : [string]
        parsed list of events, e.g. ['400M LIBRE MIXTO', '200M ESTILOS MIXTO',...]
    """
    ret_list_events = []
    possible_events = options["competition_data"]["styles"]
    possible_distances = options["competition_data"]["distances"]

    for event in list_events:
        start = 0
        # check how far we need to remove the text regarding index of event
        for d in possible_distances:
            if d in event:
                start = event.find(d)
                break

        # check "FEMENINO", "MASCULINO" or "MIXTO"
        if options["parsing_data"]["Masc_UPPER"] in event.upper():
            f_m = "MASCULINO"
        elif options["parsing_data"]["Fem_UPPER"] in event.upper():
            f_m = "FEMENINO"
        else:
            f_m = "MIXTO"

        for estilo in possible_events:
            if estilo in event:
                position = len(estilo) + event.find(estilo)
                break
        result = (event[start:position] + " " + f_m).upper()
        ret_list_events.append(" ".join(result.split()))
    return ret_list_events


# L_TIEMPO_RESULTADO = 11
# L_DIGITOS_A_EDAD = 2
# C_SEPARADOR_NOMBRE_CLUB = '-'
# C_SEPARADOR_APELLIDOS_NOMBNRE = ','
# S_SIN_TIEMPO = "NT"
# S_TIEMPO_RESULTADO = "___:___.___"
# N_CALLES = 6


def process_series(series, options):
    """

    Parameters
    ----------
    series : [[string]]
        list of series (non parsed). Each position corresponds to a serie
    options : json
        json object with the information in options.json file
    Returns
    -------
    ret_series : [string]
        parsed list of events, e.g. ['400M LIBRE MIXTO', '200M ESTILOS MIXTO',...]
    """
    ret_series = []
    for event in series:
        n_series = len(event)
        ret_event = []
        for n in range(n_series):
            # skip number of serie
            # assuming the string given starts by "n de n_series\n"
            digits_n = 1 + floor(log10(n+1))
            digits_series = 1 + floor(log10(n_series))
            position = 4 + digits_n + digits_series
            swimmers = [None] * options["parsing_data"]["N_CALLES"]
            event[n] = event[n].lstrip()

            # split the swimmers by S_TIEMPO_RESULTADO
            data = event[n][position:].split(options["parsing_data"]["S_TIEMPO_RESULTADO"])
            data.pop()

            for i in range(len(data)):
                j = 0
                # remove all leading end of line and blanks
                while j < len(data[i]):
                    if data[i][j] != ' ' and data[i][j] != '\n':
                        break
                    j += 1
                swimmer = data[i][j:]
                swimmers[int(swimmer[0])-1] = process_swimmer(swimmer[1:], options)
            ret_event.append(swimmers)
        ret_series.append(ret_event)
    return ret_series


def process_swimmer(swimmer, options):
    pos_separador_an = swimmer.find(options["parsing_data"]["C_SEPARADOR_APELLIDOS_NOMBRE"])
    apellidos = swimmer[0:pos_separador_an].strip()

    pos_fin_nombre = pos_separador_an + 2
    while not swimmer[pos_fin_nombre].isdigit():
        pos_fin_nombre = pos_fin_nombre + 1
    nombre = swimmer[pos_separador_an + 1:pos_fin_nombre].strip().upper()

    year = swimmer[pos_fin_nombre:pos_fin_nombre+options["parsing_data"]["L_DIGITOS_A_EDAD"]]

    pos_separador_club = swimmer.find(options["parsing_data"]["C_SEPARADOR_NOMBRE_CLUB"])

    if swimmer[len(swimmer)-1].isdigit():
        pos_fin_club = pos_separador_club + 1
        while not swimmer[pos_fin_club].isdigit():
            pos_fin_club = pos_fin_club + 1
    else:
        pos_fin_club = len(swimmer)-len(options["parsing_data"]["S_SIN_TIEMPO"])
    club = swimmer[pos_separador_club+1:pos_fin_club].strip()

    tiempo = swimmer[pos_fin_club:]

    # delete double blanks (thank you PDF reader -.-)
    while "  " in nombre:
        nombre = nombre.replace("  ", " ")
    while "  " in apellidos:
        apellidos = apellidos.replace("  ", " ")
    # if the name is too long put the initials
    if len(nombre) + len(apellidos) > options["parsing_data"]["L_MAXNAME"]:
        names = nombre.split(" ")
        nombre = ""
        for name in names:
            if len(name) > 0:
                nombre = nombre + name[0]
    # if it is still too long just trim the surnames
    if len(nombre) + len(apellidos) > options["parsing_data"]["L_MAXNAME"]:
        #len(nombre) + len(apellido) <= options[][], so len(apellidos) <= options[][] - len(nombre)
        options["parsing_data"]["L_MAXNAME"]
        apellidos = apellidos[:options["parsing_data"]["L_MAXNAME"] - len(nombre)]

    return {"nombre": nombre, "apellidos": apellidos, "year": year, "club": club, "tiempo": tiempo}

# hay bugs si no es una de las posibles pruebas especificadas
# posiblemente si son relevos tb
# hay bugs cuando el pdf lee espacios de mas (obviamente), pero que se le va a hacer




