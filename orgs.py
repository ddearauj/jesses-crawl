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
import time 


def selectOrg(driver, last_element=None):
	""" selected orgs is the number of orgs that have already been selected from the list """

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
	# loaded_following = driver.find_elements_by_xpath("//ul[@class='_539vh _4j13h']/li")
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


	# we can get the last element loaded and return it after the function ends
	# then, next time, we scroll until we hit that element.
	# Since once we hit it, it will be the last one and we need to go deeper,
	# We can scroll until the element is no more visible



	#this part does not laod instantly so:

	wait = WebDriverWait(driver, 10)
	wait.until(
		EC.presence_of_element_located((By.CLASS_NAME, "orgtree-body-normal"))
	)

	orgtree = driver.find_element_by_class_name('orgtree-body-normal')
	last_scroll = False
	done = False

	campi = orgtree.find_elements_by_class_name('orgtree-body-item')
	if last_element == None:
		last_element = clickOrgs(driver, campi)

	else:
		# set focus on the list
		#list_focus = driver.find_element_by_class_name("orgtree-body-normal-list")
		#ActionChains(driver).move_to_element(list_focus).click(list_focus).perform()
		ActionChains(driver).move_to_element(driver.find_element_by_class_name("orgtree-body-normal-list"))
		last_name = orgtree.find_element_by_class_name('orgtree-body-item')
		last_name = last_name.find_element_by_class_name('checkable')
		soup = BeautifulSoup(last_name.get_attribute("innerHTML"), "lxml")
		print(soup.span.text)

		while(soup.span.text != last_element):
			# scroll down!
			#driver.find_element_by_class_name("orgtree-body-normal-list").send_keys(Keys.ARROW_DOWN).perform()
			last_name = orgtree.find_element_by_class_name('orgtree-body-item')
			last_name = last_name.find_element_by_class_name('checkable')
			soup = BeautifulSoup(last_name.get_attribute("innerHTML"), "lxml")
			# final_soup = BeautifulSoup(end_of_list.get_attribute("innerHTML"), "lxml")

			print("soup: %s vs. last_element: %s" % (soup.span.text, last_element))
			# print("end_of_list: %s vs. last_element: %s " % (final_soup.span.text, last_element))
			# if(final_soup.span.text == last_element):
			# 	print("END OF LIST REACHED")
			# 	break

			if(checkEndScroll(driver, driver.find_element_by_class_name("orgtree-body-normal-list"))):
			#driver.execute_script("arguments[0].scrollBy(0,40);", driver.find_element_by_class_name("orgtree-body-normal-list"))
				last_scroll = True
				break

			time.sleep(0.01)
		campi = orgtree.find_elements_by_class_name('orgtree-body-item')

		if last_scroll:
			getOrgsLastScroll(driver, last_element, campi)
			done = True

		else:
			last_element = clickOrgs_v2(driver, campi)

	return last_element, done
	
def selectOrg_noClick(driver, last_element=None):
	""" For testing purposes only!"""


	#this part does not laod instantly so:

	wait = WebDriverWait(driver, 10)
	wait.until(
		EC.presence_of_element_located((By.CLASS_NAME, "orgtree-body-normal"))
	)

	orgtree = driver.find_element_by_class_name('orgtree-body-normal')
	last_scroll = False
	done = False

	campi = orgtree.find_elements_by_class_name('orgtree-body-item')
	if last_element == None:
		last_element = clickOrgs(driver, campi)

	else:
		# set focus on the list
		#list_focus = driver.find_element_by_class_name("orgtree-body-normal-list")
		#ActionChains(driver).move_to_element(list_focus).click(list_focus).perform()
		ActionChains(driver).move_to_element(driver.find_element_by_class_name("orgtree-body-normal-list"))
		last_name = orgtree.find_element_by_class_name('orgtree-body-item')
		last_name = last_name.find_element_by_class_name('checkable')
		soup = BeautifulSoup(last_name.get_attribute("innerHTML"), "lxml")
		print(soup.span.text)

		while(soup.span.text != last_element):
			# scroll down!
			#driver.find_element_by_class_name("orgtree-body-normal-list").send_keys(Keys.ARROW_DOWN).perform()
			last_name = orgtree.find_element_by_class_name('orgtree-body-item')
			last_name = last_name.find_element_by_class_name('checkable')
			soup = BeautifulSoup(last_name.get_attribute("innerHTML"), "lxml")
			# final_soup = BeautifulSoup(end_of_list.get_attribute("innerHTML"), "lxml")

			print("soup: %s vs. last_element: %s" % (soup.span.text, last_element))
			# print("end_of_list: %s vs. last_element: %s " % (final_soup.span.text, last_element))
			# if(final_soup.span.text == last_element):
			# 	print("END OF LIST REACHED")
			# 	break

			if(checkEndScroll(driver, driver.find_element_by_class_name("orgtree-body-normal-list"))):
			#driver.execute_script("arguments[0].scrollBy(0,40);", driver.find_element_by_class_name("orgtree-body-normal-list"))
				last_scroll = True
				break

			time.sleep(0.01)
		campi = orgtree.find_elements_by_class_name('orgtree-body-item')

		if last_scroll:
			getOrgsLastScroll(driver, last_element, campi)
			done = True

		else:
			# skips the last element
			last_element = clickOrgs_v2(driver, campi)

	return last_element, done

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

def clickOrgs(driver, list_orgs):
	for idx, campus in enumerate(list_orgs):
		if(idx < 20):
			ActionChains(driver).move_to_element(campus).click(campus).perform()
			print("clicked %s" %idx)
			name = campus.find_element_by_class_name('checkable')
			soup = BeautifulSoup(name.get_attribute("innerHTML"), "lxml")
			print(soup.span.text)
			last_element = soup.span.text

	return last_element

def clickOrgs_v2(driver, list_orgs):
	for idx, campus in enumerate(list_orgs):
		if(idx > 0 and idx < 21):
			ActionChains(driver).move_to_element(campus).click(campus).perform()
			print("clicked %s" %idx)
			name = campus.find_element_by_class_name('checkable')
			soup = BeautifulSoup(name.get_attribute("innerHTML"), "lxml")
			print(soup.span.text)
			last_element = soup.span.text

	return last_element

def checkEndScroll(driver, element):
	old = driver.execute_script("return arguments[0].scrollTop;", element)
	driver.execute_script("arguments[0].scrollBy(0,40);", element)
	
	if (driver.execute_script("return arguments[0].scrollTop;", element) > old):
		return(False)
	else:
		print("Acabou!")
		return(True)

def clickClear(driver):
	driver.find_element_by_class_name('orgtree-selector-tool-clear').click()

def loopOrganizations(driver, file_name):

	done = False
	last_element, done = selectOrg(driver)
	getReport(driver, file_name)
	driver.execute_script("window.history.go(-1)")
	clear_orgs(driver)

	while(not done):
		last_element, done = selectOrg(driver, last_element=last_element)
		getReport(driver, file_name)
		print("got report!!")
		driver.execute_script("window.history.go(-1)")
		clear_orgs(driver)
		print("new loop")

def clearOrgs(driver):
	clear = driver.find_element_by_class_name('orgtree-selector-tool-clear-text')
	ActionChains(driver).move_to_element(clear).click(clear).perform()
