from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

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
Cannot gurantee that the range labels in the radio scale is given left and
right. So far, this seems to work however, there is no concrete proof.
Cannot get the title and description of the form.
Cannot login for you and I intend to keep it that way. (for security reasons)
"""


class Question(object):
    """The data structure for a question.

    Arguments:
    webelement    - The question's web element.
    question_type - The type of the question.

    Instance variables:
    webelement    - The webelement of the question.
    question_type - The question type. The list of types is below.
    title         - The title of the question.
    description   - The description of the question.
    required      - Whether or not the question is required.
    error         - The error message given when trying to submit the question.

    Functions:
    check_errors  - Rechecks for any error messages.

    Question Types:
    Short Text          - stext
    Long Text           - ltext
    Radio Button List   - radiolist
    Radio Button Scale  - radioscale
    Checkbox            - checkbox
    Dropdown            - dropdown

    Date (no year & time)   - date
    Date (year only)        - datey
    Date (time only)        - datet
    Date (year & time)      - dateyt

    Time (normal)           - time
    Time (duration)         - duration
    """
    def __init__(self, webelement, question_type):
        # Initialize
        super(Question, self).__init__()
        self.webelement = webelement
        self.question_type = question_type

        # Create xpaths to each of the key elements in the question
        description_xpath = './/div[@class="' \
            'freebirdFormviewerViewItemsItemItemTitleContainer"]/div[@class=' \
            '"freebirdFormviewerViewItemsItemItemHelpText"]'
        title_xpath = './/div[@class="' \
            'freebirdFormviewerViewItemsItemItemTitleContainer"]/div[@class=' \
            '"freebirdFormviewerViewItemsItemItemTitle"]'
        error_xpath = './/div[@class="' \
            'freebirdFormviewerViewItemsItemErrorMessage"]'

        # Get the elements from each of the xpaths above
        self.title = webelement.find_element_by_xpath(title_xpath).text
        self.description = webelement.find_element_by_xpath(
            description_xpath).text
        self.required = "*" in self.title
        self.error = webelement.find_element_by_xpath(error_xpath).text

    def check_errors(self):
        """Rechecks itself for error messages and stores them in self.error"""
        error_xpath = './/div[@class="' \
            'freebirdFormviewerViewItemsItemErrorMessage"]'
        self.error = webelement.find_element_by_xpath(error_xpath).text


class Question_Text(Question):
    """Class for text fields. Text fields include long answer text and short
    answer text.

    Arguments:
    webelement      - The web element of the question.
    question_type   - The question type.

    Instance variables:
    text            - The current text in the text field. Does not check on
                      creation.

    Functions:
    setText         - Set the text in the text field.

    Accepted Types:
    Short Text      - stext
    Long Text       - ltext
    """
    def __init__(self, webelement, question_type):
        # Validate the question type
        if question_type not in ["stext", "ltext"]:
            raise TypeError("Wrong Question Type. Question Type Given: " +
                            question_type)

        # Initialize
        super(Question_Text, self).__init__(webelement, question_type)
        self.text = ""

    def setText(self, text):
        """Sets the text inside the text field and resets self.text to that
        text.

        Arguments:
        text        - The new text to set to.
        """
        # Set the xpath to use accordingly
        if self.question_type == "stext":
            text_xpath = './/input[@type="text"]'
        else:
            text_xpath = './/textarea'

        # Clear and type the new text into the xpath
        self.webelement.find_element_by_xpath(text_xpath).clear()
        self.webelement.find_element_by_xpath(text_xpath).send_keys(
            text)

        # Set the self.text to the typed text
        self.text = text


class Question_List_Select(Question):
    """Class for questions that include a list of options to be selected from.
    These classes include radio lists, radio scales, checkboxes and dropdowns.

    Arguments:
    webelement      - The web element of the question.
    question_type   - The type of the question.
    driver          - The selenium web driver.

    Instance variables:
    options         - The options given in the question.
    range_labels    - The labels on the left and right respectively for radio
                      scale.
    driver          - The driver passed.

    Functions:
    select          - Select an option.

    Accepted Types:
    Radio Button List   - radiolist
    Radio Button Scale  - radioscale
    Checkbox            - checkbox
    Dropdown            - dropdown
    """
    def __init__(self, webelement, question_type, driver):
        # Validate the question type
        if question_type not in ["radiolist", "radioscale", "checkbox",
                                 "dropdown"]:
            raise TypeError("Wrong Question Type. Question Type Given: " +
                            question_type)

        # Initialize
        super(Question_List_Select, self).__init__(webelement, question_type)
        self.options = []
        self.range_labels = []
        self.driver = driver

        # Set the xpath to the options accordingly
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

        # Add range labels for radio scale
        if self.question_type == "radioscale":
            range_labels_xpath = './/div[@class="' \
                    'freebirdMaterialScalecontentRangeLabel"]'
            for i in self.webelement.find_elements_by_xpath(
                    range_labels_xpath):
                self.range_labels.append(i.text)

        # Stop here for dropdowns
        if not options_xpath:
            return

        # Add options
        for i in self.webelement.find_elements_by_xpath(options_xpath):
            self.options.append(i.text)

    def select(self, option):
        """Selects an option from the options given options.
        Arguments:
        option      - The option to select.
        """
        # Validate option
        if option not in self.options:
            raise ValueError("No such option. Option Given: " + option)

        # Set xpath to option
        option_xpath = None
        if self.question_type == "radiolist":
            option_xpath = './/div[@data-value="{0}"]/../..'
        elif self.question_type == "radioscale":
            option_xpath = './/div[text()="{0}"]/..'
        elif self.question_type == "checkbox":
            option_xpath = './/div[@data-value="{0}"]'
        else:
            # Select dropdown by clicking on it, then press down arrow until
            # item index.

            # Xpath to open close element
            toggle_open_close_xpath = './/div[@class="' \
                'docssharedWizSelectPaperselectOptionList"]/..'
            # Get open close element
            toggle_open_close = self.webelement.find_element_by_xpath(
                toggle_open_close_xpath)

            # Reset dropdown
            ActionChains(self.driver).move_to_element(
                toggle_open_close).click()
            ActionChains(self.driver).move_to_element(
                toggle_open_close).click()

            # Open dropdown
            ActionChains(self.driver).move_to_element(
                toggle_open_close).click()

            # Go to option
            for i in range(self.options.index(option)):
                ActionChains(self.driver).move_to_element(
                    toggle_open_close).send_keys(Keys.ARROW_DOWN)

            # Select option
            ActionChains(self.driver).move_to_element(
                toggle_open_close).send_keys(Keys.RETURN)

        # return if type is dropdown
        if not option_xpath:
            return

        # Click on the element
        self.webelement.find_element_by_xpath(
            option_xpath.format(option)).click()


class Question_DateTime(Question):
    """Class for date fields and their variations.
    Arguments:
    webelement      - The web element of the question.
    question_type   - The question type.
    driver          - The selenium web driver.

    Instance variables:
    day             - The current value of day. Does not check on creation.
    month           - The current value of month. Does not check on creation.
    year            - The current value of year. Only created when question
                      type is either datey or dateyt. Does not check on
                      creation.
    hour            - The current value of hour. Only created when question
                      type is time, dateyt or datet. Does not check on
                      creation.
    minute          - The current value of hour. Only created when the
                      conditions in hour is met. Does not check on creation.
    am_pm           - Whether the time given is am or pm. Only created when the
                      conditions in hour is met. Does not check on creation.
    driver          - The driver passed.

    Functions:
    setDay                  - Set the day of the time field.
    setMonth                - Set the month of the time field.
    setYear                 - Set the year of the time field.
    setTime                 - Set the hours, minutes and am or pm of the time
                              field.

    Accepted Types:
    Date (no year & time)   - date
    Date (year only)        - datey
    Date (time only)        - datet
    Date (year & time)      - dateyt
    Time (normal)           - time
    """
    def __init__(self, webelement, question_type, driver):
        # Validate the question type
        if question_type not in ["date", "datey", "datet", "dateyt", "time"]:
            raise TypeError("Wrong Question Type. Question Type Given: " +
                            question_type)

        # Initialize
        super(Question_DateTime, self).__init__(webelement, question_type)
        self.driver = driver

        # Set the appropriate instance variables
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
        """Set the day value in the time field and resets the self.day value to
        that value.

        Arguments:
        day         - The value of the day to set.
        """
        # Get the day element
        day_element = self.webelement.find_element_by_xpath(
            './/div[text()="DD"]/..//input')

        # Clear and type the new day value into the element
        day_element.clear()
        day_element.send_keys(day)

        # Reset self.day value
        self.day = day

    def setMonth(self, month):
        """Set the month value in the time field and resets the self.month
        value to that value.

        Arguments:
        month       - The value of the day to set.
        """
        # Get the month element
        month_element = self.webelement.find_element_by_xpath(
            './/div[text()="MM"]/..//input')

        # Clear and type the new month value into the element
        month_element.clear()
        month_element.send_keys(month)

        # Reset self.month value
        self.month = month

    def setYear(self, year):
        """Set the year value in the time field and resets the self.year
        value to that value.

        Arguments:
        year        - The value of the day to set.
        """
        # Get the year element
        year_element = self.webelement.find_element_by_xpath(
            './/div[text()="YYYY"]/..//input')

        # Clear and type the new year value into the element
        year_element.clear()
        year_element.send_keys(year)

        # Reset the self.year value
        self.year = year

    def setTime(self, hour, minute, am_pm):
        """Set the hour, minute, am_pm value in the time field and resets the
        self.hour, self.minute and self.am_pm values respectively.

        Arguments:
        hour        - The value of the hour to set.
        minute      - The value of the minute to set.
        am_pm       - The value of am or pm to set. Either "AM" or "PM".
        """
        # Validate am_pm argument
        am_pm = am_pm.upper()
        if am_pm not in ["AM", "PM"]:
            raise ValueError("Wrong AM_PM type. Type given: " + am_pm)

        # Base xpath for time and date
        xpath = './/div[@class="freebirdFormviewerViewItems{0}TimeInputs"]' \
            '/div/div/div/..'

        # Setup the xpath according the question type
        if self.question_type == "time":
            xpath = xpath.format("Time")
        else:
            xpath = xpath.format("Date")

        # Get all time related elements in current webelement
        elements = self.webelement.find_elements_by_xpath(xpath)

        for e in elements:
            input_element = e.find_element_by_xpath(
                ".//input[@aria-label]")
            if input_element.get_attribute("aria-label") == "Hour":
                # Element is hour element
                # Clear and type the new year into the element
                input_element.clear()
                input_element.send_keys(hour)

                # Reset the self.hour value
                self.hour = hour
            elif input_element.get_attribute("aria-label") == "Minute":
                # Element is minute element
                # Clear and type the new minute into the element
                input_element.clear()
                input_element.send_keys(minute)

                # Reset the self.minute value
                self.minute = minute
            else:
                # Element is AM_PM dropdown element
                # Xpath to open close element
                toggle_open_close_xpath = './/div[@class="' \
                    'docssharedWizSelectPaperselectOptionList"]/..'
                # Get open close element
                toggle_open_close = self.webelement.find_element_by_xpath(
                    toggle_open_close_xpath)

                # Reset dropdown
                ActionChains(self.driver).move_to_element(
                    toggle_open_close).click()
                ActionChains(self.driver).move_to_element(
                    toggle_open_close).click()

                # Open dropdown
                ActionChains(self.driver).move_to_element(
                    toggle_open_close).click()

                # Go to option
                for i in range(self.options.index(option)):
                    ActionChains(self.driver).move_to_element(
                        toggle_open_close).send_keys(Keys.ARROW_DOWN)

                # Select option
                ActionChains(self.driver).move_to_element(
                    toggle_open_close).send_keys(Keys.RETURN)

                # Reset the self.am_pm value
                self.am_pm = am_pm


class Question_Duration(Question):
    """Class for time duration.
    Arguments:
    webelement      - The web element of the question.

    Instance variables:
    hour            - The current value of hour. Does not check on creation.
    minute          - The current value of minute. Does not check on creation.
    second          - The current value of second. Does not check on creation.

    Functions:
    setDuration     - Set the hour, minute and second of the time field.

    Accepted Type:
    Time (duration)         - duration
    """
    def __init__(self, webelement):
        # Initialize
        super(Question_Duration, self).__init__(webelement, question_type)
        self.hour = -1
        self.minute = -1
        self.second = -1

    def setDuration(self, hour, minute, second):
        """Set the hour, minute, second values in the time field and resets
        self.hour, self.minute, self.second.

        Arguments:
        hour        - The value of hour to set.
        minute      - The value of minute to set.
        second      - The value of second to set.
        """
        # Get the time field elements
        elements = self.webelement.find_elements_by_xpath(
            './/input[@aria-label]')
        for e in elements:
            # Get the aria-label that indicates the type of field
            hms = e.get_attribute("aria-label")

            if hms == "Hours":
                # The element is a field for hours
                # Clear and type the new hours into the element
                e.clear()
                e.send_keys(hour)

                # Reset the self.hour value
                self.hour = hour
            elif hms == "Minutes":
                # The element is a field for minutes
                # Clear and type the new minutes into the element
                e.clear()
                e.send_keys(minute)

                # Reset the self.minute value
                self.minute = minute
            elif hms == "Seconds":
                # The element is a field for seconds
                # Clear and type the new seconds into the element
                e.clear()
                e.send_keys(second)

                # Reset the self.second value
                self.second = second


def question_type(question):
    """Determines the type of the question"""

    # Function to test existence of any web elements at the given xpath
    def test(question, xpath):
        """Returns True if web element at xpath Found else False."""
        try:
            question.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException:
            return False

    # Text Questions
    stext = './/input[@type="text" and not(@role="combobox")]'
    ltext = './/textarea'

    # List  Select Questions
    radio_list = './/content[@role="presentation"]/div[not(@class=' \
        '"freebirdMaterialScalecontentContainer")]'
    radio_scale = './/content[@role="presentation"]/div[@class=' \
        '"freebirdMaterialScalecontentContainer"]'
    checkbox = './/div[@role="group"]'
    dropdown = './/div[@role="presentation"]/div'

    # Datetime Questions
    date = './/div[@class=' \
        '"freebirdFormviewerViewItemsDateDateTimeInputs"]'
    time = './/div[@class="freebirdFormviewerViewItemsTimeTimeInputs"]' \
        '/div[@aria-label="AM or PM"]'

    # Duration Questions
    duration = './/div[@class="freebirdFormviewerViewItemsTimeTimeInputs"]' \
        '//input[@aria-label="Hours"]'

    # Return accordingly
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

    # Check whether the question is a dropdown or a date type
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

    # Return question type
    if not qt:
        return False
    else:
        return qt


class Form(object):
    """Class for handling the whole Google form

    Arguments:
    url             - The URL of the Google form.

    Instance variables:
    url             - The URL of the Google form passed.
    driver          - The selenium webdriver of the form.
    questions       - The questions in the current page of the Google form.
                      Each item in the list subclasses Question.
    prompt          - Prompts the user before loading the question. (Default to
                      False)

    Functions:
    reload_questions    - Reload the questions in the Google form. This is done
                          automatically when the class is instantiated (unless
                          prompt is not False) and when `submit` is called.
    submit              - Either submits or clicks on the next page button.
    """

    def __init__(self, url, prompt=False):
        # Initialize
        self.url = url

        # Create selenium webdriver
        self.driver = webdriver.Firefox()
        # Go to url
        self.driver.get(url)

        # Prompt if needed
        if prompt:
            raw_input(prompt)

        # Populate self.questions
        self.reload_questions()

    def reload_questions(self):
        """Reloads the questions in the current page of the webdriver and
        resets self.questions."""
        # Reset self.questions
        self.questions = []

        # Set the general xpath to all questions
        questions_xpath = './/form//div[@class="' \
            'freebirdFormviewerViewItemList"]/div'

        # Create the necessary classes for each question and add them to
        # self.questions.
        for question in self.driver.find_elements_by_xpath(questions_xpath):
            qt = question_type(question)
            # Sort the question type
            if qt in ["stext", "ltext"]:
                self.questions.append(Question_Text(question, qt))
            elif qt in ["radiolist", "radioscale", "dropdown", "checkbox"]:
                self.questions.append(
                    Question_List_Select(question, qt, self.driver))
            elif qt in ["date", "datey", "dateyt", "datet", "time"]:
                self.questions.append(
                    Question_DateTime(question, qt, self.driver))
            elif qt == "duration":
                self.questions.append(Question_Duration(question))

            # Other "questions" are extra items such as pictures, videos and
            # information text.

            # TODO Add extras

    def submit(self):
        """Submits or moves the form to the next page by clicking on the submit
        or next button. Returns False if there is an error, True otherwise."""
        # Set the xpath to the submit or next button
        submit_xpath = './/span[@class="quantumWizButtonPaperbuttonLabel"' \
            ' and (text()="Next" or text()="Submit")]'

        # Click on the button
        self.driver.find_element_by_xpath(submit_xpath).click()

        # Reload and check the questions for error messages
        self.reload_questions()
        for i in self.questions:
            if i.error != "":
                return False
        return True

    def quit(self):
        """Quit the selenium webdriver."""
        self.driver.quit()
