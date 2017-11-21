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


def correct_current_semi_log_scale_new(current):
    abs_current_values = np.abs(current)
    log_currents = np.log10(abs_current_values)
    min_val_index = np.argmin(log_currents)
    min_log_current = log_currents[min_val_index]

    # add averaging for better maximum estimation
    left_maximum = np.max(log_currents[:min_val_index])
    right_maximum = np.max(log_currents[min_val_index:])
    if left_maximum < right_maximum:
        pass
    else:
        pass


def correct_current_semi_log_scale(current):
    abs_current_values = np.abs(current)
    npoints_aver = 3
    
    log_currents = np.log10(abs_current_values)
    min_val_index = np.argmin(log_currents)
    min_log_current = log_currents[min_val_index]
    
<<<<<<< HEAD
    result_log_currents = np.copy(log_currents)
    if left_avg < right_avg:
        current_left_from_zero = current[min_val_index-1]
        current_right_from_zero = current[min_val_index]
=======
    max_val_left = np.max(log_currents[:min_val_index])
    max_val_right = np.max(log_currents[min_val_index:])

    if max_val_left < max_val_right:
        max_difference2x = 2*(max_val_left - min_log_current)
        log_currents[:min_val_index] = 2 * max_val_left - log_currents[:min_val_index]
        log_currents[min_val_index:] = max_difference2x + log_currents[min_val_index:] 
        log_currents = log_currents - max_difference2x
    else:
        raise NotImplementedError()
    result_current = np.power(10, log_currents)

    return result_current

#def correct_current_semi_log_scale(current):
#    abs_current_values = np.abs(current)
#    npoints_aver = 3
#    left_avg = np.average(abs_current_values[:npoints_aver])
#    right_avg = np.average(abs_current_values[-npoints_aver:])

#    log_currents = np.log10(abs_current_values)
#    min_val_index = np.argmin(log_currents)
#    min_log_current = log_currents[min_val_index]
    
    

#    result_log_currents = np.copy(log_currents)
#    if left_avg < right_avg:
#        current_left_from_zero = current[min_val_index-1]
#        current_right_from_zero = current[min_val_index]
>>>>>>> origin/master

#        result_log_currents[:min_val_index] =  2*min_log_current - log_currents[:min_val_index]
#    else:
#        min_val_index += 1
#        current_left_from_zero = current[min_val_index-1]
#        current_right_from_zero = current[min_val_index]
#        result_log_currents[min_val_index:] =  2*min_log_current - log_currents[min_val_index:]

#    result_currents = np.power(10, result_log_currents)
#    return result_currents

def correct_current_lin_scale(current):
    max_current = currents.max()
    return (currents-max_current).abs()

def calculate_subthreshold_swing(currents, voltage_step):
    try:
        log_currents = np.log10(currents)
        voltage_step = abs(voltage_step)
        slope = signal.savgol_filter(log_currents, 21, 2, 1, voltage_step)
        max_slope_idx = np.argmax(slope)
        return slope[max_slope_idx]
    except:
        print("Error when calculating subthreshold swing")
        return None


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
    
    transfer_curves = measurement_data[measurement_data["Independent Var"] == "gate"]
    
    overdrive_voltage_for_tlm = overdrive_voltage
    analysis_data_columns = ["Filename", 
                             "Transistor No", 
                             "Width", 
                             "Length", 
                             "Treshold", 
                             #"Overdrive", 
                             #"Current@overdrive", 
                             #"Resistance@overdrive", 
                             "Drain Voltage"]
    analysis_data_frame = pd.DataFrame(columns = analysis_data_columns )


    for index,row in transfer_curves.iterrows(): #linear_transfer_curves.iterrows():
        try:
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
            
            #currents = correct_current_lin_scale(currents)
            currents = correct_current_semi_log_scale(currents)
            subthreshold_swing =  calculate_subthreshold_swing(currents, abs(voltages[1] - voltages[0]))
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
    
            #current_at_overdrive = float(overd_transfer_curve(overdrive_voltage_for_tlm))
            #resistance_at_overdrive = math.fabs(drain_voltage_value/current_at_overdrive)
            
            #current_at_voltage = float(overd_transfer_curve(max_transcond_voltage))
            #resistance_at_voltage = math.fabs(drain_voltage_value/current_at_voltage)

            pd.DataFrame.to_csv(transfer_data, os.path.join(result_folder, fname), index = False)
            # "Filename", "Transistor No", "Width", "Length", "Treshold", "Overdrive", "Current@overdrive", "Resistance@overdrive"
            #if analysis_data_frame is None:
            #    analysis_data_frame = pd.DataFrame.from_dict({"Filename":[fname], "Transistor No":[number],"Width": [width], "Length" : [length], "Treshold" : [treshold_voltage], "Overdrive" : [overdrive_voltage_for_tlm], "Current@overdrive" : [current_at_overdrive],"Resistance@overdrive" : [resistance_at_overdrive]})
            #else:
            df = pd.DataFrame.from_dict(
                {"Filename":[fname], 
                 "Transistor No":[number],
                 "Width": [width], 
                 "Length" : [length], 
                 "Treshold" : [treshold_voltage], 
                 #"Overdrive" : [overdrive_voltage_for_tlm], 
                 #"Id@overdrive" : [current_at_overdrive],
                 #"Rs@overdrive" : [resistance_at_overdrive], 
                 "Drain Voltage": [drain_voltage_value], 
                 "gm_max": [max_transcond], 
                 "Vg-Vth@gm_max":[max_transcond_voltage- treshold_voltage], 
                 "SS(V/dec)": [subthreshold_swing]
                 #"Id@gm_max": [current_at_voltage], 
                 #"Rs@gm_max":[resistance_at_voltage]
                 })
            #df.columns = analysis_data_columns
            

            for i, vov in enumerate(overdrive_voltage):
                try:
                    overdrive_col_name = "Overdrive_{0}".format(i)
                    current_at_overdrive_i_col = "Id@overdrive_{0}".format(i)
                    resistance_at_overdrive_i_col = "Rs@overdrive_{0}".format(i)
                    current_at_overdrive_i = float(overd_transfer_curve(vov))
                    resistance_at_overdrive_i = math.fabs(drain_voltage_value/current_at_overdrive_i)
                    df[overdrive_col_name] = [vov]
                    df[current_at_overdrive_i_col] = [current_at_overdrive_i]
                    df[resistance_at_overdrive_i_col] = [resistance_at_overdrive_i]

                except Exception as e:
                    print("EXCEPTION OCCURED WHEN CALCULATING VALUES FOR OVERDRIVE VOLTAGE {0} V".format(vov))
                    print(e)
                    print("*"*10)


            analysis_data_frame = analysis_data_frame.append(df, ignore_index=True)


        except Exception as e:
            print("EXCEPTION OCCURED WHILE PROCESSING")
            print(data_file_path)
            print('*'*10)
            print(e)
            print('*'*10)


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


    # add possibility of several overdrive voltages
    parser.add_argument('-vov', metavar='overdrive voltage', type=float, nargs='*', default = [],
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
    


    