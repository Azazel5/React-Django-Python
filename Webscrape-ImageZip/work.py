import csv
import time 
import zipfile
import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AmazonSearcher:
# Scrapes the top result for whateevr and returns a zip file of the product's images, 
# ----------------------------------------------------------------------------------------
# and its basic information save in a csv file. An option to send the files as an email. 

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.amazon.com/')
    
    # There are two different types of layouts are you hit "search" on amazon, which is why div_elems is
    # being set twice, depending on the type of view.
    def product_search(self, product_name):
        search_box = self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.RETURN)

        try:
            div_elems = WebDriverWait(self.driver, 3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'a-section.aok-relative.s-image-fixed-height')))
        except:
            div_elems = WebDriverWait(self.driver, 3).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'a-section.aok-relative.s-image-square-aspect'))) 
        
        div_elems[0].click()  
    
    # Save the basic info to a csv file and the images to a zip file. The images are acquired from
    # Amazon's product image magnifier with several pictures per product. 
    def save_info(self):
        product_title = (WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((
        By.ID, 'productTitle')))).text
        product_price = self.driver.find_element_by_id('priceblock_ourprice').text
        product_brand = self.driver.find_element_by_id('bylineInfo').text
        
        fields = ['Product_Title', 'Product_Price', 'Product_Brand']
        rows = [[
            product_title,
            product_price,
            product_brand
        ]]

        with open('details.csv', 'w') as csvfile:  
            csvwriter = csv.writer(csvfile)  
            csvwriter.writerow(fields)  
            csvwriter.writerows(rows) 

        image_boxes = (WebDriverWait(self.driver, 3).until(
        EC.presence_of_all_elements_located((
        By.CLASS_NAME, 'a-spacing-small.item.imageThumbnail.a-declarative'))))
        
        req_list = []
        for box in image_boxes:
            box.click()
            time.sleep(0.5)
            ul = self.driver.find_element_by_class_name('a-unordered-list.a-nostyle.a-horizontal.list.maintain-height')
            ul_soup = BeautifulSoup(ul.get_attribute('innerHTML'), 'html.parser')
            image_obj = ul_soup.find('li', {'class': 'selected'}).find('img')
            req = requests.get(image_obj['src'], stream=True)
            req_list.append(req)
        
        # Rewriting the image filename based on the product's title. Sometimes the product's title
        # is extremely long, so I took an arbitrary substring (in this case 6)
        productname = product_title.lower().strip().replace(' ', '')[:6]
        with zipfile.ZipFile('zipped_images.zip', 'w') as zipped:
            for i, request in enumerate(req_list):
                filename = f'{productname}_{str(i)}.jpg'
                zipped.writestr(filename, request.content)

        self.driver.close()


            



            
                
            


