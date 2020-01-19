from builtins import object
import os
import pytest
from food.models import *
from collections import defaultdict

def get_updated_nutrient_dict(monkeypatch):
	class get_FoodHier(object):
		def __init__(self,*args,**kwargs):
			pass
		def values(self,*args,**kwargs):
			return [
				{'fid':11, 'parent':1, 'is_representative':True},
				{'fid': 404, 'parent': 1, 'is_representative': True},
				{'fid': 16978, 'parent': 1, 'is_representative': True},
				{'fid': 572, 'parent': 1, 'is_representative': False},
				{'fid': 1816, 'parent': 1, 'is_representative': False},

				{'fid': 88, 'parent': 11, 'is_representative': True},
				{'fid': 1678, 'parent': 11, 'is_representative': True},
				{'fid': 89, 'parent': 11, 'is_representative': True},

				{'fid': 109, 'parent': 1678, 'is_representative': True},
				{'fid': 108, 'parent': 1678, 'is_representative': False},
				{'fid': 2724, 'parent': 1678, 'is_representative': True},

				{'fid': 23100, 'parent': 404, 'is_representative': False},
				{'fid': 23101, 'parent': 404, 'is_representative': False},
				{'fid': 1126, 'parent': 404, 'is_representative': True},

				{'fid': 62, 'parent': 16978, 'is_representative': False},
				{'fid': 2145, 'parent': 16978, 'is_representative': True},
				{'fid': 53, 'parent': 16978, 'is_representative': False},
				{'fid': 20884, 'parent': 53, 'is_representative': True},

				{'fid': 574, 'parent': 572, 'is_representative': True},
				{'fid': 568, 'parent': 572, 'is_representative': True},
				{'fid': 16088, 'parent': 572, 'is_representative': True},
				{'fid': 15570, 'parent': 574, 'is_representative': True},

				{'fid': 14457, 'parent': 1816, 'is_representative': False},
				{'fid': 1696, 'parent': 1816, 'is_representative': False},
				{'fid': 148, 'parent': 1816, 'is_representative': False},
				{'fid': 14942, 'parent': 1816, 'is_representative': False},
			]
	class get_Food(object):
		def __init__(self,*args,**kwargs):
			pass
		def values(self,*args,**kwargs):
			return [
				{'node_type': 'technical', 'fid': 1, 'name': 'food', 'liquid_loss': None},
				{'node_type': 'broad', 'fid': 11, 'name': 'vegetable', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 53, 'name': 'cabbage_salad', 'liquid_loss': None},
				{'node_type': 'specific', 'fid': 62, 'name': 'avocado_salad', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 88, 'name': 'cucumber', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 89, 'name': 'tomato', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 108, 'name': 'celery_root', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 109, 'name': 'celery_leaves', 'liquid_loss': None},
				{'node_type': 'specific', 'fid': 148, 'name': 'avocado', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 404, 'name': 'meatball', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 568, 'name': 'fried_peanuts', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 572, 'name': 'peanuts', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 574, 'name': 'american_peanuts', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 1126, 'name': 'chicken_patty', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 1678, 'name': 'celery', 'liquid_loss': None},
				{'node_type': 'specific', 'fid': 1696, 'name': 'salt', 'liquid_loss': None},
				{'node_type': 'technical', 'fid': 1816, 'name': 'ingredients', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 2145, 'name': 'cabbage_and_carrot_salad', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 2724, 'name': 'qincaijing', 'liquid_loss': None},
				{'node_type': 'specific', 'fid': 14457, 'name': 'natural_lemon_juice', 'liquid_loss': None},
				{'node_type': 'specific', 'fid': 14942, 'name': 'white_or_red_onion_raw', 'liquid_loss': None},
				{'node_type': 'specific', 'fid': 15570, 'name': 'american_peanuts_shekarchi', 'liquid_loss': None},
				{'node_type': 'specific', 'fid': 16088, 'name': 'peanuts_without_shell_not_roasted',
				 'liquid_loss': None},
				{'node_type': 'common', 'fid': 16978, 'name': 'salad_based_on_vegetables', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 20884, 'name': 'cabbage_salad_in_canola_oil', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 23100, 'name': 'turkey_and_veal_meatballs', 'liquid_loss': None},
				{'node_type': 'common', 'fid': 23101, 'name': 'veal_meatballs', 'liquid_loss': None}
			]

	class get_FoodComponents(object):
		def __init__(self,*args,**kwargs):
			pass
		def values(self, *args, **kwargs):
			return [
				{'amount': 3.57142857142857, 'component': 14457, 'fid': 2145},
				{'amount': 0.811688311688312, 'component': 1696, 'fid': 2145},
				{'amount': 76.6233766233766, 'component': 148, 'fid': 2145},
				{'amount': 18.9935064935065, 'component': 14942, 'fid': 2145}
			]

	def get_nutrient_dict():
			return defaultdict(dict,{
							404 :{
								74 : {'amount': Decimal('1.4102256464927816'), 'sd_amount': Decimal('0.69434840687797816581046968051495'), 'unit': u'g'} ,
								100 : {'amount': Decimal('1.5107991553969303'), 'sd_amount': Decimal('1.09073406807454988811964016467860'), 'unit': u'g'} ,
								107 : {'amount': Decimal('0.31602424120605324230'), 'sd_amount': Decimal('0.234290748717461205203431034041916127'), 'unit': u'g'} ,
								112 : {'amount': Decimal('0.04000000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								115 : {'amount': Decimal('3.3460000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},
							572 :{
								74 : {'amount': Decimal('6.2880000000000000'), 'sd_amount': Decimal('3.9515384345846872'), 'unit': u'g'} ,
								100 : {'amount': Decimal('8.4199998855590820'), 'sd_amount': Decimal('0.523067746327909462569767127539'), 'unit': u'g'} ,
								107 : {'amount': Decimal('0.02666666666666666667'), 'sd_amount': Decimal('0.03771236166328253461'), 'unit': u'g'} ,
								115 : {'amount': Decimal('15.5580000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},
							88 :{
								74 : {'amount': Decimal('1.7400000000000000'), 'sd_amount': Decimal('0.36000000000000000000'), 'unit': u'g'} ,
								90 : {'amount': Decimal('0E-20'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								100 : {'amount': Decimal('0.59999999403953550000'), 'sd_amount': Decimal('0.099999994039535499999999999999'), 'unit': u'g'} ,
								107 : {'amount': Decimal('0.82500000000000000000'), 'sd_amount': Decimal('0.07500000000000000000'), 'unit': u'g'} ,
								112 : {'amount': Decimal('0E-20'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								115 : {'amount': Decimal('0.00300000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},
							1678 :{
								74 : {'amount': Decimal('1.7293500000000000'), 'sd_amount': Decimal('0.10065000000000000000'), 'unit': u'g'} ,
								100 : {'amount': Decimal('1.5120000243186950'), 'sd_amount': Decimal('0.087999999523163000000000000000'), 'unit': u'g'} ,
								107 : {'amount': Decimal('0.37000000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								112 : {'amount': Decimal('0.48000000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								115 : {'amount': Decimal('0.07900000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},
							89 :{
								74 : {'amount': Decimal('2.6300000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								90 : {'amount': Decimal('0E-20'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								100 : {'amount': Decimal('1.20000004768371600000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								107 : {'amount': Decimal('1.37000000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								112 : {'amount': Decimal('0E-20'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								115 : {'amount': Decimal('0.08700000000000000000'), 'sd_amount': Decimal('0.01238951169336386720'), 'unit': u'g'} ,
							},
							109 :{
								100 : {'amount': Decimal('2.2000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},
							108 :{
								100 : {'amount': Decimal('1.2500000000000000'), 'sd_amount': Decimal('0.08660254037844386468'), 'unit': u'g'} ,
							},
							2724 :{
								100 : {'amount': Decimal('1.20000000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},
							1126 :{
								74 : {'amount': Decimal('1.08633369207382200000'), 'sd_amount': Decimal('0.041782081127167000000000000000'), 'unit': u'g'} ,
								100 : {'amount': Decimal('1.23128455877304100000'), 'sd_amount': Decimal('0.047357141971588000000000000000'), 'unit': u'g'} ,
								107 : {'amount': Decimal('0.24281609058380130000'), 'sd_amount': Decimal('0.00933909416198730000000000000000'), 'unit': u'g'} ,
							},
							62 :{
								74 : {'amount': Decimal('1.40103900432586700000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								90 : {'amount': Decimal('0E-20'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								100 : {'amount': Decimal('5.4673700332641600'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								107 : {'amount': Decimal('0.37624999880790710000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								115 : {'amount': Decimal('0.66000000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},
							53 :{
								74 : {'amount': Decimal('4.6258272312511096'), 'sd_amount': Decimal('1.754704494321506377794020932703'), 'unit': u'g'} ,
								100 : {'amount': Decimal('2.0885294675827027'), 'sd_amount': Decimal('0.383278196864128696109909446650'), 'unit': u'g'} ,
								107 : {'amount': Decimal('1.1520544946193694'), 'sd_amount': Decimal('0.18156919928262292642878959715187'), 'unit': u'g'} ,
							},
							574 :{
								74 : {'amount': Decimal('25.6383500000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								100 : {'amount': Decimal('4.1104998588562000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								115 : {'amount': Decimal('15.5580000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},
							568 :{
								74 : {'amount': Decimal('12.1000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								100 : {'amount': Decimal('11.9270000457763700'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								107 : {'amount': Decimal('0.20000000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								112 : {'amount': Decimal('0E-20'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								115 : {'amount': Decimal('15.3030000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},
							16088 :{
								74 : {'amount': Decimal('14.1800000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								100 : {'amount': Decimal('8.1999998092651370'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},
							15570 :{
								74 : {'amount': Decimal('25.6383500000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								100 : {'amount': Decimal('4.1104998588562000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},
							14457 :{
								74 : {'amount': Decimal('2.5200000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								100 : {'amount': Decimal('0.30000001192092900000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								107 : {'amount': Decimal('1.10000000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								115: {'amount': Decimal('4.5200000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'},
							},
							1696 :{
								74 : {'amount': Decimal('0E-20'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								100 : {'amount': Decimal('0E-20'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								115 : {'amount': Decimal('0E-20'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},
							148 :{
								74 : {'amount': Decimal('0.66000000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								100 : {'amount': Decimal('6.6999998092651370'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								107 : {'amount': Decimal('0.12000000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								112 : {'amount': Decimal('0.09000000000000000000'), 'sd_amount': Decimal('0.010000000000000000000000'), 'unit': u'g'} ,
								115 : {'amount': Decimal('1.7693333333333333'), 'sd_amount': Decimal('0.06599663291074443564'), 'unit': u'g'} ,
							},
							14942 :{
								74 : {'amount': Decimal('4.2400000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								100 : {'amount': Decimal('1.70000004768371600000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
								107 : {'amount': Decimal('1.29000000000000000000'), 'sd_amount': Decimal('0'), 'unit': u'g'} ,
							},16978 :{
								115 : {'amount': 0.2865, 'sd_amount': 0.0, 'unit': u'g'},
							},
						}
						)

	def get_fid_permit_inherit_to_child(node_type_to_filter):
		return [ obj['fid'] for obj in list(get_Food().values()) if obj['node_type'] in node_type_to_filter]

	with monkeypatch.context() as m:
		m.setattr("food.models.FoodHier.objects", get_FoodHier)
		FoodHier.objects.exclude = get_FoodHier
		m.setattr("food.models.Food.objects", get_Food)
		Food.objects.all = get_Food
		m.setattr("food.models.FoodComponents.objects", get_FoodComponents)
		FoodComponents.objects.all = get_FoodComponents
		m.setattr("food.models.update_food_nutrients_from_refs", get_nutrient_dict)
		m.setattr("food.models.get_fid_permit_inherit_to_child", get_fid_permit_inherit_to_child)
		inherit_com_spe, children_dict,_ = update_food_nutrients(reference_node_type=1, enable_update=False)
		data = {'inherit_com_spe':inherit_com_spe,'children_dict':children_dict}
	return  data

@pytest.fixture
def data(monkeypatch):
	return get_updated_nutrient_dict(monkeypatch)


@pytest.mark.django_db
def test_updated_nutrient_dict(client,data):
	'''
	Test that the function works, and returns what is supposed
	'''
	assert type(data) == dict
	assert 'inherit_com_spe' in data
	assert 'children_dict' in data

@pytest.mark.django_db
def test_case1(client,data):
	'''
	CASE 1:
		Test the case that the child inherit nutrient with valid value from parent
	parent: [celery:1678] child: [celery_root:108] nutrient[total_sugars:74]
	'''
	inherit_com_spe = data['inherit_com_spe']
	assert float(inherit_com_spe[1678][74]['amount']) == float(inherit_com_spe[108][74]['amount'])

@pytest.mark.django_db
def test_case2(client,data):
	'''
	CASE 2:
		Test the case that the child DON'T inherit nutrient from parent because parent node_type != common and specific
	parent: parent: [vegetable:11] child: [celery:1678] nutrient[added_sugars:90]
	'''
	inherit_com_spe = data['inherit_com_spe']
	assert 90 in inherit_com_spe[11]
	assert 90 not in inherit_com_spe[16789]

@pytest.mark.django_db
def test_case3(client,data):
	'''
	CASE 3:
		Test the case that the child DON'T inherit nutrient from parent because parent dont have nutrient there is not in child
	parent: [meatball:404] child: [chicken_patty:1126] nutrient[dietary_fiber:100]
	'''
	inherit_com_spe = data['inherit_com_spe']
	assert 100 in inherit_com_spe[404]
	assert 100 in inherit_com_spe[1126]
	assert float(inherit_com_spe[404][100]['amount']) != float(inherit_com_spe[1126][100]['amount'])

@pytest.mark.django_db
def test_case4(client,data):
	'''
	CASE 4:
		Test the case that the child inherit form parent, but the child has grandchild with recipe, so the nutrient is inherited but change
	parent: [peanuts:572] child: [american_peanuts:574] grandchild: [american_peanuts_shekarchi:15570] nutrient[total_sugars:74]
	'''
	inherit_com_spe = data['inherit_com_spe']
	children_dict = data['children_dict']
	assert 74 in inherit_com_spe[572]
	assert 74 in inherit_com_spe[574]
	assert 74 in inherit_com_spe[15570]
	assert float(inherit_com_spe[574][74]['amount']) == float(inherit_com_spe[15570][74]['amount'])
	assert float(inherit_com_spe[574][74]['amount']) != float(inherit_com_spe[572][74]['amount'])

@pytest.mark.django_db
def test_case5(client,data):
	'''
	CASE 5:
		Test the case that all grandchild inherit from grandparent.
	parent: [salad_based_on_vegetables:16978] child: [cabbage_salad:53] nutrient[polyunsaturated_fat:115]
	'''
	inherit_com_spe = data['inherit_com_spe']
	children_dict = data['children_dict']
	assert 115 in inherit_com_spe[16978]
	assert 115 in inherit_com_spe[53]
	for child in children_dict[53]:
		assert 115 in inherit_com_spe[child]

@pytest.mark.django_db
def test_case6(client,data):
	'''
	CASE 6:
		Test the case that the child don't inherit form parent because child has recipe.
	parent: [salad_based_on_vegetables:16978] child: [cabbage_and_carrot_salad:2145] nutrient[polyunsaturated_fat:115]
	'''
	inherit_com_spe = data['inherit_com_spe']
	children_dict = data['children_dict']
	assert 115 in inherit_com_spe[16978]
	assert 74 in inherit_com_spe[16978]
	assert 115 not in inherit_com_spe[2145]
	assert 74 in inherit_com_spe[2145]
	assert float(inherit_com_spe[16978][74]['amount']) == float(inherit_com_spe[2145][74]['amount'])
