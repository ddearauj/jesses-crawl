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
from time import sleep
import time

from orgs import selectOrgs, loopOrganizations

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
	driver.implicitly_wait(1)

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
	driver.implicitly_wait(1)

	# final download button!
	footer = driver.find_element_by_class_name('rc-dialog-footer')
	download_btn = footer.find_element_by_class_name('btn-primary')
	ActionChains(driver).move_to_element(download_btn).click(download_btn).perform()

def checkTwoWayTable(scopes_container):
	try:
		scopes_container.find_element_by_css_selector('div.twoway-table')
	except:
		return False
	else:
		return True


def checkCheckBoxes(scopes_container):
	try:
		scopes_container.find_element_by_class_name('checkbox')
	except:
		return False
	else:
		return True

def checkRadioButtons(driver, scopes_container):
	try:
		print("trying")
		radio = scopes_container.find_element_by_css_selector('div.radiobutton')
	except:
		print("not found")
		return False
	else:
		print("found")
		return True

def clickShowMore(driver):
	try:
		show_more = driver.find_element_by_class_name('twoway-table-show-more')
		ActionChains(driver).move_to_element(show_more).click(show_more).perform()
		driver.implicitly_wait(1)
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
			driver.implicitly_wait(1)

def clickCheckButtons(driver, scopes_container, year):
	checkRows = scopes_container.find_elements_by_class_name('checkbox')
	for row in checkRows:
		group = row.find_element_by_class_name('checkbox-group')
		initial_check = group.find_element_by_class_name('checked')
		checkboxes = group.find_elements_by_class_name('em-checkbox')
		if("Year" in row.text or "Admin" in row.text):
			print("CLICK CHECK")
			print(row.text)
			for date in checkboxes:
				if(year in date.text):
					print(date.text)
					ActionChains(driver).move_to_element(date).click(date).perform()
					driver.implicitly_wait(1)

			soup = BeautifulSoup(initial_check.get_attribute("innerHTML"), "lxml")
			if(year not in soup.span.text):
				ActionChains(driver).move_to_element(initial_check).click(initial_check).perform()

		else:
			for column in checkboxes:
				ActionChains(driver).move_to_element(column).click(column).perform()
				driver.implicitly_wait(1)

def clickRadioButtons(driver, scopes_container, year, report_name, program_name):
	# create a list of lists with all radio buttons, then click every combination
	radio_rows = getAllRadioButtons(scopes_container)

	# select year, this might update the buttons
	selectRadioYear(driver, year, radio_rows)
	print('cliquei no ano')

	# get new rows
	radio_rows = getAllRadioButtons(scopes_container)

	# get the admin row and the rest(non year rows)
	non_year_rows = getNonYearRow(radio_rows, year)

	recursive_click(non_year_rows, driver, report_name, program_name, [], scopes_container, year)

def recursive_click(Matrix, driver, report_name, program_name, download_file_suffix, scopes_container, year, row=0):

	# there has to be an initial check to make sure it went through all the options before
	# downloading all the reports

	initial_check = False
	if len(Matrix) > row:
		#print("nova linha, montar nova matriz")
		#print(row)
		buttons_on_row = [] # clear buttons to look for
		for row_i in Matrix: #get the rows starting from the one we are at!
			buttons_on_row.append(getButtonsFromRow(row_i, year))
		time.sleep(0.5)
		for button in buttons_on_row[row]:
			if (len(download_file_suffix) == len(Matrix)):
				download_file_suffix[row] = button.text
			else:
				print(button.text, end=" APENDEU ")
				download_file_suffix.append(button.text)
				print(download_file_suffix)
			
			ActionChains(driver).move_to_element(button).click(button).perform()
			if ((len(Matrix) == row + 1) and not initial_check):
				initial_check = True
			if (initial_check):
				file_name = "_".join(str(x) for x in download_file_suffix)
				file_name = report_name + "_" + program_name + "_" + file_name
				


				# check possible check buttons here
				clickCheckButtons(driver, scopes_container, "2016")

				#loopOrganizations(driver, file_name)
			time.sleep(0.5)
			recursive_click(Matrix, driver, report_name, program_name, download_file_suffix, scopes_container, year, row+1)
	else:
		print()

def getButtonsFromRow(radio_row, year):
	group = radio_row.find_element_by_class_name('checkbox-group')
	radios = group.find_elements_by_class_name('em-checkbox')
	if("Admin" in radio_row.text):
		admin_radios = []
		for radio in radios:
			if(year in radio.text):
				admin_radios.append(radio)
		return admin_radios
	return radios

def getAllRadioButtons(scopes_container):
	return scopes_container.find_elements_by_class_name('radiobutton')

def getAdminRadioRow(radio_rows):
	admin_year =[]
	for row in radio_rows:
		group = row.find_element_by_class_name('checkbox-group')
		radio = group.find_elements_by_class_name('em-checkbox')
		if("Admin" in row.text):
			admin_year.append(radio)
	return admin_year

def getNonYearRow(radio_rows, year):
	""" this will return all the radiobutton rows that are not year dependent"""

	non_date_rows = []	
	for row in radio_rows:
		if("Year" not in row.text):
			non_date_rows.append(row)
	return non_date_rows

def selectRadioYear(driver, year, radio_rows):
	# select year, this might update the buttons
	for row in radio_rows:
		group = row.find_element_by_class_name('checkbox-group')
		radio = group.find_elements_by_class_name('em-checkbox')
		#print(row.text)
		if("Year" in row.text):
			#print(row.text)
			for date in radio:
				if(year in date.text):
					ActionChains(driver).move_to_element(date).click(date).perform()
					driver.implicitly_wait(1)
					time.sleep(3)

def selectYearTwoWay(driver, year):
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
	checkRowYearTwoWay(driver, year)

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

def makeSelections(driver, year, report_name, program_name):
	if(checkTwoWayTable(driver.find_element_by_class_name('scopes-container'))):
		selectYearTwoWay(driver, year)
	if(checkRadioButtons(driver, driver.find_element_by_class_name('scopes-container'))):
		print("we have radio!")
		clickRadioButtons(driver, driver.find_element_by_class_name('scopes-container'), year, report_name, program_name)
	else:
		clickCheckButtons(driver, driver.find_element_by_class_name('scopes-container'), year)


if __name__ == '__main__':
	driver = webdriver.Chrome('../chromedriver')
	driver.get("https://txreports.emetric.net/?domain=1&report=1")
	program_names = getProgramNames(driver)
	for program in program_names:
		selectProgram(driver, program)
		print("new program")
		sleep(1)
		reports = getReportNames(driver)
		for report in reports:
			selectReport(driver, report)
			sleep(1)
			print("New report")
			makeSelections(driver, "2016", report, program)







	