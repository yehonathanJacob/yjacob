from __future__ import unicode_literals
from __future__ import print_function

import sys
import random, os, glob
import json
import logging
from collections import OrderedDict, defaultdict
from decorators import *

import numpy as np #std is standard deviation of population (not sample)
import pandas as pd

from django.db import models
from django.conf import settings
from django.db.models import Q, Prefetch
from django.utils.functional import cached_property
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db import connection
from contextlib import closing

from .question import Question
#from .algorithms import TextParsingAlgorithm
from .db_manager import DB
import FoodDB

import itertools

from json import loads
from decimal import Decimal
from functools import reduce


logger = logging.getLogger('debug')

db = DB()
IMAGES = settings.IMAGES_ROOT

ddbb = FoodDB.DB()

def food_lookup(name):
    food = ddbb.food_lookup(name)
    if food:
        return food["fid"]
    else:
        return None


class CircuitClosedException(Exception):
    pass


def normalize_unit(amount, unit):
    if unit != 'g':
        return amount, unit
    if 0 < amount < 0.1:
        amount *= 1000
        unit = 'mg'
        if amount < 0.1:
            amount *= 1000
            unit = '\xb5g'
    return amount, unit


def get_unit_from_average(avg):
    if 0 < avg < 0.1:
        avg *= 1000
        unit = 'mg'
        if avg < 0.1:
            avg *= 1000
            unit = '\xb5g'
    else:
        unit = 'g'
    return unit


def convert_to_unit(amount, unit):
    if unit == 'mg':
        amount *= 1000
    elif unit == '\xb5g':
        amount *= 1000000
    else:
        pass
    return amount


def convert_to_same_unit(amount, unit):
    pass


def normalize_grams_to_unit(amount, unit):
    if unit == 'mg':
        return amount * 1e3
    elif unit == '\xb5g':
        return amount * 1e6
    return amount

def get_children_dict(only_representive=False):
    children_dict= defaultdict(list)
    if only_representive:
        qset = FoodHier.objects.filter(is_primary=True,is_representative=True).values('fid','parent')
    else:
        qset = FoodHier.objects.filter(is_primary=True).values('fid', 'parent')
    for obj in qset:
        children_dict[obj['parent']].append(obj['fid'])
    return children_dict

def get_qattributes_dict():
    children_dict = get_children_dict()
    qattributes_dict = defaultdict(dict)
    for obj in FoodQAttributes.objects.all().values('fid','attribute','quantity'):
        qattributes_dict[obj['fid']][obj['attribute']] = float(obj['quantity'])
    for key in qattributes_dict:
        qattributes_dict[key]['is_inherit'] = False
    return get_reqursy_qattributes_dict(children_dict,qattributes_dict,fid=1)

def get_reqursy_qattributes_dict(children_dict,qattributes_dict,fid=1):
    for child in children_dict[fid]:
        if child not in qattributes_dict:
            qattributes_dict[child] = qattributes_dict[fid].copy()
            qattributes_dict[child]['is_inherit'] = True
        get_reqursy_qattributes_dict(children_dict,qattributes_dict,fid=child)
    return qattributes_dict

def to_grams(amount, unit):
    if unit in ['g', 'kcal']:
        return amount
    if unit == 'mg':
        return amount / 1e3
    elif unit == 'mcg':
        return amount / 1e6
    elif unit == 'iu':
        return (amount * 0.025) / 1e6
    else:
        print("error in unit ", unit)
        return None

def getRelation(only_representive=False):
    '''
    :return: hier: dict, that for each parent in FoodHier, dict[parent] contain all descendants fid
    len(hier[1]) ==  len(Food)
    '''
    hier = get_children_dict(only_representive=only_representive)
    fid = 1
    get_reqursy_hier(fid, hier)
    return hier

def get_reqursy_hier(fid,hier):
    if fid in hier:
        for child in hier[fid]:
            get_reqursy_hier(child, hier)
        for child in hier[fid]:
            if child in hier:
                hier[fid].extend(hier[child])
        hier[fid] = list(set(hier[fid]))

