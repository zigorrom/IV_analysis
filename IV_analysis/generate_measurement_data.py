import os
import datetime
import fnmatch
import ntpath
import pandas as pd
import re

file_pattern =re.compile("^[tT](?P<number>[0-9]*)[-_]IV(?P<type>(lg|bg|ds))[-_](?P<info>.*?)\.dat$") #(?P<transistor>[0-9]?)[-_](?P<wafer>.*?)[-_](?P<chip>.*?)[-_] 

def parse_measurement_filename(filename):
    filename = ntpath.basename(filename)
    pattern = file_pattern
      
    match = pattern.match(filename)
    if not match:
        return None

    d = match.groupdict()
    experiment_name = filename
    transistor_no = d.get("number", None)
    chatacteristic = d.get("type",None)
    info = d.get("info",None)
        
    return (experiment_name, transistor_no, chatacteristic, info)

def generate_measurement_data(folder):
    pattern = "[tT]*.dat"
    files = os.listdir(folder)
    matches = fnmatch.filter(files, pattern)
    if not matches:
        return 

    
    filename_format = "{0}_{1}_{2}.dat"
    measurement_data_filename = os.path.join(folder,"MeasurmentData_generated_{0}.dat".format(datetime.date.today()))


    need_to_write_header = lambda: not os.path.isfile(measurement_data_filename)
    filename_option = "Filename"
    timestamp_option = "Timestamp"
    indep_var_option = "Independent Var"
    dep_var_option = "Dependent Var"
    dep_volt_option = "Dependent Voltage"
    
    #drain_voltage_column = "Drain voltage"
    #gate_voltage_column = "Gate voltage"

    for file in matches:
        
        experiment_name,  transistor_no, characteristic, info  = parse_measurement_filename(file)
        dependent_voltage = None
        independent_var = None
        dependent_var = None

        #filename = ntpath.basename(os.path.join(folder,file))
        df = pd.DataFrame.from_csv(os.path.join(folder,file), index_col = None)
        if characteristic == "lg" or characteristic == "bg":
            gate_voltage, gate_current, gate_timestamp, drain_voltage, drain_current, drain_timestamp = list(df)
            dependent_voltage = df[drain_voltage][0]
            dependent_var = "drain"
            independent_var = "gate"

            
        elif characteristic == "ds":
            drain_voltage, drain_current, drain_timestamp,gate_voltage, gate_current, gate_timestamp = list(df)
            dependent_voltage = df[gate_voltage][0]
            dependent_var = "gate"
            independent_var = "drain"

        else:
            raise Exception()
        
        measurement_data_dataFrame = pd.DataFrame([[file, 
                                                None,
                                                independent_var,
                                                dependent_var,
                                                dependent_voltage]], index = [0], columns = [filename_option, 
                                                                                             timestamp_option, 
                                                                                             indep_var_option, 
                                                                                             dep_var_option, 
                                                                                             dep_volt_option])

        measurement_data_dataFrame.to_csv(measurement_data_filename, mode= 'a', header=need_to_write_header(), index = False)


if __name__ == "__main__":
    folder = os.getcwd()  # "D:\\PhD\\Measurements\\2017\\SOI#17L\\Chip6\\20171012\\BondedChip\\IV_liquid\\" #
    generate_measurement_data(folder)