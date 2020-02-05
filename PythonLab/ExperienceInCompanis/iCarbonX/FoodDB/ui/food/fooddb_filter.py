from __future__ import print_function
from __future__ import absolute_import
import argparse
import sys, os
import logging
from collections import defaultdict, namedtuple
import pandas as pd
import math

import django
from .models import *
from .fooddb_queries import *

def fooddb_filter_runFromQueryDict(qDict):
	res = {'status': 1,
		   'food_list': [{'fid': 1, 'name': 'food'}, {'fid': 2, 'name': 'apple'}, {'fid': 3, 'name': 'banana'}],
		   'columns': ['fid', 'name'],
		   'text': '->'}
	hier_of_filter = ""
	columns = ['fid','name']
	if 'root' in qDict:
		root = qDict.getlist('root')
		hier_of_filter += "root->"
	else:
		root = None
	if 'exclude' in qDict:
		exclude = qDict.getlist('exclude')
		hier_of_filter += "exclude->"
	else:
		exclude = None
	class temp():
		def __init__(self, root=None, exclude=None):
			self.root = root
			self.exclude = exclude
			self.safe = True
	temp_for_foodDic = temp(root=root,exclude=exclude)
	dicFood = get_dic_food(temp_for_foodDic,include_exclude=False,attr=['fid','name'])
	listFid = dicFood.keys()
	if 'load_from_data' in qDict and 'load_from' in qDict:
		fids = [int(obj) for obj in qDict.getlist('load_from')]
		listFid = list(set(fids) & set(listFid))
		hier_of_filter += "load_from_data->"
	if 'food_names' in qDict and len(qDict['food_names'])>1:
		text = qDict['food_names']
		listFid = filter_food_name(dicFood,listFid,text)
		hier_of_filter += "food_names->"

	if 'node_type' in qDict:
		node_type_arr = [int(obj) for obj in qDict.getlist('node_type')]
		listFid = filer_NodeType(dicFood,listFid,node_type_arr)
		hier_of_filter += "node_type->"
		columns.append('node_type')

	if 'attributes' in qDict:
		attributes = [int(obj) for obj in qDict.getlist('attributes')]
		listFid = filter_attribues(dicFood,listFid,attributes)
		columns.append('attributes')
		hier_of_filter += "attributes->"
	if 'rule_nutr_id' in qDict or 'nutrient_100_hights' in qDict or 'nutrient_100_lowest' in qDict or 'nutrient_in_std' in qDict:
		default_value = 'default_unit' in qDict
		nutrientDF = getNutrientDict(dicFood,listFid,default_value,qDict)
	if 'rule_nutr_id' in qDict:
		listFid = filter_rule_nutr_id(listFid,nutrientDF,qDict,dicFood)
		columns.append('nutrients')
		hier_of_filter += "nutrients->"
	if 'nutrient_100_hights' in qDict:
		listFid = filter_nutrient_100(listFid,nutrientDF,qDict.getlist('nutrient_100_hights'),dicFood,False)
		if 'nutrients' not in columns:
			columns.append('nutrients')
		hier_of_filter += "nutrient_100_hights->"
	if 'nutrient_100_lowest' in qDict:
		listFid = filter_nutrient_100(listFid,nutrientDF,qDict.getlist('nutrient_100_lowest'),dicFood,True)
		if 'nutrients' not in columns:
			columns.append('nutrients')
		hier_of_filter += "nutrient_100_lowest->"
	if 'nutrient_in_std' in qDict:
		listFid = filter_nutrient_in_std(listFid, nutrientDF, qDict.getlist('nutrient_in_std'), qDict.getlist('standard_deviations'), dicFood)
		if 'nutrients' not in columns:
			columns.append('nutrients')
		hier_of_filter += "nutrient_in_std->"

	food_list = []
	for fid in listFid:
		dic = {}
		for col in columns:
			value = dicFood[fid][col]
			if type(value) == list:
				value = sorted(list(set(value)))
				value = ", ".join(value)
			dic[col] = u"{}".format(value)
		food_list.append(dic)
	res = {
		'status': 1,
		'food_list': food_list,
		'columns': columns,
		'text': hier_of_filter
	}

	return res
# words = text.split(',')
# q = [Q(name__icontains=w.strip()) for w in words]
# q = reduce(lambda x, y: x & y, q)
# query_set = UsdaFood.objects.filter(q)

def filer_NodeType(dicFood,listFid,node_type_arr):
	qSet = Food.objects.filter(fid__in = listFid,node_type__in = node_type_arr).select_related()
	subList = []
	for food in qSet:
		dicFood[food.fid]['node_type'] =food.node_type.name
		subList.append(food.fid)
	listFid = list(set(listFid)&set(subList))
	return listFid

def filter_food_name(dicFood,listFid,text):
	names = FoodNames.objects.filter(name__icontains=text).values_list('fid', flat=True)
	foods = Food.objects.filter(name__icontains=text.replace(' ', '_')).values_list('fid', flat=True)
	listFid = list((set(names) | set(foods)) & set(listFid))
	return listFid

