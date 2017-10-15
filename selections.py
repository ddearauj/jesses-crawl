from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import itertools
import time 

def checkTwoWayTable(driver):
	try:
		driver.find_element_by_class_name('twoway-table')
		return True
	except:
		return False

def checkCheckBoxes(driver):
	try:
		driver.find_element_by_class_name('checkbox')
		return True
	except:
		return False

def checkRadioButtons(driver):
	try:
		driver.find_element_by_class_name('radiobutton')
		return True
	except:
		return False


def clickShowMore(driver):
	try:
		show_more = driver.find_element_by_class_name('twoway-table-show-more')
		ActionChains(driver).move_to_element(show_more).click(show_more).perform()
		driver.implicitly_wait(10)
	except Exception as e:
		print("The option is not available, so no click needed")

def checkRowYearTwoWay(driver, year):

	dates = []
	dates = driver.find_elements_by_class_name('twoway-table-container-y-item')
	for date in dates:
		# ok, now we want only to click on the rows that contains "year"
		if(year in date.text):
			print(date.text)
			ActionChains(driver).move_to_element(date).click(date).perform()
			driver.implicitly_wait(100)

def checkSubjects(driver):

	# There might be a way to make this more generic 
	# and avoid further website changes, but for now, lets go with the id.
	# it is fast and simple. If it breaks, email me.

	subjects = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[2]/div[3]/div[3]/div')
	non_clicked_subjects = subjects.find_elements_by_class_name('em-checkbox')
	for subj in non_clicked_subjects:
		ActionChains(driver).move_to_element(subj).click(subj).perform()
		driver.implicitly_wait(100)


def clickCheckButtons(driver, scopes_container, year):

	checkRows = scopes_container.find_elements_by_class_name('checkbox')
	for row in checkRows:
		group = row.find_element_by_class_name('checkbox-group')
		initial_check = group.find_element_by_class_name('checked')
		checkboxes = group.find_elements_by_class_name('em-checkbox')
		if("Year" in row.text or "Admin" in row.text):
			print(row.text)
			for date in checkboxes:
				if(year in date.text):
					print(date.text)
					ActionChains(driver).move_to_element(date).click(date).perform()
					driver.implicitly_wait(100)

			soup = BeautifulSoup(initial_check.get_attribute("innerHTML"), "lxml")
			if(year not in soup.span.text):
				ActionChains(driver).move_to_element(initial_check).click(initial_check).perform()

		else:
			for column in checkboxes:
				ActionChains(driver).move_to_element(column).click(column).perform()
				driver.implicitly_wait(100)

def clickRadioButtons(driver, scopes_container, year):
	# create a list of lists with all radio buttons, then click every combination
	radio_rows = scopes_container.find_elements_by_class_name('radiobutton')
	list_lists = []
	admin_year = []

	# select year, this might update the buttons
	for row in radio_rows:
		group = row.find_element_by_class_name('checkbox-group')
		radio = group.find_elements_by_class_name('em-checkbox')
		print(row.text)
		if("Year" in row.text):
			print(row.text)
			for date in radio:
				if(year in date.text):
					ActionChains(driver).move_to_element(date).click(date).perform()
					driver.implicitly_wait(100)
					time.sleep(3)

	# get new buttons
	print('cliquei no ano')
	radio_rows = driver.find_element_by_class_name('scopes-container').find_elements_by_class_name('radiobutton')
	for row in radio_rows:
		group = row.find_element_by_class_name('checkbox-group')
		radio = group.find_elements_by_class_name('em-checkbox')
		print(row.text)
		if("Admin" in row.text):
			print(row.text)
			admin_year.append(radio)

		else:
			if("Year" not in row.text):
				list_lists.append(radio)

	# remove radio buttons that are not from the year chosen
	# then append the new list to the big list of lists
	for row in admin_year:
		for date in list(row):
			if(year not in date.text):
				row.remove(date)
				break

	for row in list_lists:
		admin_year.append(row)

	for element in admin_year:
		print("new row")
		for radio in element:
			print(radio.text)

	for listi in itertools.product(*admin_year):
		for radio in listi:
			print(radio.text)
			ActionChains(driver).move_to_element(radio).click(radio).perform()
		time.sleep(3)
		print("nova combinacao")


def selectYear(driver, year):
	""" 
	this will click on any row that has "year" in it 
	and uncheck the first checked box if it is not from "year"

	"""

	# depending on the program selected, part of the table might be hidden
	clickShowMore(driver)

	# Because initially the website is selecting the most recent date, we must uncheck it
	# But first it needs to have something else checked. Lokking for a single checked box is
	# a lot simpler, we will save the initial checked box

	initial_check = driver.find_element_by_class_name('checked')

	# now we click any row containing "year"
	checkRowYear(driver, year)

	# now uncheck the first one
	ActionChains(driver).move_to_element(initial_check).click(initial_check).perform()



def selectProgram(driver, name):
	# click the arrow to show all programs
	driver.find_element_by_class_name('drop-down-arrow').click()
	programs = driver.find_elements_by_class_name('drop-down-item')

	for program in programs:
		if program.text == name:
			if "selected" not in program.get_attribute("class"):
				ActionChains(driver).move_to_element(program).click(program).perform()
				break
			else:
				driver.find_element_by_class_name('drop-down-arrow').click()
				break


def selectReport(driver, name):
	selector  = driver.find_element_by_id('reportSelector')
	button = selector.find_element_by_class_name('drop-down-arrow')
	ActionChains(driver).move_to_element(button).click(button).perform()
	reports = driver.find_elements_by_class_name('drop-down-item')
	for report in reports:
		if report.text == name:
			if "selected" not in report.get_attribute("class"):
				ActionChains(driver).move_to_element(report).click(report).perform()
				break
			else:
				ActionChains(driver).move_to_element(button).click(button).perform()
				break



driver = webdriver.Chrome('./chromedriver')
# driver.get("https://txreports.emetric.net/?domain=1&report=1")
# # selectProgram(driver, "TAKS")
# selectProgram(driver, "STAAR EOC")
# wait = WebDriverWait(driver, 10)
# wait.until(
# 	EC.presence_of_element_located((By.CLASS_NAME, "orgtree-body-normal"))
# )
# selectReport(driver, "Standard Summary")
# wait = WebDriverWait(driver, 10)
# wait.until(
# 	EC.presence_of_element_located((By.CLASS_NAME, "orgtree-body-normal"))
# )

driver.get("https://txreports.emetric.net/?domain=4&report=39")
clickRadioButtons(driver, driver.find_element_by_class_name('scopes-container'), "2016")