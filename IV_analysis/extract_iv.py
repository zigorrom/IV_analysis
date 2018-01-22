import os
import pandas as pd
import iv_analysis_library as ivlib

gate_variable = "gate"
drain_variable = "drain"

time_format = "%Y-%m-%d_%H-%M-%S"

VDS_COL = "V\-(DS)"
VGS_COL = "V\-(GS)"
ID_FORMAT = "I\-(D)@{0}"

OUTPUT_CURVES_FOLDER = "Output"
TRANSFER_CURVES_FOLDER = "Transfer"


def perform_analysis(measurement_filename, working_folder = ""):
    print("PROCESSING FILE: {0}".format(measurement_filename))
    result_folder = os.path.join(working_folder, ivlib.RESULT_FOLDER)
    os.makedirs(result_folder, exist_ok=True)
    transfer_folder = os.path.join(result_folder, TRANSFER_CURVES_FOLDER)
    output_folder = os.path.join(result_folder, OUTPUT_CURVES_FOLDER)
    os.makedirs(transfer_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    measurement_data = pd.DataFrame.from_csv(os.path.join(working_folder,measurement_filename), index_col = None)
    measurement_data_cols = list(measurement_data)
    filename_col, timestamp_col, independent_var_col, dependent_var_col, dependent_volt_col = measurement_data_cols
    #measurement_data_cols = list(measurement_data)

    transfer_curves = measurement_data[measurement_data[independent_var_col] == gate_variable]
    output_curves = measurement_data[measurement_data[independent_var_col] == drain_variable]
    
    #convert timestamp data to pandas format
    measurement_data[timestamp_col] = pd.to_datetime(measurement_data[timestamp_col], format = time_format)

    unique_drain_voltages = transfer_curves[dependent_volt_col].unique()
    unique_gate_voltages = output_curves[dependent_volt_col].unique()
    
    print("Uniquie drain voltages:")
    print(unique_drain_voltages)

    print("Uniquie gate voltages:")
    print(unique_gate_voltages)

    #print("Times")
    #print(measurement_data[timestamp_col])

    
    #export output curves ar certain gate voltage
    for gate_voltage in unique_gate_voltages:
        print("ANALYZING GATE VOLTAGE: {0}".format(gate_voltage))
        current_gate_volt_data = output_curves[output_curves[dependent_volt_col] == gate_voltage]
        current_gate_volt_data.sort_values(timestamp_col)
        #print(current_gate_volt_data[timestamp_col])


        ResultOutputCurvesDataFrame = None # pd.DataFrame.from_dict()
        ResultOutputConductanceDataFrame = None

        #iterate over measurements 
        print("ITERATING OVER ROWS")
        for index,row in current_gate_volt_data.iterrows():
            try:
                filename = os.path.join(working_folder,row[filename_col])
                timestamp = row[timestamp_col]
                print(filename)
                #open data file
                output_curve_data = pd.DataFrame.from_csv(filename, index_col = None)
                drain_voltage_col, drain_current_col, drain_timestamp_col, gate_voltage_col, gate_current_col, gate_timestamp_col  = list(output_curve_data)
                #pd.DataFrame.from_csv(
                #print(output_curve_data)

                #[:-1] remove last point

                drain_voltage_values = output_curve_data[drain_voltage_col][:-1]

                if ResultOutputCurvesDataFrame is None:
                    ResultOutputCurvesDataFrame = pd.DataFrame.from_dict(
                        {
                            VDS_COL: drain_voltage_values
                        })

                if ResultOutputConductanceDataFrame is None:
                    ResultOutputConductanceDataFrame = pd.DataFrame.from_dict(
                        {
                            VDS_COL: drain_voltage_values
                        })

                current_values = output_curve_data[drain_current_col][:-1]
                converted_current = current_values  - current_values[0]
                #print(converted_current)
                conductance = converted_current / drain_voltage_values
                ResultOutputCurvesDataFrame[ID_FORMAT.format(timestamp)] = converted_current         
                ResultOutputConductanceDataFrame[ID_FORMAT.format(timestamp)] = conductance
            except Exception as e:
                print("ERROR WHILE PROCESSING OUTPUT CURVES")
                print(str(e))
                print("*"*10)

            
        #print(ResultOutputCurvesDataFrame)
        current_result_filepath = os.path.join(output_folder, ".".join(["Current@Vg={0}".format(gate_voltage).replace(".","_").replace(",","_"), "dat"]))
        conductance_result_filepath = os.path.join(output_folder, ".".join(["Conductance@Vg={0}".format(gate_voltage).replace(".","_").replace(",","_"), "dat"]))
        print(current_result_filepath)
        print(conductance_result_filepath)
        pd.DataFrame.to_csv(ResultOutputCurvesDataFrame, current_result_filepath, index = False)
        pd.DataFrame.to_csv(ResultOutputConductanceDataFrame, conductance_result_filepath, index = False)

    #export output curves ar certain gate voltage
    for drain_voltage in unique_drain_voltages:
        print("ANALYZING GATE VOLTAGE: {0}".format(drain_voltage))
        current_drain_volt_data = transfer_curves[transfer_curves[dependent_volt_col] == drain_voltage]
        current_drain_volt_data.sort_values(timestamp_col)
        #print(current_gate_volt_data[timestamp_col])


        ResultTransferCurvesDataFrame = None # pd.DataFrame.from_dict()
        ResultTransferConductanceDataFrame = None

        #iterate over measurements 
        print("ITERATING OVER ROWS")
        for index,row in current_drain_volt_data.iterrows():
            try:
                filename = os.path.join(working_folder,row[filename_col])
                timestamp = row[timestamp_col]
                print(filename)
                #open data file
                transfer_curve_data = pd.DataFrame.from_csv(filename, index_col = None)
                gate_voltage_col, gate_current_col, gate_timestamp_col,drain_voltage_col, drain_current_col, drain_timestamp_col  = list(transfer_curve_data)
                #pd.DataFrame.from_csv(
                #print(output_curve_data)

                #[:-1] remove last point

                gate_voltage_values = transfer_curve_data[gate_voltage_col][:-1]
                if ResultTransferCurvesDataFrame is None:
                    ResultTransferCurvesDataFrame = pd.DataFrame.from_dict(
                        {
                            VGS_COL: gate_voltage_values
                        })

                if ResultTransferConductanceDataFrame is None:
                    ResultTransferConductanceDataFrame = pd.DataFrame.from_dict(
                        {
                            VGS_COL: gate_voltage_values
                        })
                
                current_values = transfer_curve_data[drain_current_col][:-1]
                converted_current = current_values  - current_values[0]
                #print(converted_current)
                conductance = converted_current / drain_voltage
                ResultTransferCurvesDataFrame[ID_FORMAT.format(timestamp)] = converted_current         
                ResultTransferConductanceDataFrame[ID_FORMAT.format(timestamp)] = conductance
            except Exception as e:
                print("ERROR WHILE PROCESSING TRANSFER CURVES")
                print(str(e))
                print("*"*10)

        #print(ResultOutputCurvesDataFrame)
        current_result_filepath = os.path.join(transfer_folder, ".".join(["Current@Vds={0}".format(drain_voltage).replace(".","_").replace(",","_"), "dat"]))
        conductance_result_filepath = os.path.join(transfer_folder, ".".join(["Conductance@Vds={0}".format(drain_voltage).replace(".","_").replace(",","_"), "dat"]))
        print(current_result_filepath)
        print(conductance_result_filepath)
        pd.DataFrame.to_csv(ResultTransferCurvesDataFrame, current_result_filepath, index = False)
        pd.DataFrame.to_csv(ResultTransferConductanceDataFrame, conductance_result_filepath, index = False)  

    ivlib.open_folder(result_folder)


def analyze_files_in_folder(folder_name):
    measurement_data_filename = ivlib.__search_for_new_style_measurement_data_file(folder_name)
    if isinstance(measurement_data_filename, str):
        perform_analysis(measurement_data_filename, folder_name)
    elif isinstance(measurement_data_filename, list):
        for fn in measurement_data_filename:
            perform_analysis(fn, folder_name)
    else:
        print("NO FILES FOUND")

def scan_folder_tree(parent_folder):
    for root, dirs, files in os.walk(parent_folder, topdown=False):
        for name in dirs:
            try:
                print("ANALYZING FOLDER:")
                folder_name = os.path.join(root, name)
                print(folder_name)
                print("*"*10)
                analyze_files_in_folder(folder_name)
            except Exception as exc:
                print("ERROR OCCURRED HANDLING FOLDER: {}".format(name))

if __name__ == "__main__":
    folder_name = os.getcwd()
    #analyze_files_in_folder(folder_name)
    print(scan_folder_tree(folder_name))

