import easygui
import os
import pandas as pd
from bs4 import UnicodeDammit

def get_default_dir():
    username = os.getlogin()
    default_dir = os.path.join(r"C:\Users", username, "dupcheck.csv")
    return default_dir

def select_save_loc():
    default_dir = get_default_dir()
    results_of_check = easygui.filesavebox("Select where to save the Duplicate Checker Results", "Save File",
                                           default=default_dir)
    if ".csv" in results_of_check is False:  # Ensure CSV filetype
        results_of_check = results_of_check + ".csv"
    return results_of_check

def select_set():
    path_in = easygui.fileopenbox(msg="Open the spreadsheet to check")
    return path_in

def detect_file_encoding(file_path):
    fp = open(file_path, "rb")
    file_byte = fp.read()
    fp.close()
    try:
        enc_detector = UnicodeDammit(file_byte)
        dec_encoding = enc_detector.original_encoding
        return dec_encoding
    except Exception as e:
        print(e)
        return False

def read_set(path_in):
    file_ext = os.path.splitext(path_in)[1]
    if file_ext == '.csv':
        open_method = pd.read_csv
    elif file_ext == '.xls' or file_ext == '.xlsx':
        open_method = pd.read_excel
    else:
        open_method = None
        print(file_ext + "Not supported")
        return False
    try:
        dup_check_data = open_method(path_in)
        return dup_check_data
    except UnicodeDecodeError:
        print("Encoding Error Attempting to Detect...")
        detected_encoding = detect_file_encoding(path_in)
        if detected_encoding is False:
            print("Unable to Detect Encoding...")
            return False
        else:
            print("Detected Encoding... " + detected_encoding)
        try:
            dup_check_data = open_method(path_in, encoding=detected_encoding)
            return dup_check_data
        except Exception as e:
            print(e)
            return False


def detect_headers(dup_check_data):  # Expects a DataFrame object
    headers = dup_check_data.columns.values.tolist()
    return headers


def prompt_header_match(headers):
    user_msg = 'The following headers are present in the file. Which ones correspond with the fields below?: \n {}'.format('\n'.join(headers))
    fields = ['First Name', 'Last Name', 'Email', 'LinkedIn']
    fi = easygui.multenterbox(msg=user_msg, fields=fields)
    if all(f in headers for f in fi):
        header_dict = {}
        for unmapped, mapped in zip(fi, fields):
            if unmapped != mapped:
                header_dict[unmapped] = mapped
        return header_dict
    else:
        print("User entries do not match list, try again.")
        return prompt_header_match(headers)

