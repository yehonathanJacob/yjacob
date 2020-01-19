import pytest
#nlp use

@pytest.mark.django_db
def test_nlp_json(client):
	response = client.get('/food/nlp_json',data={'format':'json'}, follow=True)
	data = response.json()
	assert type(data) == dict
	assert 'gram_factors' in data and len(data['gram_factors'])>0
	assert 'food_is_countable' in data and len(data['food_is_countable'])>0
	assert 'food_names' in data and len(data['food_names'])>0
	assert 'measure_words' in data and len(data['measure_words'])>0
	assert 'default_units' in data and len(data['default_units'])>0
	assert 'category' in data and len(data['category'])>0
	assert 'food_hierarchy' in data and len(data['food_hierarchy'])>0
	assert 'intent_words' in data and len(data['intent_words'])>0
	assert 'food_units' in data and len(data['food_units'])>0
	assert 'adjectives' in data and len(data['adjectives'])>0
	assert 'quantity_types' in data and len(data['quantity_types'])>0
	assert 'adding_words' in data and len(data['adding_words'])>0
	assert 'quantity_type_names' in data and len(data['quantity_type_names'])>0

@pytest.mark.django_db
def test_names_list_to_food_cach(client):
	response = client.get('/food/api/nlp/names_list_to_food', follow=True)
	assert str(response.content, 'utf-8') == 'food - ex'

@pytest.mark.django_db
def test_names_list_to_food_try(client):
	response = client.post('/food/api/nlp/names_list_to_food',data={'names':'["mango", "apple", "orange", "beer"]','fraction':0.4}, follow=True)
	assert 'fruit' == str(response.content, 'utf-8')

