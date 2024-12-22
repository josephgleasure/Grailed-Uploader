from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import json
import time
import os

class GrailedUploader:
    def __init__(self, config_path):
        with open(config_path) as f:
            self.config = json.load(f)
        self.data = pd.read_excel(self.config['excel_path'])
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        
    def login(self):
        self.driver.get("https://www.grailed.com/sell")
        email_input = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_input.send_keys(self.config['grailed_email'])
        self.driver.find_element(By.NAME, "password").send_keys(self.config['grailed_password'])
        self.driver.find_element(By.CSS_SELECTOR, "[type='submit']").click()
        time.sleep(2)

    def process_listing(self, row):
        self.driver.get("https://www.grailed.com/sell")
        
        # Category selection
        self._select_categories(row)
        
        # Basic info
        self._fill_basic_info(row)
        
        # Upload images
        self._upload_images(row)
        
        # Description and tags
        self._fill_description(row)
        self._add_tags(row['Tags'])
        
        # Price settings
        self._set_price_settings(row)
        
        input("Review listing and press Enter to submit...")
        
    def _select_categories(self, row):
        cats = [row['MainCategory'], row['SubCategory'], row['SubSubCategory']]
        for cat in cats:
            select = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[data-value='{cat}']")))
            select.click()
            time.sleep(1)
            
    def _fill_basic_info(self, row):
        fields = {
            "designer": row['Designer'],
            "title": row['Full Name'],
            "size": row['Size'],
            "color": row['Color'],
            "condition": row['Condition']
        }
        
        for name, value in fields.items():
            field = self.wait.until(EC.presence_of_element_located((By.NAME, name)))
            field.clear()
            field.send_keys(value)
            
    def _upload_images(self, row):
        base_name = row['Full Name'].replace(" ", "")
        upload = self.driver.find_element(By.CSS_SELECTOR, "[type='file']")
        
        # Find all matching images for this item
        matching_images = sorted([
            f for f in os.listdir(self.config['image_folder']) 
            if f.startswith(base_name) and f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])
        
        print(f"Found {len(matching_images)} images for {base_name}")
        
        for image in matching_images:
            img_path = os.path.join(self.config['image_folder'], image)
            try:
                upload.send_keys(img_path)
                print(f"Uploaded: {image}")
                time.sleep(1)  # Wait for upload
            except Exception as e:
                print(f"Failed to upload {image}: {str(e)}")
                
    def _fill_description(self, row):
        desc = self.wait.until(EC.presence_of_element_located((By.NAME, "description")))
        desc.clear()
        desc.send_keys(row['Final Description'])
        
    def _add_tags(self, tags):
        tags_input = self.wait.until(EC.presence_of_element_located((By.NAME, "tags")))
        for tag in tags.split(','):
            tags_input.send_keys(tag.strip())
            tags_input.send_keys(Keys.ENTER)
            
    def _set_price_settings(self, row):
        self.driver.find_element(By.NAME, "price").send_keys(str(row['Price']))
        
        if row['Accept Offers'].lower() == 'yes':
            self.driver.find_element(By.NAME, "acceptOffers").click()
            
        if row['Smart Pricing'].lower() == 'yes':
            self.driver.find_element(By.NAME, "smartPricing").click()
            self.driver.find_element(By.NAME, "floorPrice").send_keys(str(row['Floor Price']))
            
    def process_all(self):
        self.login()
        for index, row in self.data.iterrows():
            print(f"Processing listing {index + 1}/{len(self.data)}")
            self.process_listing(row)
            time.sleep(2)
            
if __name__ == "__main__":
    uploader = GrailedUploader("config.json")
    uploader.process_all()