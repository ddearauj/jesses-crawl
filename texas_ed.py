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
import time 


def clickShowMore(driver):

	try:
		show_more = driver.find_element_by_class_name('twoway-table-show-more')
		ActionChains(driver).move_to_element(show_more).click(show_more).perform()
		driver.implicitly_wait(10)
	except Exception as e:
		print("The option is not available, so no click needed")

def checkRowYear(driver, year):

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


def selectOrg(driver, selected_orgs):
	""" selected orgs is the number of orgs that have already been selected from the list """


	#this part does not laod instantly so:

	wait = WebDriverWait(driver, 10)
	wait.until(
    	EC.presence_of_element_located((By.CLASS_NAME, "orgtree-body-normal"))
	)

	orgtree = driver.find_element_by_class_name('orgtree-body-normal')
	#state = orgtree.find_element_by_class_name('expand-checkbox-input')
	#print(state.text)
	#ActionChains(driver).move_to_element(state).click(state).perform()

	# the page does not load all the orgs automatically, we must scroll the div
	# it loads dinamically so we cant just scroll all the way down
	# fuck, this is going to be hard
	# I do have an idea, we can click the scroller and press the down arrow.
	# Doing that, the only thing left is to ensure we now if the div changed or not
	# Which means they loaded something new


	# This guy did something similar for instagram.
	# So we can work with something like he did
	# 	loaded_following = driver.find_elements_by_xpath("//ul[@class='_539vh _4j13h']/li")
	# loaded_till_now = len(loaded_following)

	# while(loaded_till_now<total_following):
	#     print "following users loaded till now: ", loaded_till_now
	#     print loaded_following[loaded_till_now-1]
	#     loaded_following[loaded_till_now-1].location_once_scrolled_into_view
	#     # driver.execute_script("arguments[0].focus();", loaded_following[loaded_till_now-1])
	#     driver.find_element_by_tag_name('body').send_keys(Keys.END) # triggers AJAX request to load more users. observed that loading 10 users at a time.
	#     sleep(1) # tried wihtout sleep but throws StaleElementReferenceException. As it takes time to get the resposne and update the DOM
	#     loaded_following = driver.find_elements_by_xpath("//ul[@class='_539vh _4j13h']/li")
	#     loaded_till_now = len(loaded_following)

	# # All 239 users are loaded. 
	# driver.quit()

	campi = orgtree.find_elements_by_class_name('orgtree-body-item')
	for idx, campus in enumerate(campi):
		if(idx >= selected_orgs and (idx - selected_orgs) < 20):
			ActionChains(driver).move_to_element(campus).click(campus).perform()
			total_selected = idx
			print("clicked %s" %idx)
		print(idx)

	return total_selected + 1


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
	initDriver()
	year = "2016"
	# get programs
	# for program in programs
	#	get reports
	#   for report in reports

driver = initDriver()
# program_names = getProgramNames(driver)
# report_names = getReportNames(driver)
year = "2016"
selected_orgs = 19
selectYear(driver, year)
checkSubjects(driver)
print(selectOrg(driver, selected_orgs))
time.sleep(10)
getReport(driver, "test_one_more_time")







driver.stop_client()
driver.close()