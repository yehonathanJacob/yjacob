from __future__ import print_function
from __future__ import absolute_import
import argparse
import sys, os
import logging
from collections import defaultdict, namedtuple
import pandas as pd
import math
import copy

import django
from .models import *

class finds_outlier_nutrients(object):
	def __init__(self, nutrient_names, root = None, exclude = None, standard_deviations=None,is_representative = None):
		if type(nutrient_names) == list:
			self.nutrient_names = nutrient_names
		else:
			logging.error("nutrient_names MUST BE list")
			sys.exit(1)
		if not (root and type(root) == list):
			logging.warning('default root was taken')
		self.root = root
		if not (exclude and type(exclude) == list):
			logging.warning('default exclude was taken')
		self.exclude = exclude
		if standard_deviations is not None and type(standard_deviations) == float:
			self.standard_deviation_filter = standard_deviations
		else:
			logging.warning('default standard deviations was taken')
			self.standard_deviation_filter = 2
		if is_representative is not None and type(is_representative) == bool:
			self.is_representative = is_representative
		else:
			logging.warning('default is representative was taken')
			self.is_representative = False



	def get_listNutrient(self):
		"""
		:return: [ {'id': ,'name'},  ]
		"""
		if self.runSafe:
			arr = [int(obj) for obj in self.nutrient_names]
			d = UsdaNutrient.objects.filter(id__in=arr).values('id', 'name')
		else:
			d = UsdaNutrient.objects.filter(name__in=self.nutrient_names).values('id', 'name')
		if len(d) == len(self.nutrient_names):
			return d
		logging.error('one or more Nutrient id not finded: %s' % (str(self.nutrient_names)))
		sys.exit(1)

	def getChilds(self, dicFood):
		"""
		:param dicFood: { fid: {'name':  fid.name} , }
		:return: newDicFood: { fid: {'name':fid.name, 'id': fid_id, 'childs':[ {newDicFood, newDicFood, } ] }, }
		"""
		newDicFood = {}
		FH = FoodHier.objects.filter(parent_id__in=dicFood.keys(), is_primary=True)
		if self.is_representative:
			FH = FH.filter(is_representative= True)
		FH = FH.values()
		noName = []
		for obj in FH:
			if obj['parent_id'] not in newDicFood.keys():
				newDicFood[obj['parent_id']] = {'name': dicFood[obj['parent_id']]['name'], 'childs': [], 'id': obj['parent_id']}
			if obj['fid_id'] not in newDicFood.keys():
				if obj['fid_id'] in dicFood.keys():
					newDicFood[obj['fid_id']] = {'name': dicFood[obj['fid_id']]['name'], 'childs': [], 'id': obj['fid_id']}
				else:
					noName.append(obj['fid_id'])
					newDicFood[obj['fid_id']] = {'name': "", 'childs': [], 'id': obj['fid_id']}
			newDicFood[obj['parent_id']]['childs'].append([newDicFood[obj['fid_id']],obj['is_representative']])
		if noName:
			noName = Food.objects.filter(fid__in = noName).values()
			for obj in noName:
				newDicFood[obj['fid']]['name'] = obj['name']
		return newDicFood

	def getNutrient(self, dicFood, listNutrient):
		"""
		:param dicFood: { fid: {'name':  fid.name, .. }, }
		:param listNutrient: [ {'id':nutrient_id, 'name': nutrient.nam } ,]
		:return: dicFood: { fid: {'name':  fid.name, 'nutrients':{nutrient_id: amount, .. } , .. }, }
		"""
		d = FoodNutrient.objects.filter(fid_id__in=dicFood.keys(), nutrient_id__in=[obj['id'] for obj in listNutrient])
		for obj in d:
			if 'nutrients' not in dicFood[obj.fid_id].keys():
				dicFood[obj.fid_id]['nutrients'] = {}
			dicFood[obj.fid_id]['nutrients'][obj.nutrient_id] = float(obj.amount)

		return dicFood

	def getData(self, dicFood, newDicFood, listNutrient):
		"""
		:param dicFood: { fid: {'name':  fid.name} , }
		:param newDicFood: { fid: {'name':  fid.name, 'nutrients':{nutrient_id: amount, .. } , .. }, }
		:param listNutrient: [ {'id':nutrient_id, 'name': nutrient.nam } ,]
		:return: data: [{'parent_name':, 'parent_fid':, 'child_name': ,
							'child_fid':, 'nutrient_name': ,'nutrient_id': ,
							'average':,'standard_deviation':,'amount_of_child': ,
							'distance_of_child': }]
		"""
		data = []
		dicKeys = list(set(dicFood.keys()) & set(newDicFood.keys()))
		for nut in listNutrient:
			logging.info("- Nutrient: %s" % (str(nut)))
			for key_parent in dicKeys:
				sum = 0.0
				num = 0.0
				parent = newDicFood[key_parent]
				#logging.info("-  - Parent: %s" % (parent['name'].encode("utf-8")))
				for child,is_representive in parent['childs']:
					if 'nutrients' in child.keys() and nut['id'] in child['nutrients'].keys():
						sum += child['nutrients'][nut['id']]
						num += 1.0
				if num > 0:
					average = sum / num
					sum = 0.0
					for child,is_representive in parent['childs']:
						if 'nutrients' in child.keys() and nut['id'] in child['nutrients'].keys():
							sum += pow((child['nutrients'][nut['id']] - average), 2)
					sum = sum / num
					standard_deviation = math.sqrt(sum)
					standard_deviation_filter = self.standard_deviation_filter
					for child,is_representive in parent['childs']:
						if 'nutrients' in child.keys() and nut['id'] in child['nutrients'].keys() and abs(
										child['nutrients'][nut['id']] - average) > standard_deviation_filter * standard_deviation:
							distance_of_child = child['nutrients'][nut['id']] - average
							data.append(
								{'parent_name': parent['name'], 'parent_fid': key_parent, 'child_name': child['name'],
								 'child_fid': child['id'],'child_is_representive':is_representive,
								 'nutrient_name': nut['name'],
								 #'nutrient_id': nut['id'],
								 'parent_average': average, 'parent_standard_deviation': standard_deviation,
								 'amount_of_child': child['nutrients'][nut['id']],
								 'deviation_of_child': abs(distance_of_child/standard_deviation),
								 'distance_of_child': distance_of_child})
		return data

	def run(self):
		'''
		:return: data: contain all data of this query
		'''
		self.runSafe = False
		self.safe = True
		logging.info("checking data")
		listNutrient = self.get_listNutrient()
		logging.info("getting dic food")
		dicFood = get_dic_food(self,include_exclude=False)
		logging.info("getting childs food")
		newDicFood = self.getChilds(dicFood)
		logging.info("getting nutrient for each food")
		newDicFood = self.getNutrient(newDicFood, listNutrient)
		logging.info("getting data:")
		data = self.getData(dicFood, newDicFood, listNutrient)
		return data

	def runSafe(self):
		self.runSafe = True
		self.safe= True
		listNutrient = self.get_listNutrient()
		dicFood = get_dic_food(self,include_root=False,include_exclude=False)
		newDicFood = self.getChilds(dicFood)
		newDicFood = self.getNutrient(newDicFood, listNutrient)
		data = self.getData(dicFood, newDicFood, listNutrient)
		return {'data':data,'status':1,'Columns':['parent_name', 'parent_fid', 'child_name', 'child_fid', 'child_is_representive',
												  'nutrient_name',
												  #'nutrient_id',
												  'parent_average', 'parent_standard_deviation',
												  'amount_of_child', 'deviation_of_child', 'distance_of_child']}

