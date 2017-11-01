import easygui
import pandas as pd
# from utils import ui, avature
from utils import ui
from utils import avature
import os
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

# TODO Finalize support for multiple field types
# available_filters = []
# with open("utils/filters.txt", "r") as f:
#     af = f.readlines()
#     for fil in af:
#         available_filters.append(fil.strip())

available_filters = ['Keywords']


category_term = ui.map_headers(relevant_headers, available_filters)
dupcheck_data = dupcheck_data.replace(['null'], '')
dupcheck_data = dupcheck_data.fillna('')


# Select Save Location for Results
results_save_path = ui.select_save_loc()

# From relevant header, create dictionary with search terms

lead_holder_dict = {}

for index, row in dupcheck_data.iterrows():
    person_data_dict = {}
    for relevant_header, header_mapping in category_term.items():
        rh_value = row[relevant_header]  # Retrieve cell value
        # For common LinkedIn searching
        for s in ['/in/', '/pub/', '/profile/']:
            if s in rh_value:
                rh_value = rh_value.split(s)[1]
                break

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


# Initialize Dup Checker
dup_checker = avature.DupDriver(driver_path=r"C:\Users\estasney\PycharmProjects\Commons\utils\chromedriver.exe")
# Create dict to hold results
dup_results_dict = {}
# Open, login, etc
dup_checker.begin_session()
for k, v in lead_holder_dict.items():
    data_to_dupchecker = v

    # Returns FALSE if no matches, string of search url if matches found

    dup_result = dup_checker.dup_check_avature(data_to_dupchecker)

    # Simple index lookup

    dup_results_dict[k] = dup_result


# For profiles, without result create profiles in Avature

profiles_to_create = {}

for k, v in dup_results_dict.items():
    if v is False:
        profiles_to_create[k] = dupcheck_data.iloc[k].to_dict()


for create_profile in profiles_to_create.values():
    first_name = create_profile['Name']

    last_name = create_profile['Last Name_x']
    website = create_profile['LinkedIn url (1)']
    pdf_filename = create_profile['PDF Filename']
    pdf_filename = os.path.join(r"C:\Users\estasney\Downloads", (pdf_filename + ".pdf"))
    position_title = create_profile['Title']
    company_name = create_profile['Company Name']
    email_one = create_profile['Email 1']
    if email_one == '':
        continue
    zip_code = create_profile['Zip Code']



    dup_checker.click_create_button()
    dup_checker.click_create_person()
    dup_checker.select_create_method()
    dup_checker.create_first_name(first_name)
    dup_checker.create_last_name(last_name)
    dup_checker.create_current_company(company_name)
    dup_checker.create_position_title(position_title)
    dup_checker.create_click_select_source_dropdown()
    dup_checker.create_email(email_one)
    dup_checker.create_save_button(first_name, last_name)
    dup_checker.profile_enter_talent_hub_specialist()
    dup_checker.contact_info_click_plus()
    dup_checker.contact_info_enter_field('Website', website)
    dup_checker.contact_info_click_plus()
    dup_checker.contact_info_enter_field('Street address')

# Merge results dict with dup_check data
df_results = pd.DataFrame.from_dict(dup_results_dict, orient='index')
dupcheck_data['Results'] = df_results
easygui.msgbox(msg="The check is complete. Press OK to exit.")
dup_checker.teardown_driver()
results_save_path_ext = os.path.splitext(results_save_path)[1]
if results_save_path_ext == 'csv':
    dupcheck_data.to_csv(results_save_path)
elif results_save_path_ext == 'xlsx':
    dupcheck_data.to_excel(results_save_path)
else:
    print("Error Saving... copied to clipboard")
    dupcheck_data.to_clipboard()