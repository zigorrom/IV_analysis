import os
import ntpath
import re
import pandas as pd

def parse_measurement_filename(filename):
    filename = ntpath.basename(filename)
    pattern = re.compile("^[tT](?P<number>[0-9]*)[-_]IV(?P<type>(lg|bg|ds))[-_](?P<info>.*?)\.dat$") #(?P<transistor>[0-9]?)[-_](?P<wafer>.*?)[-_](?P<chip>.*?)[-_]
      
    match = pattern.match(filename)
    if not match:
        return None

    d = match.groupdict()
    experiment_name = filename
    transistor_no = d.get("number", None)
    chatacteristic = d.get("type",None)
    info = d.get("info",None)
        
    return (experiment_name, transistor_no, chatacteristic, info)

#def get_len_width_from_val(value):
#    val = float(value)
#    if val > 10:
#        return val/1000


working_folder = "C:\\Users\\i.zadorozhnyi\\Desktop\\Needles2\\"
measurement_data_file = "MeasurmentData_soi17l_chip13_needles.dat"

measurement_data_path = os.path.join(working_folder, measurement_data_file)

initial_current = 1e-08

measurement_data = pd.DataFrame.from_csv(measurement_data_path, index_col = None)
chip_data = pd.DataFrame.from_csv(os.path.join(working_folder,"chip2.lay"),sep="\t", index_col = None)

measurement_data_cols = list(measurement_data)
chip_data_cols = list(chip_data)

col = measurement_data["Independent Var"]

transfer_curves = measurement_data[measurement_data["Independent Var"] == "gate"]
linear_transfer_curves = transfer_curves[transfer_curves["Dependent Voltage"] == -0.1]
saturation_transfer_curves = transfer_curves[transfer_curves["Dependent Voltage"] == -1.0]

for index,row in linear_transfer_curves.iterrows():
    fname = row["Filename"]
    (experiment_name, transistor_no, chatacteristic, info) = parse_measurement_filename(fname)
    number = int(transistor_no)
    transistor = chip_data[chip_data["No"] == number]
    width = float(transistor["Width"])
    length = float(transistor["Length"])
    print(number)
    print("\t W = {0}; L = {1};".format(width,length))
