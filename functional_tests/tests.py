from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import unittest

MAX_WAIT = 10


class WebPageTest(StaticLiveServerTestCase):

    def setUp(self):
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.browser = webdriver.Firefox(options = options)
        # self.browser.get('file:///C:/Users/bielm/webcoding/project-1-Gabrielmbl/my_app/templates/creativename.html')


    def tearDown(self):
        self.browser.quit()


    def test_web_page(self):
        # Checking title
        self.browser.get(self.live_server_url)
        self.assertIn('creativename', self.browser.title.lower())
    
    def wait_for_row_in_thread_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_messages_table')
                rows = table.find_elements_by_tag_name('tr')
                rows_text = [row.text for row in rows]
                self.assertIn(row_text, ' '.join(rows_text))
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_create_a_thread_and_retrieve_it_later(self):
        # Lucas has heard about a forum called CreativeName and goes to check it out.
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention CreativeName
        self.assertIn('CreativeName', self.browser.title)

        # He sees the "Who's Speaking" box and types in his name
        username_box = self.browser.find_element_by_id('id_user')
        self.assertEqual(
            username_box.get_attribute('placeholder'),
            "Who's speaking?"
        )

        username_box.send_keys('Lucas')

        # He is invited to enter a subject title straight away
        subjectbox = self.browser.find_element_by_id('id_new_subject')
        self.assertEqual(
            subjectbox.get_attribute('placeholder'),
            'Thread subject'
        )

        # He types "My first thread" into the subject title box
        subjectbox.send_keys('My first thread')

        # He is invited to enter a message 
        inputbox = self.browser.find_element_by_id('id_new_message')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'What are you thinking?'
        )

        # He types "Hey" into a text box
        inputbox.send_keys('Hey')
        submit_button = self.browser.find_element_by_id('submit_button')

        # When he hits submit, he is redirected to his thread page,
        # and this page displays his message
        submit_button.send_keys(Keys.ENTER)
        time.sleep(1)

        self.wait_for_row_in_thread_table('Lucas')
        self.wait_for_row_in_thread_table('Hey')

        # There is still a text box inviting him to add another message. He
        # enters "My second message"

        username_box = self.browser.find_element_by_id('id_user')
        username_box.send_keys('Lucas')
        inputbox = self.browser.find_element_by_id('id_new_message')
        inputbox.send_keys('My second message')
        submit_button = self.browser.find_element_by_id('submit_button') 
        submit_button.send_keys(Keys.ENTER)

        # The page updates, and now shows both messages under the thread
        self.wait_for_row_in_thread_table('Hey')
        self.wait_for_row_in_thread_table('My second message')

    def test_multiple_users_can_start_threads_at_different_urls(self):
        # Lucas starts a new thread
        self.browser.get(self.live_server_url)

        username_box = self.browser.find_element_by_id('id_user')
        username_box.send_keys('Lucas')
        subject_inputbox = self.browser.find_element_by_id('id_new_subject')
        subject_inputbox.send_keys('Random subject')
        inputbox = self.browser.find_element_by_id('id_new_message')
        inputbox.send_keys('Hey')
        submit_button = self.browser.find_element_by_id('submit_button') 
        submit_button.send_keys(Keys.ENTER)

        self.wait_for_row_in_thread_table('Hey')

        # He notices that his list has a unique URL
        lucas_thread_url = self.browser.current_url
        self.assertRegex(lucas_thread_url, '/my_app/.+')

        # Now a new user, Pedro, comes along to the site

        ## We use a new browser session to make sure that no information 
        ## of Lucas' is coming through from cookies etc.

        self.browser.quit()
        options = Options()
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        self.browser = webdriver.Firefox(options=options)

        # Pedro visits the home page. There is no sign of Lucas' thread's message
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Hey', page_text)

        # Pedro starts a new thread by entering a new message
        username_box = self.browser.find_element_by_id('id_user')
        username_box.send_keys('Pedro')
        subject_inputbox = self.browser.find_element_by_id('id_new_subject')
        subject_inputbox.send_keys("Pedro's subject")
        inputbox = self.browser.find_element_by_id('id_new_message')
        inputbox.send_keys('Hello')
        submit_button = self.browser.find_element_by_id('submit_button') 
        submit_button.send_keys(Keys.ENTER)

        self.wait_for_row_in_thread_table('Hello')
        
        # Pedro gets his own unique URL
        pedro_thread_url = self.browser.current_url
        self.assertRegex(pedro_thread_url, '/my_app/.+')
        self.assertNotEqual(pedro_thread_url, lucas_thread_url)

        # Again, there is no trace of Lucas' thread's message
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Hey', page_text)
        self.assertIn('Hello', page_text)
  


if __name__ == '__main__':
    unittest.main(warnings='ignore')