class Lang(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    lang = models.CharField(unique=True, max_length=64)

    class Meta:
        db_table = 'lang'

    def __str__(self):
        return self.lang


class AttributeType(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Attribute(models.Model):
    type = models.ForeignKey(AttributeType, on_delete=models.CASCADE)
    value = models.CharField(max_length=64)
    comment = models.TextField(blank=True)
    url = models.URLField(blank=True)

    class Meta:
        ordering = 'type__name', 'value'

    def __unicode__(self):
        return self.value

class AttributeName(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    lang_code = models.ForeignKey(Lang, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    is_primary = models.BooleanField(default=False)
    def __unicode__(self):
        return u'attribute {}:{}'.format(self.attribute,self.name)


class Attributes(models.Model):
    name = models.CharField(primary_key=True, max_length=64)
    comment = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        db_table = 'attributes'
    def __unicode__(self):
        return u'{}'.format(self.name)


class DatasetCategories(models.Model):
    dcid = models.AutoField(primary_key=True)
    dataset = models.ForeignKey('Datasets', models.DO_NOTHING, db_column='dataset')
    category_id = models.CharField(max_length=256)
    fid = models.ForeignKey('Food', models.DO_NOTHING, db_column='fid', blank=True, null=True)
    cnt = models.IntegerField(blank=True, null=True)

    def sample_images(self, n=10):
        try:
            dir_name = IMAGES + self.dataset.name + "/" + self.category_id
            images = glob.glob(dir_name + "/*.jpg")
            images = [x.split("/")[-1] for x in images]
            return random.sample(images, min(n, len(images)))
        except:
            return []

    def sample_image_urls(self, n=10):
        return [self.dataset.name + "/" + self.category_id + "/" + x for x in  self.sample_images(n)]

    def sample_image_path(self):
        try:
            dir_name = IMAGES + self.dataset.name + "/" + self.category_id
            images = glob.glob(dir_name + "/*.jpg")
            #images = os.listdir(dir_name)
            if len(images) < 1:
                return None
            return random.choice(images)
        except:
            return None

    def images(self):
        try:
            dir_name = IMAGES + self.dataset.name + "/" + self.category_id
            images = glob.glob(dir_name + "/*.jpg")
            #images = os.listdir(dir_name)
            return sorted([self.dataset.name + "/" + self.category_id + "/" + x.split("/")[-1] for x in images])
        except:
            return []

    def image_count(self):
        try:
            dir_name = IMAGES + self.dataset.name + "/" + self.category_id
            images = glob.glob(dir_name + "/*.jpg")
            #images = os.listdir(dir_name)
            return len(images)
        except:
            return 0

    def update_fid(self, fid, user=None):
        if fid is not None:
            self.fid = Food.objects.get(pk=fid)
        else:
            self.fid = None
        #UserActivityLog.add_log(user, UserActivityLog.UPDATE, self,fid = self.fid)
        self.save(force_update=True)

    class Meta:
        managed = False
        db_table = 'dataset_categories'
        unique_together = (('dataset', 'category_id'),)


class Datasets(models.Model):
    name = models.CharField(primary_key=True, max_length=64)
    comment = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=1024, blank=True, null=True)
    for_classification = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'datasets'


def foods_with_components():
    foods = {f.fid: f for f in Food.objects.all()}
    components = FoodComponents.objects.all()
    for c in components:
        f = foods[c.fid_id]
        if hasattr(f, '_components'):
            f._components.append([foods[c.component_id], c.amount])
        else:
            f._components = [[foods[c.component_id], c.amount]]
    return foods.values()


class Foods():
    def __init__(self, fid=None, trim=True):
        self.parent_ids = db.select_as_dict('select fid,parent from food_hier where is_primary')
        self.obj = Food.objects.all()
        self.by_id = {}
        for o in self.obj:
            self.by_id[o.fid] = o
            if o.fid in self.parent_ids:
                o.parent_id = self.parent_ids[o.fid]
            else:
                o.parent_id = None

        for o in self.obj:
            if o.parent_id:
                o._parent = self.by_id[o.parent_id]
            else:
                o._parent = None


        for o in self.obj:
            o.pstring()

        self.obj_sorted = sorted(self.obj, key=lambda x: x._pstring)
        #for o in self.obj_sorted:
        #    print o._pstring , "\t" , o.name, "\t", o.fid

        level = 1
        if fid is not None:
            f     = Food.objects.get(pk=fid)
            level = f.level()
            start = self.obj_sorted.index(f)
            # print f, self.obj_sorted
            stop = start + 1
            while stop < len(self.obj_sorted) and self.obj_sorted[stop].level() > level:
                stop += 1
            #print stop
            self.obj_sorted = self.obj_sorted[start:stop]

        if trim:
            tmp = [(i, f) for i, f in enumerate(self.obj_sorted) if f.level() <= level + 1]
            while True:
                level += 1
                obj = tmp
                tmp = [(i, f) for i, f in enumerate(self.obj_sorted) if f.level() <= level + 1]
                if len(tmp) == len(obj) or len(tmp) > 100:
                    break

            def is_trimmed(i_obj, i_sorted):
                if i_sorted >= len(self.obj_sorted) - 1:
                    return False
                if i_obj >= len(obj) - 1:
                    return True
                return self.obj_sorted[i_sorted + 1] != obj[i_obj + 1][1]

            self.trimmed = list(map(lambda x: is_trimmed(x[0], x[1][0]), enumerate(obj)))
            self.obj_sorted = list(map(lambda x: x[1], obj))
        else:
            self.trimmed = (False, ) * len(self.obj_sorted)

        self.foods = list(zip(self.obj_sorted, self.trimmed))

        self.init_names()

    def init_names(self):
        all_names = FoodNames.objects.filter(fid__in=self.obj_sorted)
        all_foods = {f.fid: f for f in self.obj_sorted}
        for fid, f in all_foods.items():
            f._names = defaultdict(list)
        for name in all_names:
            if name.fid_id in all_foods:
                f = all_foods[name.fid_id]
                if name.is_primary:
                    f._names[name.lang_code_id].insert(0, name.name)
                else:
                    f._names[name.lang_code_id].append(name.name)


def set_nutrients_list():
    nutrients = UsdaNutrient.objects.all()
    with open(os.path.dirname(__file__) + '/../../data/nutritions_order.json', mode='r') as config:
        order_list = loads(config.read().lower())
    list_nutrients = [n.name for n in nutrients]
    return sorted(list_nutrients, key=lambda x: order_list.index(x) if x.lower() in order_list else 200)

def set_nutrients_list_all():
    nutrients = UsdaNutrient.objects.all()
    with open(os.path.dirname(__file__) + '/../../data/nutritions_order.json', mode='r') as config:
        order_list = loads(config.read().lower())
    list_nutrients = [n for n in nutrients]
    return sorted(list_nutrients, key=lambda x: order_list.index(x.name) if x.name.lower() in order_list else 200)

class FoodNodeType(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'food_node_type'

    def __unicode__(self):
        return u'{}'.format(self.name)

    @classmethod
    def getDic(cls):
        return None if cls.objects.count() == 0 else {obj.name:obj for obj in cls.objects.all()}


class Food(models.Model):
    fid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=256)
    for_classification = models.BooleanField()
    bad = models.NullBooleanField()
    class_num = models.IntegerField(unique=True, blank=True, null=True)
    is_category = models.NullBooleanField(default=False)
    energy = models.IntegerField(null=True)
    is_countable = models.NullBooleanField(null=True)
    liquid_loss = models.FloatField(blank=True, null=True)
    node_type = models.ForeignKey('FoodNodeType', models.DO_NOTHING, db_column='node_type', blank=True, null=True,default=FoodNodeType.objects.filter(name="common").first())
    # @classmethod
    # def all(cls):
    #     #return cls.objects.all()
    #     if not hasattr(cls, '_all'):
    #         cls._all = cls.objects.all()
    #     return cls._all

    @classmethod
    def get(cls,fid=None,name=None):
        food = cls.objects.filter(fid=fid) if fid != None else cls.objects.filter(name=name)
        if food.exists():
            return food.first()
        food = DeletedFood.objects.filter(fid=fid) if fid != None else DeletedFood.objects.filter(name=name)
        if food.exists():
            sub_fid = food.first().substitute
            return cls.objects.get(fid=sub_fid)
        raise Food.DoesNotExist

    def parent(self):
        if not hasattr(self, "_parent"):
            self._parent = self.get_parent()
        return self._parent

    def level(self):
        if not hasattr(self, "_level"):
            self._level = self.get_level()
        return self._level

    def pstring(self):
        if not hasattr(self, "_pstring"):
            self._pstring = self.get_pstring()
        return self._pstring

    def get_level(self):
        p = self.parent()
        if p:
            return p.level() + 1
        else:
            return 1

    def get_pstring(self):
        p = self.parent()

        if p:
            # print "  ... ",p.fid
            return p.pstring() + "." + self.name #removed unicode function due to Py3
        else:
            return self.name #removed unicode function due to Py3

    def get_parent(self):
        o = FoodHier.objects.filter(fid=self.fid, is_primary=True).first()
        if o is None:
            return None
        return o.parent

    def is_representative(self):
        o = FoodHier.objects.filter(fid=self.fid, is_primary=True).first()
        if o is None:
            return False
        return o.is_representative


    def ancestors(self):
        """
        Get all the ancestors of food by order, including the current item.
        :return: RawQuerySet that contains the food's ancestors.
        """
        return Food.objects.raw('''WITH RECURSIVE ancestors(fid) AS (
                                            SELECT %s
                                        UNION ALL
                                            SELECT fh.parent
                                            FROM food_hier AS fh, ancestors AS a
                                            WHERE fh.fid = a.fid and is_primary
                                        )
                                        SELECT fid FROM ancestors
                                    ''', [self.fid])

    def get_children(self):
        return [heir.fid for heir in FoodHier.objects.filter(parent=self.fid)]

    def is_descendant_of(self, other):
        if self == other:
            return True

        tmp = self.parent()
        while tmp is not None:
            if tmp.fid == other.fid:
                return True
            tmp = tmp.parent()
        return False

    def can_be_child_of(self, other):
        if other.is_descendant_of(self):
            return False
        if not self.get_components and not self.nutrition_refs and other in self.nested_recipes():
            return False
        return True

    def update_parent(self, new_parent, user=None, is_representative=False):
        logger.debug("%s %s", new_parent, is_representative)

        recipes = self.nested_recipes()
        del self._nested_recipes_started, self._recipes

        o = FoodHier.objects.filter(fid=self.fid, is_primary=True).first()
        #print ">>>",o.id
        if new_parent is None:
            if o:
                UserActivityLog.add_log(user, UserActivityLog.DELETE, o,fid =o.fid_id)
                o.delete()
            return None
        parent = Food.objects.get(pk=new_parent)
        #print ">>>",parent

        action = UserActivityLog.UPDATE
        if not self.can_be_child_of(parent):
            raise CircuitClosedException('{} is a descendant of {}'.format(parent.name, self.name))
        if o is None:
            action = UserActivityLog.CREATE
            o = FoodHier(fid=self, is_primary=True, parent=parent, is_representative = is_representative)
            #o.is_primary = True
        else:
            o.parent = parent
            o.is_representative = is_representative
        UserActivityLog.add_log(user, action, o,fid =o.fid_id)
        o.save()
        #print "!!!!!!!!!", o.is_representative
        recipes |= self.nested_recipes()
        for f in recipes:
            f.update_energy()
        return o.parent

    def __unicode__(self):
        return u'{}: {}'.format(self.fid, self.name)

    def names(self, lang):
        return self._names[lang]
        #fid = self.fid
        #return db.select_as_column("select name from food_names where fid=%s and lang_code=%s",[fid,lang])

    def en(self):
        return self.names("en")

    def he(self):
        return self.names("he")

    def cn(self):
        return self.names("cn")

    @cached_property
    def total_amount(self):
        components = self.get_components
        total = 0
        for component in components:
            total += component[1]
        return total

    def root_path(self):
        p = self.parent()
        if p is None:
            return [self]
        else:
            return p.root_path() + [self]

    def datasets(self,dataset=None):
        if dataset:
            return DatasetCategories.objects.filter(fid=self.fid, dataset=dataset)
        else:
            return DatasetCategories.objects.filter(fid=self.fid)

    def comments(self):
        return FoodComments.objects.filter(fid=self.fid)

    def attributes(self):
        return self.foodattributes_set.all()

    def has_attribute(self, attr):
        return bool(self.attributes().filter(attribute=attr))

    def refs(self):
        return FoodReferences.objects.filter(fid=self.fid)

    @cached_property
    def nutrition_refs(self):
        queryset_energy = UsdaFoodNutrient.objects.filter(nutrient__name='energy').distinct('usda')
        queryset_carbs = UsdaFoodNutrient.objects.filter(nutrient__name='total_carbohydrate').distinct('usda')
        queryset_protein = UsdaFoodNutrient.objects.filter(nutrient__name='protein').distinct('usda')
        queryset_fat = UsdaFoodNutrient.objects.filter(nutrient__name='total_fat').distinct('usda')
        prefetch_energy = Prefetch('usda__usdafoodnutrient_set', queryset=queryset_energy, to_attr='energy')
        prefetch_carbs = Prefetch('usda__usdafoodnutrient_set', queryset=queryset_carbs, to_attr='carbs')
        prefetch_protein = Prefetch('usda__usdafoodnutrient_set', queryset=queryset_protein, to_attr='protein')
        prefetch_fat = Prefetch('usda__usdafoodnutrient_set', queryset=queryset_fat, to_attr='fat')
        manager = self.foodnutritionrefs_set.select_related('usda')
        for p in [prefetch_energy, prefetch_carbs, prefetch_protein, prefetch_fat]:
            manager = manager.prefetch_related(p)
        return manager.all()

    @cached_property
    def nutrition_refs_all(self):
        """
        :return: list of sets: [
            (usda_id, long_description, group_description, database,
                ( (nutrition name, nutrition amount), .. )
            ), ... ]
        """
        manager = self.foodnutritionrefs_set.select_related('usda')
        usdaSet = []
        usdalist = []
        for obj in manager:
            usdaSet.append([obj.usda_id,obj.usda.long_description,obj.usda.group_description,obj.usda.database])
            usdalist.append(obj.usda_id)
        UFN = UsdaFoodNutrient.objects.filter(usda_id__in= usdalist).values()
        dic1 = {} #{ usda_id: { nutrient_id: amount, }, }
        for obj in UFN:
            if obj['usda_id'] not in dic1.keys():
                dic1[obj['usda_id']] = {}
            dic1[obj['usda_id']][obj['nutrient_id']]=obj['amount']
        s1=[]
        s2=[]
        for obj in usdaSet:
            if obj[0] in dic1.keys():
               s1.append(obj)
               s2.append(obj[0])
        usdaSet = s1
        usdalist = s2
        dic2 = [] #[ (usda_id, long_description, group_description, database,
        # ( (nutrition name, nutrition old amount), .. )), ]
        nutrients = {} #{ nutrition name: [nutrition old amount, nutrition old amount, ], }
        un = set_nutrients_list_all()
        for name in un:
            nutrients[name.name] = []
        for obj in usdaSet:
            subDic = []
            for name in un:
                if name.id in dic1[obj[0]].keys():
                    subDic.append([name.name,dic1[obj[0]][name.id]])
                    nutrients[name.name].append(float(dic1[obj[0]][name.id]))
                else:
                    subDic.append((name.name,None))
            dic2.append([obj[0],obj[1],obj[2],obj[3],subDic])
        self.nutrients_list_ref = [] # [ (nutrition name, unit), ]
        for name in un:
            avg = np.average(nutrients[name.name])
            the_unit = get_unit_from_average(avg)
            if name.name == u'energy' and the_unit == 'g':
                the_unit = 'kcal'
            self.nutrients_list_ref.append([{'name':name.name,'id':name.id}, the_unit])
            nutrients[name.name].append(the_unit)
        dic3 = []  # [ (usda_id, long_description, group_description, database,
        # ( (nutrition name, nutrition new amount), .. )), ]
        for obj in dic2:
            new_subDic = []
            for obj2 in obj[4]:
                if obj2[1] is not None:
                    new_subDic.append([obj2[0],convert_to_unit(obj2[1],nutrients[obj2[0]][-1])])
                else:
                    new_subDic.append([obj2[0], None])
            dic3.append([obj[0],obj[1],obj[2], obj[3],new_subDic])
        return dic3

    @property
    def get_components(self):
        if not hasattr(self, '_components'):
            self._components = [[c.component, c.amount]
                                for c in FoodComponents.objects.filter(fid=self.fid).select_related('component')]
        return self._components

    @cached_property
    def recipes(self):
        return FoodComponents.objects.filter(component=self.fid)

    def _recipes_for_circle(self):
        recipes = list(map(lambda x: x.fid, self.recipes))
        recipes.extend([f.fid for f in FoodHier.objects.filter(parent=self.fid)
                        if not f.fid.get_components and not f.fid.nutrition_refs])
        recipes_set = set(recipes)
        for recipe in recipes:
            if recipe == self:
                raise CircuitClosedException()
            recipes_set |= recipe.nested_recipes()
        if self in recipes_set:
            raise CircuitClosedException("{} is a component of itself".format(self))
        return recipes_set | {self}

    def nested_recipes(self):
        if not hasattr(self, '_recipes'):
            if hasattr(self, '_nested_recipes_started'):
                raise CircuitClosedException()
            self._nested_recipes_started = True
            self._recipes = self._recipes_for_circle()
        return self._recipes

    def grams_per_unit(self):
        return FoodUnits.objects.filter(fid=self.fid)

    def formatted(self):
        return self.name.replace('_', ' ')

    def get_descendants_by_attributes(self, attribute_requirements=None):
        # 1. get descendants under food
        food_descendants = [self.fid] + get_all_descendants(self.fid)  # including self
        # 2. get food attributes for all descendants:
        food_attributes = FoodAttributes.objects.filter(fid__in=food_descendants).select_related('fid')
        # 3. filter to foods which contain required attributes:
        selected_fid, exclusion_happened = filter_food_by_attributes(food_attributes, set(attribute_requirements))
        return selected_fid, exclusion_happened

    def nutrition_facts_from_refs(self, attribute_requirements=None):
        exclusion_happened = False
        if not attribute_requirements:  # no attributes, use only self
            selected_fid = [self.fid]
        else:  # try to filter a subset of descendants according to attributes
            selected_fid, exclusion_happened = get_descendants_by_attributes_and_food(self.fid,attribute_requirements=attribute_requirements,get_exclusion=True)
        # no attributes required, no subset found, or food already contains attributes, and nothing was found to exclude
        if not exclusion_happened or not selected_fid:
            # use nutrition directly from DB
            food_nutrients = FoodNutrient.objects.filter(fid=self.fid).select_related()
            ref_data = {f.nutrient.name: [float(f.amount), f.unit, float(f.sd_amount),f.inherited if f.sd_amount is not None else 0]
                        for f in food_nutrients}
        else:  # use only filtered descendants to recalculate nutrition facts:
            # 4. get nutrition values of selected descendants
            if self.fid in selected_fid:
                selected_fid.remove(self.fid)
            selected_food_nutrients = FoodNutrient.objects.filter(fid__in=selected_fid).select_related()
            nutrient_dict = defaultdict(dict)
            for f in selected_food_nutrients:
                nutrient_dict[f.fid.fid][f.nutrient.name] = {'amount': float(f.amount), 'unit': f.unit,
                                                             'sd_amount': float(f.sd_amount)
                                                             if f.sd_amount is not None else 0}
            # 5. get children parent hierarchy
            food_descendants = [self.fid] + get_all_descendants(self.fid)  # including self
            hier = FoodHier.objects.filter(fid__in=food_descendants).values('parent', 'fid')
            children_dict = defaultdict(list)
            for h in hier:
                children_dict[h['parent']].append(h['fid'])
            # 6. calculate nutrition values based only on descendants which appear in nutrient dict.
            # For foods that do not appear in nutrient dict, use only children, and ignore references that are directly mapped to food,
            # because they are not annotated with attributes
            # For saving time: if none of the children were excluded, skip recalculation of selected_fid
            override_mode = exclusion_happened  # True only if exclusion happened
            food_nutrients = update_food_nutrients_flow(nutrient_dict, children_dict, recipe_dict={},
                                                        recipe_mode=False, override_mode=override_mode,
                                                        food=self.fid)
            ref_data = {f: [food_nutrients[f]['amount'], food_nutrients[f]['unit'], food_nutrients[f]['sd_amount'], food_nutrients[f]['inherited']] for
                        f in food_nutrients}

        # validate required nutrients:
        required_nutrients = ['energy', 'total_carbohydrate', 'protein', 'total_fat']
        if not all(n in ref_data for n in required_nutrients):
            ref_data = {}
        return ref_data

    def nutrition_facts(self, attribute_requirements=None):
        return self.nutrition_facts_from_refs(attribute_requirements=attribute_requirements)

    def show_facts(self, attribute_requirements=None):
        nutrients = {}
        list_nutrients = []
        facts = self.nutrition_facts(attribute_requirements=attribute_requirements)
        order_list = set_nutrients_list()
        for k, v in facts.items():
            new_val = v[0]
            unit = v[1]
            std = v[2]
            inherited = v[3]
            new_val, new_unit = normalize_unit(new_val, unit)
            std, std_unit = normalize_unit(std, unit)
            nutrients[k] = [new_val, new_unit, std, std_unit]
            list_nutrients.append(
                [
                    k,
                    [new_val, new_unit, std, std_unit, inherited],
                    order_list.index(k) + 1
                ]
            )
        return list_nutrients

    def create_child_nutrients(self):
        hier = FoodHier.objects.filter(parent=self.fid)
        order_list = set_nutrients_list()

        self.children_dict = {}
        for h in hier:
            self.children_dict[h.fid.fid] = h.fid.name

        nutrients = {}
        by_nutrients = {i: {child: None for child in self.children_dict.values()} for i in order_list}

        self.nutrients_units = {}

        for child_id, child_name in self.children_dict.items():
            nutrients[child_name] = {i: "No Value" for i in order_list}
            child_food_nutrients = FoodNutrient.objects.filter(fid__in=[child_id]).select_related()

            for f in child_food_nutrients:
                # nutrients[child_name][f.nutrient.name] = float(f.amount)
                by_nutrients[f.nutrient.name][child_name] = float(f.amount)

        for nutrition, values_list in by_nutrients.items():
            avg = np.average([x for x in values_list.values() if x is not None])
            if nutrition == "energy":
                the_unit = "kcal"
            else:
                the_unit = get_unit_from_average(avg)
            self.nutrients_units[nutrition] = the_unit
            for child in self.children_dict.values():
                if by_nutrients[nutrition][child] is not None:
                    new_val = convert_to_unit(by_nutrients[nutrition][child], the_unit)
                    nutrients[child][nutrition] = new_val

        sorted_nutrient = {}
        for child, nutri_info in nutrients.items():
            sorted_nutrient[child] = sorted(nutri_info.items(), key=lambda x: order_list.index(x[0]))
        return sorted_nutrient


    def can_be_deleted(self):
        return FoodHier.objects.filter(parent=self).count() + FoodComponents.objects.filter(component=self).count() == 0

    def update_energy(self):
        if 'energy' in self.nutrition_facts():
            self.energy = self.nutrition_facts()['energy'][0]
        else:
            self.energy = None
        self.save()

    def update_energy_for_nested(self):
        for f in self.nested_recipes():
            f.update_energy()

    def get_questions(self):
        questions = list(self.foodbooleanquestion_set.all())
        questions.extend(list(self.foodamountquestion_set.all()))
        questions.extend(list(self.foodmultiplechoicequestion_set.all()))
        return [Question(q) for q in questions]

    def get_name_by_lang(self, lang_code='en'):
        result = \
                 db.select_as_value("select name from food_names where lang_code = %s and fid = %s order by is_primary desc, id",[lang_code,self.fid]) or \
                 db.select_as_value("select name from food_names where lang_code = %s and fid = %s order by is_primary desc, id",["en",self.fid]) or \
                 db.select_as_value("select name from food where  fid = %s",[self.fid])
        return result


    def get_first_from_hierarchy(self, class_, **kwargs):
        """
        Helper method to find most relevant model instance that describes food from the hierarchy tree.

        :param class_: The class that stores the attribute
        :param kwargs: filters
        :return: The model instance for the first ancestor (including self) that has a relevant instance .
        """
        ancestors = self.ancestors()
        ancestors_attributes = class_.objects.filter(fid__in=ancestors, **kwargs)
        ancestors_order = {a.fid: i for i, a in enumerate(ancestors)}
        if len(ancestors_attributes) == 0:
            return None
        first = min(ancestors_attributes, key=lambda item: ancestors_order[item.fid.fid])
        return first

    def weight_by_unit(self, unit):
        """
        Get the food weight for given unit.

        If the food has FoodUnit return it, otherwise look for parents FoodUnit.
        If none of the ancestors has the FoodUnit raises ValueError.
        :param unit: The Unit.
        :return: Weight in grams.
        """
        return self.get_first_from_hierarchy(FoodUnits, unit=unit).weight

    def get_default_unit(self):
        """
        Get the default unit for food.

        Uses the hierarchy to determine default unit.
        :return: Unit
        """
        return self.get_first_from_hierarchy(FoodDefaultUnit)


    def add_secondary_ancestor(self,parent):
        sql = "insert into food_hier(fid,parent,is_primary) values (%s,%s,false)"
        db.execute(sql,[self.fid,parent])

    def secondary_ancestors(self):
        sql  = 'select parent from food_hier where fid=%s and not is_primary'
        ancestor_fids = db.select_as_column(sql,[self.fid])
        return [Food.get(fid) for fid in ancestor_fids]
    def secondary_children(self):
        return list(Food.objects.raw('select fid from food_hier where parent=%s and not is_primary',[self.fid]))

    @classmethod
    def all_is_countable_inhereted(cls):
        sql = ''' WITH countable_inherited AS (
                    select H.fid as fid, is_countable, ROW_NUMBER() OVER(PARTITION BY H.fid ORDER BY H.rank) as inh_rank 
                    from food_predecessor_rank as H join food as F on(F.fid = H.parent) where is_countable is not NULL
                    ) 
                    SELECT fid, is_countable FROM countable_inherited WHERE inh_rank = 1
        '''
        res = db.select_as_dict(sql)
        return res


    class Meta:
        db_table = 'food'
        ordering = ['fid']


class FoodAttributes(models.Model):
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid')
    attr = models.ForeignKey(Attribute, models.CASCADE)

    class Meta:
        db_table = 'food_attributes'
        unique_together = (('fid', 'attr'),)
    def __unicode__(self):
        return u'{}-{}'.format(self.fid,self.attr)


class FoodQAttributes(models.Model):
    # primary_key=False because there is unique_together = (('fid', 'attribute'),)
    # max_digits>=1000
    # max_digits > decimal_places!!
    # quantity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid')
    attribute = models.CharField(max_length=64)
    quantity = models.DecimalField(max_digits=1000, decimal_places=10, blank=True, null=True)

    class Meta:
        db_table = 'food_qattributes'
        unique_together = (('fid', 'attribute'),)
    def __unicode__(self):
        return u'{}-{}'.format(self.fid,self.attribute)


class FoodComments(models.Model):
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid')
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'food_comments'
    def __unicode__(self):
        return u'{}:{}'.format(self.fid,self.comment)


class FoodHier(models.Model):
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid', related_name="hier")
    parent = models.ForeignKey(Food, models.DO_NOTHING, db_column='parent', related_name="+")
    is_primary        = models.BooleanField(default=True)
    is_representative = models.BooleanField(default=True)

    class Meta:
        db_table = 'food_hier'
        unique_together = (('fid', 'parent'),)

    @classmethod
    def get_dic_FoodHier(self):
        """
        :return: { fid_id: prent_id, ..}
        """
        return { obj['fid_id']:obj['parent_id'] for obj in
                 self.objects.filter(is_primary = True).values('fid_id','parent_id')}
    def __unicode__(self):
        return u'{}>{}'.format(self.parent,self.fid)


class FoodNames(models.Model):
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid', related_name="synonims")
    lang_code = models.ForeignKey('Lang', models.DO_NOTHING, db_column='lang_code')
    name = models.CharField(max_length=256)
    is_primary = models.BooleanField()
    is_long = models.BooleanField()

    @classmethod
    @memoize(timeout=60)
    def all(cls):
        # in case of duplicate names prefer foods not under "chinese_food" branch.
        chinese_food = get_all_descendants(Food.objects.get(name='chinese_food').fid)
        names = {x['name']: x['fid_id'] for x in cls.objects.filter(fid__in=chinese_food).values()}
        names.update({x['name']: x['fid_id'] for x in cls.objects.exclude(fid__in=chinese_food).values()})
        return names

    class Meta:
        db_table = 'food_names'

    def __unicode__(self):
        return u'{} - {}'.format(self.fid,self.name)


FOOD_NAMES_CHANGED_TIMESTAMP = '_food_names_last_changed'


def food_names_changed_callback(sender, **kwargs):
    NamedTimestamp.update_timestamp(FOOD_NAMES_CHANGED_TIMESTAMP)


post_save.connect(food_names_changed_callback, FoodNames)
post_delete.connect(food_names_changed_callback, FoodNames)


class FoodReferences(models.Model):
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid')
    lang_code = models.ForeignKey('Lang', models.DO_NOTHING, db_column='lang_code', blank=True, null=True)
    reftype = models.CharField(max_length=64, blank=True, null=True)
    url = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        db_table = 'food_references'

    def __unicode__(self):
        return u'{}:{}'.format(self.fid,self.reftype)


class FoodComponents(models.Model):
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid', related_name='components')
    component = models.ForeignKey(Food, models.DO_NOTHING, db_column='component', related_name='componentsof')
    amount = models.FloatField()
    unit_amount = models.FloatField(blank=True, null=True)
    unit = models.ForeignKey('Units', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'food_components'

    def __unicode__(self):
        return u'{}:{}'.format(self.fid,self.component)


class FoodNutritionRefs(models.Model):
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid')
    usda = models.ForeignKey('UsdaFood', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'food_nutrition_refs'

    def __unicode__(self):
        return u'{}:{}'.format(self.fid,self.usda)


class NamedTimestamp(models.Model):
    name = models.CharField(max_length=64, db_column='name', primary_key=True)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'named_timestamps'

    def __unicode__(self):
        return u'{}'.format(self.name)

    @classmethod
    def update_timestamp(cls, name):
        ts, _ = cls.objects.get_or_create(name=name)
        ts.save()

    @classmethod
    def is_uptodate(cls, name, test_ts):
        try:
            ts_obj = cls.objects.get(name=name)
            ts = int(ts_obj.timestamp.strftime("%s"))
            return test_ts > ts
        except cls.DoesNotExist:
            pass
        return False


class FoodUnits(models.Model):
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid')
    weight = models.FloatField()
    unit = models.ForeignKey('Units', models.DO_NOTHING, blank=True, null=True)

    def __unicode__(self):
        return u'{}:{}'.format(self.fid,self.weight)

    @classmethod
    def all(cls):
        ret = {}
        for row in cls.objects.all():
            if row.fid_id not in ret:
                ret[row.fid_id] = {}
            ret[row.fid_id][row.unit_id] = row.weight
        return ret

    @classmethod
    def all_inhereted(cls):
        sql = ''' WITH units_inhereted AS (
                     select H.fid as fid, unit_id, weight, ROW_NUMBER() OVER( PARTITION BY H.fid, unit_id ORDER BY H.rank) as inh_rank
                     from food_predecessor_rank as H join food_units as U on (U.fid=H.parent)
                   )
                 SELECT fid,unit_id,weight FROM units_inhereted WHERE inh_rank = 1
        '''
        res = db.select_as_dict_dict2(sql)
        return res


    class Meta:
        managed = False
        db_table = 'food_units'
        unique_together = (('fid', 'unit'),)


FOOD_UNITS_CHANGED_TIMESTAMP = '_food_units_last_changed'


def food_units_changed_callback(sender, **kwargs):
    NamedTimestamp.update_timestamp(FOOD_UNITS_CHANGED_TIMESTAMP)


post_save.connect(food_units_changed_callback, FoodUnits)
post_delete.connect(food_units_changed_callback, FoodUnits)

class UsdaFood(models.Model):
    usda_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    database = models.CharField(max_length=256)

    class Meta:
        db_table = 'usda_food'
        unique_together = (('name', 'database'),)

    @property
    def long_description(self):
        try:
            return self.description.long_description
        except UsdaFoodDescription.DoesNotExist:
            return  self.name

    @property
    def group_description(self):
        try:
            return self.description.group_description
        except UsdaFoodDescription.DoesNotExist:
            return None

    def __unicode__(self):
        ufd = UsdaFoodDescription.objects.filter(usda_food=self).first()
        if ufd is not None:
            return u'(long description: {})'.format(ufd.long_description)
        return u'{}'.format(self.name)


class UsdaFoodNutrient(models.Model):
    usda = models.ForeignKey(UsdaFood, models.DO_NOTHING)
    nutrient = models.ForeignKey('UsdaNutrient', models.DO_NOTHING)
    amount = models.FloatField()
    unit = models.CharField(max_length=256)

    class Meta:
        db_table = 'usda_food_nutrient'
        unique_together = (('usda', 'nutrient'),)

    def __unicode__(self):
        return u'{}-{}'.format(self.nutrient,self.usda)


class UsdaNutrient(models.Model):
    name = models.CharField(unique=True, max_length=256)
    reference_value = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'usda_nutrient'

    def __unicode__(self):
        return u'{}:{}'.format(self.name,self.reference_value)


def get_unit_id_by_name(name):
    return db.select_as_value("select unit_id from units where name_en = %s or plural_en = %s or name_he = %s or plural_he = %s or name_cn = %s",[name]*5)

class Units(models.Model):
    unit_id = models.AutoField(primary_key=True)
    name_he = models.CharField(unique=True, max_length=255, blank=True, null=True)
    plural_he = models.CharField(unique=True, max_length=255, blank=True, null=True)
    name_en = models.CharField(unique=True, max_length=255, blank=True, null=True)
    plural_en = models.CharField(unique=True, max_length=255, blank=True, null=True)
    gram_factor = models.IntegerField()
    name_cn = models.CharField(max_length=255, blank=True, null=True)
    cn = models.CharField(unique=True, max_length=255, blank=True, null=True)
    additive = models.BooleanField()
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    step = models.DecimalField(max_digits=10, decimal_places=2, default=0.5)

    class Meta:
        db_table = 'units'

    fields = ['name_he', 'plural_he', 'name_en', 'plural_en', 'name_cn']

    def __str__(self):
        if self.name_en:
            return self.name_en

        return 'no english name'

    @staticmethod
    @memoize(timeout=60)
    def all():
        return {x.unit_id: x for x in Units.objects.all()}


    @staticmethod
    @memoize(timeout=60)
    def all_names():
        a = Units.all()
        all_names = {}
        for k in Units.fields:
            tmp = {x.__dict__[k].lower(): x_id for x_id, x in a.items() if x.__dict__[k]}
            all_names.update(tmp)

        # add the nam
        # for quantity_id, quantity_type in a.iteritems():
        #     if quantity_type.fid:
        #         tmp = {foodname.name: quantity_id for foodname in quantity_type.fid.synonims.all()}
        #         all_names.update(tmp)
        return all_names

    @classmethod
    @memoize(60)
    def get_by_name(cls,name):
       pk = get_unit_id_by_name(name)
       if pk is not None:
           return cls.objects.get(pk=pk)
       else:
           return None

    @classmethod
    @memoize(60)
    def gram_factors(cls):
        return {x.unit_id: x.gram_factor for x in cls.all().values()}

    @classmethod
    @memoize(timeout=60)
    def names(cls):
        return {x.unit_id: (x.name, x.additive) for x in cls.all().values()}

    @staticmethod
    def query_name(name, prefix=''):
        q = [Q(**{prefix + f + '__icontains':name}) for f in Units.fields]
        q = reduce(lambda x,y: x|y, q)
        return q

    @property
    def name(self):
        for field in ['name_en', 'plural_en', 'name_he', 'plural_he', 'name_cn']:
            if self.__dict__[field]:
                return self.__dict__[field]


class FoodDefaultUnit(models.Model):
    fid = models.OneToOneField(Food, models.CASCADE, primary_key=True, related_name='default_unit')
    unit = models.ForeignKey(Units, models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=1)


class GrammarAddingWord(models.Model):
    word = models.CharField(max_length=32, unique=True)
    space_before = models.BooleanField(default=True)
    space_after = models.BooleanField(default=True)

    @staticmethod
    @memoize(timeout=60)
    def all():
        all_objects = GrammarAddingWord.objects.all()
        words = []
        for word in all_objects:
            text = word.word
            if word.space_before:
                text = ' ' + text
            if word.space_after:
                text += ' '
            words.append(text)
        return words


class GrammarMeasureWord(models.Model):
    word = models.CharField(max_length=32, unique=True)
    after_noun = models.BooleanField(default=False)
    quantity_unit = models.ForeignKey('Units',on_delete=models.SET_NULL, null=True, blank=True)
    value = models.FloatField(default=1)

    @staticmethod
    def _all_filtered(after=False):
        return {m['word']: m for m in GrammarMeasureWord.objects.filter(after_noun=after).values()}

    @staticmethod
    @memoize(timeout=60)
    def all_measures():
        return GrammarMeasureWord._all_filtered()

    @staticmethod
    @memoize(timeout=60)
    def all_adjactives():
        return GrammarMeasureWord._all_filtered(True)


class GrammerIntentWord(models.Model):
    word = models.CharField(max_length=32, unique=True)

    @classmethod
    @memoize(timeout=60)
    def all(cls):
        return [x.word for x in cls.objects.all()]


class UserActivityLog(models.Model):
    DELETE = -1
    UPDATE = 0
    CREATE = 1
    CHOICES = [
        (DELETE, 'delete'),
        (UPDATE, 'update'),
        (CREATE, 'create'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE, db_column='user', null=True)
    table = models.TextField()
    line = models.IntegerField()
    action = models.IntegerField(choices=CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    fid = models.ForeignKey(Food, models.DO_NOTHING, db_column='fid', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    datachange= JSONField(default=dict)

    @classmethod
    def add_log(cls, user, action, line, fid=None, description=None):
        log_lines = []
        Nfid, Ndescription,Ndatachange = cls.get_Nvalues(line, action, fid, description)
        log_lines.append(cls(user=user, table=line._meta.db_table, line=line.pk, action=action, fid_id=Nfid, description=Ndescription,datachange=Ndatachange))
        if line._meta.db_table == 'food_hier':
            new_fid_parent = line.parent_id
            old_fid_parent = parent(line.fid_id)
            if new_fid_parent is not None:
                log_lines.append(cls(user=user, table=line._meta.db_table, line=line.pk, action=action,
                                     fid_id=new_fid_parent, description=Ndescription))
            if old_fid_parent is not None and not new_fid_parent == old_fid_parent:
                log_lines.append(cls(user=user, table=line._meta.db_table, line=line.pk, action=action,
                                     fid_id=old_fid_parent, description=Ndescription))
        cls.objects.bulk_create(log_lines)

    @classmethod
    def add_logs(cls, user, action, lines, fid=None, description=None):
        log_lines = []
        for line in lines:
            Nfid, Ndescription,Ndatachange = cls.get_Nvalues(line,action, fid, description)
            log_lines.append(cls(user=user, table=line._meta.db_table, line=line.pk, action=action, fid_id=Nfid, description=Ndescription,datachange=Ndatachange))
        if len(lines) >0 and lines[0]._meta.db_table == 'food_hier':
            new_fid_parent = lines[0].parent_id
            old_fid_parent = parent(lines[0].fid_id)
            if new_fid_parent is not None:
                for line in lines:
                    log_lines.append(cls(user=user, table=line._meta.db_table, line=line.pk, action=action, fid_id=new_fid_parent,
                                         description=Ndescription))
            if  old_fid_parent is not None and not new_fid_parent == old_fid_parent:
                for line in lines:
                    log_lines.append(cls(user=user, table=line._meta.db_table, line=line.pk, action=action, fid_id=old_fid_parent,
                                         description=Ndescription))
        cls.objects.bulk_create(log_lines)

    @classmethod
    def get_Nvalues(cls, line, action, fid, description):
        # data preparetion
        dic = line.__dict__
        new = line
        if new.pk == None or action == cls.CREATE:
            old = new
        else:
            old = new.__class__.objects.get(pk=new.pk)
        # Nfid
        if fid is None and 'fid_id' in dic.keys():
            Nfid = dic['fid_id']
        elif fid is None and 'fid' in dic.keys():
            Nfid = dic['fid']
        else:
            Nfid = fid
        # Ndescription
        if description is None:
            fileds = new._meta.fields
            s = ""
            # reload(sys)
            # sys.setdefaultencoding('utf8')
            if new._meta.db_table == 'food_hier':
                s += ", child: {0}".format(new.fid)
            for filed in fileds:
                filed_name = filed.name
                new_value = getattr(new, filed_name)
                old_value = getattr(old, filed_name)
                old_value = old_value if not type(old_value) == Decimal else float(old_value)
                new_value = new_value if not type(new_value) == Decimal else float(new_value)
                if not ('fid' in filed_name or filed_name[0] == '_' or filed_name == 'id'):
                    if new_value == old_value:
                        next = ", {0}: {1}".format(filed_name, new_value)
                    else:
                        next = ", [{0}: {1} => {2}]".format(filed_name, old_value, new_value)
                    s += next
            s = s[1:]
            if action == cls.DELETE:
                Ndescription = "Deleted:" + s
            elif action == cls.UPDATE:
                Ndescription = "Updated:" + s
            elif action == cls.CREATE:
                Ndescription = "Created:" + s
                line.save()
            else:
                Ndescription = s
        else:
            Ndescription = description
            if action == cls.CREATE: #can be save from outside also, but just for benig sure.
                line.save()
        # Ndatachange
        def _checkVal(v):
            return float(v) if isinstance(v,Decimal) else v
        old_dict = {k: _checkVal(v)
                    for k, v in old.__dict__.items() if k[0] != '_'}
        new_dict = {k: _checkVal(v)
                    for k, v in new.__dict__.items() if k[0] != '_'}
        if action == cls.DELETE:
            Ndatachange = {'old':old_dict,'status':action}
        elif action == cls.UPDATE:
            Ndatachange = {'old':old_dict,'new':new_dict,'status':action}
        elif action == cls.CREATE:
            Ndatachange = {'new':new_dict,'status':action}
        else:
            Ndatachange = {}.copy()
        return Nfid, Ndescription, Ndatachange

    @classmethod
    def prepareToDelete(cls,fid):
        '''
        :param fid: food id that is going to be delted
        fix User Activity Log
        '''
        if type(fid) == int:
            food = Food.objects.get(fid = fid)
            parent_food = Food.objects.get(fid = parent(fid))
        else:
            food = fid
            parent_food = Food.objects.get(fid=parent(fid.fid))
        for ual in UserActivityLog.objects.filter(fid = food):
            ual.fid = parent_food
            ual.description = "On deleted child [{0}]: {1}".format(food,ual.description)
            ual.save()

class UsdaFoodGroup(models.Model):
    food_group_id = models.CharField(primary_key=True, max_length=4)
    food_group_description = models.CharField(max_length=60)

    class Meta:
        db_table = 'usda_food_group'


class UsdaFoodDescription(models.Model):
    usda_food = models.OneToOneField(UsdaFood, on_delete=models.CASCADE, related_name='description')
    usda_food_group = models.ForeignKey(UsdaFoodGroup, on_delete=models.DO_NOTHING, related_name='description')
    long_description = models.CharField(max_length=200)
    short_description = models.CharField(max_length=60)
    common_name = models.CharField(max_length=100, null=True)
    manufacturer = models.CharField(max_length=65, null=True)
    survey = models.CharField(max_length=1, null=True)
    ref_description = models.CharField(max_length=135, null=True)
    refuse = models.IntegerField(null=True)
    scientific_name = models.CharField(max_length=65, null=True)
    n_factor = models.FloatField(null=True)
    protein_factor = models.FloatField(null=True)
    fat_factor = models.FloatField(null=True)
    cho_factor = models.FloatField(null=True)
    ndb_no = models.IntegerField(unique=True)

    class Meta:
        db_table = 'usda_food_description'

    @property
    def group_description(self):
        description = None
        if self.usda_food_group is not None:
            description = self.usda_food_group.food_group_description
        return description


class FoodNutrient(models.Model):
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid', primary_key=True)
    nutrient = models.ForeignKey('UsdaNutrient', models.DO_NOTHING)
    amount = models.DecimalField(max_digits=25, decimal_places=20)
    sd_amount = models.DecimalField(max_digits=25, decimal_places=20, blank=True, null=True)
    unit = models.CharField(max_length=256)
    inherited = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'food_nutrient'
        unique_together = (('fid', 'nutrient'),)

class DeletedFood(models.Model):
    fid = models.IntegerField()
    name = models.CharField(max_length=256)
    substitute = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deleted_food'

    def __str__(self):
        return 'Deleted Food: {}'.format(self.name)

@transaction.atomic
def update_food_nutrients(exclude_chinese=False,reference_node_type = 1,enable_update = True):
    '''
    :param exclude_chinese: flag to exclude chinese food in the process of nutrient_dict
    :param reference_node_type: 0: for enable inheritance parent -> child for all node type
                                1: for enable inheritance parent -> child for only 'common' and 'specific' node type
                        2 or else: for enable inheritance parent -> child for None node type
    :param enable_update: flag to update the db with the result or just return them
    :return: if enable_update = False, then return nutrient_dict, children_dict
    '''

   # food hierarchy query:
    excluded_parents = ['chinese_dishes','chinese_ingredients','chinese_missing_ingredients'] if exclude_chinese else []
   # include only fid selected as representative
    hier = FoodHier.objects.exclude(fid__name__in=excluded_parents).exclude(parent__name__in=excluded_parents).\
        values('parent','fid','is_representative')
    children_dict=defaultdict(list)
    representative_children_dict=defaultdict(list)
    for h in hier:
        children_dict[h['parent']].append(h['fid'])
        if h['is_representative']:
            representative_children_dict[h['parent']].append(h['fid'])

    node_type_to_filter = [obj['name'] for obj in FoodNodeType.objects.all().values('name')] if reference_node_type == 0 \
        else ['common','specific'] if reference_node_type == 1 \
        else []
    fid_permit_inherit_to_child = get_fid_permit_inherit_to_child(node_type_to_filter)
   # food components query:
    food_components = FoodComponents.objects.all().values('fid','component','amount')
    recipe_dict=defaultdict(dict)
    for f in food_components:
        recipe_dict[f['fid']][f['component']] = f['amount']
    liquid_losses = Food.objects.all().values('fid','liquid_loss')
    liquid_loss_dict = dict((l['fid'], l['liquid_loss']) for l in liquid_losses)
    # 1. start with filling nutrients for each food from its references
    nutrient_dict = update_food_nutrients_from_refs()
    nutrients_from_refs_dict= nutrient_dict.copy()
    # 2. Update parents as average of their children and themselves, ignore recipes
    update_food_nutrients_flow(nutrient_dict, children_dict, recipe_dict, recipe_mode=False, food=1,
                               nutrients_from_refs_dict=nutrients_from_refs_dict,
                               representative_children_dict=representative_children_dict,
                               fid_permit_inherit_to_child = fid_permit_inherit_to_child)
    # 3. Update again, now calculate also recipes, and add them to parent averages:
    # Only for parents with nutrients originally based on references (and not inherited from parents),
    # their nutrients will be considered as an additional child
    update_food_nutrients_flow(nutrient_dict, children_dict, recipe_dict, recipe_mode=True, food=1,
                               nutrients_from_refs_dict=nutrients_from_refs_dict,
                               representative_children_dict=representative_children_dict,
                               liquid_loss_dict=liquid_loss_dict,
                               fid_permit_inherit_to_child = fid_permit_inherit_to_child)
    # 4. update database:
    if enable_update:
        food_nutrients_batch_insert(nutrient_dict)
    return nutrient_dict, children_dict,component_with_missing_nutrient_list


def update_food_nutrients_from_refs():
    nutrient_from_ref_query =  "select distinct on(fid,nutrient_id,unit) fid,nutrient_id,unit,amount,sd_amount from (select fid, usda_nutrient.id as nutrient_id, avg(amount) as amount, stddev_pop(amount) as sd_amount, unit, CASE WHEN usda_food.database='Tzameret' THEN 1 WHEN usda_food.database='usda' THEN 2 ELSE 3 END as source from food_nutrition_refs join usda_food_nutrient using (usda_id) join usda_nutrient on (usda_nutrient.id=nutrient_id) join usda_food using (usda_id) group by fid,usda_nutrient.id,unit,source order by fid,nutrient_id,unit,source) as q"
# note: I used stdevp in order to get sd=0 for population of size=1
    nutrient_dict=defaultdict(dict)
    with connection.cursor() as cursor:
        cursor.execute(nutrient_from_ref_query)
        for row in cursor.fetchall():
            # assumes that there is a single row for each fid and nutrient:
            # otherwise only last one is saved (shouldnt happen!)
            nutrient_dict[row[0]][row[1]] = {'unit':row[2],'amount':row[3],'sd_amount':row[4],'inherited':0}
    return nutrient_dict
#TODO push all the calcuation o a class
component_with_missing_nutrient_list = [] #TODO add this to the class ,and a flag if to calcuate
def _check_missing_component(row,recipe_fid):
    nutrient_id = row.name
    component_with_missing_nutrient_list.extend([
        {'recipe_fid':recipe_fid,'component_fid':component_fid,'nutrient_id':nutrient_id}
        for component_fid in row[row.isna()].keys()
    ])

# override_mode: True => update all foods, False=> update only foods which do not already appear in nutrient_dict
def update_food_nutrients_flow(nutrient_dict, children_dict, recipe_dict, recipe_mode= False,
                               override_mode=True, food=1, nutrients_from_refs_dict= None,
                               representative_children_dict=None, liquid_loss_dict=None,
                               fid_permit_inherit_to_child=[]):
    food_nutrients={}
    if representative_children_dict is None:
        representative_children_dict=children_dict
    # leaf with nutrition values, or any food with nutrition values in "not override" mode
    if food in nutrient_dict and (not override_mode or food not in children_dict):
        food_nutrients = nutrient_dict[food]
    elif food in children_dict: # internal nodes
        node_nutrients = defaultdict(list)
        # add nutrients from references as another child of this parent
        if nutrients_from_refs_dict is not None and food in nutrients_from_refs_dict:
            for n in nutrients_from_refs_dict[food]:
                node_nutrients[n].append(nutrients_from_refs_dict[food][n])
        children = children_dict[food]
        representative_children = representative_children_dict[food]
        for child in children:
            child_nutrients = update_food_nutrients_flow(nutrient_dict,
                                                         children_dict, recipe_dict,
                                                         recipe_mode, override_mode, food=child,
                                                         nutrients_from_refs_dict=nutrients_from_refs_dict,
                                                         representative_children_dict=representative_children_dict,
                                                         liquid_loss_dict=liquid_loss_dict,
                                                         fid_permit_inherit_to_child = fid_permit_inherit_to_child)
            if child in representative_children:
                for n in child_nutrients:
                    node_nutrients[n].append(child_nutrients[n])
        # update for parent:
        if node_nutrients and food>1:
            for n in node_nutrients:
                node_list = node_nutrients[n]
                unit = node_list[0]['unit']
                # assign only if all foods have the same unit:
                if all(x['unit']==unit for x in node_list):
                    all_amounts = [float(d['amount']) for d in node_list]
                    food_nutrients[n] = {'amount':np.mean(all_amounts),
                                         'unit':unit,
                                         'sd_amount':np.std(all_amounts),
                                         'inherited':0}
            nutrient_dict[food] = food_nutrients
        elif food==1: #finished recursion for the whole tree
            update_food_nutrients_from_parent(nutrient_dict, children_dict, recipe_dict, food=1,
                                              fid_permit_inherit_to_child=fid_permit_inherit_to_child)
    # recipe for a leaf without other nutrition values
    elif recipe_mode and food in recipe_dict and not food in nutrient_dict:
        recipe_data = recipe_dict[food]
        weights = [recipe_data[x] for x in recipe_data]
        recipe_nutrients = defaultdict(list)
        all_components_nutrients = defaultdict(list)
        for comp in recipe_data:
            if comp in nutrient_dict:
                comp_nutrients = nutrient_dict[comp]
            elif comp in recipe_dict and comp!=food:  # avoid infinite recursion:
                comp_nutrients = update_food_nutrients_flow(nutrient_dict,
                                                            children_dict, recipe_dict,
                                                            recipe_mode, override_mode, food=comp,
                                                            nutrients_from_refs_dict=nutrients_from_refs_dict,
                                                            representative_children_dict=representative_children_dict,
                                                            liquid_loss_dict=liquid_loss_dict,
                                                            fid_permit_inherit_to_child=fid_permit_inherit_to_child)
            else: # missing nutrition values for component - NONE for recipe
                return {}
            for n in comp_nutrients:
                recipe_nutrients[n].append([comp_nutrients[n],recipe_data[comp]]) #[nutrient dict amount, weight]
            all_components_nutrients[comp]=comp_nutrients
        # update for recipe:
        if 99 < np.sum(weights) < 101:
            df = pd.DataFrame(all_components_nutrients)
            df.apply(lambda row: _check_missing_component(row,food) ,axis=1)
            # calculate nutrition considering liquid loss for recipe
            liquid_loss = liquid_loss_dict[food] if liquid_loss_dict is not None and food in liquid_loss_dict else 0
            if liquid_loss is None or liquid_loss < 0 or liquid_loss >= 100:
                correction_water, correction_else_water = [1, 1]
            else:
                correction_water, correction_else_water = calc_liquid_loss(weights,recipe_nutrients,liquid_loss)
            for n in recipe_nutrients:
                recipe_list = recipe_nutrients[n]
                all_amounts = [float(d[0]['amount']) for d in recipe_list]
                weights_nut = [float(d[1]) for d in recipe_list]
                unit = recipe_list[0][0]['unit']
                # assign only if components sum up to 100% and all foods have the same unit:
                if len(weights) == len(all_amounts) and all (x[0]['unit']==unit for x in recipe_list):
                    amount = np.average(all_amounts, weights=weights_nut)
                    amount *= correction_water if n == 106 else correction_else_water
                    food_nutrients[n] = {'amount': amount,
                                         'unit': unit,
                                         'sd_amount': 0,
                                         'inherited':0} #to do change sd !!!
        nutrient_dict[food] = food_nutrients

    # else if leaf with no nutrition values, then food_nutrients={}
    return food_nutrients


# each iteration update children of this food, and call function for each child
def update_food_nutrients_from_parent(nutrient_dict, children_dict, recipe_dict, food=1,
                                      fid_permit_inherit_to_child=[]):
 # update children of internal nodes, ignoring if parent has recipe because the recipe is ignored.
    if food in children_dict:
        children = children_dict[food]
        for child in children:
            if food in nutrient_dict and food in fid_permit_inherit_to_child and child not in recipe_dict:
                #inherit to child: (nutrient in food) - (nutrient in child)
                list_to_inherit = list(set(nutrient_dict[food])-set(nutrient_dict[child]))
                for nut in list_to_inherit:
                    nutObj = nutrient_dict[food][nut].copy()
                    nutObj['inherited'] = 1
                    nutrient_dict[child][nut] = nutObj
            child_nutrients = update_food_nutrients_from_parent(nutrient_dict, children_dict,
                                                                recipe_dict, food=child,
                                                                fid_permit_inherit_to_child=fid_permit_inherit_to_child)
    # else: reached to leaf - stop
    return None

def calc_liquid_loss(weights,recipe_nutrients,liquid_lose):
    recipe_list_water = [float(d[0]['amount']) for d in recipe_nutrients[106]] # water -> nutrient_id = 106
    weights_water = [float(d[1]) for d in recipe_nutrients[106]]# water -> nutrient_id = 106
    #define three diffrent wight in the calcuation
    recipe_list_water.extend([0] * (len(weights) - len(weights_water)))  # add zero
    missing_list = list(set(weights) - set(weights_water))
    for missing in missing_list:
        weights_water.append(missing)

    water_weight_origin = float(np.average(recipe_list_water, weights=weights_water))
    all_the_food_weight = float(np.sum(weights))
    else_water_weight_origin = all_the_food_weight - water_weight_origin

    water_liquid_lose = water_weight_origin - liquid_lose
    food_liquid_lose = else_water_weight_origin + water_liquid_lose

    water_new_weight =      (water_liquid_lose       /food_liquid_lose)*100.0
    else_water_new_weight = (else_water_weight_origin/food_liquid_lose)*100.0

    correction_water = water_new_weight/water_weight_origin
    correction_else_water = else_water_new_weight/else_water_weight_origin
    return correction_water,correction_else_water



def food_nutrients_batch_insert(nutrient_dict):

    params = []
    for food in nutrient_dict:
        for n in nutrient_dict[food]:
            values = nutrient_dict[food][n]
            params.extend([food, n, values['unit'], values['amount'], values['sd_amount'],values['inherited']])
    n_columns = len(['fid','nutrient_id','unit','amount','sd_amount','inherited'])
    n_records = int(len(params) / n_columns)
    sql = 'insert into food_nutrient (fid,nutrient_id,unit,amount,sd_amount,inherited) values {}'.format(
        ', '.join(['(%s, %s, %s, %s, %s, %s)'] * n_records),
    )
    with closing(connection.cursor()) as cursor:
        cursor.execute("delete from food_nutrient")
        cursor.execute(sql, params)

def get_fid_permit_inherit_to_child(node_type_to_filter=None):
    if node_type_to_filter is None:
        node_type_to_filter = []
    return [obj['fid'] for obj in Food.objects.filter(node_type__name__in=node_type_to_filter).values('fid')]


class MultipleChoiceQuestion(models.Model):
    en = models.CharField(max_length=256)
    he = models.CharField(max_length=256)
    cn = models.CharField(max_length=256, blank=True, null=True)
    action = models.CharField(max_length=10, choices=Question.ACTION_CHOICES, default=Question.REPLACE)
    ask_on = models.CharField(max_length=10, choices=Question.ASK_CHOICES, default=Question.ALL)

    class Meta:
        managed = False
        db_table = 'multiple_choice_question'

    def is_answered(self, food_item):
        return bool(food_item.children)

    def to_dict(self, lang='en'):
        answers = [{'id': f_answer.id, 'fid': f_answer.answer.fid, 'text': f_answer.get_text(lang)}
                   for f_answer in self.get_answers()]
        return {
            'action': self.action,
            'answers': answers,
            'q_id': self.pk
        }

    def get_answers(self):
        return self.foodanswer_set.all()

    def get_text(self, lang='en'):
        if lang == 'he':
            return self.he
        if lang == 'cn' and self.cn is not None:
            return self.cn

        return self.en

    def __str__(self):
        return self.en


class FoodMultipleChoiceQuestion(models.Model):
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid')
    question = models.ForeignKey('MultipleChoiceQuestion', models.CASCADE, db_column='question', blank=True,
                                 null=True)

    class Meta:
        db_table = 'food_multiple_choice_question'

    @property
    def ask_on(self):
        return self.question.ask_on

    def is_answered(self, food_item):
        return self.question.is_answered(food_item)

    def to_dict(self, lang='en'):
        return self.question.to_dict(lang)

    def get_text(self, lang='en'):
        return self.question.get_text(lang)

    def __unicode__(self):
        return u'{} - {}'.format(self.fid, str(self.question))


class FoodAnswer(models.Model):
    answer = models.ForeignKey(Food, models.DO_NOTHING, db_column='answer')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    question = models.ForeignKey('MultipleChoiceQuestion', models.CASCADE, db_column='question')
    number = models.IntegerField(blank=True, null=True)
    en = models.CharField(max_length=256, blank=True, null=True)
    he = models.CharField(max_length=256, blank=True, null=True)
    cn = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        db_table = 'food_answer'
        unique_together = (('question', 'number'),)
        ordering = ('question', 'number',)

    def get_text(self, lang='en'):
        return self.answer.get_name_by_lang(lang)


class BooleanQuestion(models.Model):
    en = models.CharField(max_length=256)
    he = models.CharField(max_length=256)
    cn = models.CharField(max_length=256, blank=True, null=True)
    positive_answer = models.ForeignKey('Food', models.DO_NOTHING,
                                        db_column='positive_answer', related_name='+', blank=True, null=True)
    negative_answer = models.ForeignKey('Food', models.DO_NOTHING,
                                        db_column='negative_answer', related_name='+', blank=True, null=True)
    positive_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    negative_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    action = models.CharField(max_length=10, choices=Question.ACTION_CHOICES, default=Question.REPLACE)
    ask_on = models.CharField(max_length=10, choices=Question.ASK_CHOICES, default=Question.ALL)

    class Meta:
        db_table = 'boolean_question'

    def is_answered(self, food_item):
        return bool(food_item.children)

    @staticmethod
    def _get_answer(answer, amount, lang='en'):
        if answer:
            return {
                'fid': answer.fid,
                'text': answer.get_name_by_lang(lang),
                'quantity': amount
            }

        return dict.fromkeys(['fid', 'text', 'amount'], None)

    def to_dict(self, lang='en'):
        return {
            'action': self.action,
            'positive_answer': self._get_answer(self.positive_answer, self.positive_amount, lang),
            'negative_answer': self._get_answer(self.negative_answer, self.negative_amount, lang),
            'q_id': self.pk
        }


class FoodBooleanQuestion(models.Model):
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid')
    boolean_question = models.ForeignKey(BooleanQuestion, models.CASCADE, db_column='boolean_question')

    class Meta:
        db_table = 'food_boolean_question'

    @property
    def ask_on(self):
        return self.boolean_question.ask_on

    def is_answered(self, food_item):
        return self.boolean_question.is_answered(food_item)

    def to_dict(self, lang='en'):
        return self.boolean_question.to_dict(lang)

    def get_text(self, lang='en'):
        if lang == 'he':
            return self.boolean_question.he
        if lang == 'cn' and self.boolean_question.cn is not None:
            return self.boolean_question.cn

        return self.boolean_question.en

    def __unicode__(self):
        return u'{}- {}'.format(str(self.fid), self.boolean_question.en)


class AmountQuestion(models.Model):
    en = models.CharField(max_length=256)
    he = models.CharField(max_length=256)
    cn = models.CharField(max_length=256, blank=True, null=True)
    food_to_add = models.ForeignKey('Food', models.CASCADE, db_column='food_to_add')
    quantity_type = models.ForeignKey('Units', models.DO_NOTHING, db_column='quantity_type',
                                      blank=True, null=True)
    default_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ask_on = models.CharField(max_length=10, choices=Question.ASK_CHOICES, default=Question.ALL)

    class Meta:
        db_table = 'amount_question'

    def is_answered(self, food_item):
        """
        Check if should ask the question about a given food item.
        :param food_item: FoodItem
        :return: Bool
        """
        return bool(food_item.children)

    def to_dict(self, lang='en'):
        return {
            'action': Question.ADD,
            'food': {'fid': self.food_to_add.fid, 'text': self.food_to_add.get_name_by_lang(lang)},
            'quantity_type': self.quantity_type.name_en,
            'default_amount': self.default_amount,
            'max_amount': self.quantity_type.max_amount,
            'step': self.quantity_type.step,
            'q_id': self.pk
        }

    def __unicode__(self):
        return self.en


class FoodAmountQuestion(models.Model):
    fid = models.ForeignKey(Food, models.CASCADE, db_column='fid')
    amount_question = models.ForeignKey(AmountQuestion, models.CASCADE, db_column='amount_question')

    class Meta:
        db_table = 'food_amount_question'
        unique_together = (('fid', 'amount_question'),)

    def is_answered(self, food_item):
        return self.amount_question.is_answered(food_item)

    @property
    def ask_on(self):
        return self.amount_question.ask_on

    def to_dict(self, lang='en'):
        return self.amount_question.to_dict(lang)

    def get_text(self, lang='en'):
        if lang == 'he':
            return self.amount_question.he
        if lang == 'cn' and self.amount_question.cn is not None:
            return self.amount_question.cn

        return self.amount_question.en

    def __unicode__(self):
        return u'{}- {}'.format(str(self.fid), self.amount_question.en)



def refs_contain(text=''):
    words = text.split(',')
    q = [Q(name__icontains=w.strip()) for w in words]
    q = reduce(lambda x, y: x & y, q)
    query_set = UsdaFood.objects.filter(q)
    return query_set

def refs_description_contain(text=''):
    words = text.split(',')
    q = [Q(long_description__icontains=w.strip()) for w in words]
    q = reduce(lambda x, y: x & y, q)
    query_set = UsdaFoodDescription.objects.filter(q)
    return query_set


def foods_for(text='',asSubstring = True):
    if len(text) <= 3 and asSubstring:
        names = FoodNames.objects.filter(name__istartswith=text)
        foods = Food.objects.filter(name__istartswith=text.replace(' ', '_'))
    else:
        if asSubstring:
            names = FoodNames.objects.filter(name__icontains=text)
            foods = Food.objects.filter(name__icontains=text.replace(' ', '_'))
        else:
            fixTx = text
            fixTx_rep = text.replace(' ', '_')
            names = FoodNames.objects.filter(name__icontains=""+fixTx+"").exclude(Q(name__iregex=r'[\w.]%s'%(fixTx)) | Q(name__iregex=r'%s[\w.]'%(fixTx)))
            foods = Food.objects.filter(name__icontains=""+fixTx_rep+"").exclude(Q(name__iregex=r'[\w.]%s'%(fixTx_rep)) | Q(name__iregex=r'%s[\w.]'%(fixTx_rep)))

    name_names = {n.name for n in names}

    res =   [{'id': n.fid_id, 'text': n.name, 'f': n.fid} for n in names] + [{'id': f.fid, 'text': f.name.replace('_', ' '), 'f': f} for f in foods if f.name.replace('_', ' ') not in name_names]
    res = sorted(res, key = lambda x: (not x["text"].startswith(text), x["text"]))
    return res

def users_for(text=''):
    users = User.objects.filter(username__icontains=text)
    return [{'id':user.id,'text':user.username} for user in users]

def foods_for_short(text='',asSubstring = True):
    if len(text) <= 3 and asSubstring:
        names = FoodNames.objects.filter(name__istartswith=text).values()
        foods = Food.objects.filter(name__istartswith=text.replace(' ', '_')).values()
    else:
        if asSubstring:
            names = FoodNames.objects.filter(name__icontains=text).values()
            foods = Food.objects.filter(name__icontains=text.replace(' ', '_')).values()
        else:
            fixTx = text
            fixTx_rep = text.replace(' ', '_')
            names = FoodNames.objects.filter(name__icontains=""+fixTx+"").exclude(Q(name__iregex=r'[\w.]%s'%(fixTx)) | Q(name__iregex=r'%s[\w.]'%(fixTx))).values()
            foods = Food.objects.filter(name__icontains=""+fixTx_rep+"").exclude(Q(name__iregex=r'[\w.]%s'%(fixTx_rep)) | Q(name__iregex=r'%s[\w.]'%(fixTx_rep))).values()

    name_names = {n['name'] for n in names}

    res =   [{'id': n['fid_id'], 'text': n['name']} for n in names] + [{'id': f['fid'], 'text': f['name'].replace('_', ' ')} for f in foods if f['name'].replace('_', ' ') not in name_names]
    res = sorted(res, key = lambda x: (not x["text"].startswith(text), x["text"]))
    return res

def get_foods_for_parent_select(food, text=''):

    l = [{'id': cur_food['id'], 'text': cur_food['text']}
         for cur_food in foods_for(text) if food.can_be_child_of(cur_food['f'])]
    return json.dumps(l)


def get_foods_for_moving_dataset(text=''):
    l = [{'id': cur_food['id'], 'text': cur_food['text']} for cur_food in foods_for(text)]
    return json.dumps(l)


def get_foods_for_components(food, text=''):
    nested_recipes = food.nested_recipes()
    l = [{'id': cur_food['id'], 'text': cur_food['text']}
         for cur_food in foods_for(text) if cur_food['f'] not in nested_recipes]
    return json.dumps(l)


def get_usda_names(text=''):
    '''
    Get food name as it appears in USDA database
    :param text: str A name to look in database
    :return: list All possible names
    '''
    # lookup in food description (preferred):
    description_query_set=refs_description_contain(text)
    l = [{'id': u.usda_food.usda_id, 'text': '{u.long_description} [{u.group_description}] ({u.usda_food.database})'.format(u=u)}
         for u in description_query_set]
    described_ids = set([item['id'] for item in l])

    # lookup in food names (second best):
    # l = [{'id': u.usda_id, 'text': '{u.name} ({u.database})'.format(u=u)} for u in query_set]
    name_query_set=refs_contain(text)
    for u in name_query_set:
        if u.usda_id in described_ids:
            continue
        l.append({'id': u.usda_id, 'text': '{u.name} ({u.database})'.format(u=u)})
    # return merged list
    return json.dumps(l, ensure_ascii=False)


def get_units(text=''):
    text = text.lower()
    fields = ['name_en', 'plural_en', 'name_he', 'plural_he', 'name_cn']
    q = list(map(lambda x: Q(**{x + '__icontains': text}), fields))
    q = reduce(lambda x, y: x | y, q)
    quantity_types = Units.objects.filter(q).all()
    all_names = OrderedDict()
    all_ids = set()
    for k in fields:
        tmp = {x.__dict__[k].lower(): x.unit_id for x in quantity_types if x.__dict__[k] is not None
               and text in x.__dict__[k].lower() and x.unit_id not in all_ids}
        all_ids |= set(tmp.values())
        all_names.update(tmp)
    return [{'id': str(v), 'text': k} for k, v in all_names.items()]


def get_nutrients(text=''):
    nutrients = UsdaNutrient.objects.filter(name__icontains=text)
    return [{'id': n.id, 'text': n.name} for n in nutrients]

def get_attributes(text = ''):
    attributes = Attribute.objects.filter(value__icontains=text)
    return [{'id': n.id, 'text': n.value} for n in attributes]

def get_database(text = ''):
    databaseList = UsdaFood.objects.filter(database__icontains=text).distinct("database").values_list('database',flat=True)
    return [{'id': n, 'text': n} for n in databaseList]

def get_node_type(text=''):
    node_type_list = FoodNodeType.objects.filter(name__icontains=text)
    return [{'id': n.id, 'text': n.name} for n in node_type_list]

def calc_weight(food, quantity, quantity_unit):
    if quantity is None:
        return None
    if not quantity_unit:
        if quantity > 10:
            quantity_unit = Units.objects.get(pk=2)  # Gram
        else:
            quantity_unit = Units.objects.get(pk=9)  # Serving
    gpu = FoodUnits.objects.filter(fid=food.fid, quantity_type=quantity_unit).first()
    if gpu:
        return quantity * gpu.weight
    else:
        return quantity * quantity_unit.gram_factor


# def parse_free_text(text):
#     text_parser = TextParsingAlgorithm(text)
#     ret = []
#     for food, quantity, quantity_unit in text_parser.parsed_text:
#         d = {'food': food, 'amount': quantity, 'unit_type': quantity_unit}
#         ret.append(d)
#     return ret, text_parser.unknown_words


def get_names_for_china(lang='en'):
    index = {'en': 5, 'cn': 2}
    with open(os.path.dirname(__file__) + '/../../data/nutri.csv') as f:
        nutri = defaultdict(lambda: '')
        for line in f.readlines()[2:]:
            s = line.strip().decode('utf8').split(',')
            nutri[s[3]] = s[index[lang]]
    return nutri



def parent(fid):
    return  db.select_as_value('select parent from food_hier where fid = %s and is_primary',[fid])

def qattributes(fid, get_inherited = False):
    data = db.select_as_dict('select attribute,quantity from food_qattributes where fid=%s', [fid])
    p = None
    while len(data) == 0 :
        p = parent(fid)
        if not p:
            break
        fid = p
        data = db.select_as_dict('select attribute,quantity from food_qattributes where fid=%s', [fid])

    for d in data:
        data[d] = float(data[d])
    if get_inherited:
        return {'data':data, 'inherited': p}
    return data

def quantity_names():
    sql = "select unit_id,COALESCE(name_en, plural_en, name_he, plural_he, name_cn) from units"
    return db.select_as_dict(sql)

def food_units(fid):
    sql = 'select unit_id,weight,id,fid,name from food_units join food using (fid) where fid=%s'
    units = db.select_as_dict_dict(sql,[fid])
    p = parent(fid)
    while (p):
        parent_units = db.select_as_dict_dict(sql,[p])
        for unit in parent_units:
            if unit not in units:
                units[unit] = parent_units[unit]
        p = parent(p)


    qnames = quantity_names()
    for d in units.values():
        d["quantity_name"] =  qnames[d["unit_id"]]
    return units.values()

def food_units_with_gram(fid):
    data = list(food_units(fid))
    unts = Units.objects.filter(name_en__icontains='gram').values() #<QuerySet [<Units: Kilogram>, <Units: Gram>].. and anything other unit that is onsists of gram>
    for un in unts:
        data.append({u'quantity_name': un['name_en'],
              'weight': un['gram_factor'],
               'unit_id': un['unit_id'],
                'fid': fid})
    return data

def get_is_countable(fid):
    if fid is None:
        return {'is_countable':None,'fid':None,'name': None}
    f = Food.objects.get(pk=fid)
    if f.is_countable is None:
        return get_is_countable(parent(fid))
    else:
        return {'fid':fid,'is_countable':f.is_countable,'name':f.name}

def get_sortedByHier_fidList():
    foods = Foods(trim=False).obj_sorted
    lst = []
    for obj in foods:
        lst.append(obj.fid)
    return lst


def get_all_descendants(fid):
    if type(fid) == list:
        all_descendants = db.select_as_column('select fid from food_predecessors where parent in %s', [tuple(fid)])
    else:
        all_descendants = db.select_as_column('select fid from food_predecessors where parent=%s', [fid])
    return all_descendants
# ========================== attribute requirement methods =============================================================

# return subset of attributes summary containing only foodIDs which contain required attribute if exclude=False,
# or only foodIDs which do not contain required attribute, if exclude=True.
# If no food matches requirement or required attrbiute in not included in attributes summary columns,
# return original summary (instead of subset)
# def apply_requirement(attributes_summary, r):
#
#     att = r['attribute']
#     exclude = r['exclude']
#     exclusion_happened = False
#     if att in attributes_summary.columns:
#         if not exclude and attributes_summary[att].notnull().any(): #filter to foods containing attribute
#             attributes_summary = attributes_summary[attributes_summary[att].notnull()]
#         elif exclude and attributes_summary[att].isnull().any(): #filter to foods not containing attribute
#             attributes_summary = attributes_summary[attributes_summary[att].isnull()]
#             exclusion_happened = True
#     return attributes_summary, exclusion_happened

def get_descendants_by_attributes_and_food(fid,attribute_requirements=[],get_exclusion=False):
    # 1. get descendants under food
    food_descendants = [fid] + get_all_descendants(fid)  # including self
    # 2. get food attributes for all descendants:
    food_attributes = FoodAttributes.objects.filter(fid__in=food_descendants).values()
    # 3. filter to foods which contain required attributes:
    selected_fid = food_descendants
    ls = []
    exclusion_happened=False
    for i in range(len(attribute_requirements),0,-1):
        #4 get all posibel list with i attributes, sorted by the index
        lists = list(itertools.combinations(attribute_requirements,i))
        for ls in lists:
            selected_fid, exclusion_happened = filter_food_by_attributes_sort(food_attributes, list(ls))
            if len(selected_fid)>0:
                break
        if len(selected_fid) > 0:
            break
    selected_fid.sort()
    if get_exclusion:
        return selected_fid, exclusion_happened
    else:
        return {'descendants': selected_fid, 'attributes': ls, 'exclusion_happened': exclusion_happened}

def filter_food_by_attributes(food_attributes, attribute_requirements):
    """

    :param food_attributes: set of FoodAttributes
    :param attribute_requirements: list of Attribute
    :return: set of Food ids that have all the attributes
    """
    original_foods = {fa.fid.fid for fa in food_attributes}
    filtered_food_attributes = food_attributes.filter(attr_id__in = attribute_requirements)
    foods = {fa.fid.fid for fa in filtered_food_attributes}
    exclusion_happened = len(foods) < len(original_foods)
    return foods, exclusion_happened
    # exclusion_happened = False
    # attributes_summary = food_attributes_df.pivot_table(index='fid', columns='attribute', values='fid', aggfunc=len)
    # if not attribute_requirements is None:
    #     for r in attribute_requirements:
    #         attributes_summary, exclusion_happened = apply_requirement(attributes_summary, r)
    # return attributes_summary.index, exclusion_happened

def filter_food_by_attributes_sort(food_attributes, attribute_requirements):
    """

    :param food_attributes: set of FoodAttributes
    :param attribute_requirements: list of Attribute
    :return: set of Food ids that have all the attributes
    """
    original_foods = {fa['fid_id'] for fa in food_attributes}
    filtered_food_attributes = food_attributes.filter(attr_id__in = attribute_requirements)
    ls = []
    for attr in attribute_requirements:
        ls.append([fa['fid_id'] for fa in filtered_food_attributes.filter(attr_id = attr).values('fid_id')])
    foods = [fa['fid_id'] for fa in filtered_food_attributes]
    for subLs in ls:
        foods = list(set(foods) & set(subLs))
    exclusion_happened = len(foods) < len(original_foods)
    return foods, exclusion_happened

def delete_secondary_ancestor(fid,parent):
    sql = "delete from  food_hier where fid = %s and parent=%s"
    db.execute(sql,[fid,parent])




def default_units_data():
    sql = '''
                WITH units_inhereted AS (
                     select H.fid as fid, unit_id, amount, ROW_NUMBER() OVER( PARTITION BY H.fid ORDER BY H.rank) as inh_rank
                     from food_predecessor_rank as H join food_fooddefaultunit as U on (U.fid_id=H.parent)
                   )
                 SELECT fid , unit_id, amount FROM units_inhereted where inh_rank=1 order by fid;
    '''
    return dict(db.select_lambda(sql, lambda x : (x[0],(x[1],x[2]))))

def PutUnitInCommponent(components):
    '''
    for each component in components, add to component.food.units his units from FoodUnits+ Gram+ kilogram
    '''
    for obj in components:
        if obj is not None:
            obj.food.units = food_units_with_gram(obj.food.fid)
            flag = True
            if obj.unit_type is not None:
                for un in obj.food.units:
                    if un['quantity_name'] == obj.unit_type.name:
                        flag = False
                if flag:
                    obj.unit_type = None
    return components