class report_inconsistent_default_units(object):
	def __init__(self, maximal_percent = None, root = None, exclude = None):
		if maximal_percent and type(maximal_percent) == float:
			self.maximal_percent = maximal_percent
		else:
			logging.warning("defult maximal_percent was taken")
			self.maximal_percent = 125.0
		logging.info("maximal percent: %f"%(self.maximal_percent))
		if not (root and type(root) == list):
			logging.warning('defult root was taken')
		self.root = root
		if not (exclude and type(exclude) == list):
			logging.warning('defult exclude was taken')
		self.exclude = exclude

	def sortData(self, data):
		"""
		:param data: [ {obj of data} ]
		:return: sorted data by hier tree
		"""
		lst = get_sortedByHier_fidList()
		for obj in data:
			obj['index'] = lst.index(obj['fid'])
		return data

	def getData(self, dicFood):
		"""
		:param dicFood: {fid: 'name'}
		:return: [ {} ]
		"""
		logging.info("- get default_units_data")
		DUD = default_units_data()
		logging.info("- get FoodUnits.all_inhereted")
		AI = FoodUnits.all_inhereted()
		FU = FoodUnits.objects.all().values()
		lsFU = [str(obj['fid_id'])+"_"+str(obj['unit_id']) for obj in FU ]
		FD =  FoodDefaultUnit.objects.all().values()
		lsFD = [str(obj['fid_id'])+"_"+str(obj['unit_id']) for obj in FD]
		ServingID = Units.objects.get(name_en="Serving").pk
		percent_max = self.maximal_percent / 100.0
		percent_min = 100.0 / self.maximal_percent
		data = []
		logging.info("- run over: %d items" % (len(dicFood.keys())))
		num_of_no_AI = 0
		for key in dicFood.keys():
			food = dicFood[key]
			if key in DUD.keys() and key in AI.keys() and ServingID in AI[key].keys():
				default = DUD[key]
				serving = AI[key][ServingID]
				originServing = "" if str(key)+"_"+str(ServingID) not in lsFU else AI[key][ServingID]
				originUnit = "" if str(key)+"_"+str(default[0]) not in lsFD else default[0]
				oridinWeight = "" if str(key) + "_" + str(default[0]) not in lsFU else AI[key][default[0]]
				if default[0] in AI[key].keys():
					weight = AI[key][default[0]]
					if not (float(default[1]) * weight * percent_min) <= serving <= (
							float(default[1]) * weight * percent_max):
						data.append({'Food_name': food['name'], 'fid': key,
									 'defult_unit': default[0], 'defult_unit_sum':float(default[1]) , 'origin_unit':originUnit, 'origin_amount':'',
									 'weight': weight, 'origin_weight':oridinWeight, 'unit*weight': (float(default[1]) * weight),
									 'serving': serving, 'origin_serving':originServing, 'status': 'serving not in range'
									 })
				else:
					data.append({'Food_name': food['name'], 'fid': key,
								 'defult_unit': default[0],'defult_unit_sum' :float(default[1]), 'origin_unit':originUnit, 'origin_amount':'',
								 'weight': "", 'origin_weight':oridinWeight, 'unit*weight': "",
								 'serving': serving, 'origin_serving':originServing, 'status': 'defult unit not in food units'
								 })
			elif not (key in DUD.keys() and key in AI.keys()):
				if not key in DUD.keys():
					logging.error("miising key: %s in default_units_data" % (str(key)))
				else:
					num_of_no_AI += 1
		if num_of_no_AI > 0:
			logging.error("there are: %d of foods in dicFood with no FoodUnits" % (num_of_no_AI))
		return data

	def convertData(self, data):
		"""
		:param data:
		:return:
		"""
		listUnitId = []
		for obj in data:
			listUnitId.append(obj['defult_unit'])
		listUnit = Units.objects.filter(unit_id__in=listUnitId).values('unit_id', 'name_en')
		dicUnit = {}
		for obj in listUnit:
			dicUnit[obj['unit_id']] = obj['name_en']
		for obj in data:
			unitName = dicUnit[obj['defult_unit']]
			obj['defult_unit'] = str(unitName)+": "+str(obj['defult_unit_sum'])
			if not obj['origin_unit'] == "":
				obj['origin_unit'] = unitName
				obj['origin_amount'] = obj['defult_unit_sum']
		#delete un relevent row (with no _origin)
		newData = [obj for obj in data if obj['origin_unit'] or obj['origin_amount'] or obj['origin_weight'] or obj['origin_serving']]
		return newData

	def run(self):
		self.runSafe = False
		self.safe = False
		logging.info("get dic food")
		dicFood = get_dic_food(self,include_exclude=False)
		logging.info("get data")
		data = self.getData(dicFood)
		logging.info("convert data")
		data = self.convertData(data)
		data = self.sortData(data)
		data = sorted(data, key=lambda k: k['index'])
		return data

	def runSafe(self):
		self.runSafe = True
		self.safe = True
		dicFood = get_dic_food(self,include_exclude=False)
		data = self.getData(dicFood)
		data = self.convertData(data)
		data = self.sortData(data)
		data = sorted(data, key=lambda k: k['index'])
		return {'data': data, 'status': 1, 'Columns': ['Food_name','fid','defult_unit','origin_unit','origin_amount',
													   'weight', 'origin_weight', 'unit*weight','serving',
													   'origin_serving','status']}

class attr_id_AND_fid(object):
	def __init__(self,safe , type_id = None, type_name = None, only_new = None,excluding = None,attributes = []):
		self.safe = safe
		if self.safe:
			if type_id and type(type_id) == int:
				self.type_id = type_id
			else:
				logging.warning('no type id')
				self.type_id = None

			if type_name and type(type_name ) == str:
				self.type_name = type_name
			else:
				logging.warning('no type name')
				self.type_name = None

			if only_new and type(only_new) == str:
				self.only_new = only_new
			else:
				logging.warning('no only new')
				self.only_new = None

			if excluding is not None:
				self.excluding = excluding
			else:
				logging.warning('no excluding')
				self.excluding = excluding
		else:
			self.type_id = type_id
			self.type_name = type_name
			self.only_new = only_new
			self.excluding = excluding
		if type(attributes) == list:
				self.attributes = attributes

	def get_all_attribute_rellevent_name(self, type_id=-1):
		"""
		Input: optional: type_id of relevent attributes, defult -1 for all of them
		Output: [{ "id":atrr_id, "names": [], "value": "", "type_id": -1}, ]
		"""
		logging.info("doing query: get_all_attribute_rellevent_name")
		dbList = []
		if type_id == -1:
			dbList = Attribute.objects.all().values()
		else:
			dbList = Attribute.objects.filter(type_id=type_id).values()
		db = []
		ls = []
		for obj in dbList:
			if obj['id'] in ls:
				logging.error('id: %d id twice in food_attribute, taken only one')
				sys.exit(1)
			else:
				ls.append(obj['id'])
				db.append({"id": obj['id'], "names": [obj['value']], "value": obj['value'], "type_id": obj['type_id']})
		dbList = AttributeName.objects.all().values()
		for obj in dbList:
			if obj['attribute_id'] in ls:
				i = ls.index(obj['attribute_id'])
				db[i]["names"].append(obj['name'])
		return db

	def get_attributes_name_from_list(self, attributes=[]):
		dbList = Attribute.objects.filter(id__in = attributes).values()
		db = []
		ls = []
		for obj in dbList:
			if obj['id'] in ls:
				sys.exit(1)
			else:
				ls.append(obj['id'])
				db.append({"id": obj['id'], "names": [obj['value']], "value": obj['value'], "type_id": obj['type_id']})
		dbList = AttributeName.objects.all().values()
		for obj in dbList:
			if obj['attribute_id'] in ls:
				i = ls.index(obj['attribute_id'])
				db[i]["names"].append(obj['name'])
		return db

	def get_comper_fid_TO_attr_id(self, backData=None):
		"""
		Output: [{ "fid": food.fid, "food_name": food.name, "attr_name": AttributeName.name , "attr_id": Attribute.id, "type_id": -1}, ]
		"""
		data = []
		if not backData is None:
			data = backData
			#data = data.T.to_dict().values()
		else:
			logging.info('taking data from server')
			if not self.type_id:
				logging.warning('should have "type_id" parameter if using this function, otherwise it brings all')
				self.type_id = -1
			data = self.get_all_attribute_rellevent_name(type_id=self.type_id)
		old = data
		data = []
		for obj in old:
			data.append({"attr_id": obj["id"], "attr_name": obj["value"], "type_id": obj["type_id"],
						 "names": obj["names"]})
		old = data
		data = []
		reload(sys)
		sys.setdefaultencoding('utf8')
		if self.safe:
			logging.info("working on attribute")
		for obj in old:
			#logging.info("|-working on attr: %s" % (obj["attr_name"]))
			fids = []
			foods = []
			for name in obj["names"]:
				#logging.info("|\t|-working on name: %s" % (name))
				fid_list = foods_for_short(name, asSubstring=False)
				for obj2 in fid_list:
					if not (obj2['id'] in fids):
						fids.append(obj2['id'])
						foods.append({"fid": obj2['id'], "food_name": obj2['text']})
			data.append(
				{"attr_id": obj["attr_id"], "attr_name": obj["attr_name"], "type_id": obj["type_id"], "foods": foods})

		if self.safe:
			logging.info("working on excluded data")
		# exclud old data and 'args.excluding' data
		old = data
		data = []
		self.dfEx = pd.DataFrame(columns=['fid', 'attr_id'])
		if self.excluding is not None and self.excluding.any:  # exclud file must have [fid,attr_id]
			self.dfEx =  self.excluding
			for col in ('fid', 'attr_id'):  # check excluding file
				if col not in self.dfEx.columns:
					logging.error('Csv file does not have a "%s" column. Columns found: %s', col, self.dfEx.columns)
					sys.exit(2)
		FA = FoodAttributes.objects.all().values()
		FAarr = [str(obj['fid_id'])+'_'+str(obj['attr_id']) for obj in FA]
		for obj in old:
			for food in obj["foods"]:
				if ((not self.only_new) or (str(food["fid"])+'_'+str(obj["attr_id"]) not in FAarr)) and not (
					(self.dfEx['fid'] == food["fid"]) & (self.dfEx['attr_id'] == obj["attr_id"])).any():
					data.append({"fid": food["fid"], "food_name": food['food_name'], "attr_name": obj["attr_name"],
								 "attr_id": obj["attr_id"], "type_id": obj["type_id"]})
		return data

	def run(self):
		backData = None
		if self.type_name:
			dt = AttributeType.objects.filter(name=self.type_name)
			if dt:
				self.type_id = dt[0].id
				logging.info("type_id selected: %s" % (str(self.type_id)))
			else:
				logging.error("type name: %s is not found in food_attributetype" % (self.type_name))
				sys.exit(1)
		logging.info("doing query: get_comper_fid_TO_attr_id")
		backData = self.get_comper_fid_TO_attr_id(backData)
		return backData

	def runSafe(self):
		backData = self.get_attributes_name_from_list(self.attributes)
		backData = self.get_comper_fid_TO_attr_id(backData)
		return {'data': backData, 'status': 1, 'Columns': ["fid", "food_name", "attr_name", "attr_id", "type_id"]}

