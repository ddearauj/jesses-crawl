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

from orgs import selectOrg, loopOrganizations
from selections import checkSubjects, selectYear

import time 

def getReport(driver, name):

	get_report = driver.find_element_by_class_name('list-get-reports')
	button = get_report.find_element_by_class_name('btn')
	ActionChains(driver).move_to_element(button).click(button).perform()

	# this will lead to a different page with the report
	# the download button is in the new page

	download = driver.find_element_by_class_name('icon-download3')
	ActionChains(driver).move_to_element(download).click(download).perform()

	# another popup will show. Now select csv and give it a name
	form = driver.find_elements_by_class_name('di-form-control')
	pdf_vs_csv = form[0].find_elements_by_class_name('em-checkbox')
	#pdf_vs_csv = form[0].find_elements_by_xpath("//label[@class='em-checkbox']")

	for option in pdf_vs_csv:
		print(option.text)
		if 'CSV' in option.text:
			ActionChains(driver).move_to_element(option).click(option).perform()

	input_name = form[1].find_element_by_class_name('di-form-input')
	input_name.clear()
	input_name.send_keys(str(name))
	driver.implicitly_wait(100)

	# final download button!
	footer = driver.find_element_by_class_name('rc-dialog-footer')
	download_btn = footer.find_element_by_class_name('btn-primary')
	ActionChains(driver).move_to_element(download_btn).click(download_btn).perform()

def initDriver():
	driver = webdriver.Chrome('./chromedriver')
	driver.get("https://txreports.emetric.net/?domain=1&report=1")
	return driver


def getProgramNames(driver):
	program_drop_down = driver.find_element_by_class_name('selections-program')
	program_drop_down = program_drop_down.find_element_by_class_name('drop-down-item-scroll')
	program_drop_down = program_drop_down.find_elements_by_class_name('drop-down-item')
	names = []
	for program in program_drop_down:
		#print(program.get_attribute("innerHTML"))
		soup = BeautifulSoup(program.get_attribute("innerHTML"), "lxml")
		print(soup.span.text)
		names.append(soup.span.text)
	return names

def getReportNames(driver):
	report_drop_down = driver.find_element_by_class_name('selections-report')
	report_drop_down = report_drop_down.find_element_by_class_name('drop-down-item-list')
	report_drop_down = report_drop_down.find_elements_by_class_name('drop-down-item')
	names = []
	for program in report_drop_down:
		#print(program.get_attribute("innerHTML"))
		soup = BeautifulSoup(program.get_attribute("innerHTML"), "lxml")
		print(soup.span.text)
		names.append(soup.span.text)
	return names

def main():

	driver = initDriver()
	# program_names = getProgramNames(driver)
	# report_names = getReportNames(driver)
	year = "2016"
	selected_orgs = 0
	selectYear(driver, year)
	checkSubjects(driver)
	#selected_orgs, last_element = selectOrg(driver, selected_orgs)

	done = False
	loopOrganizations(driver, "STAAR_3-8_Group_Summary:_Performance_Levels")
	# last_element, done = selectOrg(driver)
	# getReport(driver, "")
	# driver.get("https://txreports.emetric.net/?domain=1&report=1")

	# while(not done):
	# 	selectYear(driver, year)
	# 	checkSubjects(driver)
	# 	last_element, done = selectOrg(driver, last_element=last_element)
	# 	getReport(driver, "STAAR_3-8_Group_Summary:_Performance_Levels")
	# 	#driver.execute_script("window.history.go(-1)")
	# 	driver.get("https://txreports.emetric.net/?domain=1&report=1")
	# 	time.sleep(2)
	# 	#clear the orgs

	# 	print("new loop")


	# selected_orgs, last_element = selectOrg_noClick(driver, selected_orgs, last_element=last_element)
	# selected_orgs, last_element = selectOrg(driver, selected_orgs, last_element=last_element)


	time.sleep(10)

	driver.stop_client()
	driver.close()


if __name__ == '__main__':
	main()