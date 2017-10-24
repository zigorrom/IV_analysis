import os
import ntpath
import re
import fnmatch
import math
import argparse
import pandas as pd
import numpy as np



from scipy.interpolate import interp1d, UnivariateSpline
from scipy import optimize
from scipy import signal

LAYOUT_FOLDER = "layouts"
RESULT_FOLDER = "Results"

def parse_measurementdata_filename(filename):
        filename = ntpath.basename(filename)
        pattern = re.compile("MeasurmentData_(?P<wafer>.*?)_(?P<chip>.*?)_(?P<info>.*?)\.dat$")
        
        match = pattern.match(filename)
        if not match:
            return None

        d = match.groupdict()

        experiment_name = filename
        wafer_name = d.get("wafer",None)
        chip_name = d.get("chip",None)
        info = d.get("info", None)
        return (experiment_name, wafer_name,chip_name,info)

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


#working_folder = os.getcwd() #"C:\\Users\\i.zadorozhnyi\\Desktop\\Needles2\\"
###working_folder = "C:\\Users\\Dell\\Desktop\\Needles2\\"

#result_folder = os.path.join(working_folder,"Results")
#os.makedirs(result_folder, exist_ok=True)

#measurement_data_file = "MeasurmentData_soi17l_chip13_needles.dat"

#measurement_data_path = os.path.join(working_folder, measurement_data_file)

#initial_current = 1e-08

#measurement_data = pd.DataFrame.from_csv(measurement_data_path, index_col = None)
#chip_data = pd.DataFrame.from_csv(os.path.join(working_folder,"chip2.lay"),sep="\t", index_col = None)

#measurement_data_cols = list(measurement_data)
#chip_data_cols = list(chip_data)

#col = measurement_data["Independent Var"]

#transfer_curves = measurement_data[measurement_data["Independent Var"] == "gate"]
#linear_transfer_curves = transfer_curves[transfer_curves["Dependent Voltage"] == -0.1]
#saturation_transfer_curves = transfer_curves[transfer_curves["Dependent Voltage"] == -1.0]

#for index,row in transfer_curves.iterrows(): #linear_transfer_curves.iterrows():
#    fname = row["Filename"]
#    (experiment_name, transistor_no, chatacteristic, info) = parse_measurement_filename(fname)
#    number = int(transistor_no)
#    transistor = chip_data[chip_data["No"] == number]
#    width = float(transistor["Width"])
#    length = float(transistor["Length"])
#    print(number)
#    print("\t W = {0}; L = {1};".format(width,length))

#    value_current = initial_current * width / length

#    data_file_path = os.path.join(working_folder, fname)

#    transfer_data = pd.DataFrame.from_csv(data_file_path, index_col = None)
#    #Gate voltage, Gate current, Gate timestamp, Drain voltage, Drain current, Drain timestamp
#    gate_voltage, gate_current, gate_timestamp, drain_voltage, drain_current, drain_timestamp = list(transfer_data)
    
    

#    voltages = transfer_data[gate_voltage]
    
#    currents = transfer_data[drain_current]
#    max_current = currents.max()
#    currents = (currents-max_current).abs()


#    print(value_current)

#    inverse_transfer_curve = interp1d(currents, voltages)

#    treshold_voltage = inverse_transfer_curve(value_current)
    
#    print(treshold_voltage)

#    overdrive_gate_voltage = voltages - treshold_voltage

#    #dy = np.zeros(y.shape,np.float)
#    transconductance  = np.zeros(currents.shape,np.float)
#    transconductance[0:-1] = np.diff(currents)/np.diff(voltages)
#    #transconductance[-1] = (currents[-1] - currents[-2])/(voltages[-1] - voltages[-2]) 
#    #dy[-1] = (y[-1] - y[-2])/(x[-1] - x[-2])
#    #transconductance = UnivariateSpline(voltages, currents).derivative()(voltages)

#    transfer_data[drain_current] = currents
    
#    transfer_data["Overdrive gate voltage"] = overdrive_gate_voltage

#    transfer_data["Transconductance"] = transconductance
    
#    pd.DataFrame.to_csv(transfer_data, os.path.join(result_folder, fname))

#request = 'explorer "{0}"'.format(result_folder)
#print(request)
#os.system(request)

#import PyOriginTools as OR # <-- this module is what you're reading about!
#sheet=OR.Sheet()
#print(sheet.colNames)
#print(sheet.data)

def __search_for_new_style_measurement_data_file(folder):
    print("SEARCHING FOT MEASUREMENT DATA FILE IN:\n\r{0}".format(folder))
    print("*"*10)
    pattern = "MeasurmentData_*.dat"
    files = os.listdir(folder)
    matches = fnmatch.filter(files, pattern)
    if matches:
        print("FOUND MATCHES:\n\r{0}".format(matches))
        print("*"*10)
    #print(matches)
    return matches

def __search_layout_parameters_in_database(measurment_data_filename):
    pass