class nutrient_TO_fid(object):
	def __init__(self, read_from_csv, root = None, exclude = None, only_new = None, excluding = None):
		if read_from_csv is None:
			logging.error("need to have read_from_csv")
			sys.exit(1)
		else:
			self.read_from_csv = read_from_csv
			if type(self.read_from_csv) == list:
				self.safe = False
			else:
				self.safe = True
		if self.safe:
			if not (root and type(root) == list):
				logging.warning('defult root was taken')
			self.root = root
			if not (exclude and type(exclude) == list):
				logging.warning('defult exclude was taken')
			self.exclude = exclude

			if only_new and type(only_new) == str:
				self.only_new = only_new
			else:
				logging.warning('no only new')
				self.only_new = None

			if excluding is not None:
				self.excluding = excluding
			else:
				logging.warning('no excluding')
				self.excluding = excluding
		else:
			self.root = root
			self.exclude = exclude
			self.only_new = only_new
			self.excluding = excluding


	def check_data(self,read_from_csv):
		"""
		Input: a CSV file to check the data in it
		Output: number of errors
		:param read_from_csv_file: the path to the CSV file
		"""
		# check read_from_csv_file file
		df = read_from_csv
		numError = 0
		for col in ('nutrient_name', 'min', 'max', 'attribute_name', 'nutrient_name2', 'action'):
			if col not in df.columns:
				logging.error('Csv file does not have a "%s" column. Columns found: %s', col, df.columns)
				numError += 1
		if df.dtypes['nutrient_name'] != 'O':
			logging.error('Csv file contains non-string values in "nutrient_name" column')
			numError += 1
		if df.dtypes['min'] != int and df.dtypes['min'] != float:
			logging.error('Csv file contains non-float values in "min" column')
			numError += 1
		if df.dtypes['max'] != int and df.dtypes['max'] != float:
			logging.error('Csv file contains non-float values in "max" column')
			numError += 1
		if df.dtypes['attribute_name'] != 'O':
			logging.error('Csv file contains non-string values in "attribute_name" column')
			numError += 1
		indices_of_rows_without_nutrient_name = []
		indices_of_rows_without_nutrient_name2 = []
		indices_of_rows_without_attribute_name = []
		for i, row in df.iterrows():
			if pd.isnull(row['nutrient_name']):
				indices_of_rows_without_nutrient_name.append(i)
			if pd.isnull(row['attribute_name']):
				indices_of_rows_without_attribute_name.append(i)
			if (not pd.isnull(row['nutrient_name2'])) and (
				pd.isnull(row['action']) or not row['action'] in ['/', '*', '+', '-', '%']):
				indices_of_rows_without_nutrient_name2.append(i)
		if indices_of_rows_without_nutrient_name:
			logging.error('Rows without nutrient_name detected. Indices: %s', indices_of_rows_without_nutrient_name)
			numError += len(indices_of_rows_without_nutrient_name)
		if indices_of_rows_without_attribute_name:
			logging.error('Rows without attribute_name detected. Indices: %s', indices_of_rows_without_attribute_name)
			numError += len(indices_of_rows_without_attribute_name)
		if indices_of_rows_without_nutrient_name2:
			logging.error('Rows with nutrient_name2 but without action in ["/","*","+","-","//"] detected. Indices: %s',
						  indices_of_rows_without_nutrient_name2)
			numError += len(indices_of_rows_without_nutrient_name2)
		# check excluding_csv file
		if self.excluding is not None and self.excluding.any:  # exclud file must have [fid,attr_id]:
			dfEx = self.excluding
			for col in ('fid', 'attr_id'):
				if col not in dfEx.columns:
					logging.error('Csv file does not have a "%s" column. Columns found: %s', col, dfEx.columns)
					numError += 1
		return numError

	def conver_data(self,read_from_csv):
		"""
		Input: a CSV file to convert the data in it
		Output: [{nutr_id: ,nutr_name: ,min: ,max: ,attr_id: ,attr_name:}, ]
		:param read_from_csv_file: the path to the CSV file
		"""
		df = read_from_csv
		numError = 0
		UN = UsdaNutrient.objects.all()
		AN = AttributeName.objects.all()
		data = []
		for i, row in df.iterrows():
			nutr_id = 0
			nutr_id_2 = None
			action = None
			# nutr_name = ""
			min = 0
			max = float("inf")
			attr_id = 0
			attr_name = ""

			if UN.filter(name=row['nutrient_name']):
				nutr_id = UN.filter(name=row['nutrient_name'])[0].id
				nutr_name = row['nutrient_name']
			else:
				logging.error('Nutrient name: %s in line: %d is not find.' % (row['nutrient_name'], i))
				sys.exit(2)
			if AN.filter(name__iexact=row['attribute_name']):
				attr_id = AN.filter(name__iexact=row['attribute_name'])[0].attribute_id
				attr_name = row['attribute_name']
			else:
				logging.error('Attribute name: %s in line: %d is not find.' % (row['attribute_name'], i))
				sys.exit(2)
			if not math.isnan(row['min']):
				min = row['min']
			if not math.isnan(row['max']):
				max = row['max']
			if not pd.isnull(row['nutrient_name2']):  # for rule with action
				if UN.filter(name=row['nutrient_name2']):
					nutr_id_2 = UN.filter(name=row['nutrient_name2'])[0].id
					action = row['action']
					nutr_name = str(row['nutrient_name']) + str(action) + str(row['nutrient_name2'])
				else:
					logging.error('Nutrient name: %s in line: %d is not find.' % (row['nutrient_name'], i))
					sys.exit(2)
			data.append({'nutr_id': nutr_id, 'nutr_name': nutr_name, 'min': min, 'max': max, 'attr_id': attr_id,
						 'attr_name': attr_name, 'nutr_id_2': nutr_id_2, 'action': action})
		# data.append({'nutr_id': nutr_id, 'min': min, 'max': max, 'attr_id': attr_id, 'attr_name': attr_name})
		return data

	FN = FoodNutrient.objects.all()

	def get_old_connections(self,attrid):
		"""
		Output: all fid <-> attr_id connections
		return: [ 'fid_attr_id', ]
		"""
		FA = FoodAttributes.objects.filter(attr_id=attrid).values()
		ls = []
		logging.info("|  |_getting: %d old connections of attr_id: %d" % (len(FA), attrid))
		for obj in FA:
			ls.append(str(obj['fid_id']) + '_' + str(obj['attr_id']))
		return ls

	def get_list_fid(self, dic, rule):
		"""
		Input: dic of avalibel fid, nutrition id to look for, min snd msx range
		Output: [{fid: ,food_name: ,amount: },]
		"""
		FN = FoodNutrient.objects.all()
		nutr_id = rule['nutr_id']
		min = rule['min']
		max = rule['max']
		list_food = []
		if not rule['nutr_id_2'] is None:  # for rule with action
			nutr_id_2 = rule['nutr_id_2']
			action = rule['action']
			FoodNutrientARR = FN.filter(Q(fid__in=dic.keys()) & (Q(nutrient_id=nutr_id) | Q(nutrient_id=nutr_id_2)))
			if self.safe:
				logging.info('|  |_run over: %d FoodNutrient items.' % (len(FoodNutrientARR)))
			nutrient_dict = defaultdict(dict)
			i = 0
			for f in FoodNutrientARR:
				nutrient_dict[f.fid_id][f.nutrient_id] = {'amount': float(f.amount)}
				nutrient_dict[f.fid_id]['name'] = dic[f.fid_id]
			if self.safe:
				logging.info('|  |  |_run over: %d nutrient_dict items.' % (len(nutrient_dict.keys())))
			for f in nutrient_dict.keys():
				if nutr_id in nutrient_dict[f].keys() and nutr_id_2 in nutrient_dict[f].keys():
					try:
						res = eval(str(nutrient_dict[f][nutr_id]['amount']) + action + str(
							nutrient_dict[f][nutr_id_2]['amount']))
						if res <= max and res >= min:
							list_food.append({'fid': f, 'food_name': nutrient_dict[f]['name'], 'amount': res})
					except Exception as e:
						if self.safe:
							logging.error('Error in item:%s\n\t\teval:%s\n\t\terror:%s' % (nutrient_dict[f], str(
							nutrient_dict[f][nutr_id]['amount']) + action + str(nutrient_dict[f][nutr_id_2]['amount']),
																					   e))
		else:  # for rule with out action
			FoodNutrientARR = FN.filter(
				Q(fid__in=dic.keys()) & Q(nutrient_id=nutr_id) & Q(amount__gte=min) & Q(amount__lte=max))
			if self.safe:
				logging.info('|  |_run over: %d FoodNutrient items.' % (len(FoodNutrientARR)))
			for obj in FoodNutrientARR:
				list_food.append({'fid': obj.fid_id, 'food_name': dic[obj.fid_id], 'amount': obj.amount})
		return list_food

	def getSafeDate(self,dic_fid):
		'''
		Input self.read_from_csv = [{'nutr_id', 'min', 'max', 'attr_id', 'nutr_id_2', 'action'}]
		:return: [{'nutr_id', 'nutr_name', 'min', 'max', 'attr_id', 'attr_name', 'nutr_id_2', 'nutr_name_2', 'action'}]
		'''
		nutrients = []
		attributes = []
		for rul in self.read_from_csv:
			nutrients.append(rul['nutr_id'])
			attributes.append((rul['attr_id']))
			if rul['nutr_id_2'] is not None:
				nutrients.append(rul['nutr_id_2'])
		exLs = []
		if self.only_new:
			FA = FoodAttributes.objects.filter(attr_id__in=attributes,fid_id__in = dic_fid.keys()).values()
			for obj in FA:
				exLs.append(str(obj['fid_id']) + '_' + str(obj['attr_id']))
		nutrients = {obj['id']:obj['name'] for obj in UsdaNutrient.objects.filter(id__in=nutrients).values()}
		attributes = {obj['id']:obj['value'] for obj in Attribute.objects.filter(id__in=attributes).values()}
		for	rul in self.read_from_csv:
			rul['nutr_name'] = nutrients[rul['nutr_id']]
			rul['attr_name'] = attributes[rul['attr_id']]
			rul['nutr_name_2'] = None if rul['nutr_id_2'] is None else nutrients[rul['nutr_id_2']]
		return self.read_from_csv, exLs
	def run(self):
		logging.info("checking data")
		numError = self.check_data(self.read_from_csv)
		if numError:
			logging.error("Number of errors: %d" % (numError))
			sys.exit(1)
		logging.info("converting data")
		data = self.conver_data(self.read_from_csv)
		logging.info("get dic food")
		dic_fid = get_dic_food(self, reves_safe=True,include_root = False,include_exclude=True)
		logging.info('number of food: %d' % (len(dic_fid.keys())))
		excluding_data = []
		if self.excluding is not None and self.excluding.any:  # exclud file must have [fid,attr_id]:
			for i, row in self.excluding.iterrows():
				excluding_data.append(str(row['fid']) + '_' + str(row['attr_id']))
		logging.info("number of excluding data: %d" % (len(excluding_data)))
		new_connect = []
		ls = []
		logging.info("start working on rules")
		for rule in data:
			logging.info("|_working on rule: %s" % (str(rule)))
			nutr_id = rule['nutr_id']
			min = rule['min']
			max = rule['max']
			old_connections = excluding_data
			if self.only_new == "yes":
				old_connections.extend(self.get_old_connections(rule['attr_id']))
			list_food = self.get_list_fid(dic_fid, rule)
			logging.info('|  |_run over: %d list_food items.' % (len(list_food)))
			for f in list_food:
				connection = '' + str(f['fid']) + '_' + str(rule['attr_id'])
				# checking if to add new connection
				# if not connection in ls and ((not args.only_new) or (not FA.filter(fid_id=f['fid'], attr_id=rule['attr_id']))):
				if not connection in ls and not connection in old_connections:
					ls.append(connection)
					new_connect.append({'fid': f['fid'], 'food_name': f['food_name']['name'], 'attr_id': rule['attr_id'],
										'attr_name': rule['attr_name'], 'nutrient_name': rule['nutr_name'],
										'nutrient_value': f['amount']})
		return new_connect
	def runSafe(self):
		dic_fid = get_dic_food(self, reves_safe=True,include_root = False,include_exclude=True)
		data, excluding_data = self.getSafeDate(dic_fid) #{'nutr_id': nutr_id, 'nutr_name': nutr_name, 'min': min, 'max': max, 'attr_id': attr_id, 'attr_name': attr_name, 'nutr_id_2': nutr_id_2, 'action': action}
		new_connect = []
		ls = []
		for rule in data:
			nutr_id = rule['nutr_id']
			min = rule['min']
			max = rule['max']
			old_connections = excluding_data
			list_food = self.get_list_fid(dic_fid, rule)
			for f in list_food:
				connection = '' + str(f['fid']) + '_' + str(rule['attr_id'])
				if not connection in ls and not connection in old_connections:
					ls.append(connection)
					new_connect.append(
						{'fid': f['fid'], 'food_name': f['food_name']['name'], 'attr_id': rule['attr_id'],
						 'attr_name': rule['attr_name'], 'nutrient_name': rule['nutr_name'],
						 'nutrient_value': float(f['amount'])})
		return {'data': new_connect, 'status': 1, 'Columns': ['fid', 'food_name', 'attr_id', 'attr_name',
															  'nutrient_name', 'nutrient_value']}

