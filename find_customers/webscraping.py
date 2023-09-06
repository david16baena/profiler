from time import sleep
from typing import List, Dict
from typing_extensions import Self
from random import uniform

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class linkedin:
    
    def __init__(self, driver: WebDriver = None) -> None:
        
        if driver is None:
            driver = webdriver.Chrome()
        
        self.driver = driver
        
    
    def __enter__(self) -> Self:
        
        self.driver.get("https://linkedin.com/uas/login")
        self.wait(5)
        
        return self
    
    
    def __exit__(self, exception_type, exception_value, traceback) -> None:
        
        self.driver.quit()
        
        
    def wait(self, seconds: float, begin: float = 1.0) -> None:
        
        sleep(uniform(begin, seconds))
    
    
    def login(self, usr:str, pwd:str) -> None:
        
        username = self.driver.find_element(By.ID, "username")
        username.send_keys(usr) 
 
        pword = self.driver.find_element(By.ID, "password")
        pword.send_keys(pwd)
        self.wait(5)
 
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        self.wait(7, 5)
        
    
    def search_by_job(self, job:str, page:int):
        
        self.wait(5)
        self.driver.get(f"https://www.linkedin.com/search/results/people/?keywords={job}&page={page}")
        self.wait(5)
        
        
    def info_profiles(self) -> List[WebElement]:
        
        potential_customer_path = './/div[contains(@class, "entity-result__content")]'
        info = self.driver.find_elements("xpath", potential_customer_path)
        self.wait(7, 5)
        
        return info
    
    
    def set_info(self, useful_profile:List[str], useful_results:List[str]) -> Dict[str, str]:
        
        if len(useful_profile) > 4:
            useful_results[useful_profile[0]] = {"cargo":useful_profile[2],
                                                 "ubicacion":useful_profile[3],
                                                 "detalles":useful_profile[4:]}
        elif len(useful_profile) > 3:
            useful_results[useful_profile[0]] = {"cargo":useful_profile[2],
                                                 "ubicacion":useful_profile[3],
                                                 "detalles":None}
        elif len(useful_profile) > 2:
            useful_results[useful_profile[0]] = {"cargo":useful_profile[2],
                                                 "ubicacion":None,
                                                 "detalles":None}
        else:
            useful_results[useful_profile[0]] = {"cargo":None,
                                                 "ubicacion":None,
                                                 "detalles":None}
        return useful_results
    
    
    def extract_info(self, info_profiles:List[WebElement]) -> Dict[str, str]:
        
        results = [profile.text.split("\n") for profile in info_profiles]
        
        useful_results = {}
        for profile in results:
            useful_profile = []
            for info in profile:
                if ('contacto' not in info.lower()) & ('º' not in info.lower()):
                    useful_profile.append(info)
            
            useful_results = self.set_info(useful_profile, useful_results)
        
        return useful_results
    
    
    def extract_info_by_job(self, jobs:List[str], from_page:int, to_page:int) -> Dict[str,str]:
    
        result = {}
        for job in jobs:
            for page in range(from_page, to_page + 1):
                self.search_by_job(job, page)
                info = self.info_profiles()
                result.update(self.extract_info(info))
        
        return result