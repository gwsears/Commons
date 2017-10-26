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

    def set_filter(self, filter_type, filter_text):  # If Keywords is present in Recent or Favorites. If not, get it to Recent
        try:
            try:
                filter_selector_base = "//span[contains(@class,'Floating)]//span[contains(text(),'{}')]"
                filter_selector = filter_selector_base.format(filter_type)
                target_filter = self.driver.find_element_by_xpath(filter_selector)
                self.cursor_to_element(target_filter)
                target_filter.click()
                text_box = self.driver.find_element_by_xpath("//textarea")
                text_box.clear()
                text_box.send_keys(filter_text)
                apply_button = self.driver.find_element_by_xpath("//button[text()='Apply']")
                apply_button.click()
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
                self.confirm_filter_clear(dup_key)
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
            self.clear_filter(dup_check_row)
        else:
            return False
        return dup_results