class getlistDublicate(object):
	def __init__(self, exclude_lan):
		if exclude_lan is not None and type(exclude_lan) == list:
			self.exclude_lan = exclude_lan
		else:
			self.exclude_lan = []
	def get_allName(self):
		logging.info("get all names exluded language: %s"%(str(self.exclude_lan)))
		listName = FoodNames.objects.all()
		for lan in self.exclude_lan:
			listName = listName.exclude(lang_code=lan)
		listName = listName.values('name','fid_id')
		logging.info("run over: %d FoodNames objects"%(len(listName)))
		dicNames = {}
		for name in listName:
			if name['name'] not in dicNames:
				dicNames[name['name']] = []
			dicNames[name['name']].append(name['fid_id'])
		return dicNames
	def getData(self,dicName):
		data = []
		logging.info("run over: %d names" % (len(dicName.keys())))
		for key in dicName.keys():
			obj = dicName[key]
			if len(obj)>1:
				data.append({'name':key,'fids':str('#'.join([str(x) for x in obj]))})
		return data
	def run(self):
		dicName = self.get_allName()
		data  = self.getData(dicName)
		return data
	def runSafe(self):
		dicName = self.get_allName()
		data  = self.getData(dicName)
		return {'data': data, 'status': 1, 'Columns': ['name','fids']}

class find_problems_in_units(object):
	def __init__(self):
		self.QUERIES = {
			'gram_weight_different_than_1': lambda: self._query_gram_weight_different_than_1(),
			'kg_weight_different_than_1000': lambda: self._query_kg_weight_different_than_1000(),
			'problematic_ratio_between_teaspoon_and_spoon': lambda: self._query_teaspoon_to_spoon_ratio(),
			'zero_weight': lambda: self._query_zero_weight(),
			'negative_weight': lambda: self._query_negative_weight(),
		}

		# Both fids and units_ids_involved can be any iterable
		self.QueryResult = namedtuple('QueryResult', ['fids', 'units_ids_involved'])
		self.QueriesResult = namedtuple('QueriesResult', ['query_names', 'unit_ids_involved'])
		self._units_dict = None

	def get_obj_or_none(self,model_class, **kwargs):
		try:
			return model_class.objects.select_related().get(**kwargs)
		except model_class.DoesNotExist:
			return None

	# unit_id for gram is 2
	def _query_gram_weight_different_than_1(self):
		q = FoodUnits.objects.filter(unit_id__exact=2).exclude(weight__exact=1)
		return self.QueryResult([item.fid.fid for item in q], {2})

	# unit_id for kg is 173
	def _query_kg_weight_different_than_1000(self):
		q = FoodUnits.objects.filter(unit_id__exact=173).exclude(weight__exact=1000)
		return self.QueryResult([item.fid.fid for item in q], {173})


	def _get_units_dict(self):
		if self._units_dict is None:
			self._units_dict = defaultdict(lambda: defaultdict(dict))
			all_food_units = FoodUnits.objects.select_related('fid').select_related('unit').all()
			for food_unit in all_food_units:
				self._units_dict[food_unit.fid.fid][food_unit.unit.unit_id] = food_unit.weight
		return self._units_dict

	# unit_id for teaspoon is 6
	# unit_id for spoon is 0
	def _query_teaspoon_to_spoon_ratio(self):
		def is_ratio_problematic(ratio):
			return ratio <= 2.0 or ratio >= 4

		units_dict = self._get_units_dict()
		return self.QueryResult([fid for fid, units in units_dict.items() if
							6 in units and 0 in units and units[6] != 0 and is_ratio_problematic(
								units[0] / float(units[6]))],
						   {0, 6})

	# Argument should be a predicate accepting a (fid, unit_id, weight)
	def helper_for_unit_predicate_queries(self,unit_predicate):
		units_dict = self._get_units_dict()
		fids = []
		unit_ids_involved = set()
		for fid, units in units_dict.items():
			cur_unit_ids_involved = [unit_id for unit_id, weight in units.items() if
									 unit_predicate((fid, unit_id, weight))]
			if cur_unit_ids_involved:
				fids.append(fid)
				unit_ids_involved.update(cur_unit_ids_involved)
		return self.QueryResult(fids, unit_ids_involved)

	def _query_zero_weight(self):
		return self.helper_for_unit_predicate_queries(lambda fid_unit_id_weight: fid_unit_id_weight[2] == 0)

	def _query_negative_weight(self):
		return self.helper_for_unit_predicate_queries(lambda fid_unit_id_weight1: fid_unit_id_weight1[2] < 0)

	def run_queries(self, queries):
		results = defaultdict(lambda: self.QueriesResult(set(), set()))  # fid -> QueriesResult
		for query_name in queries:
			logging.info("run query: %s" % (query_name))
			query_result = self.QUERIES[query_name]()
			for fid in query_result.fids:
				results[fid].query_names.add(query_name)
				results[fid].unit_ids_involved.update(query_result.units_ids_involved)
		return results

