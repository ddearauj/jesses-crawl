from time import sleep
from selenium import webdriver
from orgs import loopOrganizations


def initDriver():
	driver = webdriver.Chrome('../chromedriver')
	driver.get("https://txreports.emetric.net/?domain=1&report=1")
	return driver

def main():
	driver = initDriver()
	loopOrganizations(driver)

if __name__ == '__main__':
	main()
