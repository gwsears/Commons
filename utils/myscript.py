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
relevant_headers = ui.select_relevant_headers(current_headers, dup_check=True)

# TODO Finalize support for multiple field types
# available_filters = []
# with open("utils/filters.txt", "r") as f:
#     af = f.readlines()
#     for fil in af:
#         available_filters.append(fil.strip())

available_filters_dup = ['Keywords']


category_term = ui.map_headers(relevant_headers, available_filters_dup, dup_check=True)
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

dupcheck_data['Results'] = dup_results_dict.values()


# For profiles, without result create profiles in Avature
# Make a list of indexed rows that should be created

profiles_to_create = dupcheck_data[(dupcheck_data['Results'] == False)]

pdf_files_dir = ui.prompt_user_downloads()


# create_profiles_df = pd.read_excel(r"C:\Users\estasney\Downloads\temp_results.xlsx")

current_headers_create = ui.detect_headers(profiles_to_create)
relevant_headers_create = ui.select_relevant_headers(current_headers_create, dup_check=False)
available_filters_create = ['First Name', 'Last Name', 'Website', 'PDF Filename', 'Position Title', 'Company Name',
                            'Email', 'Zip Code']

create_supports_multiple = ['Website', 'Email']

category_term_create = ui.map_headers(relevant_headers_create, available_filters_create, dup_check=False)

creation_dict_holder = []

create_profiles_df = profiles_to_create.replace(['null'], '')
create_profiles_df = create_profiles_df.fillna('')

for index, row in create_profiles_df.iterrows():
    person_creation_dict = {}
    for relevant_header, header_mapping in category_term_create.items():
        rh_value = row[relevant_header]  # Retrieve cell value
        rh_type = header_mapping  # Retrieve value type
        if rh_type == 'PDF Filename':
            pdf_path = ui.file_exists(rh_value, pdf_files_dir)
            if pdf_path is False:
                rh_value = ''
            else:
                rh_value = pdf_path
        creation_data = person_creation_dict.get(rh_type, [])
        if rh_value != '':
            creation_data.append(rh_value)
        else:
            continue
        person_creation_dict[rh_type] = creation_data

    # creation_dict now contains list of Type: Values, with Values being list
    # If len(list) > 1, this will be treated as separate entries

    for k, v in person_creation_dict.items():
        if len(v) == 1:
            nd = v[0]
            person_creation_dict[k] = nd
        elif len(v) > 1:
            if k in create_supports_multiple:
                person_creation_dict[k] = v
            else:
                print("Multiple Data Selected for Unsupported Field.")
                print("Using first entry")
                person_creation_dict[k] = v[0]

    creation_dict_holder.append(person_creation_dict)

for creation_person in creation_dict_holder:
    if creation_person.get('Email', False) is False:
        ci = creation_dict_holder.index(creation_person)
        creation_dict_holder.pop(ci)

dup_checker.values_to_creation_dialog(creation_dict_holder[0])
dup_checker.profile_additional_info(creation_dict_holder[0])

# Pass creation values to dup_checker










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