class report_inconsistent_units_fid_to_parent(object):
	def __init__(self, maximal_percent=None, root=None, exclude=None):
		if maximal_percent and type(maximal_percent) == float:
			self.maximal_percent = maximal_percent
		else:
			logging.warning("defult maximal_percent was taken")
			self.maximal_percent = 125.0
		logging.info("maximal percent: %f" % (self.maximal_percent))
		if not (root and type(root) == list):
			logging.warning('defult root was taken')
		self.root = root
		if not (exclude and type(exclude) == list):
			logging.warning('defult exclude was taken')
		self.exclude = exclude

	def getData(self,dicFood):
		listUnits = FoodUnits.objects.filter(fid__in=dicFood.keys()).values()
		for fid in dicFood:
			dicFood[fid]['units'] = {}
		for unit in listUnits:
			if unit['fid_id'] in dicFood.keys():
				dicFood[unit['fid_id']]['units'][unit['unit_id']] = unit['weight']
		foodHire = FoodHier.get_dic_FoodHier()
		data = []
		#logging.info("- run over %d foods"%(len(dicFood.keys())))
		for child_fid in dicFood.keys():
			child = dicFood[child_fid]
			parent_fid = foodHire[child_fid]
			if parent_fid in dicFood.keys():
				parent = dicFood[parent_fid]
				#logging.info("- run over %d units" % (len(child['units'].keys())))
				for unit in child['units'].keys():
					child_value = child['units'][unit]
					if unit in parent['units'].keys():
						parent_value = parent['units'][unit]
						try:
							ratio = 100 * (parent_value / child_value) if parent_value > child_value else 100 * (
									child_value / parent_value)
						except ZeroDivisionError:
							if parent_value == child_value:
								ratio = 100
							else:
								ratio = "infinity"
						if ( ratio == "infinity" or ratio>=self.maximal_percent):
							data.append({'fid_child':child_fid, 'name_child': child['name'],
										 'fid_parent':parent_fid, 'name_parent':parent['name'],
										 'unit':unit, 'weight_child':child_value, 'weight_parent': parent_value,
										 'ratio': ratio})
		return data
	def convertData(self,data):
		logging.info('p1')
		lsUnits = [obj['unit'] for obj in data]
		lsUnits = list(set(lsUnits))
		logging.info('p2')
		dicUnits = Units.objects.filter(unit_id__in = lsUnits).values('unit_id','name_en')
		dicUnits = { obj['unit_id']:obj['name_en'] for obj in dicUnits}
		logging.info('p3')
		for obj in data:
			obj['unit'] = dicUnits[obj['unit']]
		logging.info('p4')
		return data
	def sortData(self, data):
		"""
		:param data: [ {obj of data} ]
		:return: sorted data by hier tree
		"""
		lst = get_sortedByHier_fidList()
		for obj in data:
			obj['index'] = lst.index(obj['fid_child'])
		return data

	def runSafe(self):
		self.runSafe = True
		self.safe = True
		dicFood = get_dic_food(self,include_exclude=False)
		if 1 in dicFood:
			dicFood.pop(1) #we don't want 'food'
		data = self.getData(dicFood)
		data = self.convertData(data)
		data = self.sortData(data)
		data = sorted(data, key=lambda k: k['index'])
		return {'data': data, 'status': 1, 'Columns': ['fid_child', 'name_child',
										 'fid_parent', 'name_parent',
										 'unit', 'weight_child', 'weight_parent', 'ratio']}
class fid_with_child_and_recipe():
	def __init__(self,root=None,exclude=None):
		self.root = root
		self.exclude = exclude

	def getData(self,dicFood):
		listFid = dicFood.keys()
		fid_with_comp = FoodComponents.objects.filter(fid_id__in=listFid).values('fid_id')
		fid_with_comp = [obj['fid_id'] for obj in fid_with_comp]
		fid_with_child = FoodHier.objects.filter(parent_id__in=listFid,is_primary = True).values('parent_id')
		fid_with_child = [obj['parent_id'] for obj in fid_with_child]
		badlist = list(set(fid_with_child) & set(fid_with_comp))
		data = []
		for fid in badlist:
			data.append({'fid':fid,'name':dicFood[fid]['name']})
		return data

	def runSafe(self):
		self.safe = True
		dicFood = get_dic_food(self)
		data = self.getData(dicFood)
		return {'data': data, 'status': 1, 'Columns': ['fid', 'name']}

class fid_NO_with_child_and_recipe():
	def __init__(self,root=None,exclude=None):
		self.root = root
		self.exclude = exclude

	def getData(self,dicFood):
		listFid = dicFood.keys()
		fid_with_comp = FoodComponents.objects.filter(fid_id__in=listFid).values('fid_id')
		fid_with_comp = [obj['fid_id'] for obj in fid_with_comp]
		fid_with_child = FoodHier.objects.filter(parent_id__in=listFid,is_primary = True).values('parent_id')
		fid_with_child = [obj['parent_id'] for obj in fid_with_child]
		fid_with_ref = [obj['fid_id'] for obj in  FoodNutritionRefs.objects.filter(fid_id__in=listFid).values('fid_id')]
		badlist = list(set(listFid) - set(fid_with_child))
		badlist = list(set(badlist) - set(fid_with_comp))
		badlist = list(set(badlist) - set(fid_with_ref))
		data = []
		for fid in badlist:
			data.append({'fid':fid,'name':dicFood[fid]['name']})
		return data

	def runSafe(self):
		self.safe = True
		dicFood = get_dic_food(self)
		data = self.getData(dicFood)
		return {'data': data, 'status': 1, 'Columns': ['fid', 'name']}

class fid_with_missing_nutrients():
	def __init__(self, all_nutrient = False, nutrient_ids=None, root = None, exclude = None):
		if all_nutrient:
			self.nutrient_ids = [obj['id'] for obj in UsdaNutrient.objects.all().values('id')]
		elif nutrient_ids is not None and type(nutrient_ids) == list:
			self.nutrient_ids = [int(obj) for obj in  nutrient_ids]
		else:
			self.nutrient_ids = []
		self.root = root
		self.exclude = exclude

	def getData(self, dicFood):
		listFid = dicFood.keys()
		listFoodNutrient = FoodNutrient.objects.filter(fid_id__in =listFid, nutrient_id__in = self.nutrient_ids).values()
		for obj in listFid:
			dicFood[obj]['nutrients'] = []
		for obj in listFoodNutrient:
			dicFood[obj['fid_id']]['nutrients'].append(obj['nutrient_id'])
		data = []
		for fid in listFid:
			for nutrient_id in self.nutrient_ids:
				if nutrient_id not in dicFood[fid]['nutrients']:
					data.append({'fid':fid,'food_name':dicFood[fid]['name'],'nutrient_id':nutrient_id})
		UsdaNutrientsDic = {obj['id']:obj['name']
							for obj in UsdaNutrient.objects.filter(id__in=self.nutrient_ids).values() }
		for obj in data:
			obj['nutrient_name'] = UsdaNutrientsDic[obj['nutrient_id']]
		return data

	def runSafe(self):
		self.safe = True
		dicFood = get_dic_food(self)
		data = self.getData(dicFood)
		return {'data': data, 'status': 1, 'Columns': ['fid','food_name','nutrient_id','nutrient_name']}

