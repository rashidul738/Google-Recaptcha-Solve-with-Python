from sys import audit
from selenium import webdriver
from time import sleep
import time,requests
import sys
import random
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import sys
import time
import requests


audioToTextDelay = 10
delayTime = 5
audioFile = "\\payload.mp3"
SpeechToTextURL = "https://speech-to-text-demo.ng.bluemix.net/"
URL = "https://www.washco.utah.gov/forms/assessor/search/"

def delay():
    time.sleep(random.randint(5, 10))

def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)
    time.sleep(5)

    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    sleep(5)

    return result

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(URL)
sleep(7)

g_recaptcha = driver.find_elements_by_class_name('g-recaptcha')[0]
outerIframe = g_recaptcha.find_element_by_tag_name('iframe')
outerIframe.click()
sleep(10)
allIframesLen = driver.find_elements_by_tag_name('iframe')
audioBtnFound = False
audioBtnIndex = -1

for index in range(len(allIframesLen)):
    driver.switch_to.default_content()
    iframe = driver.find_elements_by_tag_name('iframe')[index]
    driver.switch_to.frame(iframe)
    driver.implicitly_wait(50)
sleep(10)
audio = driver.find_element_by_xpath('//button[@class="rc-button goog-inline-block rc-button-audio"]')
audio.click()
sleep(4)
audioBtnFound = True
audioBtnIndex = index



if audioBtnFound:
    try:
        while True:
            # get the mp3 audio file
            src = driver.find_element_by_id("audio-source").get_attribute("src")
            print("[INFO] Audio src: %s" % src)

            # download the mp3 audio file from the source
            urllib.request.urlretrieve(src, os.getcwd() + audioFile)

            # Speech To Text Conversion
            key = audioToText(os.getcwd() + audioFile)
            print("[INFO] Recaptcha Key: %s" % key)

            driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[audioBtnIndex]
            driver.switch_to.frame(iframe)
            sleep(4)

            # key in results and submit
            inputField = driver.find_element_by_id("audio-response")
            inputField.send_keys(key)
            sleep(10)
            inputField.send_keys(Keys.ENTER)
            sleep(5)

            err = driver.find_elements_by_class_name('rc-audiochallenge-error-message')[0]
            if err.text == "" or err.value_of_css_property('display') == 'none':
                print("[INFO] Success!")
                break

    except Exception as e:
        print(e)
        sys.exit("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
else:
    sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")
    
driver.find_element    