""" General functions for the txreports website"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time



def selectProgram(driver, name):
	# click the arrow to show all programs
	driver.find_element_by_class_name('drop-down-arrow').click()
	programs = driver.find_elements_by_class_name('drop-down-item')

	for program in programs:
		if program.text == name:
			if "selected" not in program.get_attribute("class"):
				ActionChains(driver).move_to_element(program).click(program).perform()
				# once we select a new program, we must wait for the page to load!
				# so we check if the reportSelector exists for 10 seconds. Other wise, we get an error
				wait = WebDriverWait(driver, 10)
				wait.until(
					EC.presence_of_element_located((By.ID, "reportSelector"))
				)
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
				# wait for scopes containers scopes-container
				break
			else:
				ActionChains(driver).move_to_element(button).click(button).perform()
				break

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

def getReport(driver, name):

	get_report = driver.find_element_by_class_name('list-get-reports')
	button = get_report.find_element_by_class_name('btn')
	ActionChains(driver).move_to_element(button).click(button).perform()

	# this will lead to a different page with the report
	# the download button is in the new page

	wait = WebDriverWait(driver, 10)
	wait.until(
		EC.presence_of_element_located((By.CLASS_NAME, "icon-download3"))
	)
	time.sleep(5)
	download = driver.find_element_by_class_name('icon-download3')
	ActionChains(driver).move_to_element(download).click(download).perform()
	driver.implicitly_wait(10)

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