class fid_with_nutrient_out_of_given_range():
	def __init__(self, min=0, max_g=100,max_kcal=900, root=None, exclude=None):
		self.root = root
		self.exclude = exclude
		self.min = min
		self.max_g = max_g
		self.max_kcal = max_kcal

	def getData(self, dicFood):
		listFid = dicFood.keys()
		badList = FoodNutrient.objects.filter(fid_id__in= listFid)
		badList = badList.filter(Q(amount__lt = self.min)
											| Q(unit = 'g',amount__gt =self.max_g)
											| Q(unit = 'kcal',amount__gt=self.max_kcal)).values()
		lsNutrient = []
		data=[]
		for obj in badList:
			data.append({'fid':obj['fid_id'], 'food_name': dicFood[obj['fid_id']]['name'],
						 'nutrient_id':obj['nutrient_id'],'amount':float(obj['amount']),
						 'unit':obj['unit']})
			lsNutrient.append(obj['nutrient_id'])
		lsNutrient = list(set(lsNutrient))
		UsdaNutrientsDic = {obj['id']: obj['name']
							for obj in UsdaNutrient.objects.filter(id__in=lsNutrient).values()}
		for obj in data:
			obj['nutrient_name'] = UsdaNutrientsDic[obj['nutrient_id']]
		return data

	def runSafe(self):
		self.safe = True
		dicFood = get_dic_food(self)
		data = self.getData(dicFood)
		return {'data': data, 'status': 1, 'Columns': ['fid','food_name','nutrient_id','nutrient_name','amount','unit']}

class fid_with_nutrient_out_of_standard_deviation():
	def __init__(self, standard_deviation=4,nutrient_ids=None, all_nutrient = False, root=None, exclude=None):
		self.root = root
		self.exclude = exclude
		self.standard_deviation =standard_deviation
		if all_nutrient:
			self.nutrient_ids = [obj['id'] for obj in UsdaNutrient.objects.all().values('id')]
		elif nutrient_ids is not None and type(nutrient_ids) == list:
			self.nutrient_ids = [int(obj) for obj in  nutrient_ids]
		else:
			self.nutrient_ids = []

	def getData(self, dicFood):
		listFid = dicFood.keys()
		nutrientDict = {}
		for nut in UsdaNutrient.objects.filter(id__in = self.nutrient_ids).values():
			nutrientDict[nut['id']] = {'name':nut['name'],'FoodNutrient':[],'sum':0.0}
		foodNutrientList = FoodNutrient.objects.filter(fid_id__in= listFid,nutrient_id__in = self.nutrient_ids).values()
		dictUnitNutrient = {}
		for obj in foodNutrientList:
			if obj['unit'] not in dictUnitNutrient.keys():
				dictUnitNutrient[obj['unit']] = []
			dictUnitNutrient[obj['unit']].append(obj)
		data = []
		for unit in dictUnitNutrient.keys():
			foodNutrientList = dictUnitNutrient[unit]
			subNutDict = copy.deepcopy(nutrientDict)
			for fooNut in foodNutrientList:
				subNutDict[fooNut['nutrient_id']]['FoodNutrient'].append([float(fooNut['amount']),fooNut['fid_id']])
				subNutDict[fooNut['nutrient_id']]['sum'] += float(fooNut['amount'])
			for nut_id in subNutDict.keys():
				num = len(subNutDict[nut_id]['FoodNutrient'])
				if num >0:
					sum = subNutDict[nut_id]['sum']
					average =  sum/ num
					sum = 0.0
					for amount, fid_id in subNutDict[nut_id]['FoodNutrient']:
						sum += pow((amount - average), 2)
					sum = sum / num
					standard_deviation_nut = math.sqrt(sum)
					for amount, fid_id in subNutDict[nut_id]['FoodNutrient']:
						if abs(amount-average) > standard_deviation_nut*self.standard_deviation:
							data.append({'fid_id':fid_id,'food_name':dicFood[fid_id]['name'],
										 'nutrient_id':nut_id,'nutrient_name':subNutDict[nut_id]['name'],
										 'amount':amount,'average':average,'standard_deviation':standard_deviation_nut,
										 'distance_of_standard_deviation':abs(amount-average)/standard_deviation_nut,'unit':unit})
		return data

	def runSafe(self):
		self.safe = True
		dicFood = get_dic_food(self)
		data = self.getData(dicFood)
		return {'data': data, 'status': 1, 'Columns': ['fid_id', 'food_name', 'nutrient_id', 'nutrient_name',
										 'amount', 'average', 'standard_deviation', 'distance_of_standard_deviation','unit']}

class food_units_with_zero_weight():
	def __init__(self, root=None, exclude=None):
		self.root = root
		self.exclude = exclude

	def getData(self, dicFood):
		listFid = dicFood.keys()
		data = []
		for obj in FoodUnits.objects.filter(weight=0,fid_id__in=listFid):
			data.append({'fid':obj.fid_id,'food_name':dicFood[obj.fid_id]['name'],'unit':obj.unit.name})
		return data

	def runSafe(self):
		self.safe = True
		dicFood = get_dic_food(self)
		data = self.getData(dicFood)
		return {'data': data, 'status': 1, 'Columns': ['fid','food_name','unit']}

class find_usda_reference_more_one_food():
	def __init__(self, root=None, exclude=None,alow_parent=False,database=None):
		self.root = root
		self.exclude = exclude
		self.alow_parent = alow_parent
		self.database = database

	def getData(self, dicFood):
		listFid = dicFood.keys()
		if self.database is None:
			qSet = FoodNutritionRefs.objects.filter(fid_id__in=listFid).values('fid','usda_id')
		else:
			qSet = FoodNutritionRefs.objects.filter(fid_id__in=listFid,usda__database__in=self.database).values('fid', 'usda_id')
		data=[]
		usda_fid=defaultdict(dict)
		for obj in qSet:
			usda_fid[obj['usda_id']][obj['fid']]={'usda_id':obj['usda_id'],'fid':obj['fid']}

		if self.alow_parent:
			children_dict = getRelation()
			old = usda_fid.copy()
			usda_fid = defaultdict(dict)
			for usda in old.keys():
				fid_keys = []
				for fid in old[usda]:
					if len(set(children_dict[fid] + [fid])&set(fid_keys)) == 0:
						fid_keys.extend(children_dict[fid] + [fid])
						usda_fid[usda][fid] = old[usda][fid].copy()
		usdaDicData = {obj['usda_id']:obj for obj in UsdaFood.objects.filter(usda_id__in =usda_fid.keys()).values('usda_id','name','database')}
		temp = {obj['usda_food_id']:obj['long_description'] for obj in UsdaFoodDescription.objects.filter(usda_food_id__in =usda_fid.keys()).exclude(long_description="").values('usda_food_id','long_description')}
		for usda_id in temp:
			if usdaDicData[usda_id]['name'] != temp[usda_id] and len(usda_fid[usda_id].keys())>1:
				usdaDicData[usda_id]['name']=temp[usda_id]
		for usda in usda_fid.keys():
			if len(usda_fid[usda].keys())>1:
				data.append({'usda_id':usda,'usda_name':usdaDicData[usda]['name'], 'database':usdaDicData[usda]['database'],'fids':str('#'.join([str(x) for x in usda_fid[usda].keys()]))})
		return data

	def runSafe(self):
		self.safe = True
		dicFood = get_dic_food(self,include_exclude=False)
		data = self.getData(dicFood)
		return {'data': data, 'status': 1, 'Columns': ['usda_id','usda_name','database','fids']}

