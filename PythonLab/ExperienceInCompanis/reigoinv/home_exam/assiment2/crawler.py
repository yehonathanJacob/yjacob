import os
import argparse
from dataclasses import dataclass, asdict

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import ElementClickInterceptedException

DRIVER_DEFAULT_PATH = os.path.join(os.environ['CHROMEDRIVER_DIR'], 'chromedriver')
SELECTED_DRIVER = webdriver.Chrome

def test_google_recaptcha(web_driver:WebDriver):
    return len(web_driver.find_elements_by_css_selector(".error-text-content")) > 0 and len(
        web_driver.find_elements_by_css_selector(".error-text-content #px-captcha")) > 0

class ZillowCrawler:
    def __init__(self, driver_path = None):
        driver_path = driver_path or DRIVER_DEFAULT_PATH
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.web_driver = webdriver.Chrome(driver_path, chrome_options=options)

    @staticmethod
    def prepare_url_request(address:str)->str:
        url = f"https://www.zillow.com/homes/{address.replace(' ','-')}_rb"
        return url

    def crawle_apartment_details(self, address):
        parsed_url = self.prepare_url_request(address)
        self.web_driver.get(parsed_url)

        if test_google_recaptcha(self.web_driver):
            raise ElementClickInterceptedException("Can't continue, user must pass the Google reCAPTCHA")

        area_details = AreaDetails.init_from_web_driver(self.web_driver)
        sales_details = SalesDetails.init_from_web_driver(self.web_driver)
        neighborhood_details = NeighborhoodDetails.init_from_web_driver(self.web_driver)
        great_schools = get_great_schools(self.web_driver)

        return {**asdict(area_details),
                **asdict(sales_details),
                **asdict(neighborhood_details),
                'great_schools':great_schools}


def get_great_schools(web_driver:WebDriver):
    return [
        great_school_name.get_attribute("innerText")
        for great_school_name in
        web_driver.find_elements_by_css_selector('.Spacer-c11n-8-33-0__sc-17suqs2-0 li a.notranslate')
    ]


@dataclass
class NeighborhoodDetails:
    walk_score: object
    transit_score: object

    @classmethod
    def init_from_web_driver(cls, web_driver: WebDriver):
        neighborhood_component = web_driver.find_element_by_css_selector('.ds-neighborhood .zsg-content-component')
        neighborhood_details = [
            int(neighborhood_detail.get_attribute("innerText"))
            for neighborhood_detail in neighborhood_component.find_elements_by_css_selector('span.eTicsB')
        ]
        return cls(*neighborhood_details)



@dataclass
class SalesDetails:
    sold_date: str
    property_price: str

    @classmethod
    def init_from_web_driver(cls, web_driver:WebDriver):
        container = web_driver.find_element_by_css_selector('p.jfHfpE')
        sold_date = container.find_elements_by_css_selector('.bvTLbK')[0].get_attribute("innerText").replace("Sold on ",
                                                                                                            "")
        property_price = container.find_elements_by_css_selector('.bvTLbK')[1].find_element_by_css_selector(
            '.flSprY').get_attribute("innerText").replace("$", "").replace(",", "_")
        property_price = int(property_price)
        return cls(sold_date, property_price)


@dataclass
class AreaDetails:
    number_of_bedrooms: int
    number_of_bathrooms: int
    property_size: int

    @classmethod
    def init_from_web_driver(cls, web_driver:WebDriver):
        living_area_container = web_driver.find_element_by_css_selector('.ds-bed-bath-living-area-container')
        area_details = [
            int([x.get_attribute("innerText")
                 for x in area_detail.find_elements_by_tag_name("span")
                 ][0].replace(",", "_")
                )
            for area_detail in living_area_container.find_elements_by_css_selector('.iIPyzR')
        ]
        return cls(*area_details)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--address',
                        help='Enter house address, add apostrophes (") before and after for address with space ',
                        type=str)

    args = parser.parse_args()

    zillow_crawler = ZillowCrawler()
    try:
        print(zillow_crawler.crawle_apartment_details("2517 E 13th St, Indianapolis, IN, 46201"))
    except ElementClickInterceptedException as e:
        print('Please pass the reCAPTCHA and click Enter.')
        input()
        print(zillow_crawler.crawle_apartment_details("2517 E 13th St, Indianapolis, IN, 46201"))
