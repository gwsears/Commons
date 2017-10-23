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


# Select Save Location for Results
results_save_path = ui.select_save_loc()

# Create LeadPerson objects and append to lead_person_holder

lead_person_holder = []

for index, row in dupcheck_data.iterrows():
    first_name = row['First Name']
    last_name = row['Last Name']
    email = row['Email']
    website = row['LinkedIn']



# Start Checking

for lead in lead_person_holder:
    try:
        dup_check_test = dup_check_avature(lead.dupcheckkey)
        dup_key_ran = lead.dupcheckkey
        with open(results_of_check, "a+", encoding='utf-8', newline='') as csv_file:
            outputwriter = csv.writer(csv_file, dialect='excel')
            if dup_check_test is True:
                dup_status = "POSSIBLE DUPLICATE"
                outputwriter.writerow([dup_status, lead.fname, lead.email, lead.oemail, lead.li_url, lead.phone, dup_key_ran])
            elif dup_check_test is False:
                dup_status = "NO DUPLICATES FOUND"
                outputwriter.writerow([dup_status, lead.fname, lead.email, lead.oemail, lead.li_url, lead.phone, dup_key_ran])
    except:

        dup_key_ran = lead.dupcheckkey
        with open(results_of_check, "a+", encoding='utf-8', newline='') as csv_file:
            outputwriter = csv.writer(csv_file, dialect='excel')
            dup_status = "ERROR CHECKING"
            outputwriter.writerow([dup_status, lead.fname, lead.email, lead.oemail, lead.li_url, lead.phone, dup_key_ran])

easygui.msgbox(msg="The check is complete. Press OK to exit.")
avature_driver.quit()



