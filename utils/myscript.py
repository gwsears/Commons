from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import pandas as pd
import csv
import easygui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import math
import os
from utils import ui, avature

"""
EXPECTS...
First Name
Last Name
Email
LinkedIn
"""



# TODO Welcome Screen

# Select File to Check
data_in_path = ui.select_set()
dupcheck_data = ui.read_set(data_in_path)
if dupcheck_data is False:
    print("Error opening file, check encoding")
    quit()

# Map Headers via User prompt
current_headers = ui.detect_headers(dupcheck_data)
rename_scheme = ui.prompt_header_match(current_headers)
dupcheck_data = dupcheck_data.rename(columns=rename_scheme)

dupcheck_data = dupcheck_data.fillna('')

# Select Save Location for Results
results_save_path = ui.select_save_loc()

# Create LeadPerson objects and append to lead_person_holder

lead_holder = []

for index, row in dupcheck_data.iterrows():
    data_as_dict = {}
    data_as_dict['First Name'] = row['First Name']
    data_as_dict['Last Name'] = row['Last Name']
    data_as_dict['Email'] = row['Email']
    data_as_dict['LinkedIn'] = row['LinkedIn']

    new_lead = avature.LeadPerson(*['LinkedIn'], **data_as_dict)
    lead_holder.append(new_lead)

dup_checker = avature.DupDriver(driver_path=r"C:\Users\estasney\Documents\ChromeDriver\chromedriver.exe")

for l in lead_holder:
    dup_key = l.dup_key
    dup_checker.append_data(dup_key)


# Start Checking

dup_checker.begin_session()
dup_checker.dup_check_batch()



easygui.msgbox(msg="The check is complete. Press OK to exit.")
avature_driver.quit()



