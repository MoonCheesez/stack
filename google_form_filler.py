"""
IMPORTANT: When giving this out, please change the name.
"""

"""
MIT License

Copyright (c) 2016 MoonCheesez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Current features of the program:
Fills out every part of the google form for you.
Able to click on the "next" or "submit" button and tell you whether it is
successful
Able to tell you which questions have errors when trying to submit

What it CANNOT do:
Cannot fill out dropdowns.
Cannot gurantee that the range labels in the radio scale is given left and
right. So far, this seems to work however, there is no concrete proof.
Cannot get the title and description of the form.
Cannot login for you and I intend to keep it that way. (for security reasons)
"""

from selenium.common.exceptions import NoSuchElementException

class Question(object):
	"""The data structure for a question.
	Types:
	Short Text 			- stext
	Long Text 			- ltext
	Radio Button List 	- radiolist
	Radio Button Scale 	- radioscale
	Checkbox 			- checkbox
	Dropdown 			- dropdown

	Date (no year & time)	- date
	Date (year only)		- datey
	Date (time only)		- datet
	Date (year & time)		- dateyt

	Time (normal)			- time
	Time (duration)			- duration
	"""
	def __init__(self, webelement, question_type):
		super(Question, self).__init__()
		self.webelement = webelement
		self.question_type = question_type

		description_xpath = './/div[@class="' \
		'freebirdFormviewerViewItemsItemItemTitleContainer"]/div[@class="' \
		'freebirdFormviewerViewItemsItemItemHelpText"]'
		title_xpath = './/div[@class="' \
		'freebirdFormviewerViewItemsItemItemTitleContainer"]/div[@class="' \
		'freebirdFormviewerViewItemsItemItemTitle"]'
		error_xpath = './/div[@class="' \
		'freebirdFormviewerViewItemsItemErrorMessage"]'

		self.title = webelement.find_element_by_xpath(title_xpath).text
		self.description = webelement.find_element_by_xpath(
			description_xpath).text
		self.required = "*" in self.title
		self.error = webelement.find_element_by_xpath(error_xpath).text

	def check_errors(self):
		error_xpath = './/div[@class="' \
		'freebirdFormviewerViewItemsItemErrorMessage"]'
		self.error = webelement.find_element_by_xpath(error_xpath).text

class Question_Text(Question):
	"""Class for text fields.
	Types:
	Short Text 			- stext
	Long Text 			- ltext

	Actions:
	setText(text)
	"""
	def __init__(self, webelement, question_type):
		if question_type not in ["stext", "ltext"]:
			raise TypeError("Wrong Question Type. Question Type Given: " +
				question_type)

		super(Question_Text, self).__init__(webelement, question_type)
		self.text = ""

	def setText(self, text):
		if self.question_type == "stext":
			text_xpath = './/input[@type="text"]'
		else:
			text_xpath = './/textarea'

		# Is there a need to click first?
		# self.webelement.find_element_by_xpath(text_xpath).click()
		self.webelement.find_element_by_xpath(text_xpath).clear()
		self.webelement.find_element_by_xpath(text_xpath).send_keys(
			text)

		self.text = text

class Question_List_Select(Question):
	"""Class for radio, checkbox and dropdowns.
	Types:
	Radio Button List 	- radiolist
	Radio Button Scale 	- radioscale
	Checkbox 			- checkbox
	Dropdown 			- dropdown

	Actions:
	select(option)
	"""
	def __init__(self, webelement, question_type, driver):
		if question_type not in ["radiolist", "radioscale", "checkbox",
		  "dropdown"]:
			raise TypeError("Wrong Question Type. Question Type Given: " +
				question_type)

		super(Question_List_Select, self).__init__(webelement, question_type)
		self.options = []
		self.range_labels = []
		self.driver = driver

		options_xpath = None
		if self.question_type == "radiolist":
			options_xpath = './/div[not(@role="heading")]/span[text()]'
		elif self.question_type == "radioscale":
			options_xpath = './/label/div[text()]'
		elif self.question_type == "checkbox":
			options_xpath = './/div[not(@role="heading")]/span'
		else:
			self.options.append("Choose")
			for i in self.webelement.find_elements_by_xpath(
			  './/div[@role="option"]/content/..')[1:]:
				self.options.append(i.get_attribute("data-value"))

		if self.question_type == "radioscale":
			range_labels_xpath = './/div[@class="freebirdMaterialScalecontentRangeLabel"]'
			for i in self.webelement.find_elements_by_xpath(range_labels_xpath):
				self.range_labels.append(i.text)

		if not options_xpath:
			return

		for i in self.webelement.find_elements_by_xpath(options_xpath):
			self.options.append(i.text)

	def select(self, option):
		if option not in self.options:
			raise ValueError("No such option. Option Given: " + option)

		option_xpath = None
		if self.question_type == "radiolist":
			option_xpath = './/div[@data-value="{0}"]/../..'
		elif self.question_type == "radioscale":
			option_xpath = './/div[text()="{0}"]/..'
		elif self.question_type == "checkbox":
			option_xpath = './/div[@data-value="{0}"]'
		else:
			# The dropdown can only work by removing and adding
			# classes to the element

			# Get the selected element
			selected = self.webelement.find_element_by_xpath(
				'.//div[contains(@class, "isSelected")]')
			# Parent data-item-id
			current_data_id = self.webelement.get_attribute(
				"data-item-id")

			# xpath of currently selected element
			xpath = ".//div[@data-item-id={0}]//div[contains(@class, " \
			"'isSelected')]".format(current_data_id)
			# Remove isSelected class
			script = "document.evaluate(\"{0}\", document, null, " \
			"XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue" \
			".className"
			script = script.format(xpath)
			script = script + " = " + script + ".replace('isSelected'" \
			", '')"
			self.driver.execute_script(script)

			# Choose has no data-value
			if option == "Choose":
				option = ""
			# xpath of element to be selected
			xpath = ".//div[@data-item-id={0}]//div[@data-value='" \
			"{1}']".format(current_data_id, option)
			# Add isSelected class
			script = "document.evaluate(\"{0}\", document, null, " \
			"XPathResult.FIRST_ORDERED_NODE_TYPE, null)" \
			".singleNodeValue.className += ' isSelected'".format(xpath)
			self.driver.execute_script(script)

		# return if type is dropdown
		if not option_xpath:
			return
		
		# Click on the element
		self.webelement.find_element_by_xpath(
			option_xpath.format(option)).click()

