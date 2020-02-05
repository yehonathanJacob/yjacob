from builtins import object
import os
import pytest


@pytest.mark.django_db
class TestAnalyzeFood(object):

    @staticmethod
    def food_items_from_text(client, text, lang='en'):
        resp = client.post('/food/analyze_food/', {'text': text, 'lang': lang})
        assert resp.status_code == 200
        return resp.json()['items']

    @staticmethod
    def food_items_from_image(client, image_path):
        with open(image_path, 'rb') as image:
            resp = client.post('/food/analyze_food/', {'image': image})
            assert resp.status_code == 200
            return resp.json()['foods']

    def test_food_basic(self, client):
        items = self.food_items_from_text(client, 'I ate an apple at 09:45')
        assert len(items) == 1
        item = items[0]
        assert 'type' in item and type(item['type']) == str
        assert 'food' in item and type(item['food']) == str
        assert 'time' in item
        assert 'amount' in item and type(item['amount']) == int
        assert 'weight' in item and (type(item['weight']) == int or type(item['weight']) == float)

    def test_sleep_basic(self, client):
        items = self.food_items_from_text(client, 'I slept from 22:00 until 7:00')
        assert len(items) == 1
        item = items[0]
        assert item['type'] == 'sleep'
        assert 'start' in  item
        assert 'end' in item

    def test_sport_basic(self, client):
        items = self.food_items_from_text(client, 'I run 5 km')
        assert len(items) == 1
        item = items[0]
        assert 'type' in item and type(item['type']) == str
        assert 'distance' in item and type(item['distance']) == int

    def test_image_single_food(self, client):
        items = self.food_items_from_image(client, os.path.join(os.path.dirname(__file__), 'black_coffee.jpeg'))
        assert len(items) == 1
        item = items[0]
        assert 'type' in item and type(item['type']) == str
        assert 'food' in item and type(item['food']) == str
        assert 'weight' in item and type(item['weight']) == int

    def test_image_multiple_food(self, client):
        items = self.food_items_from_image(client, os.path.join(os.path.dirname(__file__), 'california-burger.jpg'))
        assert len(items) == 2
        burger, fries = (items[0], items[1]) if items[0]['food'] == 'hamburger' else (items[1], items[0])
        assert 'food' in burger and type(burger['food']) == str
        assert 'food' in fries and type(fries['food']) == str

    def test_food_topping(sefl, client):
        items = sefl.food_items_from_text(client, 'yogurt with granola')
        assert len(items) == 2
        yogurt, granola = (items[0], items[1]) if items[0]['food'] == 'yogurt' else (items[1], items[0])
        assert 'food' in yogurt and type(yogurt['food']) == str
        assert 'food' in granola and type(granola['food']) == str
        assert 'unit_type' in granola and type(granola['unit_type']) == str

    # Test is not relevent
    # def test_boolean_question(self, client):
    #     items = self.food_items_from_text(client, 'coffee')
    #     questions = items[0]['questions']
    #     bq = None
    #     for q in questions:
    #         if q['type'] == 'FoodBooleanQuestion':
    #             bq = q
    #             break
    #     assert bq
    #     assert bq['text']
    #     assert bq['positive_answer']['text']
    #     assert bq['action'] == 'replace'

    def test_amount_question(self, client):
        items = self.food_items_from_text(client, 'espresso')
        questions = items[0]['questions']
        aq = None
        for q in questions:
            if q['type'] == 'FoodAmountQuestion':
                aq = q
                break
        assert aq
        assert aq['text']
        assert aq['food']
        assert aq['action'] == 'add'

    def test_multiple_choice_question(self, client):
        items = self.food_items_from_text(client, 'pasta')
        questions = items[0]['questions']
        mq = None
        for q in questions:
            if q['type'] == 'FoodMultipleChoiceQuestion':
                mq = q
                break
        assert mq
        assert mq['text']
        assert mq['action'] == 'replace'
        assert len(mq['answers']) > 2

    def test_dietary_info(self, client, monkeypatch):
        def mock_nlp(text, tz=None, input_time=None):
            return {
                "items": [
                    {
                        "amount": 1,
                        "brand_name": None,
                        "children_list": [],
                        "dietary_info": [
                            'LOW FAT FOOD'
                        ],
                        "fid": 6,
                        "food": "yogurt",
                        "is_category": False,
                        "parent_food": None,
                        "preparation_technique": None,
                        "relative_size": None,
                        "type": "food",
                        "unit_type": "Serving",
                        "weight": 150
                    }
                ]
            }

        with monkeypatch.context() as m:
            m.setattr("food.nlp.analyze", mock_nlp)
            items_low_fat = self.food_items_from_text(client, 'low fat yogurt')

        items_regular = self.food_items_from_text(client, 'yogurt')

        assert len(items_regular) == 1
        assert items_regular[0]['food'] == 'yogurt'
        assert len(items_regular[0]['attributes']) == 0

        assert len(items_low_fat) == len(items_regular)

        # nutrients are recalculated based on low fat attribute:
        assert items_low_fat[0]['nutrients']['total_fat']['value'] < items_regular[0]['nutrients']['total_fat']['value']

    def test_brand(self, client):

        items_low_fat = self.food_items_from_text(client, 'low fat danone yogurt')
        items_regular = self.food_items_from_text(client, 'danone yogurt')

        assert len(items_regular) == 1
        assert items_regular[0]['food'] == 'yogurt'
        # Not inconsistent for different DB
        # danone_attributes = items_regular[0]['attributes']
        # assert len(danone_attributes) == 1
        # assert danone_attributes[0]['value'].upper() == 'DANONE'

        assert len(items_low_fat) == 1
        assert 'food' in items_low_fat[0] and type(items_low_fat[0]['food']) == str
        # Not inconsistent for different DB
        # attributes_low_fat = items_low_fat[0]['attributes']
        # assert len(attributes_low_fat) == 2
        # assert attributes_low_fat[0]['value'] == 'LOW FAT FOOD' or attributes_low_fat[1]['value'] == 'LOW FAT FOOD

        # nutrients are recalculated based on low fat and danone attributes:
        assert items_low_fat[0]['nutrients']['total_fat']['value'] <= items_regular[0]['nutrients']['total_fat']['value']

    def test_no_time(self, client):
        items = self.food_items_from_text(client, 'I ate an apple')
        assert len(items) == 1
        item = items[0]
        #doing insted:
        assert 'time' in item


    def test_wrong_language(self, client):
        items = self.food_items_from_text(client, 'pizza', lang='il')
        assert len(items) == 1
        assert len(items[0]['questions']) >= 1
