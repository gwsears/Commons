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

class DupDriver(object):
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.lead_holder = []
        self.avature_driver = webdriver.Chrome(executable_path=self.driver_path)
        self.avature_driver.implicitly_wait(15)

    def login_avature(self):
        self.avature_driver.get("https://cisco.avature.net")
        easygui.msgbox("Please Login Into Avature. Minimize this window and then click OK when you are logged in.")
        time.sleep(5)
        await_avature_login = easygui.ccbox("Confirming You Are Logged In to Avature")
        if await_avature_login:
            pass

        self.avature_driver.get(
            "https://cisco.avature.net/#People/Id:2266/Filters:{\"entityTypeId\":2,\"id\":396094,\"set\":null,\"timeZone\":\"America*/New_York\"}")
        easygui.msgbox(
            "DupCheck Will Now Check for " + str(len(self.lead_holder)) + " leads. You may minimize the browser "
                                                                            "window. Please do not login to "
                                                                            "Avature through a different browser "
                                                                            "as this will stop the checker. Click "
                                                                            "OK when you are ready")

    def retrieve_key(self):

    def dup_check_avature(dupcheck_key):
        add_filter_menu = driver.find_element_by_xpath("//div[3]/div/span/span")
        add_filter_menu_hover = ActionChains(driver).move_to_element(add_filter_menu)
        add_filter_menu_hover.perform()
        add_filter_menu.click()

        keyword_filter = driver.find_element_by_css_selector(
            "div.FloatingMenuButton:nth-child(7) > span:nth-child(1) > span:nth-child(2)")
        keyword_filter.click()

        filter_textbox = driver.find_element_by_xpath("//textarea")
        filter_textbox.send_keys(dupcheck_key)
        filter_textbox.send_keys(u'\ue007')
        filter_apply_button = driver.find_element_by_xpath("//button")
        time.sleep(2)
        filter_apply_button.click()
        time.sleep(3)
        try:
            dup_results = driver.find_element_by_css_selector(".uicore_list_NoResultsMessage")
            dup_results_test = False
        except:
            dup_results_test = True
        # Clear the filter search
        filter_hyperlink = driver.find_element_by_css_selector("a.list_conditionsviewer_ItemValuePopupLink_Link")
        filter_hyperlink_hover = ActionChains(driver).move_to_element(filter_hyperlink)
        filter_hyperlink_hover.perform()
        filter_hyperlink.click()
        filter_hyperlink_remove = driver.find_element_by_link_text("Remove filter")
        filter_hyperlink_remove_hover = ActionChains(driver).move_to_element(filter_hyperlink_remove)
        filter_hyperlink_remove_hover.perform()
        filter_hyperlink_remove.click()
        time.sleep(5)
        return dup_results_test

class LeadPersonHolder(object):
    def __init__(self, dupcheck_data):




class LeadPerson(object):

    def __init__(self, **person_data):
        self.__dict__.update(person_data)
        self.__dict__.update((k, v) for k, v in person_data.iteritems())


    def blank_test(self, value_passed):
        if str(value_passed).lower() == 'nan':
            return False
        else:
            vp = str(value_passed)
            vp = vp.splitlines()
            vp = vp[0]
            return vp

    def dup_key(self):

        dup_key = []
        if self.li_url:
            try:
                li_key = self.li_url.split("/in/")[1]
            except:
                li_key = ""
        else:
            li_key = ""

        dup_key.append(li_key)

        if self.email:
            dup_key.append(self.email)
        if self.oemail:
            dup_key.append(self.oemail)
        if self.phone:
            dup_key.append(self.phone)

        dup_key = ' OR '.join([key for key in dup_key])
        return dup_key


def dup_check_avature(dupcheck_key):
    add_filter_menu = driver.find_element_by_xpath("//div[3]/div/span/span")
    add_filter_menu_hover = ActionChains(driver).move_to_element(add_filter_menu)
    add_filter_menu_hover.perform()
    add_filter_menu.click()

    keyword_filter = driver.find_element_by_css_selector("div.FloatingMenuButton:nth-child(7) > span:nth-child(1) > span:nth-child(2)")
    keyword_filter.click()

    filter_textbox = driver.find_element_by_xpath("//textarea")
    filter_textbox.send_keys(dupcheck_key)
    filter_textbox.send_keys(u'\ue007')
    filter_apply_button = driver.find_element_by_xpath("//button")
    time.sleep(2)
    filter_apply_button.click()
    time.sleep(3)
    try:
        dup_results = driver.find_element_by_css_selector(".uicore_list_NoResultsMessage")
        dup_results_test = False
    except:
        dup_results_test = True
    # Clear the filter search
    filter_hyperlink = driver.find_element_by_css_selector("a.list_conditionsviewer_ItemValuePopupLink_Link")
    filter_hyperlink_hover = ActionChains(driver).move_to_element(filter_hyperlink)
    filter_hyperlink_hover.perform()
    filter_hyperlink.click()
    filter_hyperlink_remove = driver.find_element_by_link_text("Remove filter")
    filter_hyperlink_remove_hover = ActionChains(driver).move_to_element(filter_hyperlink_remove)
    filter_hyperlink_remove_hover.perform()
    filter_hyperlink_remove.click()
    time.sleep(5)
    return dup_results_test







