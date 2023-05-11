from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
from typer import Typer
from bs4 import BeautifulSoup
import selenium.webdriver.support.expected_conditions as EC
import chromedriver_autoinstaller
import time



def create_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-data-dir=C:/Users/Andrew/AppData/Local/Google/Chrome/User Data')
    options.add_argument('profile-directory=Default')
    driver = webdriver.Chrome(options=options)
    return driver


def find_current_event():
    def get_most_recent_article(driver):
        driver.get("https://www.cnn.com/politics")
        time.sleep(2) #CHANGE FROM IMPLICIT TO ELEMENT BASED WAIT LATER
        soup = BeautifulSoup(driver.page_source, "html.parser")
        urls = soup.find_all("a", class_="container_lead-plus-headlines__link", href=True)
        read_article(urls[1]['href'], driver)



    def read_article(article, driver):
        driver.get("https://cnn.com" + article)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        article_parts = ""
        for x in soup.find_all("p", class_="paragraph"):
            article_parts += x.get_text()
        if "This story has been updated with additional information." in article_parts:
            article_parts = article_parts.replace(
                "This story has been updated with additional information.", "")
        talk_to_chatgpt(article_parts, driver)

    driver = create_webdriver()
    get_most_recent_article(driver)


def talk_to_chatgpt(article, driver):
    driver.get("https://chat.openai.com")
    time.sleep(5)
    input_field = driver.find_element(By.TAG_NAME, "textarea")
    actions = [
        {
            'script': f"""document.getElementsByTagName('textarea')[0].value = `
                        Can you write a one paragraph summary of this article: '{article}'
                        `""",
            'text': Keys.RETURN,
            'sleep': 10
        },
        {
            'script': "document.getElementsByTagName('textarea')[0].value = 'Now write an opinion on that article from the perspective of an 11th grader without mentioning that you're an 11th grader'",
            'text': Keys.RETURN,
            'sleep': 10
        },
        {
            'script': "document.getElementsByTagName('textarea')[0].value = 'Now write a question you have about the events of the article'",
            'text': Keys.RETURN,
            'sleep': 10
        }
    ]

    for action in actions:
        driver.execute_script(action['script'])
        input_field.send_keys(action['text'])
        time.sleep(action['sleep'])

    summary = driver.find_element(By.XPATH, "(//div[contains(@class,'markdown prose')]//p)[1]").text 
    opinion = driver.find_element(By.XPATH, "(//div[contains(@class,'markdown prose')]//p)[2]").text 
    question = driver.find_element(By.XPATH, "(//div[contains(@class,'markdown prose')]//p)[3]").text 
    write_out_events(summary, opinion, question, driver)
    

def write_out_events(summary, opinion, question, driver):
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