def print_experiment_data(experiment_name, wafer_name, chip_name, info):
    print("*" * 10)
    print("EXPERIMENT NAME: {0}".format(experiment_name))
    print("WAFER NAME: {0}".format(wafer_name))
    print("CHIP NAME: {0}".format(chip_name))
    print("INFO: {0}".format(info))
    print("*" * 10)

def new_style_iv_analysis(measurment_filename, wafer_name, chip_name, layout_filename, overdrive_voltage):
    program_path = os.path.dirname(os.path.realpath(__file__))
    #print(program_path)
    if not layout_filename:
        print("layout filename is NOT specified")
        if wafer_name and chip_name:
            print("wafer and chip names are specified - looking for corresponding layout...")
            print_experiment_data("UNKNOWN", wafer_name, chip_name, "UNKNOWN")
            layout_filename = "{0}.lay".format(chip_name)
        else:
            print("wafer and chip names are NOT specified - parsing filename")
            experiment_name, wafer_name, chip_name, info = parse_measurementdata_filename(measurment_filename)
            print_experiment_data(experiment_name, wafer_name, chip_name, info)
            layout_filename = "{0}.lay".format(chip_name)
    else:
        print("layou filename is specified - reading specifications")

    print(layout_filename)

    layout_filepath = os.path.join(program_path, LAYOUT_FOLDER,layout_filename)
    if not os.path.isfile(layout_filepath):
        raise FileNotFoundError("layout file is NOT found")

    print("LAYOUT FILE: {0}".format(layout_filepath)) 

    working_folder = os.path.dirname(measurment_filename)
    result_folder = os.path.join(working_folder, RESULT_FOLDER)
    os.makedirs(result_folder, exist_ok=True)

    chip_data = pd.DataFrame.from_csv(layout_filepath,sep="\t", index_col = None)
    chip_data_cols = list(chip_data)

    initial_current = 1e-08
    measurement_data = pd.DataFrame.from_csv(measurment_filename, index_col = None)
    measurement_data_cols = list(measurement_data)
    
    #col = measurement_data["Independent Var"]

    transfer_curves = measurement_data[measurement_data["Independent Var"] == "gate"]
    #linear_transfer_curves = transfer_curves[transfer_curves["Dependent Voltage"] == -0.1]
    #saturation_transfer_curves = transfer_curves[transfer_curves["Dependent Voltage"] == -1.0]

    overdrive_voltage_for_tlm = overdrive_voltage
    analysis_data_columns = ["Filename", "Transistor No", "Width", "Length", "Treshold", "Overdrive", "Current@overdrive", "Resistance@overdrive", "Drain Voltage"]
    analysis_data_frame = pd.DataFrame(columns = analysis_data_columns )


    for index,row in transfer_curves.iterrows(): #linear_transfer_curves.iterrows():
        fname = row["Filename"]
        (experiment_name, transistor_no, chatacteristic, info) = parse_measurement_filename(fname)
        number = int(transistor_no)
        transistor = chip_data[chip_data["No"] == number]
        width = float(transistor["Width"])
        length = float(transistor["Length"])
        drain_voltage_value = float(row["Dependent Voltage"])
        print(number)
        print("\t W = {0}; L = {1};".format(width,length))

        

        data_file_path = os.path.join(working_folder, fname)

        transfer_data = pd.DataFrame.from_csv(data_file_path, index_col = None)
        #Gate voltage, Gate current, Gate timestamp, Drain voltage, Drain current, Drain timestamp
        gate_voltage, gate_current, gate_timestamp, drain_voltage, drain_current, drain_timestamp = list(transfer_data)
    
        voltages = transfer_data[gate_voltage]
    
        currents = transfer_data[drain_current]
        max_current = currents.max()
        currents = (currents-max_current).abs()

        #constant current treshold calculation
        
        #value_current = initial_current * width / length
        #print(value_current)

        #inverse_transfer_curve = interp1d(currents, voltages)

        #treshold_voltage = inverse_transfer_curve(value_current)
    
        #print(treshold_voltage)

        ## end constant current 

        # derivative treshold voltage calculation

        delta = voltages[1] - voltages[0]
        sign = np.sign(delta)
        delta = abs(delta)

        transconductance = signal.savgol_filter(currents, 21, 2, 1, delta)

        max_transcond_idx = np.argmax(transconductance)
        max_transcond_voltage, max_transcond = (voltages[max_transcond_idx], sign * transconductance[max_transcond_idx])
        #y = f(x0) + f'(x0)(x-x0)
        #x = (y - f(x0) + x0*f'(x0))/f'(x0)
        treshold_voltage = (np.amin(currents) - currents[max_transcond_idx] + max_transcond_voltage * max_transcond)/ max_transcond

        # end derivative treshold calcultation


        transfer_data["Transconductance"] = transconductance





        overdrive_gate_voltage = voltages - treshold_voltage

        transfer_data[drain_current] = currents
    
        transfer_data["Overdrive gate voltage"] = overdrive_gate_voltage
        
        overd_transfer_curve = interp1d(overdrive_gate_voltage, currents)
        current_at_overdrive = float(overd_transfer_curve(overdrive_voltage_for_tlm))
        resistance_at_overdrive = math.fabs(drain_voltage_value/current_at_overdrive)
        
        
       
        

        


        pd.DataFrame.to_csv(transfer_data, os.path.join(result_folder, fname))
        # "Filename", "Transistor No", "Width", "Length", "Treshold", "Overdrive", "Current@overdrive", "Resistance@overdrive"
        #if analysis_data_frame is None:
        #    analysis_data_frame = pd.DataFrame.from_dict({"Filename":[fname], "Transistor No":[number],"Width": [width], "Length" : [length], "Treshold" : [treshold_voltage], "Overdrive" : [overdrive_voltage_for_tlm], "Current@overdrive" : [current_at_overdrive],"Resistance@overdrive" : [resistance_at_overdrive]})
        #else:
        df = pd.DataFrame.from_dict({"Filename":[fname], "Transistor No":[number],"Width": [width], "Length" : [length], "Treshold" : [treshold_voltage], "Overdrive" : [overdrive_voltage_for_tlm], "Current@overdrive" : [current_at_overdrive],"Resistance@overdrive" : [resistance_at_overdrive], "Drain Voltage": drain_voltage_value})
        #df.columns = analysis_data_columns
        analysis_data_frame = analysis_data_frame.append(df, ignore_index=True)

    pd.DataFrame.to_csv(analysis_data_frame, os.path.join(result_folder, "analysis.dat"), index = False)
    open_folder(result_folder)

