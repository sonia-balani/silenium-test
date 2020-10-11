import csv, unittest
from ddt import ddt, data, unpack
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re


def get_csv_data(csv_path):
    rows = []
    csv_data = open(str(csv_path), "rt")
    content = csv.reader(csv_data)
    next(content, None)
    for row in content:
        rows.append(row)
    return rows

@ddt
class ProductDetailTestDDT(unittest.TestCase):
    def setUp(self):
        # create a new browser session
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

        # navigate to the test page
        self.driver.get("http://automationpractice.com/index.php/index.php")

  
    @data(*get_csv_data("test_data.csv"))
    @unpack
    def test_product_details(self, search, product_title, max_product_price, product_short_desc,product_size,product_color):
        driver = self.driver

        WebDriverWait(self.driver, 30000).until(expected_conditions.visibility_of_element_located((By.ID, "search_query_top")))
        self.driver.find_element(By.ID, "search_query_top").click()
        
        element = self.driver.find_element(By.ID, "search_query_top")
        self.driver.find_element(By.ID, "search_query_top").send_keys(search)
        self.driver.find_element(By.NAME, "submit_search").click()
        self.driver.implicitly_wait(30)
    
        
        #Results
        actions = ActionChains(self.driver)
        self.driver.find_element(By.CSS_SELECTOR, ".heading-counter").click()
        self.driver.find_element(By.CSS_SELECTOR, ".right-block .product-name").click()
        self.driver.find_element(By.CSS_SELECTOR, "h1").click()
        
        
        
        element = self.driver.find_element(By.CSS_SELECTOR, "h1")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.implicitly_wait(30)
        
        #Details Page
        h1value = self.driver.find_element(By.CSS_SELECTOR, "h1").text
        self.assertIn(product_title,h1value.lower(),"Product categtory not matching the defined type") #optional
        
        #Product Price
        price = self.driver.find_element(By.ID, "our_price_display").text
        regprice = re.compile(r'[^\d.,]+')
        result = regprice.sub('', price)
        print(result)
        self.assertLess(float(result),float(max_product_price),"Price higher then maximum defined price.")
        
        #Short Description
        short_desc = self.driver.find_element(By.CSS_SELECTOR, "#short_description_content > p").text
        self.assertIn(product_short_desc,short_desc.lower(),"Product description not matching the defined type.")
        
        #Product Size    
        dropdown = self.driver.find_element(By.ID, "group_1")
        products_size = product_size.split(":")
        for psize in products_size:
            dropdown.find_element(By.XPATH, "//option[. = '"+ psize  + "']").click()
            self.assertEqual(psize,psize)
            self.driver.implicitly_wait(30)
            
        #Colors
        colors = set()
        elems = driver.find_elements_by_xpath('//*[@id="color_to_pick_list"]/li/a')
        for elem in elems:
            colors.add(elem.get_attribute("title"))
        
        #Check colors : / represents OR , add similar delimiter for other conditions
        product_colors = set(product_color.split("/"))
        print(colors)
        print(product_colors)
        if(len(colors.intersection(product_colors)) == 0):
        	self.assertEqual(colors,product_colors,"No matching colors found")
        else:
        	self.assertTrue(colors)       	
        
        #Add to Cart    
        driver.find_element_by_xpath('//*[@id="add_to_cart"]/button').click()
        self.driver.implicitly_wait(30)
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".button-medium > span")
        assert len(elements) > 0
   
    def tearDown(self):
        # close the browser window
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
