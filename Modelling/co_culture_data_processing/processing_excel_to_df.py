import numpy as np

def convert_time(seconds, mode="hour"):
    ''' This should not be used for very short time intervalls. 
        Optimized for 30, 60, ... minutes/ 0.5, 1, 1.5 hours.
        It converts seconds into minutes or hours.
        
        seconds: number of seconds to convert
        mode: either "hour" or "minute", default is "hour"'''
    
    if mode == "minute":
        minutes = round(seconds/60)
        return minutes
        
    elif mode == "hour":
        minutes = round(seconds/60)
        hours = minutes/60
        return hours
    
    else:
        print("Wrong mode, choose 'minute' or 'hour'")
        
def convert_time_in_df(df, mod="hour"):
    ''' The name of the time row must be "Time [s]".
        This function adds a row to your dataframe. 
        It changes the dataframe you put in as input.
        
        df: the dataframe must have a row named "Time [s]
        mod: either "minute" or "hour", default is "hour"'''
    
    time = df.loc[['Time [s]']]
    
    col_name_time = []
    for col_name in time:
        col_name_time.append(col_name)
    
    new_times = []
    for col_name in col_name_time:
        time_sec = time.iloc[0][col_name]
        converted_time = convert_time(time_sec, mode=mod)
        new_times.append(converted_time)
    
    if mod == "minute":
        df.loc["Time [min]"] = new_times
        return df
    elif mod == "hour":
        df.loc["Time [h]"] = new_times
        return df
    else: 
        print("Wrong mod, choose 'minute' or 'hour'")
        
def get_control_value(df, control):
    '''This function takes the control columns from the plate to calculate a control value to normalize the 
    sample values. If something has grown in the control, the part under double checking checks for rows that 
    should not be used to calculate the control.
    
    df: your dataframe
    list_with_control_positions: insert a list with the plate position(s) where you have your controls'''
    
    collect_control_values = []
    for row_name in control:
        row_values = df.loc[row_name]
        for value in row_values:
            collect_control_values.append(value)
    control_value_array = np.array(collect_control_values)
    mean_before_check = np.mean(control_value_array)
    std_before_check = np.mean(control_value_array)
    
    if std_before_check >= (mean_before_check)/2:
        collect_control_values_new = []
        for row_name in control:
            row_values = df.loc[row_name]
            if row_values[len(df.iloc[1])-1] > mean_before_check:
                continue
            else: 
                for value in row_values:
                    collect_control_values_new.append(value)
        control_value_array_new = np.array(collect_control_values_new)
        control_summary = [np.mean(control_value_array_new), np.std(control_value_array_new)]
    else:
        control_summary = [np.mean(control_value_array), np.std(control_value_array)]
    return control_summary

def normalize(df, control): 
    '''This function normalizes the values in the dataframe by subtracting a control value from them.
    
    df: dataframe
    control: int or float that will be substracted from the values in the dataframe'''
    
    rownames = df.index
    rownames_to_change = []
    for name in rownames:
        if name.startswith("T"):
            continue
        else:
            rownames_to_change.append(name)

    for i in range(1, len(df.iloc[1])+1):
        for name in rownames_to_change:
            old_value = df.loc[name,i]
            if old_value == "OVER":
                continue
            else:
                new_value = old_value - control
                df.loc[name,i] = new_value
                
def calculate_mean_and_std(name_dict_nr, df):
    '''This function takes a dictionary with dataframe rownames assigned to letters and uses it to calculate mean
    and std with the corresponding values from the dataframe.
    
    name_dict_nr: dictionary with rownames assigned to a letter; e.g. "B": ["B2", "B3", "B4"]
    df: dataframe'''
    
    dict_for_final = {}

    for letter in name_dict_nr:
        means = []
        std = []

        for i in range(1,len(df.columns)+1):
            list_of_rownames = name_dict_nr[letter]
            list_of_values = []
            for name in list_of_rownames:
                if df[i].loc[name] == "OVER":
                    list_of_values.append("NaN")
                else:
                    list_of_values.append(df[i].loc[name])
            if "NaN" in list_of_values:
                break
            else:
                value_array = np.array(list_of_values)

                means.append(np.mean(value_array))
                std.append(np.std(value_array))
            
        dict_for_final[letter+" mean"] = means
        dict_for_final[letter+" std"] = std
    
    return dict_for_final