def old_style_iv_analysis():
    pass

def perform_analysis(f = "", o = False, w = "", c = "", lay = "" , vov = 0, **kwargs):
    
    measurement_data_filename = f
    old_style_measurement = o
    wafer_name = w
    chip_name = c
    layout_filename = lay
    overdrive_voltage = vov
    data_folder = os.getcwd()

    if not measurement_data_filename:
        print("measurement filename is NOT specified - looking for the measurement data file...")
        measurement_data_filename = __search_for_new_style_measurement_data_file(data_folder)
        if not measurement_data_filename:
            raise FileNotFoundError("measurement data file is not found.")
    
    else:
        print("measurement file is specified - performing analysis")
    #if not layout_filename:
    #    layout_filename =  __search_layout_filename(measure)

    if old_style_measurement:
        raise NotImplementedError()
        #old_style_iv_analysis()
    else:
        if isinstance(measurement_data_filename, str):
            new_style_iv_analysis(measurement_data_filename, wafer_name, chip_name, layout_filename, overdrive_voltage)
        elif isinstance(measurement_data_filename, list):
            for fn in measurement_data_filename:
                new_style_iv_analysis(fn, wafer_name, chip_name, layout_filename, overdrive_voltage)

    #if not measurement_data_filename:
    #    print("analysis")

def open_folder(folder):
    request = "explorer \"{0}\"".format(folder)
    print("OPENING FOLDER:\n\r{0}".format(folder))
    os.system(request)


if __name__ == "__main__":
    # options:
    # -n - new_style_measurement_data - default value
    # -a - old_style_measurement_data 
    # -f - measurement_data_filename
    # -w - wafer name
    # -c - chip name
    # -lay - layout filename name
    #
    #

    parser = argparse.ArgumentParser(description='IV analysis')
    parser.add_argument('-f', metavar='f', type=str, nargs='?', default = "",
                    help='the name of measurement data file')
    #parser.add_argument('-n', action = 'store_true', default = True,
    #                help='use new style measurement data')
    parser.add_argument('-o', action = 'store_true', default = False,# type = bool,
                    help='use old style measurement data')
    
    parser.add_argument('-lf', action = 'store_true', default = False,# type = bool,
                    help='open layout folder')
    parser.add_argument('-sf', action = 'store_true', default = False,# type = bool,
                    help='open software folder')

    parser.add_argument('-vov', metavar='overdrive voltage', type=float, nargs='?', default = 0,
                    help='overdrive voltage at which current for analysis would be taken')

    parser.add_argument('-w', metavar='wafer name', type=str, nargs='?', default = "",
                    help='the name of wafer')
    parser.add_argument('-c', metavar='chip name', type=str, nargs='?', default = "",
                    help='the name of chip')
    parser.add_argument('-lay', metavar='chip layout filename', type=str, nargs='?', default = "",
                    help='chip layout filename')



    args = parser.parse_args()
    if args.lf:
        layout_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), LAYOUT_FOLDER)
        open_folder(layout_folder)
    elif args.sf:
        software_folder = os.path.dirname(os.path.realpath(__file__))
        open_folder(software_folder)
    else:
        perform_analysis(**vars(args))
    


    