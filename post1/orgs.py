from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 


def selectOrg(driver, last_element=None, position=None):
	""" last_element is the last clicked element from the previous iteration """

	#this part does not laod instantly so:
	wait = WebDriverWait(driver, 10)
	wait.until(
		EC.presence_of_element_located((By.CLASS_NAME, "orgtree-body-normal"))
	)

	orgtree = driver.find_element_by_class_name('orgtree-body-normal')
	last_scroll = False
	done = False

	org = orgtree.find_elements_by_class_name('orgtree-body-item')
	element = driver.find_element_by_class_name("orgtree-body-normal-list")
	if last_element == None:
		last_element, position = clickOrgs(driver, org, element)

	else:
		# set focus on the list
		ActionChains(driver).move_to_element(element)
		last_loaded_org_list = orgtree.find_element_by_class_name('orgtree-body-item')
		last_loaded_org_list = last_loaded_org_list.find_element_by_class_name('checkable')
		soup = BeautifulSoup(last_loaded_org_list.get_attribute("innerHTML"), "lxml")
		print(soup.span.text)

		while(soup.span.text != last_element):
			last_loaded_org_list = orgtree.find_element_by_class_name('orgtree-body-item')
			last_loaded_org_list = last_loaded_org_list.find_element_by_class_name('checkable')
			soup = BeautifulSoup(last_loaded_org_list.get_attribute("innerHTML"), "lxml")
			print("soup: %s vs. last_element: %s" % (soup.span.text, last_element))
			if(checkEndScroll(driver, element, position)):
				last_scroll = True
				break
			time.sleep(0.01)
		org = orgtree.find_elements_by_class_name('orgtree-body-item')

		if last_scroll:
			getOrgsLastScroll(driver, last_element, org)
			done = True

		else:
			last_element, position = clickOrgs_v2(driver, org, element)

	return last_element, done, position
	
def getOrgsLastScroll(driver, last_org, list_orgs):
	""" last org is a str and list of orgs is a list of webElements """

	# what we need to do is go through the list of orgs until we hit the one we have seen before

	#	iterate over a copy of the list so we can remove things
	for org in list(list_orgs):
		name = org.find_element_by_class_name('checkable')
		soup = BeautifulSoup(name.get_attribute("innerHTML"), "lxml")
		name = soup.span.text

		if (name != last_org):
			list_orgs.remove(org)
		else:
			list_orgs.remove(org)
			break

	for idx, campus in enumerate(list_orgs):
		if(idx < 20):
			ActionChains(driver).move_to_element(campus).click(campus).perform()
			print("clicked %s" %idx)
			name = campus.find_element_by_class_name('checkable')
			soup = BeautifulSoup(name.get_attribute("innerHTML"), "lxml")
			print(soup.span.text)
			last_element = soup.span.text

def clickOrgs(driver, list_orgs, element):
	for idx, campus in enumerate(list_orgs):
		if(idx < 20):
			ActionChains(driver).move_to_element(campus).click(campus).perform()
			print("clicked %s" %idx)
			name = campus.find_element_by_class_name('checkable')
			soup = BeautifulSoup(name.get_attribute("innerHTML"), "lxml")
			print(soup.span.text)
			last_element = soup.span.text
			position = driver.execute_script("return arguments[0].scrollTop;", element)
			print(position)

	return last_element, position

def clickOrgs_v2(driver, list_orgs, element):
	for idx, campus in enumerate(list_orgs):
		if(idx > 0 and idx < 21):
			ActionChains(driver).move_to_element(campus).click(campus).perform()
			print("clicked %s" %idx)
			name = campus.find_element_by_class_name('checkable')
			soup = BeautifulSoup(name.get_attribute("innerHTML"), "lxml")
			print(soup.span.text)
			last_element = soup.span.text
			position = driver.execute_script("return arguments[0].scrollTop;", element)
			print(position)

	return last_element, position

def checkEndScroll(driver, element, position=None):
	old = driver.execute_script("return arguments[0].scrollTop;", element)
	print("old: %s x %s element" % (old, position))
	if (position > old):
		driver.execute_script("arguments[0].scrollBy(0,arguments[1]);", element, position)
	else:
		driver.execute_script("arguments[0].scrollBy(0,40);", element)
	
	if (driver.execute_script("return arguments[0].scrollTop;", element) > old):
		return(False)
	else:
		print("Acabou!")
		return(True)

def resetPosition(driver, element):
	driver.execute_script("arguments[0].scrollTo(0, 0);", element)

def loopOrganizations(driver, last_element=None, position=None):

	done = False
	last_element, done, position = selectOrg(driver, last_element=last_element)
	element = driver.find_element_by_class_name("orgtree-body-normal-list")

	while(not done):
		# when we get the report, it takes us to a new page, when we return to this one we lose the
		# organizations that were clicked, so to simulate this, we reset the orgs scroll position
		clearOrgs(driver)
		resetPosition(driver, element)

		# just so it is easier to see what is going on, you can comment this if you want
		time.sleep(1)

		last_element, done, position = selectOrg(driver, last_element=last_element, position=position)

def clearOrgs(driver):
	clear = driver.find_element_by_class_name('orgtree-selector-tool-clear-text')
	ActionChains(driver).move_to_element(clear).click(clear).perform()
