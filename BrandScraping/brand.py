import os 
import time 
from functools import reduce 
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BrandScraper:
# Goes into instagram and searches a company for its followers, searches followers for more,
# -------------------------------------------------------------------------------------------
# and checks what other verified brands the users follow. There are time.sleep functions 
# scattered across the code to make the script wait for the browser.

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.instagram.com/') 
        time.sleep(2)
    
    def login(self):
        self.driver.find_element_by_name('username').send_keys(os.environ.get('instagram_username'))
        passw = self.driver.find_element_by_name('password')
        passw.send_keys(os.environ.get('instagram_password'))
        passw.send_keys(Keys.RETURN)
        time.sleep(2)

    def search(self, search_str):
        try:
            self.close_popup()
        except:
            print("Popup not there..")
       
        search_box = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'
        )
        search_box.send_keys(search_str)
        time.sleep(2)
        search_box.send_keys(Keys.RETURN)
        search_box.send_keys(Keys.RETURN)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)


    def close_popup(self):
        time.sleep(3)
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]').click()

    # Extracts people from the page's followers, stores it in a list. Instagram loads the 
    # div 12 elements at a time. Pass in n (how many batches of 12 profiles you want.)
    def extract_n_people_info(self, n):
        (WebDriverWait(self.driver, 5).until(
        EC.presence_of_element_located((
        By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')))).click()

        time.sleep(3)
        pzus_div = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div')
        list_a = pzus_div.find_elements_by_css_selector('a._0imsa')
        
        for i in range(n):
            self.driver.execute_script("arguments[0].scrollIntoView();", list_a[-1])
            time.sleep(2)
            list_a = pzus_div.find_elements_by_css_selector('a._0imsa')

        href_list = []
        for a in list_a:
            href_list.append(a.get_attribute('href'))

        return href_list

    # Helper method to get the user's verified following info
    def follower_following_extractor(self, link):
        verified_list = []
        self.driver.get(link)
        # Check if account is private first 
        try:
            message = self.driver.find_element_by_class_name('rkEop')
            print("The account is private")
            return None 
        except:
            # Not private, so start looking at their following list 
            print("Coolbeans, not private")            
            while True:
                this_profile = input("Scrape this profile or not? (y/n)")
                if this_profile == 'y':
                    break 
                elif this_profile == 'n':
                    return None 
                else:
                    print("Incorrect choice!")
                
            time.sleep(2)
            link = self.driver.find_element_by_partial_link_text('following')
            numFollowing = int(link.find_element_by_tag_name('span').text)
            print("Total number of accounts followed by the user: ", numFollowing)
            link.click()
            time.sleep(2)

            scroller_div = self.driver.find_element_by_class_name('isgrP')            
            startheight = self.driver.execute_script("return arguments[0].scrollHeight;", scroller_div)
            pzuss_div = scroller_div.find_element_by_class_name('PZuss')

            # The instagram page handles people with 12 followers or less using different web elements, sp
            # check that and set the 'inner_divs' variable according to each. 

            if numFollowing > 12:
                # Checking if we have completely scrolled the scroller_div or not, if yes, break out
                # of the while loop. We only have to scroll down if numFollowing > 12. 
                while True:
                    self.driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight; ",
                        scroller_div
                    )
                    time.sleep(1)
                    newheight = self.driver.execute_script("return arguments[0].scrollHeight;", scroller_div)
                    if startheight != newheight:
                        startheight = newheight
                    else:
                        break 
                inner_divs = pzuss_div.find_elements_by_class_name('d7ByH')
            else:
                inner_divs = pzuss_div.find_elements_by_css_selector('div.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm')

            for inner_div in inner_divs:
                a = inner_div.find_element_by_tag_name('a')
                account_name = a.get_attribute('title')
                # Check if the account is verified or not 
                try:
                    span = inner_div.find_element_by_tag_name('span')
                    print(f'Account with name {account_name} is verified!')
                    verified_list.append(a.get_attribute('href'))
                except:
                    pass 
        
        return verified_list

    # list_followers using self.extract_n_people_info and user_verified_following using
    # self.follower_following_extractor. This function finds all common verified followings 
    # between the followers. 
    def find_commons(self, list_followers):
        master_list = []
        for follower in list_followers:
            user_verified_following = self.follower_following_extractor(follower)
            if user_verified_following != None:
                master_list.append(user_verified_following)
                
        self.driver.close()
        return list(reduce(lambda i, j: i & j, (set(x) for x in master_list)))








