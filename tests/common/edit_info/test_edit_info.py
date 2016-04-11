from codebender_testing.config import TEST_PROJECT_NAME
from codebender_testing.utils import SeleniumTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from codebender_testing import config
from time import gmtime
from time import strftime
from time import strptime
import os
import time

class TestEditInfo(SeleniumTestCase):

    def test_navigate_home(self, tester_logout):
        """ opens browser to codebender """
        self.open("/")
        assert "codebender" in self.driver.title

    def test_edit_info(self, tester_logout):
        credentials = {
            'username': os.environ.get('CODEBENDER_TEST_USER'),
            'password': os.environ.get('CODEBENDER_TEST_PASS'),
        }
        driver = self.driver
        self.open("/")

        """ tests to ensure login div appears """
        login_elem = self.get_element(By.ID, "login_btn")    #finds login button
        login_elem.send_keys(Keys.RETURN)                      #clicks login button
        logbox_elem = self.get_element(By.ID, "login_box")   #finds login div
        assert logbox_elem.is_displayed()                      #checks to see if div is visible

        """ tests login with invalid username """
        # define elements in login form
        username_elem = self.get_element(By.ID, "username")
        password_elem = self.get_element(By.ID, "password")
        submit_elem = self.get_element(By.ID, "_submit")

        # log in to site using correct credentials
        username_elem.send_keys(credentials['username'])
        password_elem.send_keys(credentials['password'])
        submit_elem.click()
        assert "Logged in as" in driver.page_source

        # create sketch named test_project
	self.create_sketch("test_project", "test project description");

	# return to home page	
	self.driver.get("https://staging.codebender.cc/home")
	
	# hover over project name
	project_link = self.driver.find_element_by_link_text("test_project")
        #project_link.send_keys(Keys.ENTER)
    	hov = ActionChains(self.driver).move_to_element(project_link)
    	hov.perform()

	#time.sleep(5)

        WebDriverWait(self.driver, 30).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, ".sketch-block-edit-info")
            )
        )

	# click edit info
	info_link = self.driver.find_element_by_link_text("Edit Info")
	info_link.click()
	time.sleep(5)

        #WebDriverWait(self.driver, 30).until(
            #expected_conditions.invisibility_of_element_located(
                #(By.ID, "edit-sketch-modal-type-controls")
            #)
        #)

	# click radio button
	publicRadioButton = self.driver.find_elements_by_css_selector("input[type='radio'][value='public']")
        publicRadioButton[2].click()

	# save project changes
	saveButton = self.driver.find_element_by_id('edit-sketch-modal-action-button')
	saveButton.click()

	time.sleep(5)
	
	assert self.driver.find_element_by_link_text('test_project').is_displayed()
	assert self.driver.find_element(By.CSS_SELECTOR, '.sketch-block-short-description').text=="test project description"
		
	
	# hover over project name
        project_link = self.driver.find_element_by_link_text("test_project")
        #project_link.send_keys(Keys.ENTER)
        hov = ActionChains(self.driver).move_to_element(project_link)
        hov.perform()

        time.sleep(5)

        #WebDriverWait(self.driver, 30).until(
            #expected_conditions.presence_of_element_located(
                #(By.CSS_SELECTOR, "sketch-block-edit-info")
            #)
        #)

        # click edit info
        info_link = self.driver.find_element_by_link_text("Edit Info")
        info_link.click()
        time.sleep(5)

	# set sketch name to project
	projectNameField = self.driver.find_element_by_id('edit-sketch-name')
        projectNameField.clear()
        projectNameField.send_keys("project")
        projectNameField.send_keys(Keys.ENTER)
	
	# save project changes
	saveButton = self.driver.find_element_by_id('edit-sketch-modal-action-button')
        saveButton.click()

	time.sleep(5)
	
	# verify description and privacy setting	
        assert self.driver.find_element(By.CSS_SELECTOR, '.sketch-block-short-description').text=="test project description"

	time.sleep(5)

	project_link = self.driver.find_element_by_link_text("project")
	li_element = project_link.find_element_by_xpath('../../../..')
	class_name = li_element.get_attribute("class")
	assert class_name=="sketch-block public static-filter dynamic-filter"

	time.sleep(5)

	 # hover over project name
        project_link = self.driver.find_element_by_link_text("project")
        #project_link.send_keys(Keys.ENTER)
        hov = ActionChains(self.driver).move_to_element(project_link)
        hov.perform()

        time.sleep(5)

        #WebDriverWait(self.driver, 30).until(
            #expected_conditions.presence_of_element_located(
                #(By.CSS_SELECTOR, "sketch-block-edit-info")
            #)
        #)

        # click edit info
        info_link = self.driver.find_element_by_link_text("Edit Info")
        info_link.click()
        time.sleep(5)

	projectDescriptionArea = self.driver.find_element_by_id('edit-sketch-modal-sort-description')
        projectDescriptionArea.clear()
        projectDescriptionArea.send_keys("description")
        projectDescriptionArea.send_keys(Keys.ENTER)

	# save project changes
        saveButton = self.driver.find_element_by_id('edit-sketch-modal-action-button')
        saveButton.click()

	time.sleep(5)
	
	# verify project name and privacy setting
	assert self.driver.find_element_by_link_text('project').is_displayed()
        project_link = self.driver.find_element_by_link_text("project")

        li_element = project_link.find_element_by_xpath('../../../..')
        class_name = li_element.get_attribute("class")
        assert class_name=="sketch-block public static-filter dynamic-filter"

	# delete project
	self.delete_project("project")
	time.sleep(5)
