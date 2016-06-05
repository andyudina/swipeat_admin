# -*- coding: utf-8 -*-
import re
from pymongo import MongoClient

from selenium.webdriver import DesiredCapabilities, Remote, Firefox
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException

class AfishaToMongoWrapper(object):
    def __init__(self):
        client = MongoClient()
        self.db = client.afisha
        
    def insert(self, **kwargs):
        self.db.restaurants.insert_one(kwargs)
            
class AfishaPage(object):
    URL = 'https://www.afisha.ru/msk/restaurants/restaurant_list/?&q=&page={}'
    #START_PAGE = 0
    page = 0
    RESTAURANT_INFO_SELECTOR = '.search_list_item'
    TIMEOUT = 100

    
    def wait(self, element):
        return WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located(
            element))
            
    def __init__(self, driver):
        self.driver = driver
       
    def get_url(self, page):
        return self.URL.format(page)
        
    def open(self, url):
        self.driver.get(url)
        self.driver.maximize_window()
                
    def go_to_next_page(self):
        self.page += 1
        url = self.get_url(self.page)
        self.open(url)    
        
    def get_restaurants(self):
        self.wait([By.CSS_SELECTOR, self.RESTAURANT_INFO_SELECTOR])
        return self.driver.find_elements_by_css_selector(self.RESTAURANT_INFO_SELECTOR)
        #     self.parse_restaurant(element)
 
class AfishaParser(object): 
    RESTAURANT_LINK_SELECTOR = '.places_link'
    RESTAURANT_IMAGE_SELECTOR = '.places_img'
    RESTAURANT_CUISINE_SELECTOR = '.places_cuisine'
    RESTAURANT_CONTACTS_SELECTOR = '.places_contact'
    RESTAURANT_RATINGS_SELECTOR = '.places_ratings_item'
    RESTAURANT_REAL_RATING_SELECTOR = '.rating'
    RESTAURANT_COST_SELECTOR = '.range'
    RESTAURANT_SELECTIONS_SELECTOR = '.places_selections'
    RESTAURANT_REAL_SELECTION_SELECTOR = '.selection_icon'
          
    def parse_rest_contacts(self, el):
        text_regex = re.compile('(.*)<br><nobr>(.*)</nobr><br>(.*)')
        match = text_regex.match(el.get_attribute('innerHTML'))
        if not match: 
            #print el.text
            return [None, ]  * 3
        return [match.group(i) for i in xrange(1, 4)]
        
    def parse_stations(self, stations):
        if not stations: return []
        return filter(lambda x: not not x and x not in [u'м. ', ', '], re.compile(u"(,\s+|\s+м\.\s+)").split(stations))
        
    def parse_selections(self, selections):
        result = []
        for selection in selections:
            try:
                result.append(
                    selection.find_element_by_css_selector(self.RESTAURANT_REAL_SELECTION_SELECTOR).get_attribute('data-text')
                )
            except NoSuchElementException:
                pass
        return result
        
    def parse_restaurant(self, el):
        try:
            title = el.find_element_by_css_selector(self.RESTAURANT_IMAGE_SELECTOR).get_attribute('alt')
        except NoSuchElementException:
            try:
                title = el.find_element_by_css_selector(self.RESTAURANT_LINK_SELECTOR).text
            except NoSuchElementException:
                title = None
        try:
            cuisine = el.find_element_by_css_selector(self.RESTAURANT_CUISINE_SELECTOR).text
        except NoSuchElementException:
            cuisine = None
        try:
            address, phone, stations = self.parse_rest_contacts(el.find_element_by_css_selector(self.RESTAURANT_CONTACTS_SELECTOR))
        except NoSuchElementException:
            address, phone, stations = [None, ] * 3
        rating = None
        cost = None
        try:
            ratings = el.find_elements_by_css_selector(self.RESTAURANT_RATINGS_SELECTOR)
        except NoSuchElementException:
            raitings = None        
        if ratings:
            try:
                rating = ratings[0].find_element_by_css_selector(self.RESTAURANT_REAL_RATING_SELECTOR).text
            except NoSuchElementException:
                pass
            if len(ratings) >= 2:
                try:
                    cost = ratings[1].find_element_by_css_selector(self.RESTAURANT_COST_SELECTOR).get_attribute('data-text')
                except NoSuchElementException:
                    pass
        try:
            selections = self.parse_selections(el.find_elements_by_css_selector(self.RESTAURANT_SELECTIONS_SELECTOR))
        except NoSuchElementException:
            selections = [] 
        return {
            'title': title,
            'cuisine': cuisine,
            'address': address,
            'phone': phone,
            'stations': self.parse_stations(stations),
            'rating': rating,
            'cost': cost,
            'selections': selections
        } 
        
     
if __name__ == '__main__':
    afisha_page = AfishaPage(Firefox())
    afisha_parser = AfishaParser()
    afisha_client = AfishaToMongoWrapper()
    
    ENOUGH_RESTAURANTS_NUMBER = 200
    i = 0
    while i < ENOUGH_RESTAURANTS_NUMBER:
        afisha_page.go_to_next_page()
        for place in afisha_page.get_restaurants():
            place = afisha_parser.parse_restaurant(place)
            print place
            afisha_client.insert(**place)
            i += 1      
             
             
        
