from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import easygui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium.common.exceptions
import time

class DupDriver(object):
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.DataDict = {}
        self.ErrorDict = {}
        self.iter_tally = 0
        self.driver = None
        self.setup_driver()
        self.login_avature()

    def append_data(self, data_row):
        new_data_key = self.next_available_key(self.DataDict)
        self.DataDict[new_data_key] = data_row

    def next_available_key(self, data_holder):
        dict_len = len(data_holder)
        return dict_len

    def append_data_error(self, current_key):
        error_data_key = self.next_available_key(self.ErrorDict)
        self.ErrorDict[error_data_key] = self.DataDict[current_key]

    def setup_driver(self):
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.driver.implicitly_wait(5)

    def login_avature(self):
        self.driver.get("https://cisco.avature.net")
        easygui.msgbox("Please Login Into Avature. Minimize this window and then click OK when you are logged in.")
        time.sleep(5)
        easygui.ccbox("Confirming You Are Logged In to Avature")
        self.driver.get(
            "https://cisco.avature.net/#People/Id:2266/Filters:{\"entityTypeId\":2,\"id\":396094,\"set\":null,\"timeZone\":\"America*/New_York\"}")
        easygui.msgbox(
            "DupCheck Will Now Check for " + str(len(self.dup_data_holder)) + " leads. You may minimize the browser "
                                                                            "window. Please do not login to "
                                                                            "Avature through a different browser "
                                                                            "as this will stop the checker. Click "
                                                                            "OK when you are ready")
    def iter_tally_one(self):
        self.iter_tally = self.iter_tally + 1


    def present_dup(self): # extract one data record to check for duplicates
        loaded_dup = self.dup_data_holder[self.iter_tally]
        return loaded_dup

    def cursor_to_element(self, element):  # Move mouse over element
        element_to_hover = ActionChains(self.driver).move_to_element(element)
        element_to_hover.perform()

    def open_filter_dropdown(self): # Hover and click on Add Filter Dropdown Menu
        add_filter_menu = self.driver.find_element_by_xpath("//div[3]/div/span/span")
        self.cursor_to_element(add_filter_menu)
        add_filter_menu.click()

    def set_filter_keywords(self, filter_text): # If Keywords is present in Recent or Favorites. If not, get it to Recent
        try:
            keyword_filter = self.driver.find_element_by_xpath("//span[text()='Keywords']")
            self.cursor_to_element(keyword_filter)
            keyword_filter.click()
            keyword_filter.clear()
            keyword_filter.send_keys(filter_text)
            apply_button = self.driver.find_element_by_xpath("//button[text()='Apply']")
            apply_button.click()
        except selenium.common.exceptions.NoSuchElementException:
            self.add_more_filters_select()
            self.set_filter_keywords_addmore()
            self.set_filter_keywords() # Try again

    def add_more_filters_select(self): # Selecting add more filters when Keywords is not present
        add_more = self.driver.find_element_by_xpath("//span[text()='Add more filters']")
        self.cursor_to_element(add_more)
        add_more.click()

    def set_filter_keywords_addmore(self): # From more filters screen, select keywords in order to push to recent
        filter_box = self.driver.find_element_by_css_selector("input#TIN_input_TextInput487")
        self.cursor_to_element(filter_box)
        filter_box.click()
        filter_box.clear()
        filter_box.send_keys("Keywords")
        keyword_filter_element = self.driver.find_element_by_xpath("//span[text()='Keywords']")
        keyword_filter_element.click()
        apply_button = self.driver.find_element_by_xpath("//button[text()='Apply']")
        apply_button.click()

    def interpret_search(self):
        try:  # No results
            search_results = self.driver.find_element_by_css_selector(".uicore_list_NoResultsMessage")
            return False
        except selenium.common.exceptions.NoSuchElementException: # Results found
            search_url = self.driver.current_url
            return search_url

    def clear_filter(self):
        filter_hyperlink = self.driver.find_element_by_css_selector("a.list_conditionsviewer_ItemValuePopupLink_Link")
        filter_hyperlink_hover = ActionChains(self.driver).move_to_element(filter_hyperlink)
        filter_hyperlink_hover.perform()
        filter_hyperlink.click()
        filter_hyperlink_remove = self.driver.find_element_by_link_text("Remove filter")
        self.cursor_to_element(filter_hyperlink_remove)
        filter_hyperlink_remove.click()


    def dup_check_avature(self):
        dup_check_row = self.present_dup()
        self.open_filter_dropdown()
        self.set_filter_keywords(dup_check_row)
        dup_results = self.interpret_search()
        # Clear the filter search
        self.clear_filter()
        return dup_results

class LeadPersonHolder(object):

    def __init__(self):
        self.DataDict = {}
        self.ErrorDict = {}
        self.DupDriver = DupDriver(driver_path=r"C:\Users\erics_qp7a9\PycharmProjects\Scraping\chromedriver.exe")

        #TODO Fix how filepath is passed

    def append_data(self, data_row):
        new_data_key = self.next_available_key(self.DataDict)
        self.DataDict[new_data_key] = data_row

    def next_available_key(self, data_holder):
        dict_len = len(data_holder)
        return dict_len

    def append_data_error(self, current_key):
        error_data_key = self.next_available_key(self.ErrorDict)
        self.ErrorDict[error_data_key] = self.DataDict[current_key]


class LeadPerson(object):

    def __init__(self, *key_data, **person_data):
        self.__dict__.update(person_data)
        self.__dict__['dup_key'] = self.dup_key(key_data)

    """
    :key_data - Specify which dictionary keys from person_data are to be used for key generation
    :person_data - Dictionary with desired person data
    """

    def dup_key(self, *key_data):
        dup_key = []
        for k, v in self.__dict__.items():
            if k in key_data or k.lower() in key_data:
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








