from selenium import webdriver
from typer import Typer
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import By
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
from selenium.webdriver.support.wait import WebDriverWait
import time
import selenium.webdriver.support.expected_conditions as EC


def create_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-data-dir=C:/Users/Andrew/AppData/Local/Google/Chrome/User Data')
    options.add_argument('profile-directory=Default')
    driver = webdriver.Chrome(options=options)
    return driver


def find_current_event():
    driver = create_webdriver()
    # driver.get("https://www.cnn.com/POLITICS/")
    # driver.find_element(By.XPATH, "(//h3[@class='cd__headline']//a)[1]").click
    # driver.implicitly_wait(20)
    driver.get(
        "https://www.cnn.com/2023/05/10/politics/governor-bill-lee-tennessee-school-shooting/index.html")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    article_parts = ""
    for x in soup.find_all("p", class_="paragraph"):
        article_parts += x.get_text()
    if "This story has been updated with additional information." in article_parts:
        article_parts = article_parts.replace(
            "This story has been updated with additional information.", "")
    talk_to_chatgpt(article_parts, driver)


def talk_to_chatgpt(article, driver):
    driver.get("https://chat.openai.com")
    time.sleep(4)
    input_field = driver.find_element(By.TAG_NAME, "textarea")
    js = f"""
    document.getElementsByTagName('textarea')[0].value = `
    Can you write a one paragraph summary of this article: '{article}'
    `
    """ 
    driver.execute_script(js)
    input_field.send_keys(Keys.RETURN)
    time.sleep(10)
    js = "document.getElementsByTagName('textarea')[0].value = 'Now write an opinion on that article from the perspective of an 11th grader without mentioning that you're an 11th grader'"
    driver.execute_script(js)
    input_field.send_keys(Keys.RETURN)
    time.sleep(10)
    js = "document.getElementsByTagName('textarea')[0].value = 'Now write a question you have about the events of the article'"
    driver.execute_script(js)
    input_field.send_keys(Keys.RETURN)
    time.sleep(10)
    summary = driver.find_element(By.XPATH, "(//div[contains(@class,'markdown prose')]//p)[1]").text 
    opinion = driver.find_element(By.XPATH, "(//div[contains(@class,'markdown prose')]//p)[2]").text 
    question = driver.find_element(By.XPATH, "(//div[contains(@class,'markdown prose')]//p)[3]").text 
    

def write_out_events():
    driver = create_webdriver()
    driver.get("https://classroom.google.com/u/1")

def typing_example():
    driver = webdriver.Chrome()
    driver.get("https://write-box.appspot.com/")
    text = "The quick brown fox jumps over the lazy dog"
    element = driver.find_element(By.ID, 'editor')
    element.clear()
    # https://github.com/saadejazz/humanTyper
    ty = Typer(accuracy = 0.90, correction_chance = 0.50, typing_delay = (0.04, 0.08), distance = 2)
    ty.send(element, text)

chromedriver_autoinstaller.install()
find_current_event()
