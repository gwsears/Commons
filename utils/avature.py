from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import easygui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.common.exceptions
import time

class DupDriver(object):
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = None
        # self.setup_driver()
        # self.login_avature()

    def begin_session(self):
        self.setup_driver()
        self.login_avature()
        self.clean_slate()


    def clean_slate(self):
        try:
            filter_i = self.driver.find_element_by_css_selector("span.conditionViewer a")
            filter_text = filter_i.text
            self.clear_filter(filter_text)
        except selenium.common.exceptions.NoSuchElementException:
            return

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

    def set_filter_keywords(self, filter_text):  # If Keywords is present in Recent or Favorites. If not, get it to Recent
        try:
            try:
                keyword_filter = self.driver.find_element_by_xpath("//span[text()='Keywords']")
                self.cursor_to_element(keyword_filter)
                keyword_filter.click()
                keyword_box = self.driver.find_element_by_xpath("//textarea")
                keyword_box.clear()
                keyword_box.send_keys(filter_text)
                apply_button = self.driver.find_element_by_xpath("//button[text()='Apply']")
                apply_button.click()
            except selenium.common.exceptions.NoSuchElementException:
                self.add_more_filters_select()
                self.set_filter_keywords_addmore()
                self.set_filter_keywords(filter_text)  # Try again
        except Exception as e:
            print("Problem Setting Keywords")
            print(e)

    def add_more_filters_select(self):  # Selecting add more filters when Keywords is not present
        add_more = self.driver.find_element_by_xpath("//span[text()='Add more filters']")
        self.cursor_to_element(add_more)
        add_more.click()
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@title='Columns']"))
        )

    def set_filter_keywords_addmore(self):  # From more filters screen, select keywords in order to push to recent
        filter_box = self.driver.find_element_by_css_selector("input#TIN_input_TextInput487")
        self.cursor_to_element(filter_box)
        filter_box.click()
        filter_box.clear()
        filter_box.send_keys("Keywords")
        keyword_filter_element = self.driver.find_element_by_xpath("//span[text()='Keywords']")
        keyword_filter_element.click()
        apply_button = self.driver.find_element_by_xpath("//button[text()='Apply']")
        apply_button.click()


    def set_columns(self, columns):
        self.open_filter_dropdown()
        self.add_more_filters_select()
        column_button = self.driver.find_element_by_xpath("//a[@title='Columns']")
        column_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "table.EditableSelect"))
        )

    def set_column(self, column):
        column_entry = self.driver.find_element_by_css_selector
        column_entry.click()
        button_add_selection = self.driver.find_element_by_xpath("//td/button[text()='add >']")
        button_add_selection.click()
        WebDriverWait(self.driver, 10).until()



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
                relevancy = self.results_relevant()
                search_url = self.driver.current_url
                return search_url
        except Exception as e:
            print("Problem interpreting results")
            print(e)

    def results_relevant(self):


    def clear_filter(self, dup_key):
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
                    EC.element_to_be_clickable((By.LINK_TEXT, dup_key)))
                self.confirm_filter_clear()
            except selenium.common.exceptions.NoSuchElementException:
                pass
        except Exception as e:
            print("Problem Clearing Filter")
            print(e)


    def confirm_filter_clear(self):
        try:
            filter_hyperlink = self.driver.find_element_by_css_selector("a.list_conditionsviewer_ItemValuePopupLink_Link")
            self.clear_filter()
        except selenium.common.exceptions.NoSuchElementException:
            pass



    def dup_check_avature(self, dup_check_row):
        if self.avature_session_status():
            self.open_filter_dropdown()
        else:
            return False
        if self.avature_session_status():
            self.set_filter_keywords(dup_check_row)
        else:
            return False
        if self.avature_session_status():
            dup_results = self.results_exist()
        else: return False
        # Clear the filter search
        if self.avature_session_status():
            self.clear_filter(dup_check_row)
        else:
            return False
        return dup_results

    def dup_check_batch(self):
        while self.iter_tally < len(self):
            dup_check_row = self.present_dup()
            if dup_check_row == '':
                self.ResultsDict[self.iter_tally] = {'key': dup_check_row, 'results': 'No Key Loaded'}
                self.iter_tally_one()
                continue
            else:
                dup_check = self.dup_check_avature(dup_check_row)
                if dup_check is False:
                    result = 'No Duplicates Found'
                else:
                    result = dup_check
                self.ResultsDict[self.iter_tally] = {'key': dup_check_row, 'results': result}
                self.iter_tally_one()






class LeadPerson(object):

    def __init__(self, *key_data, **person_data):
        self.person_data = person_data
        self.key_data = key_data
        self.dup_key = self.dup_key_gen()


    """
    :key_data - Specify which dictionary keys from person_data are to be used for key generation
    :person_data - Dictionary with desired person data
    """

    def dup_key_gen(self):
        dup_key = []
        for k, v in self.person_data.items():
            if k in self.key_data or k.lower() in self.key_data:
                if k == 'LinkedIn':
                    linkedin_v = self.linkedin_key(v)
                    dup_key.append(linkedin_v)
                else:
                    dup_key.append(k)
        concat_key = self.concat_key(dup_key)
        return concat_key


    def linkedin_key(self, url):
        if "/in/" in url:
            url = url.split("/in/")[1]
        elif "/pub/" in url:
            url = url.split("/pub/")[1]
        elif "/recruiter/" in url:
            url = url.split("/profile/")[1]
        else:
            return url
        return url


    def concat_key(self, dup_key_raw):
        dup_key = ' OR '.join([key for key in dup_key_raw])
        return dup_key








