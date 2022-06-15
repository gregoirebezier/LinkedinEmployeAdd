#!/usr/bin/python3

from selenium import webdriver
from time import sleep
from decouple import config
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
import warnings


###---------REMOVE THE DEPRECATIONWARNING---------###
warnings.filterwarnings("ignore", category=DeprecationWarning)

def GetNames():
    df = pd.read_csv('general_bamboohr_org_chart.csv')
    names = df["Name"].unique()
    AllNames = df.loc[df["Name"] == names]["Name"].values
    return AllNames

def connectionLinkedin(names):
    passwordsecret = config('PASSWORD')
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    driver.set_page_load_timeout(30)
###---------MAXIMIZE WINDOW---------###
    driver.maximize_window()
    sleep(4)
    Username = driver.find_element_by_id("username")
    Username.send_keys('beziergregoire@gmail.com')
    password = driver.find_element_by_id("password")
    password.send_keys(passwordsecret)
    Signin = driver.find_element_by_xpath("//*[@type='submit']")
    Signin.click()
    sleep(4)
    tempVar = 0
    for name in names:
        tempVar += 1
        if (tempVar >= 50):
            try:
                driver.execute_script("window.open('');") 
                driver.switch_to.window(driver.window_handles[1])
                driver.get("https://www.linkedin.com/")
                sleep(3)
                driver.switch_to.window(driver.window_handles[0])
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                tempVar = 0
                sleep(1)
            except:
                print ("PROBLEM WITH THE NEW WINDOW")

        try:
            driver.find_element_by_xpath("//input[@placeholder='Recherche']").clear()
            driver.find_element_by_xpath("//input[@placeholder='Recherche']").send_keys(name)
            driver.find_element_by_xpath("//input[@placeholder='Recherche']").send_keys(Keys.ENTER)
            sleep(5)
            driver.find_element_by_xpath("//*[@class='app-aware-link artdeco-button artdeco-button--default artdeco-button--2 artdeco-button--primary']").click()
            sleep(4)
            buttons = driver.find_elements_by_xpath("//*[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action']")
            for element in buttons:
                try:
                    element.click()
                    sleep(2)
                    break
                except:
                    pass
            driver.find_element_by_xpath("//*[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1']").click()
            sleep(2)
            with open('linkedin_connections.txt', 'a') as f:
                f.write(name + '\n')
        except:
            print("No connection found for " + name)
            with open ("NoConnection.txt", "a") as myfile:
                myfile.write(name + "\n")
    sleep(1000)
###---------NAVIGATE TO TWITTER---------###
def main():
    names = GetNames()
    driver = connectionLinkedin(names)

if __name__ == '__main__':
    main()