class present_category_by_nutrition_variability():
	def __init__(self, root=None, exclude=None,only_representative =True,node_type=None,nutrient_ids=None):
		self.root = root
		self.exclude = exclude
		self.only_representative = only_representative
		self.node_type = node_type
		self.nutrient_ids =nutrient_ids

	def getData(self,dicFood):
		listFid =dicFood.keys()
		if self.nutrient_ids is None:
			self.nutrient_dic = {key:value for key, value in UsdaNutrient.objects.all().values_list('id','name')}
			self.nutrient_ids = self.nutrient_dic.keys()
		else:
			self.nutrient_dic = {key: value for key, value in UsdaNutrient.objects.filter(id__in=self.nutrient_ids).values_list('id', 'name')}
			self.nutrient_ids = self.nutrient_dic.keys()

		childrenDict = get_children_dict(only_representive=self.only_representative)
		listToRun = list(set(listFid)&set(childrenDict.keys()))
		if self.node_type is not None:
			subLs = Food.objects.filter(node_type__id__in=self.node_type).values_list('fid',flat=True)
			listToRun = list(set(listToRun) & set(subLs))
		foodNutrientDict = defaultdict(dict)
		qset = FoodNutrient.objects.filter(fid_id__in=listFid)
		if len(self.nutrient_ids) >0:
			qset = qset.filter(nutrient_id__in = self.nutrient_ids)
		qset = qset.values('fid_id','nutrient_id','amount')
		for obj in qset:
			foodNutrientDict[obj['fid_id']][obj['nutrient_id']] = float(obj['amount'])
		data = []
		node_type_dic = {obj.id:obj.name for obj in FoodNodeType.getDic().values()}
		for key_parent in listToRun:
			if key_parent in childrenDict and key_parent != 1:
				for nutrient_id in self.nutrient_ids:
					val_ls=[]
					for key_child in childrenDict[key_parent]:
						if key_child in foodNutrientDict and nutrient_id in foodNutrientDict[key_child]:
							val_ls.append(foodNutrientDict[key_child][nutrient_id])
					num = float(len(val_ls))
					if len(val_ls)>3:
						average = sum(val_ls)/num
						val_pow = [math.pow((val-average),2) for val in val_ls]
						standard_deviation = math.sqrt(sum(val_pow)/num)
						coefficient_of_variation = 100*(standard_deviation/average) if average>0 else 0
						data.append({'fid':key_parent,'name':dicFood[key_parent]['name'],
									 'node_type':node_type_dic[dicFood[key_parent]['node_type_id']],'nutrient':self.nutrient_dic[nutrient_id],
									 'average':average, 'standard_deviation':standard_deviation,
									 'coefficient_of_variation':coefficient_of_variation,'number_of_children':len(val_ls)})
		df = pd.DataFrame(data)
		df = df.sort_values(['node_type', 'nutrient','coefficient_of_variation'])
		#df = df[['fid','name','node_type','nutrient','coefficient_of_variation','standard_deviation','average']]
		#data = df.to_dict(orient='records')
		return df

	def getDescription(self,df,tree=None):
		tree = self.getTreeResult(df) if tree is None else tree
		txt =""
		for nutrient in tree:
			txt += nutrient + ":\n"
			for node in tree[nutrient]:
				txt += "\t"+node+":\n"
				for key in sorted(tree[nutrient][node].keys()):
					sub = tree[nutrient][node][key]
					sub = "{:.4e}".format(sub) if sub < 1 else "{:.4f}".format(sub)
					txt += "\t\t" + key + ":\t" + sub + "\n"
		return txt

	def getTreeResult(self,df):
		def percentile(n):
			def percentile_(x):
				return np.percentile(x, n)

			percentile_.__name__ = 'percentile_%s' % n
			return percentile_
		tree = {}
		for nutrient in self.nutrient_dic.values():
			subDf = df[df['nutrient']==nutrient]
			subDf = subDf.groupby('node_type').agg(['min', 'max', 'median', percentile(10), percentile(90)])[
				['coefficient_of_variation']]
			nodes={}
			for node_type, serice in subDf.iterrows():
				calculations={}
				for key, value in pd.DataFrame(serice).iterrows():
					val = value[node_type]
					k = key[1]
					calculations[k] = val
				nodes[node_type] = calculations
			tree[nutrient] = nodes
		return tree

	def set_candidates(self,df,tree):
		subtxt = ""
		df['candidate_to_be_move']=""
		for nutrient in tree:
			if 'broad' in tree[nutrient] and 'common' in tree[nutrient]:
				borad_percentile_10 = tree[nutrient]['broad']['percentile_10']
				common_percentile_90 = tree[nutrient]['common']['percentile_90']
				to_common = df[(df.nutrient == nutrient) & (df.coefficient_of_variation <= borad_percentile_10) &
							   (df.coefficient_of_variation <= common_percentile_90) & (df.node_type ==  "broad")].index
				to_broad  = df[(df.nutrient == nutrient) & (df.coefficient_of_variation >= borad_percentile_10) &
							   (df.coefficient_of_variation >= common_percentile_90) & (df.node_type == "common")].index
				df.loc[to_common, 'candidate_to_be_move'] = "to common"
				df.loc[to_broad, 'candidate_to_be_move'] = "to broad"
			else:
				subtxt+="\nCouldn't load to_common and to_broad because there is not broad or common in {}".format(nutrient)
		return df,subtxt

	def runSafe(self):
		self.safe = True
		dicFood = get_dic_food(self,include_exclude=False,attr=['node_type_id','name'])
		df = self.getData(dicFood)
		tree = self.getTreeResult(df)
		txt = self.getDescription(df,tree)
		df,subtxt = self.set_candidates(df,tree)
		txt+=subtxt
		df['coefficient_of_variation'] = df['coefficient_of_variation'].map('{:,.2f}%'.format)
		data = df.to_dict(orient='records')
		return {'data': data, 'status': 2,'description':txt, 'Columns': ['fid','name','number_of_children','node_type','nutrient','coefficient_of_variation','standard_deviation','average','candidate_to_be_move']}

class fid_component_loop():
	def __init__(self, root=None, exclude=None, only_representative=True, node_type=None, nutrient_ids=None):
		self.root = root
		self.exclude = exclude

	def checkBad(self,badList,parents=[],fid=1):
		if fid in self.listFid and fid in self.FoodComponentsDict:
			comp = set(self.FoodComponentsDict[fid])
			ls = list(set(parents + [fid]) & comp)
			for com in ls:
				badList.append({'fid':fid,'comp':com})
		if fid in self.children_dict:
			for child in self.children_dict[fid]:
				self.checkBad(badList,parents=parents+[fid],fid=child)


	def getData(self,dicFood):
		self.listFid = dicFood.keys()
		self.children_dict = get_children_dict()
		self.FoodComponentsDict = defaultdict(list)
		for obj in FoodComponents.objects.filter(fid_id__in = self.listFid):
			self.FoodComponentsDict[obj.fid_id].append(obj.component_id)
		badList = []
		self.checkBad(badList)
		data = [{'fid':obj['fid'],'component_fid':obj['comp'],'food_name':dicFood[obj['fid']]['name'],'component_name':dicFood[obj['comp']]['name']} for obj in badList]
		return data



	def runSafe(self):
		self.safe = True
		dicFood = get_dic_food(self,include_exclude=False)
		data = self.getData(dicFood)
		return {'data': data, 'status': 1, 'Columns': ['fid','food_name','component_name','component_fid']}

class find_parent_with_no_rep():
	def __init__(self, root=None, exclude=None,only_with_children=True):
		self.root = root
		self.exclude = exclude
		self.only_with_children = only_with_children

	def getData(self,dicFood):
		self.listFid = dicFood.keys()
		with_out_rep = get_children_dict(only_representive=True)
		with_all = get_children_dict(only_representive=False) if self.only_with_children else self.listFid
		fid_with_missing_repChild=[]
		for fid in self.listFid:
			if fid in with_all and fid not in with_out_rep:
				fid_with_missing_repChild.append(fid)
		data = [{'fid':fid,'food_name':dicFood[fid]['name']} for fid in fid_with_missing_repChild]
		return data

	def runSafe(self):
		self.safe = True
		dicFood = get_dic_food(self,include_exclude=False)
		data = self.getData(dicFood)
		return {'data': data, 'status': 1, 'Columns': ['fid','food_name']}

class output_Atrribute_from_FNNDS():
	def __init__(self,directory_to_tsv=os.path.join(os.environ['ICX_ROOT'],'tools/image/food/FoodDB/data/FNDDS/CleanData.tsv')):
		self.directory_to_tsv=directory_to_tsv

	def __get_attribute_from_row(self,row):
		first = True
		for potential_atrr in row['Main food description'].split(',')[1:]:
			name = potential_atrr.lower()
			if name != "":
				name = name[1:] if name[0] == "" else name
				if first:
					self.potential_atributes.add((name,'second'))
					first = False
				else:
					self.potential_atributes.add((name, 'third+'))

	def getData(self):
		df = pd.read_csv(self.directory_to_tsv, sep='\t', encoding='utf-8')
		self.potential_atributes = set()
		df.apply(lambda row: self.__get_attribute_from_row(row),axis=1)
		self.potential_atributes = list(self.potential_atributes)
		q = map(lambda potential_atrr: Q(**{'value__icontains': potential_atrr}), self.potential_atributes)
		q = reduce(lambda x, y: x | y, q)
		self.dic_Attribute_to_id = {obj['value']:obj['id'] for obj in Attribute.objects.filter(q).values('value','id')}
		self.data =[]
		for potential_atrr in self.potential_atributes:
			name = potential_atrr[0]
			id_in_FB = "" if not name in self.dic_Attribute_to_id else name #self.dic_Attribute_to_id[name]
			level = potential_atrr[1]
			self.data.append({'name':name,'attr_in_FB':id_in_FB,'enter_new?':'','leve':level})

		return self.data

	def runSafe(self):
		self.safe = True
		data = self.getData()
		return {'data': data, 'status': 1, 'Columns': ['name','attr_in_FB','enter_new?','leve']}


