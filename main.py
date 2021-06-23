import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

login_url = "https://www.talque.com/app#/onboard/login?loginVia=NONE"
email = 'sherif.neamatalla.26@gmail.com'
password = 'helloworld26'

parser_type = 'html.parser'

login_button_id = 'pro-login'
email_input_id = 'input_14'
password_input_id = 'input_15'
anchor_tag_link_text = 'Teilnehmer'

participants_list_tag_name = 'rli-participant-lib-participant-list-card'

scroll_tag_name = 'layout-lib-vscroll-row-center-column'
scroll_pause_time = 2

max_scrolls = 170


def login_and_get_participants_page():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override",
                           "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0")
    # Get instance of firefox browser
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_profile=profile)
    # Go to login URL
    driver.get(login_url)

    # Wait for page to load by waiting for the form to load, otherwise wouldn't be able to find the expected content
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'loginForm')))

    # Find input and submit tags then sign in
    email_input = driver.find_element_by_id(email_input_id)
    password_input = driver.find_element_by_id(password_input_id)

    email_input.send_keys(email)
    password_input.send_keys(password)

    driver.find_element_by_id(login_button_id).click()

    # Wait for after login page to load by waiting for the anchor with "Teilnehmer" text
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, anchor_tag_link_text)))

    # Find the "Teilnehmer" anchor tag and click on it
    driver.find_element_by_link_text(anchor_tag_link_text).click()

    # Waits for the tag containing list of participants to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, participants_list_tag_name)))

    return driver


def add_new_participants(driver, old_list):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    participants_tags = soup.find_all('rli-participant-lib-participant-list-card')
    new_list = old_list + participants_tags

    return new_list


# Keeps scrolling down to retrieve all participants pages
def do_load_all_content(driver):
    all_participants_tags = list()
    # if the scroll doesn't exist we reached the end voila boys
    element = driver.find_element_by_tag_name(scroll_tag_name)
    scroll_count = 0

    all_participants_tags = add_new_participants(driver, all_participants_tags)
    while element and (not max_scrolls or scroll_count <= max_scrolls):
        print('Scrolling once more time boys')
        print('Current scroll count : ', scroll_count)
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(scroll_pause_time)
        element = driver.find_element_by_tag_name(scroll_tag_name)

        all_participants_tags = add_new_participants(driver, all_participants_tags)

        scroll_count += 1

    time.sleep(5)

    return all_participants_tags


def start_scrapping():
    silenium_driver = login_and_get_participants_page()

    participants_tags = do_load_all_content(silenium_driver)

    # soup = BeautifulSoup(full_content, 'html.parser')

    # print(soup.prettify())

    content = ''

    print('Creating file.')
    print("Number of participants scrapped: ", len(participants_tags))
    for tag in participants_tags:
        content += str(tag) + '\n'
    f = open('result.html', 'w+')
    f.write(content)

    f.close()
    pass


if __name__ == '__main__':
    start_scrapping()
