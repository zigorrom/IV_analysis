import os
import sys

import sqlite3

import pandas as pd


LAYOUT_FOLDER = "layouts"
DB_FILENAME = "chip_registry_db.db"

WAFERS_TABLE = "wafers"
WAFER_NAME_COL = "wafer_name"
WAFER_DOPING_COL = "wafer_doping"
WAFER_INFO_COL = "wafer_info"


CHIPS_TABLE = "chips"
CHIP_NUMBER_COL = "chip_no"
CHIP_TYPE_COL = "chip_type"
CHIP_WAFER_NAME = WAFER_NAME_COL

TRANSISTORS_TABLE = "transistors"
TRANSISTOR_NUMBER_COL = "transistor_number"
TRANSISTOR_CHIP_CUMBER = CHIP_NUMBER_COL
TRANSISTOR_WAFER_NAME = WAFER_NAME_COL
TRANSISTOR_WIDTH_COL = "width"
TRANSISTOR_LENGTH_COL = "length"
TRANSISTOR_DOPING = WAFER_DOPING_COL

program_path = os.path.dirname(os.path.realpath(__file__))
chip_registry_db_file = os.path.join(program_path, LAYOUT_FOLDER,DB_FILENAME)

def perform_insert_operation(connection, request, *params):
    try:
        c = connection.cursor()
        c.execute(request, params)
        return True
    except sqlite3.IntegrityError:
        print('ERROR: ID already exists in PRIMARY KEY column')
        return False

def add_wafer(connection, name, doping, info):
    request = "INSERT INTO {tn} VALUES (?,?,?);".format(tn = WAFERS_TABLE) 
    return perform_insert_operation(connection, request, name, doping, info)

def add_chip(connection, wafer_name, chip_number, chip_type):
    request = "INSERT INTO {tn} VALUES (?,?,?);".format(tn = CHIPS_TABLE)
    return perform_insert_operation(connection, request, chip_number, chip_type, wafer_name)

def add_transistor(connection, wafer_name, chip_number, transistor_number, width, length, doping):
    request = "INSERT INTO {tn} VALUES (?,?,?,?,?,?);".format(tn = TRANSISTORS_TABLE)
    return perform_insert_operation(connection, request, transistor_number, chip_number, wafer_name, width, length, doping )


if __name__ == "__main__":

    conn = sqlite3.connect(chip_registry_db_file)
    wafer_name = "soi00"
    chip_name = "chip01"
    chip_number = 1
    chip_type = "chip2"
    add_wafer(conn, wafer_name, "ppp", "test")
    add_chip(conn, chip_name, chip_number, chip_type)
    

    chip2_lay = os.path.join(program_path, LAYOUT_FOLDER,"chip2.lay")
    chip_data = pd.DataFrame.from_csv(chip2_lay ,sep="\t", index_col = None)
    #for index,row in transfer_curves.iterrows()
    for index, row in chip_data.iterrows():
        add_transistor(conn, wafer_name, chip_number, int(row["No"]), float(row["Width"]), float(row["Length"]), "ppp")
    
                       
                       
    conn.commit()
    conn.close()    



