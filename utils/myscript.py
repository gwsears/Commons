import easygui
import pandas as pd
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
user_path = os.path.join("C:\\Users", os.getlogin())
chromedriver_path = os.path.join(user_path, r"PycharmProjects\Commons\utils\chromedriver.exe")
dup_checker = avature.DupDriver(driver_path=chromedriver_path)
# Create dict to hold results
dup_results_dict = {}
# Open, login, etc
dup_checker.begin_session()


dupcheck_data = dupcheck_data.drop_duplicates()

for k, v in lead_holder_dict.items():
    data_to_dupchecker = v

    # Returns FALSE if no matches, string of search url if matches found

    dup_result = dup_checker.dup_check(data_to_dupchecker)

    # Simple index lookup

    dup_results_dict[k] = dup_result


# Add the results as new column to original DataFrame
dupcheck_data['Results'] = dup_results_dict.values()

# Where are the PDF's located?
pdf_files_dir = ui.prompt_user_downloads()

# This won't include the Results column
relevant_headers_create = ui.select_relevant_headers(current_headers, dup_check=False)

# These are options the user may choose
# Every relevant header is mapped to one of these
available_filters_create = ['First Name', 'Last Name', 'Website', 'PDF Filename', 'Position Title', 'Company Name',
                            'Email', 'Zip Code']

# These are options that support lists as values
create_supports_multiple = ['Website', 'Email']

# Asking the user to map the headers
# Returns dict in col : data_type format
col_data_type_create = ui.map_headers(relevant_headers_create, available_filters_create, dup_check=False)

# It would be useful to have data_type : col mapping as well
data_type_col_create = {}
for k, v in col_data_type_create.items():
    # If key not found, return list
    # Recall we are swapping k, v
    lookup = data_type_col_create.get(v, [])
    lookup.append(k)
    data_type_col_create[v] = lookup


# Create new DataFrame of Leads
# Remove potential duplicates
no_dups = dupcheck_data[(dupcheck_data['Results'] == False)]

# We also drop any duplicates
no_dups = no_dups.drop_duplicates()

# All should have at least one email
# Remove rows without emails, using our reverse mapping from above
email_columns = data_type_col_create['Email']
for i, row in no_dups.iterrows():
    will_drop = True
    if isinstance(email_columns, list):
        for ec in email_columns:
            if row[ec] != '':
                will_drop = False
    elif isinstance(email_columns, str):
        if row[email_columns] != '':
            will_drop = False
    if will_drop:
        no_dups.drop([i], inplace=True)


creation_dict_holder = []
for index, row in no_dups.iterrows():
    person_creation_dict = {}
    for relevant_header, header_mapping in col_data_type_create.items():
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


for i in creation_dict_holder:
    dup_checker.create_profile(creation_dict_holder[i])

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