class Question_DateTime(Question):
	"""Class for dates
	Types:
	Date (no year & time)	- date
	Date (year only)		- datey
	Date (time only)		- datet
	Date (year & time)		- dateyt
	Time (normal)			- time

	Actions:
	setDay(day)
	setMonth(month)
	setYear(year)
	setTime(hour, minute, am_pm)
	"""
	def __init__(self, webelement, question_type, driver):
		if question_type not in ["date", "datey", "datet", "dateyt", "time"]:
			raise TypeError("Wrong Question Type. Question Type Given: " +
				question_type)

		super(Question_DateTime, self).__init__(webelement, question_type)
		self.driver = driver

		if question_type != "time":
			self.day = -1
			self.month = -1
		if "y" in question_type:
			self.year = -1
		if question_type.endswith("t") or question_type == "time":
			self.hour = -1
			self.minute = -1
			self.am_pm = None

	def setDay(self, day):
		day_element = self.webelement.find_element_by_xpath(
			'.//div[text()="DD"]/..//input')

		day_element.clear()
		day_element.send_keys(day)
		
		self.day = day
	def setMonth(self, month):
		month_element = self.webelement.find_element_by_xpath(
			'.//div[text()="MM"]/..//input')

		month_element.clear()
		month_element.send_keys(month)

		self.month = month
	def setYear(self, year):
		year_element = self.webelement.find_element_by_xpath(
			'.//div[text()="YYYY"]/..//input')

		year_element.clear()
		year_element.send_keys(year)

		self.year = year
	def setTime(self, hour, minute, am_pm):
		# Check am_pm
		am_pm = am_pm.upper()
		if am_pm not in ["AM", "PM"]:
			raise ValueError("Wrong AM_PM type. Type given: " + am_pm)

		xpath = './/div[@class="freebirdFormviewerViewItems{0}TimeInputs"]' \
			'/div/div/div/..'

		if self.question_type == "time":
			xpath = xpath.format("Time")
		else:
			xpath = xpath.format("Date")

		# Get all time elements in current webelement
		elements = self.webelement.find_elements_by_xpath(xpath)

		for e in elements:
			try:
				input_element = e.find_element_by_xpath(
					".//input[@aria-label]") 
				if input_element.get_attribute("aria-label") == "Hour":
					input_element.clear()
					input_element.send_keys(hour)
					self.hour = hour
				elif input_element.get_attribute("aria-label") == "Minute":
					# Minute
					input_element.clear()
					input_element.send_keys(minute)
					self.minute = minute
				else:
					raise NoSuchElementException

			except NoSuchElementException:
				# Get the selected element
				selected = e.find_element_by_xpath(
					'.//div[contains(@class, "isSelected")]')
				# Parent data-item-id
				current_data_id = self.webelement.get_attribute("data-item-id")

				# xpath of currently selected element
				xpath = ".//div[@data-item-id={0}]//div[contains(@class, " \
				"'isSelected')]".format(current_data_id)
				# Remove isSelected class
				script = "document.evaluate(\"{0}\", document, null, " \
				"XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue" \
				".className"
				script = script.format(xpath)
				script = script + " = " + script + ".replace('isSelected'" \
				", '')"
				self.driver.execute_script(script)
				
				# xpath of element to be selected
				xpath = ".//div[@data-item-id={0}]//div[@data-value='" \
				"{1}']".format(current_data_id, am_pm)
				# Add isSelected class
				script = "document.evaluate(\"{0}\", document, null, " \
				"XPathResult.FIRST_ORDERED_NODE_TYPE, null)" \
				".singleNodeValue.className += ' isSelected'".format(xpath)
				self.driver.execute_script(script)
				self.am_pm = am_pm

