import pytest
from assiment2.crawler import ZillowCrawler, ElementClickInterceptedException

@pytest.fixture()
def basic_parameters():
    address = "2517 E 13th St, Indianapolis, IN, 46201"
    expected_result = {'number_of_bedrooms': 3, 'number_of_bathrooms': 2, 'property_size': 2494,
                      'sold_date': '12/31/20', 'property_price': 105_357, 'walk_score': 65,
                      'transit_score': 38,
                      'great_schools': ['Brookside School 54', 'H.L. Harshman Magnet Middle School',
                                        'Arsenal Technical High School']}
    return address, expected_result

def test_crawler_end_to_end(basic_parameters):
    address, expected_result = basic_parameters
    zillow_crawler = ZillowCrawler()

    try:
        result = zillow_crawler.crawle_apartment_details(address)
    except ElementClickInterceptedException as e:
        print('Please pass the reCAPTCHA and click Enter.')
        input()
        result = zillow_crawler.crawle_apartment_details(address)

    for k, v in expected_result.items():
        assert result[k] == v
