from txreports import getProgramNames, getReportNames, selectProgram, selectReport, getReport
from time import sleep
from selenium import webdriver


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
		# added the sleeps so the video would not be too fast
		sleep(2)
		reports = getReportNames(driver)
		for report in reports:
			selectReport(driver, report)
			sleep(2)
			print("New report")

if __name__ == '__main__':
	main()