class Question_Duration(Question):
	"""Class for duration
	Type:
	Time (duration)		- duration
	
	Actions:
	setDuration(hour, minute, second)
	"""
	def __init__(self, webelement, question_type):
		if question_type != "duration":
			raise TypeError("Wrong Question Type. Question Type Given: " +
				question_type)

		super(Question_Duration, self).__init__(webelement, question_type)
		self.hour = -1
		self.minute = -1
		self.second = -1

	def setDuration(self, hour, minute, second):
		elements = self.webelement.find_elements_by_xpath(
			'.//input[@aria-label]')
		for e in elements:
			hms = e.get_attribute("aria-label")
			if hms == "Hours":
				e.clear()
				e.send_keys(hour)
				self.hour = hour
			elif hms == "Minutes":
				e.clear()
				e.send_keys(minute)
				self.minute = minute
			elif hms == "Seconds":
				e.clear()
				e.send_keys(second)
				self.second = second

def question_type(question):
	def test(question, xpath):
		try:
			question.find_element_by_xpath(xpath)
			return True
		except NoSuchElementException:
			return False

	"""Determines the type of the question"""
	stext = './/input[@type="text" and not(@role="combobox")]'
	ltext = './/textarea'
	radio_list = './/content[@role="presentation"]/div[not(@class=' \
	'"freebirdMaterialScalecontentContainer")]'
	radio_scale = './/content[@role="presentation"]/div[@class=' \
	'"freebirdMaterialScalecontentContainer"]'
	checkbox = './/div[@role="group"]'
	dropdown = './/div[@role="presentation"]/div'
	date = './/div[@class=' \
	'"freebirdFormviewerViewItemsDateDateTimeInputs"]'
	time = './/div[@class="freebirdFormviewerViewItemsTimeTimeInputs"]' \
	'/div[@aria-label="AM or PM"]'
	duration = './/div[@class=' \
	'"freebirdFormviewerViewItemsTimeTimeInputs"]//input[@aria-label="Hours"]'

	if test(question, stext):
		return "stext"
	elif test(question, ltext):
		return "ltext"
	elif test(question, radio_list):
		return "radiolist"
	elif test(question, radio_scale):
		return "radioscale"
	elif test(question, checkbox):
		return "checkbox"
	elif test(question, time):
		return "time"
	elif test(question, duration):
		return "duration"

	qt = ""
	if test(question, dropdown):
		qt = "dropdown"
	if test(question, date):
		qt = "date"
		if question.find_element_by_xpath(date + "/div").get_attribute(
			"data-includeyear"):
			qt += "y"
		if len(question.find_elements_by_xpath(date + "/div")) == 2:
			qt += "t"

	if not qt:
		return False
	else:
		return qt

class Form(object):

	def __init__(self, url):
		self.url = url
		self.driver = webdriver.Firefox()
		# Setup
		self.driver.get(url)
		# Allow user to login
		input("Ready? ")
		self.reload_questions()
		
	def reload_questions(self):
		# Get questions
		questions_xpath = './/form//div[@class="' \
		'freebirdFormviewerViewItemList"]/div'
		self.questions = []
		for question in self.driver.find_elements_by_xpath(questions_xpath):
			qt = question_type(question)
			if qt in ["stext", "ltext"]:
				self.questions.append(Question_Text(question, qt))
			elif qt in ["radiolist", "radioscale", "dropdown", "checkbox"]:
				self.questions.append(
					Question_List_Select(question, qt, self.driver))
			elif qt in ["date", "datey", "dateyt", "datet", "time"]:
				self.questions.append(
					Question_DateTime(question, qt, self.driver))
			elif qt == "duration":
				self.questions.append(Question_Duration(question, qt))

	def submit(self):
		submit_xpath = './/span[@class="quantumWizButtonPaperbuttonLabel"' \
		' and (text()="Next" or text()="Submit")]'

		self.driver.find_element_by_xpath(submit_xpath).click()
		self.reload_questions()
		for i in self.questions:
			if i.error != "":
				return False
		return True

	def quit(self):
		self.driver.quit()

from selenium import webdriver

url = "https://docs.google.com/a/s2014.sst.edu.sg/forms/d/e/1FAIpQLScw10fAih4wUP45kl1TIUnGYbVCsLtgFvBx8wYOb_pom1QZIw/viewform"
form = Form(url)