def filter_attribues(dicFood,listFid,attributes):
	FA = FoodAttributes.objects.filter(fid_id__in=listFid, attr_id__in=attributes).select_related()
	attrFids = []
	for obj in FA:
		attrFids.append(obj.fid_id)
		if 'attributes' not in dicFood[obj.fid_id]:
			dicFood[obj.fid_id]['attributes'] = []
		dicFood[obj.fid_id]['attributes'].append(obj.attr.value)
	listFid = list(set(attrFids) & set(listFid))
	return listFid

def getNutrientDict(dicFood,listFid,default_value,qDict):
	nutrientFilter = list(set(qDict.getlist('nutrient_100_hights') + qDict.getlist('nutrient_100_lowest') + qDict.getlist('rule_nutr_id') + qDict.getlist('nutrient_in_std')))
	nutrientLS = []
	if default_value:
		DUD = default_units_data()
		AI = FoodUnits.all_inhereted()
	print('p0.3')
	qSet = FoodNutrient.objects.filter(fid__in=listFid,nutrient_id__in= nutrientFilter).values()
	#print 'len(qSet)',len(qSet)
	nutrientDict = {obj['id']:obj['name'] for obj in UsdaNutrient.objects.filter(id__in=nutrientFilter).values()}
	for obj in qSet:
		nutrient_id = obj['nutrient_id']
		nutrient_name = nutrientDict[nutrient_id]
		amount = float(obj['amount'])
		unit  = obj['unit']
		fid = obj['fid_id']
		if default_value:
			if fid in DUD and fid in AI and DUD[fid][0] in AI[fid]:
				ratio = float(DUD[fid][1]) * AI[fid][DUD[fid][0]]
				amount = (ratio/100)*amount
		nutrientLS.append({'fid':fid,'nutrient_id':nutrient_id,'nutrient_name':nutrient_name,'amount':amount,'unit':unit})
	print('p0.4')
	nutrientDF = pd.DataFrame(nutrientLS)
	return nutrientDF

def filter_rule_nutr_id(listFid,nutrientDF,qDict,dicFood):
	rules = {}
	for r_nutr_id, r_min,r_max in zip(qDict.getlist('rule_nutr_id'),qDict.getlist('rule_min'),qDict.getlist('rule_max')):
		nutr_id = int(r_nutr_id)
		min = float(r_min)
		max = float("inf") if r_max == "-1" else float(r_max)
		rules[nutr_id]=[min,max]
	return filter_by_rule(listFid,nutrientDF,dicFood,rules)

def filter_by_rule(listFid,nutrientDF,dicFood,rules):
	'''
	:param rules: { nitrient_id: [min,max], ... }
	'''
	n = nutrientDF[nutrientDF.apply(
		lambda row: row['nutrient_id'] in rules and row['amount'] >= rules[row['nutrient_id']][0] and row['amount'] <=
					rules[row['nutrient_id']][1], axis=1)]
	listFid = list(set(listFid) & set(n['fid'].tolist()))
	for index,row in n.iterrows():
		fid = row['fid']
		amount = row['amount']
		unit = row['unit']
		name = row['nutrient_name']
		if 'nutrients' not in dicFood[fid]:
			dicFood[fid]['nutrients'] = []
		amount = "{:.2f}".format(amount) if amount >= 0.1 else "{:.2e}".format(amount)
		dicFood[fid]['nutrients'].append('[nutrient: {}, amount: {}, unit: {}]'.format(name, amount,unit))
	return listFid

def filter_nutrient_100(listFid,nutrientDF,nutr_arr,dicFood,ascending):
	subDF = nutrientDF[nutrientDF['fid'].isin(listFid)].sort_values(by=['amount'], ascending=ascending)
	groups = subDF.groupby('nutrient_id')
	subListFid =[]
	nutr_arr = [int(obj) for obj in nutr_arr]
	for nutrient_id,group in groups:
		if nutrient_id in nutr_arr:
			for row in group.head(100).itertuples():
				fid = row.fid
				amount = row.amount
				unit = row.unit
				name = row.nutrient_name
				subListFid.append(fid)
				if 'nutrients' not in dicFood[fid]:
					dicFood[fid]['nutrients'] = []
				amount = "{:.2f}".format(amount) if amount >= 0.1 else "{:.2e}".format(amount)
				dicFood[fid]['nutrients'].append('[nutrient: {}, amount: {}, unit: {}]'.format(name, amount,unit))
	listFid = list(set(listFid)&set(subListFid))
	return listFid

def filter_nutrient_in_std(listFid, nutrientDF, nutr_arr,std_arr, dicFood):
	subDF = nutrientDF.groupby('nutrient_id').agg(['mean','std'])[['amount']]
	rules = {} #{} { nitrient_id: [min,max], ... }
	std_dict = {int(nutr_id):float(std) for nutr_id,std in zip(nutr_arr,std_arr)}
	for nutrient_id, serice in subDF.iterrows():
		if nutrient_id in std_dict:
			dic = {}
			for key,value in pd.DataFrame(serice).iterrows():
				dic[key[1]] = value[nutrient_id]
			median = dic['mean']
			std = dic['std'] *std_dict[nutrient_id]
			rules[nutrient_id] = [median-std,median+std]
	return filter_by_rule(listFid,nutrientDF,dicFood,rules)

