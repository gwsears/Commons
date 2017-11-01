from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import easygui
import selenium.common.exceptions
import time

class DupDriver(object):
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = None

    def begin_session(self):
        self.setup_driver()
        self.login_avature()
        self.clean_slate()

    def clean_slate(self):
        dirty_slate = True
        while dirty_slate is True:
            try:
                filter_i = self.driver.find_element_by_css_selector("span.conditionViewer a")
                filter_text = filter_i.text
                self.clear_filter(filter_text)
            except selenium.common.exceptions.NoSuchElementException:
                dirty_slate = False
        return

    def clear_filter(self, filter_text):
        try:
            try:
                filter_hyperlink = self.driver.find_element_by_css_selector("a.list_conditionsviewer_ItemValuePopupLink_Link")
                self.cursor_to_element(filter_hyperlink)
                filter_hyperlink.click()
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Remove filter")))
                filter_hyperlink_remove = self.driver.find_element_by_link_text("Remove filter")
                self.cursor_to_element(filter_hyperlink_remove)
                filter_hyperlink_remove.click()
                WebDriverWait(self.driver, 10).until_not(
                    EC.element_to_be_clickable((By.LINK_TEXT, filter_text)))
                self.confirm_filter_clear(filter_text)
            except selenium.common.exceptions.NoSuchElementException:
                pass
        except Exception as e:
            print("Problem Clearing Filter")
            print(e)


    def confirm_filter_clear(self, dup_key):
        try:
            self.driver.find_element_by_css_selector("a.list_conditionsviewer_ItemValuePopupLink_Link")
            self.clear_filter(dup_key)
        except selenium.common.exceptions.NoSuchElementException:
            pass


    def setup_driver(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path)

    def teardown_driver(self):
        open_nav_menu = self.driver.find_element_by_css_selector(".crmui_usernamemenu_Menu")
        self.cursor_to_element(open_nav_menu)
        open_nav_menu.click()
        log_out_button = self.driver.find_element_by_xpath("//*[text()='Log out']")
        self.cursor_to_element(log_out_button)
        log_out_button.click()
        self.driver.quit()


    def avature_session_status(self):
        try:
            # Returns True if Session is Still Active
            session_active = WebDriverWait(self.driver, 5).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.DialogLoginPopup"))
            )
            return True
        except:
            return False


    def login_avature(self):
        self.driver.get("https://cisco.avature.net")
        easygui.msgbox("Please Login Into Avature. Minimize this window and then click OK when you are logged in.")
        time.sleep(5)
        easygui.ccbox("Confirming You Are Logged In to Avature")
        self.clean_slate()
        self.driver.get(
            "https://cisco.avature.net/#People/Id:2266/Filters:{\"entityTypeId\":2,\"id\":396094,\"set\":null,\"timeZone\":\"America*/New_York\"}")


    def cursor_to_element(self, element):  # Move mouse over element
        try:
            element_to_hover = ActionChains(self.driver).move_to_element(element)
            element_to_hover.perform()
        except Exception as e:
            print("Cursor to Element Problem")
            print(e)

    def open_filter_dropdown(self):  # Hover and click on Add Filter Dropdown Menu
        try:
            add_filter_menu = self.driver.find_element_by_xpath("//div[3]/div/span/span")
            self.cursor_to_element(add_filter_menu)
            add_filter_menu.click()
            WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "div.FloatingMenu.filtersFloatingMenu"))
            )

        except Exception as e:
            print("Open Filter Problem")
            print(e)

    def set_filter(self, filter_type, filter_text):  # If Keywords is present in Recent or Favorites. If not, get it to Recent
        try:
            try:
                filter_selector_base = "//span[contains(@class,'Floating')]//span[contains(text(),'{}')]"
                filter_selector = filter_selector_base.format(filter_type)
                target_filter = self.driver.find_element_by_xpath(filter_selector)
                self.cursor_to_element(target_filter)
                target_filter.click()
                # If available, will click from floating menu
                try:
                    # Depending on filter selected... keywords
                    text_box = self.driver.find_element_by_xpath("//textarea")
                except selenium.common.exceptions.NoSuchElementException:
                    # I.e. full name filter
                    text_box = self.driver.find_element_by_xpath("//div[@class='inputContainer']/input")
                text_box.clear()
                text_box.send_keys(filter_text)
                apply_button = self.driver.find_element_by_xpath("//button[text()='Apply']")
                apply_button.click()
                # Wait for apply button to not be visible
                WebDriverWait(self.driver, 10).until_not(
                    EC.visibility_of_element_located((By.XPATH, "//button[text()='Apply']"))
                )
            except selenium.common.exceptions.NoSuchElementException:
                self.add_more_filters_select()
                self.set_filter_addmore(filter_type)
                self.set_filter(filter_type, filter_text)  # Try again
        except Exception as e:
            print("Problem Setting Keywords")
            print(e)

    def add_more_filters_select(self):  # Selecting add more filters when desired filter is not present
        add_more = self.driver.find_element_by_xpath("//span[text()='Add more filters']")
        self.cursor_to_element(add_more)
        add_more.click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='Columns']"))
        )

    def set_filter_addmore(self, filter_type):  # From more filters screen, select keywords in order to push to recent
        filter_box = self.driver.find_element_by_css_selector("div.formContainer:nth-of-type(1) span[id*='Advanced'] input[id*='TIN']")
        self.cursor_to_element(filter_box)
        filter_box.click()
        filter_box.clear()
        filter_box.send_keys(filter_type)
        filter_base_selector = "//span[@title='{}']".format(filter_type)
        filter_element = self.driver.find_element_by_xpath(filter_base_selector)
        filter_element.click()
        apply_button = self.driver.find_element_by_xpath("//button[text()='Apply']")
        apply_button.click()
        WebDriverWait(self.driver, 10).until_not(
            EC.visibility_of_element_located((By.XPATH, "//button[text()='Apply']"))
        )
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ListRefresherIcon"))
        )


    def set_columns(self, columns):
        for col in columns:
            self.open_filter_dropdown()
            self.add_more_filters_select()
            column_button = self.driver.find_element_by_xpath("//a[@title='Columns']")
            column_button.click()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "table.EditableSelect"))
            )
            self.set_column(col)

    def set_column(self, column):
        selector_base_available = "//td[@class='TwoPaneSelectAvailableTd']//option[@title='{}']"
        selector_col_available = selector_base_available.format(column)
        selector_base_selected = "//td[@class='EditableSelectElementColumn']//option[@title='{}']"
        selector_col_selected = selector_base_selected.format(column)
        try:
            column_entry = self.driver.find_element_by_xpath(selector_col_available)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector_col_selected))
            )
        except selenium.common.exceptions.NoSuchElementException:
            try:
                self.driver.find_element_by_xpath(selector_col_selected)
                return
            except selenium.common.exceptions.NoSuchElementException:
                print("Error Selecting Column Filter")
                return
        column_entry.click()
        button_add_selection = self.driver.find_element_by_xpath("//td/button[text()='add >']")
        button_add_selection.click()

    def click_create_button(self):
        create_button = self.driver.find_element_by_css_selector(".crmui_recordcreator_Base")
        self.cursor_to_element(create_button)
        create_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='crmui_Sidebar']//span[text()='Person']"))
        )

    def click_create_person(self):
        create_person = self.driver.find_element_by_xpath("//div[@class='crmui_Sidebar']//span[text()='Person']")
        self.cursor_to_element(create_person)
        create_person.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[text()='Create person']"))
        )

    def select_create_method(self): # TODO Add different method supports, by file, copy paste, etc
        manual_selection = self.driver.find_element_by_xpath("// li[text() = 'Manually']")
        self.cursor_to_element(manual_selection)
        manual_selection.click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "PersonCreatorManualFirstName"))
        )

    def create_first_name(self, text_entry):
        first_name_box = self.driver.find_element_by_css_selector(".PersonCreatorManualFirstName input")
        self.cursor_to_element(first_name_box)
        first_name_box.send_keys(text_entry)

    def create_last_name(self, text_entry):
        last_name_box = self.driver.find_element_by_css_selector(".PersonCreatorManualLastName input")
        self.cursor_to_element(last_name_box)
        last_name_box.send_keys(text_entry)

    def create_position_title(self, text_entry):
        position_title_box = self.driver.find_element_by_css_selector(".PersonCreatorManualFormRow.PersonCreatorPositionTitleRow input[placeholder='Position title']")
        self.cursor_to_element(position_title_box)
        position_title_box.send_keys(text_entry)

    def create_current_company(self, text_entry):
        current_company_box = self.driver.find_element_by_css_selector(".PersonCreatorManualFormRow.PersonCreatorPositionTitleRow input[placeholder='Company']")
        self.cursor_to_element(current_company_box)
        current_company_box.send_keys(text_entry)

    def create_click_select_source_dropdown(self, source_text="LinkedIn Recruiter, Sourced from"):
        select_source_dropdown = self.driver.find_element_by_css_selector("span.AdvancedSelectInput")
        select_source_input = select_source_dropdown.find_element_by_css_selector("input")
        select_source_input.send_keys(source_text)
        matched_selector = "//span[text()='{}']".format(source_text)
        matched_source = self.driver.find_element_by_xpath(matched_selector)
        self.cursor_to_element(matched_source)
        matched_source.click()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, matched_selector))
        )

    def create_email(self, text_entry):
        email_box = self.driver.find_element_by_css_selector("input[placeholder='Email']")
        self.cursor_to_element(email_box)
        email_box.send_keys(text_entry)

    def create_save_button(self, person_first, person_last):
        save_button = self.driver.find_element_by_css_selector(".PersonCreatorManual button.TIN_input_button_Primary")
        self.cursor_to_element(save_button)
        save_button.click()
        person_profile_selector = "//span[@class='record_EditableTitle_Viewer']/span[text()='{} {}']".format(
            person_first, person_last)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, person_profile_selector))
        )

    def profile_enter_talent_hub_specialist(self, ths="Eric Stasney"):
        ths_box = self.driver.find_element_by_xpath("//span[text()='Talent Hub Specialist']//ancestor::div[@class='row']//span[text()='Edit']")
        ths_box.click()
        ths_dropdown = self.driver.find_element_by_xpath("//div[@class='AdvancedSelectInput']")
        ths_dropdown_input = ths_dropdown.find_element_by_xpath("//input")
        ths_dropdown_input.send_keys(ths)
        matched_selector = "span[title*='{}']".format(ths)
        matched_ths = self.driver.find_element_by_css_selector(matched_selector)
        matched_ths.click()
        ths_confirmed_selector = "//span[contains(text(), '{}')]".format(ths)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, ths_confirmed_selector))
        )

    def contact_info_click_plus(self):
        plus_button = self.driver.find_element_by_css_selector("div.contactInfoList .uicore_layout_panel_HeaderToolbar_Item > span")
        self.cursor_to_element(plus_button)
        plus_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.FloatingMenuButton span[title='Phone']"))
        )

    def contact_info_enter_field(self, field_type, text_entry): # 'Email', 'Website' 'Street Address'
        desired_field_selector = "span[title='{}']".format(field_type)
        desired_field = self.driver.find_element_by_css_selector(desired_field_selector)
        desired_field.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table.EditContactInfoContainer"))
        )
        if field_type != 'Street address':
            field_entry_box = self.driver.find_element_by_xpath("//input")
            field_entry_box.send_keys(text_entry)
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "table.EditContactInfoContainer"))
            )
            return
        else:
            country_dropdown = self.driver.find_element_by_xpath("//option[@title='United States']")
            country_dropdown.click()
            zip_code_box = self.driver.find_element_by_css_selector("input[placeholder='Zip/Postal code']")
            zip_code_box.send_keys(text_entry)

    def attach_pdf(self, file_name, file_path):
        attach_button = self.driver.find_element_by_xpath("//a[text()='Attach']")
        self.cursor_to_element(attach_button)
        attach_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        choose_file = self.driver.find_element_by_css_selector("input[type='file']")
        try:
            choose_file.send_keys(file_path)
        except:
            return
        save_file_button = self.driver.find_element_by_xpath("//button[text()='Save']")
        save_file_button.click()
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.TIN_input_button_Base TIN_input_button_Cancel"))
        )
        cancel_button = self.driver.find_element_by_css_selector("button.TIN_input_button_Base TIN_input_button_Cancel")
        cancel_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "button.TIN_input_button_Base TIN_input_button_Cancel"))
        )










    def results_exist(self):
        # TODO : Filter results that match from fields not associated with keyword search
        try:
            filter_on_page = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "span.conditionViewer"))
                    )
            # Filter is present on page check if results returned or no results
            try:  # No results
                search_results = self.driver.find_element_by_css_selector(".uicore_list_NoResultsMessage")
                return False
            except selenium.common.exceptions.NoSuchElementException:  # Results found
                # relevancy = self.results_relevant()
                search_url = self.driver.current_url
                return search_url
        except Exception as e:
            print("Problem interpreting results")
            print(e)

    # def results_relevant(self, dup_key_map):





# TODO Add dup_key_map

    def dup_check_avature(self, type_value_dict):  # Expects Dictionary with Type : Data format
        if self.avature_session_status():
            for k, v in type_value_dict.items():
                self.open_filter_dropdown()
                self.set_filter(k, v)
        else:
            return False
        if self.avature_session_status():
            dup_results = self.results_exist()
        else:
            return False
        # Clear the filter search
        if self.avature_session_status():
            self.clean_slate()
        else:
            return False
        return dup_results