class temp(object):
	def __init__(self, root=None, exclude=None):
		self.root = root
		self.exclude = exclude
		self.safe = True

def get_dic_food(obj = None,reves_safe=False,include_root = True,include_exclude=True,attr=[]):
	"""
	Input: root name and exclude name
	Output: { fid:name, } with all child of self.root exclude the self.exclude
	defult: root = 1, exclude = [1922,2205,2208]
	"""
	if obj == None:
		obj = temp()
	root = [1]
	exclude = [1922, 2205, 2208, 1816]
	safe = obj.safe if not reves_safe else not obj.safe
	if obj.root:
		root.remove(1)
		if safe:
			for fd in obj.root:
				root.append(int(fd))
		else:
			for fd in obj.root:
				food_root = Food.objects.filter(name=fd)
				if food_root:
					root.append(food_root[0].fid)
				else:
					logging.error('food name in root: %s was not in food tree' % (fd))
					sys.exit(1)
	if obj.exclude:
		exclude.remove(1922)
		exclude.remove(2205)
		exclude.remove(2208)
		exclude.remove(1816)
		if safe:
			for fd in obj.exclude:
				exclude.append(int(fd))
		else:
			for ex in obj.exclude:
				exclude_root = Food.objects.filter(name=ex)
				if exclude_root:
					exclude.append(exclude_root[0].fid)
				else:
					logging.error('food name in exclude: %s was not in food tree.' % (ex))
					sys.exit(1)
	list_root = []
	list_exlude = []
	if include_root:
		list_root.extend(root)
	if not include_exclude:
		list_exlude.extend(exclude)
	hier = getRelation()
	for parent in root:
		list_root.extend(hier[parent])
	for parent in exclude:
		list_exlude.extend(hier[parent])
	list_fid = list(set(list_root).difference(set(list_exlude)))
	attributes = set(attr)
	attributes.add('name')
	dic = {}
	for obj in Food.objects.filter(fid__in=list_fid).values():
		dic[obj['fid']] = { attr:obj[attr]
							for attr in attributes}
	return dic

def fooddb_querise_runFromQueryDict(qDict):
	if "queryName" in qDict:
		if qDict["queryName"] == "Find_outlier_nutrients":
			standard_deviations = None if "standard_deviations" not in qDict else float(qDict["standard_deviations"])
			is_representative = False if "is_representative" not in qDict else True
			nutrients = qDict.getlist('nutrients')
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			runObj = finds_outlier_nutrients(nutrient_names = nutrients, root = root, exclude = exclude,standard_deviations= standard_deviations, is_representative = is_representative)
			return runObj.runSafe()
		elif qDict["queryName"] == "report_inconsistent_default_units":
			maximal_percent = None if "maximal_percent" not in qDict else float(qDict["maximal_percent"])
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			runObj = report_inconsistent_default_units(maximal_percent=maximal_percent, root=root, exclude=exclude)
			return runObj.runSafe()
		elif qDict["queryName"] == "getlistDublicate":
			exclude_lan = None if not 'exclude_lan' in qDict else qDict.getlist('exclude_lan')
			runObj = getlistDublicate(exclude_lan=exclude_lan)
			return runObj.runSafe()
		elif qDict["queryName"] == "report_inconsistent_units_fid_to_parent":
			maximal_percent = None if "maximal_percent" not in qDict else float(qDict["maximal_percent"])
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			runObj = report_inconsistent_units_fid_to_parent(maximal_percent=maximal_percent, root=root, exclude=exclude)
			data = runObj.runSafe()
			return data
		elif qDict["queryName"] == "connect_attr_to_food_by_attr_name":
			attributes = qDict.getlist('attributes')
			only_new = False if 'only_new' not in qDict else True
			runObj = attr_id_AND_fid(False,attributes=attributes,only_new = only_new)
			data = runObj.runSafe()
			return data
		elif qDict["queryName"] == "nutrient_TO_fid":
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			only_new = False if 'only_new' not in qDict else True
			data = []
			for nutr_id_2, min,max ,  nutr_id,attr_id, action in zip(qDict.getlist('nutr_id_2'),
																	 qDict.getlist('min'),
																	 qDict.getlist('max'),
																	 qDict.getlist('nutr_id'),
																	 qDict.getlist('attr_id'),
																	 qDict.getlist('action')):
				max_s = float("inf") if max == "-1" else float(max)
				min_s = float(min)
				nutr_id_2_s =  None if nutr_id_2 == "None" else int(nutr_id_2)
				action_s = None if nutr_id_2 == "None" else action
				if action_s == u'None':
					return {'Error': "second nutrient is selected but there is no action", 'status': -1}
				nutr_id_s = int(nutr_id)
				attr_id_s = int(attr_id)
				data.append({'nutr_id_2':nutr_id_2_s,
							 'min':min_s,
							 'max':max_s,
							 'nutr_id':nutr_id_s,
							 'attr_id':attr_id_s,
							 'action':action_s})
			runObj = nutrient_TO_fid(read_from_csv=data,root =root,exclude = exclude,only_new=only_new)
			res =  runObj.runSafe()
			return res
		elif qDict["queryName"] == "fid_with_child_and_recipe":
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			runObj =fid_with_child_and_recipe(root=root,exclude=exclude)
			res = runObj.runSafe()
			return res
		elif qDict["queryName"] == "fid_NO_with_child_and_recipe":
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			runObj =fid_NO_with_child_and_recipe(root=root,exclude=exclude)
			res = runObj.runSafe()
			return res
		elif qDict["queryName"] == "fid_with_missing_nutrients":
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			all_nutrient = False if 'all_nutrient' not in qDict else True
			nutrient_ids = None if 'nutrients' not in qDict else qDict.getlist('nutrients')
			runObj =fid_with_missing_nutrients(all_nutrient =all_nutrient,nutrient_ids= nutrient_ids,root=root, exclude=exclude)
			res = runObj.runSafe()
			return res
		elif qDict["queryName"] == "fid_with_nutrient_out_of_given_range":
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			max_g = None if "max_g" not in qDict else float(qDict["max_g"])
			max_kcal = None if "max_kcal" not in qDict else float(qDict["max_kcal"])
			min = None if "min" not in qDict else float(qDict["min"])
			runObj = fid_with_nutrient_out_of_given_range(min =min,max_g =max_g,max_kcal=max_kcal,root=root,exclude=exclude)
			res = runObj.runSafe()
			return res
		elif qDict["queryName"] == "food_units_with_zero_weight":
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			runObj = food_units_with_zero_weight(root=root,exclude=exclude)
			res = runObj.runSafe()
			return res
		elif qDict["queryName"] == "fid_with_nutrient_out_of_standard_deviation":
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			all_nutrient = False if 'all_nutrient' not in qDict else True
			nutrient_ids = None if 'nutrients' not in qDict else qDict.getlist('nutrients')
			standard_deviation = None if "standard_deviation" not in qDict else float(qDict["standard_deviation"])
			runObj =fid_with_nutrient_out_of_standard_deviation(standard_deviation=standard_deviation,all_nutrient =all_nutrient,nutrient_ids= nutrient_ids,root=root, exclude=exclude)
			res = runObj.runSafe()
			print('back to user: ',len(res['data']))
			return res
		elif qDict["queryName"] == "find_usda_reference_more_one_food":
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			alow_parent = False if 'alow_parent' not in qDict else True
			database = None if not 'database' in qDict else qDict.getlist('database')
			runObj = find_usda_reference_more_one_food(alow_parent=alow_parent, root=root, exclude=exclude,database=database)
			res = runObj.runSafe()
			return res
		elif qDict["queryName"] == "present_category_by_nutrition_variability":
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			only_representative = False if 'only_representative' not in qDict else True
			node_type = None if 'node_type' not in qDict else qDict.getlist('node_type')
			nutrient_ids = None if 'nutrients' not in qDict else qDict.getlist('nutrients')
			runObj = present_category_by_nutrition_variability(root=root,exclude=exclude,only_representative=only_representative,node_type=node_type,nutrient_ids=nutrient_ids)
			res = runObj.runSafe()
			return res
		elif qDict["queryName"] == "fid_component_loop":
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			runObj = fid_component_loop(root=root, exclude=exclude)
			res = runObj.runSafe()
			return res
		elif qDict["queryName"] == "find_parent_with_no_rep":
			root = None if 'root' not in qDict else qDict.getlist('root')
			exclude = None if 'exclude' not in qDict else qDict.getlist('exclude')
			only_with_children = False if 'only_with_children' not in qDict else True
			runObj = find_parent_with_no_rep(root=root, exclude=exclude,only_with_children=only_with_children)
			res = runObj.runSafe()
			return res
		elif qDict["queryName"] == "output_Atrribute_from_FNNDS":
			runObj = output_Atrribute_from_FNNDS()
			res = runObj.runSafe()
			return res
		else:
			return {'Error':"can't find query name",'status':-1}
	else:
		return {'Error':"no query_name",'status':-1}