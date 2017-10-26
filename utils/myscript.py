import easygui
from utils import ui, avature

"""


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
relevant_headers = ui.select_relevant_headers(current_headers)
available_filters = []
with open("utils/filters.txt", "r") as f:
    af = f.readlines()
    for fil in af:
        available_filters.append(fil.strip())
category_term = ui.map_headers(relevant_headers, available_filters)
dupcheck_data = dupcheck_data.fillna('')

# Select Save Location for Results
results_save_path = ui.select_save_loc()

# Create LeadPerson objects and append to lead_person_holder

lead_holder_dict = {}

for index, row in dupcheck_data.iterrows():
    person_data_dict = {}
    for relevant_header, header_mapping in category_term.items():
        rh_value = row[relevant_header]  # Retrieve cell value

        rh_type = header_mapping  # Retrieve value type

        current_data = person_data_dict.get(rh_type, [])

        if rh_value != '':
            current_data.append(rh_value)
        else:
            continue
        person_data_dict[rh_type] = current_data

    # person_data_dict now contains list of Type: Values, with Values being list
    # lists are joined with ' OR ' to be useable

    for k, v in person_data_dict.items():
        if len(v) == 1:
            nd = v[0]
            person_data_dict[k] = nd
        elif len(v) > 1:
            nd = ' OR '.join(v)
            person_data_dict[k] = nd


    lead_holder_dict[index] = person_data_dict



dup_checker = avature.DupDriver(driver_path="chromedriver.exe")

dup_results_dict = {}

dup_checker.begin_session()


for k, v in lead_holder_dict.items():
    data_to_dupchecker = v
    dup_result = dup_checker.dup_check_avature(data_to_dupchecker)
    dup_results_dict[k] = dup_result


# Start Checking




easygui.msgbox(msg="The check is complete. Press OK to exit.")
avature_driver.quit()



