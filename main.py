from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.wait import WebDriverWait
from typer import Typer
from bs4 import BeautifulSoup
import selenium.webdriver.support.expected_conditions as EC
import chromedriver_autoinstaller
import time
import random
import re
import requests



def create_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-data-dir=C:/Users/Andrew/AppData/Local/Google/Chrome/User Data')
    options.add_argument('profile-directory=Default')
    driver = webdriver.Chrome(options=options)
    return driver


def find_current_event():
    def get_most_recent_article():
        try:
            r = requests.get("https://cnn.com/politics")
        except requests.exceptions.RequestException as e:  
            raise SystemExit(e)
        else:
            soup = BeautifulSoup(r.text, "html.parser")
            urls = soup.find_all("a", class_="container_lead-plus-headlines__link", href=True)
            read_article(urls[1]['href'])



    def read_article(article):
        try:
            r = requests.get(f'https://cnn.com{article}')
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        else:
            soup = BeautifulSoup(r, "html.parser")
            article_parts = """Write a one paragraph summary of this article: '"""
            for x in soup.find_all("p", class_="paragraph"):
                article_parts += x.get_text()
            if "This story has been updated with additional information." in article_parts:
                article_parts = article_parts.replace(
                    "This story has been updated with additional information.", "")
            article_parts += """'"""
            cleaned_text = re.sub('\s+', ' ', article_parts).strip()
            single_line_text = re.sub('(?<=[.!?])\s+(?=[A-Z])', ' ', cleaned_text)
            talk_to_chatgpt(single_line_text)

    get_most_recent_article()


def talk_to_chatgpt(article, driver):
    driver.get("https://chat.openai.com")
    time.sleep(2)
    input_field = driver.find_element(By.TAG_NAME, "textarea")
    for char in article:
        driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div[2]/div/main/div[3]/form/div/div[2]/textarea').send_keys(char)
        time.sleep(random.uniform(0.01, 0.03))



    time.sleep(100)

    summary = driver.find_element(By.XPATH, "(//div[contains(@class,'markdown prose')]//p)[1]").text 
    opinion = driver.find_element(By.XPATH, "(//div[contains(@class,'markdown prose')]//p)[2]").text 
    question = driver.find_element(By.XPATH, "(//div[contains(@class,'markdown prose')]//p)[3]").text 
    write_out_events(summary, opinion, question, driver)
    

def write_out_events(summary, opinion, question, driver):
    driver.get("https://classroom.google.com/u/1/c/NDg4OTcyNTcwNzI4/sp/MjIyODEzODc2/all")

def typing_example():
    driver = webdriver.Chrome()
    driver.get("https://write-box.appspot.com/")
    text = "The quick brown fox jumps over the lazy dog"
    element = driver.find_element(By.ID, 'editor')
    element.clear()
    # https://github.com/saadejazz/humanTyper
    ty = Typer(accuracy = 0.90, correction_chance = 0.50, typing_delay = (0.04, 0.08), distance = 2)
    ty.send(element, text)

def scrape_assignments_test():
    driver = create_webdriver()
    driver.get("https://classroom.google.com/u/1/c/NDg4OTcyNTcwNzI4/sp/MjIyODEzODc2/all")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    html = soup.prettify()
    with open("output1.html", "w", encoding='utf-8') as file:
        file.write(str(html))

chromedriver_autoinstaller.install()
find_current_event()
#scrape_assignments_test()

