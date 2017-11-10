from time import sleep
from selenium import webdriver
from orgs import loopOrganizations
from txreports import getProgramNames, getReportNames, selectProgram, selectReport
from selections import makeSelections


def initDriver():
	driver = webdriver.Chrome('../chromedriver')
	driver.get("https://txreports.emetric.net/?domain=1&report=1")
	return driver

def main():
	driver = initDriver()
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

if __name__ == '__main__':
	main()
