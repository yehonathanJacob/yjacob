###  -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from __future__ import print_function
from __future__ import absolute_import

import itertools
import re
from collections import defaultdict

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseRedirect, JsonResponse,
                         HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound)
from .models import *
from .csv_utils import CsvUtils
from .forms.multiple_choice_question import ChoiceQuestionForm
from .food_item import FoodItem
from django.core.exceptions import ObjectDoesNotExist
from geolite2 import geolite2
from .fooddb_queries import fooddb_querise_runFromQueryDict
from .fooddb_filter import fooddb_filter_runFromQueryDict
from csv import writer as csvwriter

from langdetect import detect
from unidecode import unidecode
from .analyzer import ImageAnalyzer
from .question import Question
import numpy as np
from django.conf import settings
from PIL import Image
from io import BytesIO
import logging
import pickle
from datetime import datetime
import dateutil.parser
import threading
from . import nlp
import sys

logger = logging.getLogger('debug')

def hello(request):
    response_text = str('hello world')
    response_text += ' Python version: {}'.format(sys.version)
    logger.debug("hello!!!")
    return HttpResponse(response_text)


def home(request):
    r = render(request, 'home.html', {})
    return r

def get_food_component_of(request):
    fid = request.GET.get('fid')
    data = [ {'fid':obj.fid_id, 'name': obj.fid.name} for obj in FoodComponents.objects.select_related('fid').filter(component_id=fid)]
    return JsonResponse(data,safe=False)

def food_table(request, fid=None):
    fid = int(fid) if fid is not None else None
    f = Foods(fid)
    foods_with_images = set(Food.objects.filter(datasetcategories__isnull=False))
    food      = None
    root_path = []
    if fid:
        food = Food.objects.get(pk=fid)
        root_path = food.root_path()[:-1]

    listName = FoodNames.objects.filter(fid=fid).exclude(lang_code="cn").values('name')
    listDublicate = [obj['name'] for obj in listName if FoodNames.objects.filter(name=obj['name']).count() >1]

    r = render(request, 'food_table.html', { 'foods': f.foods,
                                             'f': food  ,
                                             "root_path": root_path,
                                             'is_superuser': request.user.is_superuser,
                                             'is_loggedin' : request.user.is_authenticated,
                                             'with_images': foods_with_images,
                                             'images_host': get_images_host_by_request(request),
                                             'root' : f.foods[0][0].fid,
                                             'listDublicate': listDublicate
                                         })
    return r


def dataset(request, ds, cat):
    dataset = Datasets.objects.get(pk=ds)
    category = DatasetCategories.objects.filter(dataset=dataset, category_id=cat).first()
    return render(request, 'dataset.html', {"ds": category, 'images_host': get_images_host_by_request(request)})


def food(request, fid):
    #print request.user.get_all_permissions()
    fid = int(fid)
    try:
        f = Food.get(fid=fid)
    except Food.DoesNotExist:
        return HttpResponseNotFound('<h1>No matching fid</h1>')
    fid = f.fid # can be also the substitute food
    n = FoodNames.objects.filter(fid=fid)
    can_remove = f.components.count() + f.nutrition_refs.count() != 1 or f.parent() not in f.nested_recipes()
    can_delete = request.user.is_superuser and f.can_be_deleted()
    custom_nutrients = UsdaFoodNutrient.objects.filter(usda__name=f.name, usda__database='FoodDB').select_related('nutrient')
    # is_curated = f.attributes().filter(attr__value="curated").first()
    # if is_curated:
    #     is_curated = is_curated.id
    nutrients_list = set_nutrients_list()

    foods = Foods(fid)
    foods = foods.foods
    listRepresentative = [food.name for food, trimmed in foods if food.is_representative()]

    listName = FoodNames.objects.filter(fid=fid).exclude(lang_code="cn").values('name')
    listDublicate = [obj['name'] for obj in listName if FoodNames.objects.filter(name=obj['name']).count() > 1]

    nutrition_refs_all = f.nutrition_refs_all
    all_nutrients_list = set_nutrients_list_all()

    ret = render(request, 'food.html', {'food': f,
                                        'names': n,
                                        "root_path": f.root_path()[:-1],
                                        "datasets": f.datasets(),
                                        "refs": f.refs(),
                                        "comments": f.comments(),
                                        'components': f.components.all(),
                                        'nutrition_refs': f.nutrition_refs,
                                        'grams_per_unit_rec': food_units(fid),
                                        'default_unit': f.get_default_unit(),
                                        'can_remove': can_remove,
                                        'is_superuser': can_delete,
                                        'images_host': get_images_host_by_request(request),
                                        'food_attributes': [(a.attr.type.name, a) for a in f.attributes()],
                                        'langs': Lang.objects.all(),
                                        'attribute_types': AttributeType.objects.all(),
                                        'attributes': Attribute.objects.all(),
                                        # 'is_curated': is_curated,
                                        'custom_nutrients': custom_nutrients,
                                        'food_amount_questions': f.foodamountquestion_set.all,
                                        'boolean_questions': f.foodbooleanquestion_set.all(),
                                        'choice_questions': f.foodmultiplechoicequestion_set.all(),
                                        'amount_questions': AmountQuestion.objects.all(),
                                        'nutrients_list': nutrients_list,
                                        'listRepresentative': listRepresentative,
                                        'listDublicate':listDublicate,
                                        'is_countable': get_is_countable(fid),
                                        'nutrition_refs_all':nutrition_refs_all,
                                        'food_node_type': f.node_type,
                                        'node_type_option': FoodNodeType.getDic().values(),
                                        'all_nutrients_list':all_nutrients_list[:8]
                                        })
    return ret


def random_image(request, fid):
    IMAGE_HEIGHT = 65
    datasets = DatasetCategories.objects.filter(fid_id=fid).order_by('?')
    for d in datasets:
        image = d.sample_image_path()
        if image:
            im = Image.open(image)
            width, height = im.size
            new_width, new_height = int(width * (IMAGE_HEIGHT / height)), IMAGE_HEIGHT
            im = im.resize((new_width, new_height), Image.BICUBIC)
            output = BytesIO()
            im.save(output, 'png')
            output.seek(0)
            return HttpResponse(output.read(),content_type='image/png')
    return HttpResponse('')

def thumbnail(request, ds, cat, image_path):
    #IMAGE_WIDTH, IMAGE_HEIGHT = 180, 180
    OUT_SIZE = 180
    path = '{}/{}/{}/{}'.format(IMAGES, ds, cat, image_path)
    im = Image.open(path)
    resize_factor=OUT_SIZE/float(max(im.size))
    im = im.resize((int(im.size[0] * resize_factor), int(im.size[1] * resize_factor)))
    output = BytesIO()
    im.save(output, 'png')
    output.seek(0)
    return HttpResponse(output.read(), content_type='image/png')


def missing_nutrition(request):
    all_foods = set(Food.objects.all())
    all_foods -= {f.fid for f in FoodComponents.objects.select_related('fid')}
    all_foods -= {f.fid for f in FoodNutritionRefs.objects.select_related('fid')}
    all_foods -= {f.fid for f in FoodAttributes.objects.filter(attr__value='chinese_dishes').select_related('fid')}
    return render(request, 'missing_nutrition.html', {'foods': all_foods})


def missing_units(request):
    all_foods = set(Food.objects.all())
    all_foods -= {f.fid for f in FoodUnits.objects.select_related('fid')}
    all_foods -= {f.fid for f in FoodAttributes.objects.filter(attribute__name='chinese_dishes').select_related('fid')}
    return render(request, 'missing_nutrition.html', {'foods': all_foods})


def missing_serving_size(request):
    all_foods = set(Food.objects.all())
    all_foods -= {f.fid for f in FoodUnits.objects.filter(quantity_type__name_en='Serving').select_related('fid')}
    all_foods -= {f.fid for f in FoodAttributes.objects.filter(attribute__name='chinese_dishes').select_related('fid')}
    return render(request, 'missing_nutrition.html', {'foods': all_foods})

def clean_text(t):
    t = re.sub("\s+", " ", t.strip().lower()).replace('_', ' ')
    return t


def clean_symbol(t):
    t = clean_text(t).replace(' ', '_')
    return t

def clean_ascii_symbol(t):
    t = t.lower()
    t = re.sub("\W","_",t)
    return t

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

lang_detect_codes = {
    'zh-cn' : 'cn',
    'ru'    : 'ru',
    'he'    : 'he',
    'en'    : 'en',
}

def language(symbol):
    lang   = detect(symbol)
    logger.debug("detect=%s",lang)
    if lang in lang_detect_codes:
        return lang_detect_codes[lang]
    if is_ascii(symbol):
        return 'en'
    return None

@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def add_food(request):
    symbol = clean_symbol(request.POST['symbol'])
    lang   = language(symbol)
    logger.debug("%s [%s]",symbol,lang)

    if is_ascii(symbol):
        ascii_symbol = symbol
    else:
        ascii_symbol = clean_symbol(unidecode(symbol))

    ascii_symbol = clean_ascii_symbol(ascii_symbol)
    try:
        parent = int(request.POST['parent'])
    except:
        parent = None

    try:
        exists = Food.objects.get(name=ascii_symbol)
        if exists:
            return HttpResponseRedirect('/food/' + str(exists.fid))
    except:
        pass

    food = Food(name=ascii_symbol)
    food.for_classification = food.bad = False
    food.save()
    UserActivityLog.add_log(request.user,UserActivityLog.CREATE, food,fid = food.fid)
    food.update_parent(parent, request.user, False)

    if lang:
        try:
            o = FoodNames(fid=food,
                      lang_code=Lang.objects.get(pk=lang),
                      name=clean_text(symbol)
                      )
            UserActivityLog.add_log(request.user, UserActivityLog.CREATE, o)
            o.save()
        except Exception as e:
            print(e)

    return HttpResponseRedirect('/food/' + str(food.fid))

@login_required(redirect_field_name='home')
def delete_food(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    fid = int(request.GET['fid'])
    food = Food.objects.get(pk=fid)
    children = FoodHier.objects.filter(parent=food).count()
    if children:
        raise Exception('Only leaf nodes can be deleted')
    deleted_food = DeletedFood(fid=fid,name= food.name)
    if 'substitute_food' in request.GET:
        substitute_fid = int(request.GET['substitute_food'])
        deleted_food.substitute = substitute_fid
        description = "Deleted Food: {} with substitute to : {}".format(food.name,Food.objects.filter(fid=substitute_fid).first())
    else:
        substitute_fid = None
        description = "Deleted Food: {} with NO substitute.".format(food.name)
    deleted_food.save()
    UserActivityLog.add_log(request.user, UserActivityLog.CREATE, deleted_food,fid = fid,description=description)
    if substitute_fid is not None:
        UserActivityLog.add_log(request.user, UserActivityLog.CREATE, deleted_food, fid=substitute_fid, description=description)
    qSet = DeletedFood.objects.filter(substitute = fid)
    if qSet.exists():
        ls = []
        for obj in qSet:
            obj.substitute = substitute_fid
            ls.append(obj)
        UserActivityLog.add_logs(request.user,UserActivityLog.UPDATE,ls,fid=substitute_fid)
        for obj in ls:
            obj.save()
    UserActivityLog.add_log(request.user, UserActivityLog.DELETE, food)
    UserActivityLog.prepareToDelete(food)
    #FoodQAttributes.objects.filter(fid=fid).delete()
    food.delete()
    return HttpResponseRedirect('/food/')


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def update_food_name(request):
    logger.debug("pk=%s val=%s", request.POST["pk"], request.POST["value"])
    if FoodNames.objects.filter(name=clean_text(request.POST["value"])).exclude(pk=int(request.POST["pk"])):
        raise Exception('Name is Already in use')
    try:
        # pass
        o = FoodNames.objects.get(pk=int(request.POST["pk"]))
        o.name = clean_text(request.POST["value"])
        UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, o)
        o.save()
    except Exception as e:
        print(e)
    return HttpResponse("")


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def update_food_symbol(request):
    logger.debug("hi %s",request.method)
    logger.debug("pk=%s val=%s", request.POST["pk"], request.POST["value"])
    try:
        # pass
        o = Food.objects.get(pk=int(request.POST["pk"]))
        o.name = clean_symbol(request.POST["value"])
        UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, o,fid = o.fid)
        o.save()
    except Exception as e:
        print(e)
    return HttpResponse("")


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def add_food_name(request):
    logger.debug("hi %s",request.method)
    fid = int(request.POST["fid"])
    lang = request.POST["lang"]
    is_primary = 'is_primary' in request.POST
    is_long = 'is_long' in request.POST
    food_name_id = int(request.POST["food_name_id"])
    if food_name_id == -1:
        name = clean_text(request.POST["name"])
        #if FoodNames.objects.filter(name=name):
        #    raise Exception('Name is Already in use')
        try:
            o = FoodNames(fid=Food.objects.get(pk=fid),
                          lang_code=Lang.objects.get(pk=lang),
                          name=name,
                          is_primary=is_primary,
                          is_long=is_long
                          )
            o.save()
            UserActivityLog.add_log(request.user, UserActivityLog.CREATE, o)
        except Exception as e:
            print(e)
    else:
        f_name = FoodNames.objects.get(pk=food_name_id)
        f_name.lang_code = Lang.objects.get(pk=lang)
        f_name.is_primary = is_primary
        f_name.is_long = is_long
        UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, f_name)
        f_name.save()
    return HttpResponseRedirect("/food/" + request.POST["fid"])


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def delete_food_name(request):
    logger.debug("hi %s",request.method)
    logger.debug("%s",request.GET)
    fid = int(request.GET["fid"])
    pk  = int(request.GET["pk"])
    try:
        o = FoodNames.objects.get(pk=pk)
        UserActivityLog.add_log(request.user, UserActivityLog.DELETE, o)
        o.delete()
    except Exception as e:
        print(e)
        logger.exception()

    return HttpResponseRedirect("/food/" + str(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def change_food_parent(request):
    logger.debug("hi %s %s",request.method, request.POST)

    fid = int(request.POST["fid"])
    is_representative = request.POST.get("is_representative", "") == "on"
    #print is_representative

    if request.POST["parent"]:
        parent = int(request.POST["parent"])
    else:
        parent = None
    try:
        f = Food.objects.get(pk=int(fid))
        f.update_parent(parent, request.user, is_representative)
    except Exception as e:
        print(e)

    return HttpResponseRedirect("/food/" + str(fid) + '/#actions')

@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def change_node_type(request):
    fid = int(request.POST["fid"])
    selected_node_type = request.POST["food_node_type"]
    CHOICES = FoodNodeType.getDic()
    if selected_node_type != '':
        f = Food.objects.get(fid = fid)
        f.node_type = CHOICES[selected_node_type]
        UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, f)
        f.save()
    else:
        print('selected_node_type: ',selected_node_type)
    return HttpResponseRedirect("/food/" + str(fid) + '/#actions')


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def add_secondary_ancestor(request):
    #print "Hi add_secondary_ancestor ", request.method, request.POST
    logger.debug("hi %s %s",request.method, request.POST)

    fid    = int(request.POST["fid"])
    parent = int(request.POST["parent"])


    Food.get(fid).add_secondary_ancestor(parent)
    f = FoodHier.objects.get(fid_id = fid,parent_id=parent)
    UserActivityLog.add_log(request.user, UserActivityLog.CREATE, f,fid =f.fid_id)
    return HttpResponseRedirect("/food/" + str(fid) + '/#actions')

@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def del_secondary_ancestor(request):
    print("Hi del_secondary_ancestor ", request.method, request.POST)

    fid    = int(request.GET["fid"])
    parent = int(request.GET["parent"])

    f = FoodHier.objects.filter(fid = fid, parent= parent).first()
    UserActivityLog.add_log(request.user, UserActivityLog.DELETE, f)
    delete_secondary_ancestor(fid,parent)


    return HttpResponseRedirect("/food/" + str(fid) + '/#actions')





@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def add_food_ref(request):
    fid = int(request.POST["fid"])
    lang = request.POST["lang"]
    reftype = request.POST["reftype"]
    url = request.POST["url"]
    print(fid, lang, reftype, url.encode("utf-8"))
    try:
        o = FoodReferences(fid=Food.objects.get(pk=fid),
                           lang_code=Lang.objects.get(pk=lang),
                           reftype=reftype, url=url)
        o.save()
        UserActivityLog.add_log(request.user, UserActivityLog.CREATE, o)
    except Exception as e:
        print(e)
    return HttpResponseRedirect("/food/" + request.POST["fid"] + "#wiki")

@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def add_or_edit_ref(request):
    if request.method == "POST":
        fid = int(request.POST['fid'])
        usda_id = int(request.POST['usda_id'])
        if usda_id == -1:
            new_usda = UsdaFood(name = request.POST['usda-name'],database = request.POST['usda-db'])
            UserActivityLog.add_log(request.user,UserActivityLog.CREATE,new_usda,fid=fid)
            new_usda.save()
            usda_ed = new_usda
        else:
            usda_ed = UsdaFood.objects.get(pk=usda_id)
            if usda_ed.name != request.POST['usda-name'] or usda_ed.database != request.POST['usda-db']:
                flag = True
            else:
                flag = False
            usda_ed.name = request.POST['usda-name']
            usda_ed.database = request.POST['usda-db']
            if flag:
                UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, usda_ed,fid=fid)
                usda_ed.save()
        if 'add_food_nutrient_ref' in request.POST:
            fnr, created  = FoodNutritionRefs.objects.get_or_create(fid_id = fid,usda=usda_ed)
            if created:
                UserActivityLog.add_log(request.user, UserActivityLog.CREATE, fnr)
                fnr.save()

        ufnList = []
        for nutr_id,amount,unit in zip(request.POST.getlist('nutr_id'),request.POST.getlist('amount'),request.POST.getlist('unit')):
            UFN = UsdaFoodNutrient.objects.filter(usda = usda_ed,nutrient_id=int(nutr_id)).first()
            amount = to_grams(float(amount),unit)
            unit = 'kcal' if unit=='kcal' else 'g'
            if amount == None:
                return HttpResponseRedirect(request.build_absolute_uri())
            if UFN is None:
                UFN = UsdaFoodNutrient(usda = usda_ed,nutrient_id=int(nutr_id), amount=float(amount), unit=unit)
                UserActivityLog.add_log(request.user, UserActivityLog.CREATE, UFN, fid=fid)
            elif float(UFN.amount) != float(amount) or UFN.unit != unit:
                UFN.amount = float(amount)
                UFN.unit = unit
                UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, UFN,fid=fid)
            UFN.save()
            ufnList.append(UFN.pk)
        ufnToDelete = UsdaFoodNutrient.objects.filter(usda =  usda_ed).exclude(pk__in =ufnList)
        if len(ufnToDelete)>0:
            UserActivityLog.add_logs(request.user, UserActivityLog.DELETE, ufnToDelete,fid=fid)
            ufnToDelete.delete()
        return HttpResponseRedirect("/food/"+request.POST['fid']+"/#nutrition")
    else:
        return HttpResponseRedirect(request.build_absolute_uri())

@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def delete_food_ref(request):
    pk = int(request.GET['pk'])
    o = FoodReferences.objects.get(id=pk)
    UserActivityLog.add_log(request.user, UserActivityLog.DELETE, o)
    o.delete()
    return HttpResponseRedirect("/food/" + request.GET["fid"] + "#wiki")


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def flags(request):
    fid = int(request.POST["fid"])
    flag1 = "for_classification" in request.POST
    flag2 = "bad" in request.POST
    flag3 = "is_category" in request.POST

    print(fid, flag1, flag2)
    try:
        f = Food.objects.get(pk=fid)
        f.for_classification = flag1
        f.bad = flag2
        f.is_category = flag3
        UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, f,fid = f.fid)
        f.save()
    except Exception as e:
        print(e)
    return HttpResponseRedirect("/food/" + str(fid)+ "#actions")

@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def repr_flags(request):
    fid = int(request.POST["fid"])
    is_repr = "repr" in request.POST
    print(fid,is_repr)
    qset = FoodHier.objects.filter(fid=fid)
    qset.update(is_representative = is_repr)
    if qset.exists():
        UserActivityLog.add_logs(request.user, UserActivityLog.UPDATE, qset,fid=fid, description="Updated: [is_representative: {0}=>{1}]".format(not is_repr,is_repr))
    # objs = db.execute("update food_hier set is_representative = %s where fid = %s",[is_repr,fid])
    # if len(objs.__dict__['cursor'].fetchall())>0:
    #     UserActivityLog.add_logs(request.user, UserActivityLog.UPDATE, FoodHier.objects.filter(is_representative = is_repr,fid = fid),fid=fid, description="Updated: [is_representative: {0}=>{1}]".format(not is_repr,is_repr))
    return HttpResponseRedirect("/food/" + str(fid)+ "#actions")

@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def add_food_comment(request):
    try:
        fid = int(request.POST["pk"])
        f = Food.objects.get(pk=fid)
        c = FoodComments(fid=f, comment=request.POST["value"].strip())
        c.save()
        UserActivityLog.add_log(request.user, UserActivityLog.CREATE, c,fid=fid)
    except Exception as e:
        print(e)
    return HttpResponseRedirect("/food/" + str(fid) + "#comments")


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def update_food_comment(request):
    try:
        # pass
        id = int(request.POST["pk"])
        o = FoodComments.objects.get(pk=id)
        o.comment = request.POST["value"].strip()
        UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, o)
        o.save()
    except Exception as e:
        print(e)
    return HttpResponse("")


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def delete_food_comment(request):
    fid = int(request.GET["fid"])
    pk = int(request.GET["pk"])
    try:
        o = FoodComments.objects.filter(pk=pk)
        UserActivityLog.add_log(request.user, UserActivityLog.DELETE, o.first(),fid=fid)
        o.delete()
    except Exception as e:
        print(e)


    return HttpResponseRedirect("/food/" + str(fid) + "#comments")


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def move_category(request):
    fid = int(request.POST['fid'])
    ds = request.POST['dataset']
    cat = request.POST['cid']
    cur_fid = request.POST['cur_fid']
    dataset = Datasets.objects.get(pk=ds)
    category = DatasetCategories.objects.get(dataset=dataset, category_id=cat)

    category.update_fid(fid, request.user)
    return HttpResponseRedirect("/food/" + cur_fid)


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def remove_category(request):
    fid = int(request.POST['cur_fid'])
    ds = request.POST['dataset']
    cat = request.POST['cid']
    dataset = Datasets.objects.get(pk=ds)
    category = DatasetCategories.objects.get(dataset=dataset, category_id=cat)

    category.update_fid(None, request.user)
    return HttpResponseRedirect("/food/" + str(fid))


def go_to_food(request):
    if 'fid' not in request.POST:
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/food/' + request.POST['fid'])


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def change_component(request):
    fid = int(request.POST['fid'])
    comp_id = int(request.POST['comp-id'])
    component = int(request.POST['component'])
    amount = float(request.POST['amount'])
    f = Food.objects.get(pk=fid)
    comp = Food.objects.get(pk=component)
    if comp in f.nested_recipes():
        raise CircuitClosedException()
    new_comp = FoodComponents.objects.get(id=comp_id)
    new_comp.component = comp
    new_comp.amount = amount
    UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, new_comp)
    new_comp.save()
    f.update_energy_for_nested()
    return HttpResponseRedirect('/food/{}/?recipe=true'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def remove_component(request):
    fid = int(request.POST['fid'])
    comp_id = int(request.POST['comp-id'])
    new_comp = FoodComponents.objects.get(id=comp_id)
    UserActivityLog.add_log(request.user, UserActivityLog.DELETE, new_comp)
    new_comp.delete()
    f = Food.objects.get(pk=fid)
    f.update_energy_for_nested()
    return HttpResponseRedirect('/food/{}/?recipe=true'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def add_component(request):
    fid = int(request.POST['fid'])
    component = int(request.POST['component'])
    amount = float(request.POST['amount'])
    f = Food.objects.get(pk=fid)
    c = Food.objects.get(pk=component)
    if c in f.nested_recipes():
        raise CircuitClosedException()
    new_comp = FoodComponents(fid=f, component=c, amount=amount)
    UserActivityLog.add_log(request.user, UserActivityLog.CREATE, new_comp)
    new_comp.save()
    f.update_energy_for_nested()    
    return HttpResponseRedirect('/food/{}/?recipe=true'.format(fid))

@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def update_liquid_loss(request):
    fid = int(request.POST['fid'])
    amount = float(request.POST['amount'])

    f = Food.objects.get(pk=fid)
    if (type(amount) is int or type(amount) is float) and amount>=0 and amount<=100:
        f.liquid_loss = amount
        UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, f, fid=f.fid)
        f.save()
    return HttpResponseRedirect('/food/{}/?recipe=true'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def change_ref(request):
    fid = int(request.POST['fid'])
    usda_reference = int(request.POST['usda-name'])
    usda_food = UsdaFood.objects.get(pk=usda_reference)
    f = Food.objects.get(pk=fid)
    new_ref = FoodNutritionRefs(fid=f)
    new_ref.usda = usda_food
    #new_ref.percentage = 100
    new_ref.save()
    f.update_energy_for_nested()
    UserActivityLog.add_log(request.user, UserActivityLog.CREATE, new_ref)
    return HttpResponseRedirect('/food/{}/#nutrition'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def remove_ref(request):
    fid = int(request.GET['fid'])
    usda_id = int(request.GET['refid'])
    o = FoodNutritionRefs.objects.filter(usda_id=usda_id,fid=fid)
    UserActivityLog.add_logs(request.user, UserActivityLog.DELETE, o,fid=fid)
    o.delete()
    f = Food.objects.get(pk=fid)
    f.update_energy_for_nested()
    return HttpResponseRedirect('/food/{}/#nutrition'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def add_all_refs(request):
    fid = int(request.POST['fid'])
    all_refs = request.POST['all_refs']
    action = request.POST['action']
    f = Food.objects.get(pk=fid)
    if action == 'contain':
        refs = refs_contain(all_refs)
    elif action == 'start-with':
        refs = UsdaFood.objects.filter(name__istartswith=all_refs)
    else:
        refs = models.QuerySet()
    refs = refs.exclude(foodnutritionrefs__fid=f)
    new_refs = []
    for ref in refs:
        new_ref = FoodNutritionRefs(fid=f, usda=ref)
        new_refs.append(new_ref)
    FoodNutritionRefs.objects.bulk_create(new_refs)
    f.update_energy_for_nested()
    UserActivityLog.add_logs(request.user, UserActivityLog.CREATE, new_refs)
    return HttpResponseRedirect('/food/{}#nutrition'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def remove_all_refs(request):
    fid = int(request.POST['fid'])
    all_refs = request.POST['all_refs']
    action = request.POST['action']
    f = Food.objects.get(pk=fid)
    if action == 'contain':
        refs = FoodNutritionRefs.objects.filter(fid=f,usda__name__icontains=all_refs)
    elif action == 'start-with':
        refs = FoodNutritionRefs.objects.filter(fid=f, usda__name__istartswith=all_refs)
    else:
        refs = models.QuerySet()
    UserActivityLog.add_logs(request.user, UserActivityLog.DELETE, refs)
    refs.delete()

    if action == 'contain':
        refs = FoodNutritionRefs.objects.filter(fid=f,usda__description__long_description__icontains=all_refs)
    elif action == 'start-with':
        refs = FoodNutritionRefs.objects.filter(fid=f, usda__description__long_description__istartswith=all_refs)
    UserActivityLog.add_logs(request.user, UserActivityLog.DELETE, refs)
    refs.delete()
    f.update_energy_for_nested()
    
    return HttpResponseRedirect('/food/{}#nutrition'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def change_weight(request):
    q_id = int(request.POST['q_id'])
    fid = int(request.POST['fid'])
    weight = float(request.POST['weight'])
    quantity_type = int(request.POST['quantity_type'])
    f = Food.objects.get(pk=fid)
    try:
        action = UserActivityLog.UPDATE
        new_weight = FoodUnits.objects.get(pk=q_id)
    except:
        action = UserActivityLog.CREATE
        new_weight = FoodUnits(fid=f)
    new_weight.unit_id = quantity_type
    new_weight.weight = weight
    UserActivityLog.add_log(request.user, action, new_weight)
    new_weight.save()
    return HttpResponseRedirect('/food/{}/#units'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def change_default_unit(request):
    unit = Units.objects.get(pk=request.POST['unit'])
    f = Food.objects.get(pk=request.POST['food'])
    amount = float(request.POST['amount'])
    obj = FoodDefaultUnit.objects.filter(fid=f).first()
    if obj is None:
        obj = FoodDefaultUnit(fid=f, unit = unit, amount= amount)
        action = UserActivityLog.CREATE
    else:
        obj.unit = unit
        obj.amount = amount
        action = UserActivityLog.UPDATE
    UserActivityLog.add_log(request.user, action, obj)
    obj.save()
    return HttpResponseRedirect('/food/{}/#units'.format(f.fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def remove_weight(request):
    q_id = int(request.GET['q_id'])
    fid = int(request.GET['fid'])
    o = FoodUnits.objects.get(pk=q_id)
    UserActivityLog.add_log(request.user, UserActivityLog.DELETE, o)
    o.delete()
    return HttpResponseRedirect('/food/{}/#units'.format(fid))

@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def remove_is_countable(request):
    fid = int(request.GET['fid'])
    f = Food.objects.filter(fid=fid).first()
    f.is_countable = None
    UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, f,fid = f.fid)
    f.save()
    return HttpResponseRedirect('/food/{}/#units'.format(fid))

@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def change_is_countable(request):
    fid = int(request.POST["fid"])
    is_repr = "for_classification" in request.POST
    print(fid, is_repr)
    objs = db.execute("update food set is_countable = %s where fid = %s", [is_repr, fid])
    if len(objs.__dict__['cursor'].fetchall()) > 0:
        UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, Food.objects.get(pk=fid), fid=fid,
                                description="Updated: [is_countable: {0}=>{1}]".format(not is_repr,is_repr))
    return HttpResponseRedirect('/food/{}/#units'.format(fid))

@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def remove_default_unit(request):
    fid = int(request.GET['fid'])
    fs = FoodDefaultUnit.objects.filter(fid = fid)
    UserActivityLog.add_logs(request.user, UserActivityLog.DELETE, fs, fid=fid)
    fs.delete()
    return HttpResponseRedirect('/food/{}/#units'.format(fid))

@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def change_cn(request):
    c_id = int(request.POST['c_id'])
    fid = int(request.POST['fid'])
    amount = float(request.POST['amount'])
    unit = request.POST['unit']
    if unit == 'mg':
        amount *= 1e-3
        unit = 'g'
    elif unit == 'mcg':
        amount *= 1e-6
        unit = 'g'
    nutrient_id = int(request.POST.get('nutrient', 0))

    f = Food.objects.get(pk=fid)
    try:
        action = UserActivityLog.UPDATE
        new_weight = UsdaFoodNutrient.objects.get(pk=c_id)
    except:
        action = UserActivityLog.CREATE
        usda, created = UsdaFood.objects.get_or_create(name=f.name, database=settings.CUSTOM_DATA_DB)
        if created:
            usda.save()
            UserActivityLog.add_log(request.user, UserActivityLog.CREATE, usda,fid=fid)
        ref, created = FoodNutritionRefs.objects.get_or_create(fid=f, usda=usda)
        if created:
            ref.save()
            UserActivityLog.add_log(request.user, UserActivityLog.CREATE, ref,fid=fid)
        new_weight = UsdaFoodNutrient(usda=usda, amount=amount, unit=unit, nutrient_id=nutrient_id)
    new_weight.amount = amount
    if new_weight.nutrient.name == "energy":
        unit = 'kcal'
    new_weight.unit = unit
    UserActivityLog.add_log(request.user, action, new_weight,fid=fid)
    new_weight.save()
    f.update_energy_for_nested()
    
    return HttpResponseRedirect('/food/{}/#custom_data'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def remove_cn(request):
    c_id = int(request.GET['c_id'])
    fid = int(request.GET['fid'])
    o = UsdaFoodNutrient.objects.get(pk=c_id)
    UserActivityLog.add_log(request.user, UserActivityLog.DELETE, o,fid=fid)
    o.delete()
    f = Food.objects.get(pk=fid)
    f.update_energy_for_nested()
    
    return HttpResponseRedirect('/food/{}/#custom_data'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def change_food_attribute(request):
    fid = int(request.POST['fid'])
    attribute_id = request.POST['attribute']
    attr = Attribute.objects.get(pk=attribute_id)
    f_atr_id = int(request.POST.get('f_atr_id'))
    if f_atr_id != -1:
        food_attribute = FoodAttributes.objects.get(pk=f_atr_id)
        food_attribute.attribute = attr
        UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, food_attribute)
        food_attribute.save()
    else:
        f = Food.objects.get(pk=fid)
        food_attribute = FoodAttributes(fid=f, attr=attr)
        food_attribute.save()
        UserActivityLog.add_log(request.user, UserActivityLog.CREATE, food_attribute)

    page = request.POST.get('page', 'attributes')
    return HttpResponseRedirect('/food/%d/#%s' % (fid,page))
    #return HttpResponseRedirect('/food/{}/#attributes'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def remove_food_attribute(request):
    f_atr_id = int(request.GET['f_atr_id'])
    fid = int(request.GET['fid'])
    o = FoodAttributes.objects.get(pk=f_atr_id)
    UserActivityLog.add_log(request.user, UserActivityLog.DELETE, o)
    o.delete()
    page = request.GET.get('page', 'attributes')
    return HttpResponseRedirect('/food/%d/#%s' % (fid,page))


def ref_list(request):
    return HttpResponse(get_usda_names(request.GET['q']))


def food_list(request):
    text = clean_text(request.GET['q'])
    return HttpResponse(get_foods_for_moving_dataset(text))

def user_list(request):
    text = clean_text(request.GET['q'])
    return HttpResponse(json.dumps(users_for(text)))

def search_usda(request):
    text = request.GET['usda']
    dataHTML ='<a href="javascript:;" onclick="this.parentNode.classList.remove('+"'show'"+""');"><strong>just select:</strong>{text}</a>'.format(text=text)
    dataHTML += '<a usda-name="{name}" usda-database="{database}" usda-id="{id}" href="javascript:;" onclick="selectUsda(this);"><strong>create new:</strong>{text}</a>'.format(
        name=text, database="food_labels", id="-1", text=text
    )
    if len(text)>=3:
        data = []
        #qSet = refs_description_contain(text)
        #qSet = qSet.filter(usda_food__database="food_labels")
        #qSet = qSet.select_related()
        #data += [{'id': u.usda_food.usda_id, 'text': '{u.long_description} [{u.group_description}] ({u.usda_food.database})'.format(u=u),
        #         'name':u.usda_food.name, 'database':u.usda_food.database}
        #       for u in qSet]
        #described_ids = set([item['id'] for item in data])
        qSet = refs_contain(text)
        qSet = qSet.filter(database='food_labels')
        for u in qSet:
            #if u.usda_id in described_ids:
            #   continue
            #dataHTML = ""
            data.append({'id': u.usda_id, 'text': '{u.name} ({u.database})'.format(u=u),
                         'name': u.name, 'database':u.database})
        for ref in data:
            dataHTML += '<a usda-name="{name}" usda-database="{database}" usda-id="{id}" href="javascript:;" onclick="selectUsda(this);">{text}</a>'.format(
                name=ref['name'], database=ref['database'],id=ref['id'],text=ref['text']
            );
    return JsonResponse({'dataHTML':dataHTML},safe=False)

def get_nutrient(request):
    usda_id = request.GET['usda_id']
    qSet = UsdaFoodNutrient.objects.filter(usda_id = usda_id).select_related()
    dataHTML = ''
    for nut in qSet:
        nextHTML = '<tr><td><button type="button" onclick="remove_parent(this.parentNode)"><img src="/static/food/icons/delete.png" height="15" width="15"></button></td>' \
                   '<td><select name="nutr_id" class="nutrients-select2" required><option value="{u.nutrient.id}">{u.nutrient.name}</option></select></td>' \
                   '<td><input type="number" name="amount" min="0" step=any style="width:auto;" value="{u.amount}" required></td>' \
                   '<td><select name="unit" class="unit-nutrients-select2" required><option value="{u.unit}">{u.unit}</option></select></td></tr>'
        nextHTML = nextHTML.format(u=nut)
        dataHTML += nextHTML
    return JsonResponse({'dataHTML': dataHTML}, safe=False)


def grams_by_unit(request):
    fid = request.GET['fid']
    unit = request.GET['unit']
    amount = float(request.GET['amount'])
    data = food_units_with_gram(fid)
    grams = 0
    for db_result in data:
        if str(unit) == str(db_result["unit_id"]) or unit == db_result["quantity_name"]:
            grams = int(db_result["weight"])
            break
    else:
        quantity_types = Units.objects.get(pk=unit)
        grams = quantity_types.gram_factor
    final_number = amount * int(grams)
    return HttpResponse(final_number)

def get_units_view(request):
    fid = request.GET['fid']
    data = food_units_with_gram(fid)
    lsUnits = [un['quantity_name'] for un in data]
    return JsonResponse({'lsUnits':lsUnits})


def parent_list(request, fid):
    fid = int(fid) if fid is not None else None
    text = clean_text(request.GET['q'])
    food = Food.objects.get(pk=fid)
    return HttpResponse(get_foods_for_parent_select(food, text))


def component_list(request, fid):
    fid = int(fid) if fid is not None else None
    food = Food.objects.get(pk=fid)
    text = request.GET.get("q","")

    return HttpResponse(get_foods_for_components(food, text))


def unit_list(request):
    text = request.GET.get('q', '')

    return JsonResponse(get_units(text), safe=False, json_dumps_params={'ensure_ascii': False})

def unit_list_with_no_gram(request):
    text = request.GET.get('q', '')
    dic = [obj for obj in get_units(text) if obj['id'] not in ['2','173']]
    return JsonResponse(dic, safe=False, json_dumps_params={'ensure_ascii': False})


def nutrient_list(request):
    text = request.GET.get('q', '')
    return JsonResponse(get_nutrients(text), safe=False, json_dumps_params={'ensure_ascii': False})

def attribute_list(request):
    text = request.GET.get('q', '')
    return JsonResponse(get_attributes(text), safe=False, json_dumps_params={'ensure_ascii': False})

def database_list(request):
    text = request.GET.get('q', '')
    return JsonResponse(get_database(text), safe=False, json_dumps_params={'ensure_ascii': False})

def node_type_list(request):
    text = request.GET.get('q', '')
    return JsonResponse(get_node_type(text), safe=False, json_dumps_params={'ensure_ascii': False})

def get_all_names_with_replaces():
    '''
    foreach name in FoodNames.all() and foreach key in replaceArr {name.repalece(key,""):fid}
    :return: {name:fid, ..}
    '''
    replaceArr = ["׳", "ʹ", "ʼ", "ʽ", "ʾ", "ʿ", "ˈ", "ˊ", "ˋ", "ʻ", "    ʼ", "˴", "˹", "˺", "΄", " ҅", " ҆", "‹", "›", "’", "'"]
    dic = FoodNames.all()
    return { key.replace(sub,""):value
             for key, value in dic.items()
             for sub in replaceArr}

def nlp_json(request):
    data = {'adding_words': GrammarAddingWord.all(),
            'measure_words': GrammarMeasureWord.all_measures(),
            'adjectives': GrammarMeasureWord.all_adjactives(),
            'intent_words': GrammerIntentWord.all(),
            'quantity_type_names': Units.all_names(),
            'quantity_types': Units.names(),
            'food_names'  : get_all_names_with_replaces(),
            'food_units'  : FoodUnits.all_inhereted(),
            'gram_factors': Units.gram_factors(),
            'category'    : [f.fid for f in Food.objects.filter(is_category=True)],
            'default_units' : default_units_data(),
            'food_is_countable' : Food.all_is_countable_inhereted(),
            'food_hierarchy': FoodHier.get_dic_FoodHier()
            }

    # m = FoodUnits.all()
    # print "="*80
    # # for k in m:
    # #     print k.encode("utf-8")
    # print m
    # print "="*80

    if request.GET.get("format",None) == "json":
        return JsonResponse(data)

    pkl = pickle.dumps(data)
    return HttpResponse(pkl, content_type='application/pkl')



def fast_view(request, fid):
    filter_db  =  request.GET.get("db",None)
    fid = int(fid) if fid is not None else None
    f = Foods(fid,trim=False)
    datasets = [food.datasets(filter_db) for food in f.obj_sorted]
    uniq_dataset_names = set([x.dataset.name for ds in datasets for x in ds])

    # uniq_dataset_names = set()
    # for ds in datasets:
    #     print(ds)
    #     for x in ds:
    #         uniq_dataset_names.add(x.dataset.name)


    r = render(request, 'fast_view.html', {'list': list(zip(f.obj_sorted, datasets)),
                                           'images_host': get_images_host_by_request(request),
                                           'uniq_dataset_names' : uniq_dataset_names,
                                           'filter_db' : filter_db,
                                       })
    return r


def dataset_view(request, dataset_name):
    datasets = DatasetCategories.objects.filter(dataset__name=dataset_name).select_related('fid')
    foods = [d.fid for d in datasets]
    datasets = [[d] for d in datasets]
    r = render(request, 'fast_view.html', {'list': list(zip(foods, datasets)),
                                           'images_host': get_images_host_by_request(request)})
    return r


def food_names(request):
    lang_code = request.GET.get('lang', None)
    test_ts = int(request.GET.get('timestamp', 0))

    #print("In names: lang {0} ts {1}".format(lang_code, test_ts))
    if test_ts and NamedTimestamp.is_uptodate(FOOD_NAMES_CHANGED_TIMESTAMP, test_ts):
        return HttpResponse("", status=304)

    if not lang_code:
        lang_code = '%'
    sql = 'select food_names.name, fid from food_names join food using(fid) where not bad and lang_code ilike %s'


    #q = FoodNames.objects.raw(sql, [lang_code])
    # q = FoodNames.objects.all()
    # if lang_code:
    #     try:
    #         lang = Lang.objects.get(pk=lang_code)
    #     except Lang.DoesNotExist:
    #         return JsonResponse({'error': 'Lang {0} not supported'.format(lang_code)}, status=400)
    #     q = q.filter(lang_code=lang)
    # q = q.order_by('name')

    # names = [{'label': o.name, 'value': o.fid.fid} for o in q]
    names = db.select_lambda(sql, lambda r: {'label': r[0], 'value': r[1]}, [lang_code])
    return JsonResponse({'names': list(names)})


def food_info_list(request):
    lang_code = request.GET.get('lang', None)
    test_ts = int(request.GET.get('timestamp', 0))
    units_list = request.GET.getlist('units', [])
    include_bad =  request.GET.get('include_bad', False)
    exclude_list = request.GET.getlist('exclude_list', [])

    print (units_list)

    # check the timestamp on FOOD_UNITS_CHANGED_TIMESTAMP as well as FOOD_NAMES_CHANGED_TIMESTAMP
    if test_ts and NamedTimestamp.is_uptodate(FOOD_NAMES_CHANGED_TIMESTAMP, test_ts) \
            and NamedTimestamp.is_uptodate(FOOD_UNITS_CHANGED_TIMESTAMP, test_ts):
        return HttpResponse("", status=304)

    if not lang_code:
        lang_code = '%'
    sql = 'WITH units_inhereted AS ( \
                     select H.fid as fid, unit_id, weight, ROW_NUMBER() OVER( PARTITION BY H.fid, unit_id ORDER BY H.rank) as inh_rank \
                     from food_predecessor_rank as H join food_units as U on (U.fid=H.parent) \
                   ) \
                 select food.name, food_names.name, fid, name_en, unit_id from food_names join food using(fid) left join units_inhereted using(fid) left join units using(unit_id)  where not bad and lang_code ilike %s and fid NOT IN %s'
    if include_bad is not False:
        sql = sql.replace('not bad and','')
    full_list = []
    exclude_fids = [0] #must have at least one fid (even fake) for sql tuple()
    if exclude_list:
        exclude_roots = Food.objects.filter(name__in = exclude_list).values_list('fid',flat=True)
        hier = getRelation()
        for ex_fid in exclude_roots:
            exclude_fids.extend(hier[ex_fid])
            exclude_fids.append(ex_fid)

    name_list = []
    unit_id_list = []
    current_fid = -1
    for food_name,name, fid, name_en, unit_id in db.execute(sql, [lang_code,tuple(exclude_fids)]):
        if not current_fid == fid:
            if current_fid > -1:
                # here we finished one fid and start another
                entry = {}
                entry['food_id'] = current_fid
                entry['labels'] = name_list
                entry['food_name']=name_of_next_fid
                entry['units'] = unit_id_list
                full_list.append(entry)
                name_list = []
                unit_id_list = []
            current_fid = fid
            name_of_next_fid = food_name

        # here we only append if the values are not in there already
        if not (name in name_list):
            name_list.append(name)

        if name_en is not None and name_en in units_list \
                and unit_id is not None and not unit_id in unit_id_list :
            unit_id_list.append(unit_id)

    return JsonResponse({'foods': full_list})


def food_names_lookup(request):
    lang_code = request.GET.get('lang', None)
    term = request.GET['term']

    if not lang_code:
        lang_code = '%'
    sql   = 'select food_names.* from food_names join food using(fid) where not bad and food_names.name ilike %s  and lang_code ilike %s order by food_names.name'
    term_sql = '%' + term + '%'
    names_q = FoodNames.objects.raw(sql, [term_sql,lang_code])
    names = [{'label': o.name, 'value': o.fid.fid} for o in names_q]
    return JsonResponse(names, safe=False)


def get_all_billfare_info(request):
    lang = request.META.get('HTTP_LANGUAGE', 'en')
    data = [{'synonyms': [n.name for n in f.synonims.filter(lang_code=lang)],
             'id': f.fid,
             'kcal': f.energy}
            for f in Food.objects.all()]
    return JsonResponse(data, safe=False)


def billfare_info(request):
    def get_chinese_food(name):
        f = Food.objects.filter(name=name).first()
        if f:
            return f
        f = Food.objects.filter(synonims__name=name, hier__parent__name__startswith='chinese_').first()
        if f:
            return f
        return Food.objects.filter(synonims__name=name).first()
    names = [x['billfareName'] for x in json.loads(request.body)]
    foods =list(map(get_chinese_food, names))
    data = [{'id': f.fid if f else None, 'billfareName': n.replace('_', ' ')} for f, n in zip(foods, names)]
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


def nutrition_element_info(request):
    short_names = {'total_carbohydrate': 'carbs', 'saturated_fat': 'satur_fat', 'riboflavin-b2': 'vitamin_b2',
                   'glycemic_index': 'GI'}

    lang = request.META.get('HTTP_LANGUAGE', 'en')
    print(lang)

    def short_name(x):
        n = short_names[x] if x in short_names else x
        if n.startswith('total'):
            n = n[6:]
        if n == x and len(x) > 10:
            if 'omega-3' in x:
                n = '\u03a93 ' + x[:3].upper()
        n = n[0].upper() + n[1:]
        return n.replace('_', ' ').replace('-', ' ')

    json_foods = json.loads(request.body)
    nutrients = {x.name: [0, 'g'] for x in UsdaNutrient.objects.all()}
    names = get_names_for_china(lang)
    for f in json_foods:
        food = Food.objects.get(pk=int(f['id']))
        amount = float(f['weight'])
        quantity_type_name = f['quantity_type'] if 'quantity_type' in f else 'gram'
        quantity_type = Units.objects.filter(name_en__icontains=quantity_type_name).first()
        weight = calc_weight(food, amount, quantity_type)
        for n, v in food.nutrition_facts().items():
            nutrients[n][0] += v[0] * weight / 100
            nutrients[n][1] = v[1]

    nutrients = {k: normalize_unit(*v) for k, v in nutrients.items()}

    nutrients_data = {n.name: n for n in UsdaNutrient.objects.all()}
    ret = [{'alias': short_name(n), 'name': names[n] or n, 'id': nutrients_data[n].id,
            'value': nutrients[n][0], 'unit': nutrients[n][1],
            'referenceValue': normalize_grams_to_unit(nutrients_data[n].reference_value, nutrients[n][1])}
           for n in nutrients]
    return JsonResponse(ret, safe=False)


def food_info(request):
    test_ts = int(request.GET.get('timestamp', 0))

    if test_ts and NamedTimestamp.is_uptodate(FOOD_NAMES_CHANGED_TIMESTAMP, test_ts):
        return HttpResponse("", status=304)

    fn_list = FoodNames.objects.all().select_related('fid', 'lang_code')
    ret = {}
    for fn in fn_list:
        if fn.lang_code.code not in ret:
            ret[fn.lang_code.code] = []
        ret[fn.lang_code.code].append([fn.name, fn.fid.fid])
    return JsonResponse(ret)


def food_nutrients(request):
    food_name = request.GET.get('name', '').lower()
    if not food_name:
        return HttpResponseBadRequest()
    if re.findall(r'\d+(?:\.\d+)?\%', food_name, re.I | re.U):
        print('MATCH')
        regex = '^' + re.sub(r'\d+(?:\.\d+)?\%', r'\d+(?:\.\d+)?\%', food_name) + '$'
        items = FoodNames.objects.filter(name__regex=regex).select_related('fid')
        num_regex = regex.replace(r'\d+(?:\.\d+)?', r'(\d+(?:\.\d+)?)')
        interp_num = int(re.findall(num_regex, food_name)[0])
        nutrients = defaultdict(lambda: {})
        metadata = {}
        for item in items:
            item_x = int(re.findall(num_regex, item.name)[0])
            for nutrient, amount in item.fid.nutrition_facts().items():
                nutrients[nutrient][item_x] = amount[0]
                if nutrient not in metadata:
                    metadata[nutrient] = [amount[1], 0]
        return JsonResponse({k: [np.interp(interp_num, v.keys(), v.values())] + metadata[k]
                             for k, v in nutrients.items()})

    try:
        symbol = food_name.replace(' ', '_')
        food_item = Food.objects.filter(Q(synonims__name=food_name)|Q(name=symbol)).first()
        return JsonResponse(food_item.nutrition_facts())
    except:
        return HttpResponseBadRequest('No matching Name')


def food_nutrition(request, fid):
    """
    Returns the nutritional values of fid with given attributes for 100 grams.
    :param request: A request with a list of attributes ids.
    :param fid: the id of the requested food.
    :return: Json response with the nutritional values.
    """

    try:
        f = Food.get(fid=fid)
    except Food.DoesNotExist:
        return HttpResponseNotFound('No matching fid')
    try:
        attributes = [Attribute.objects.get(pk=a) for a in request.GET.getlist('attributes')]
    except Attribute.DoesNotExist:
        attributes = []
    nutrients = f.nutrition_facts(attribute_requirements=attributes)
    nutrients = {key: {'value': nutrients[key][0], 'units': nutrients[key][1]} for key in nutrients}
    return JsonResponse(nutrients)


def food_descendants_by_attributes(request, fid):
    """
    Returns the  of fid with given attributes.
    :param request: A request with a list of attributes ids.
    :param fid: the id of the requested food.
    :return: Json response with the list of descendant food ids that match at least one of the attributes.
    """

    try:
        f = Food.objects.get(pk=fid)
    except Food.DoesNotExist:
        return HttpResponseNotFound('No matching fid')
    try:
        attributes = [Attribute.objects.get(pk=a) for a in request.GET.getlist('attributes')]
    except Attribute.DoesNotExist:
        attributes = []
    food_descendants, exclusion_happened = get_descendants_by_attributes_and_food(f.fid,attribute_requirements=attributes,get_exclusion=True)
    ret = {'descendants': [f for f in food_descendants], 'exclusion_happened':exclusion_happened}
    return JsonResponse(ret)

def food_descendants_by_attributes_any(request, fid):
    """
    Returns the list of fid with given attributes.
    :param request: A request with a list of attributes ids.
    :param fid: the id of the requested food.
    :return: list of descendant food ids that match at least one of the attributes.
    """
    try:
        f = Food.objects.get(pk=fid)
    except Food.DoesNotExist:
        return HttpResponseNotFound('No matching fid')
    try:
        attributes = []
        ls = request.GET.getlist('attributes')
        for obj in ls:
            attributes.append(int(obj))
    except Attribute.DoesNotExist:
        attributes = []
    ls = get_descendants_by_attributes_and_food(f.fid,attribute_requirements=attributes)
    return JsonResponse(ls)



def food_weight(request):
    food_name = request.GET.get('name')
    if food_name is None:
        return HttpResponseBadRequest()

    try:
        food_item = Food.objects.filter(synonims__name=food_name.lower()).first()
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('No matching name')

    fid = food_item.fid
    units = food_units(fid)

    unit = request.GET.get('unit')
    if unit is None:
        data = {u["quantity_name"]: u["weight"] for u in units}
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})

    data = [u["weight"] for u in units if u["quantity_name"] == unit]
    if len(data) > 0:
        return JsonResponse({'weight': data[0]})

    quantity_type = Units.objects.filter(Units.query_name(unit)).first()
    if not quantity_type:
        return HttpResponseBadRequest('No matching unit')
    return JsonResponse({'weight': quantity_type.gram_factor})


def food_questions(request):
    fid = request.GET.get('fid')
    if not fid:
        return HttpResponseBadRequest('Must supply valid fid')

    try:
        food = Food.get(fid=fid)
    except Food.DoesNotExist:
        return HttpResponseBadRequest('Must supply valid fid')

    questions = food.get_questions()
    media = request.GET.get('media')
    lang = request.GET.get('lang', 'en')
    return JsonResponse({
        'questions': [q.to_dict(lang) for q in questions if q.should_ask(media=media)]
    })


def get_foods(request):
    food_name = request.GET.get('name', '')
    fid = request.GET.get('fid')
    normalize = request.GET.get('normalize', 'true').lower() == 'true'

    def gather_data(food_item):
        synonyms = [{'lang:': n.lang_code.lang, 'name': n.name, 'primary': n.is_primary, 'lang_code': n.lang_code_id}
                    for n in food_item.synonims.all().select_related('lang_code')]
        allnames = db.select_as_dict('select lang_code,name from food_names where fid=%s', [food_item.fid])
        allnames.update(db.select_as_dict('select lang_code,name from food_names where fid=%s and is_primary', [food_item.fid]))

        ## If chineese name is absent, try to use parent's chineese name
        if 'cn' not in allnames:
            parent_cn = db.select_as_value("""select name from food_names
                                                          join food_hier on (food_names.fid = food_hier.parent)
                                                 where food_hier.fid=%s and lang_code='cn'
                                                 order by food_names.is_primary desc""",[food_item.fid])
            if parent_cn:
                allnames['cn'] = parent_cn

        weights = [{'unit': f["quantity_name"], 'weight':f["weight"]} for f in food_units(food_item.fid)]
        default_unit = food_item.get_default_unit()

        body = {
            'id': food_item.fid,
            'name': food_item.name,
            'synonyms': synonyms,
            'allnames': allnames,
            'weights': weights,
            'default_unit': (default_unit.unit.name,float(default_unit.amount)),
        }

        try:
            attributes = [Attribute.objects.get(pk=a) for a in request.GET.getlist('attributes')]
        except Attribute.DoesNotExist:
            attributes = []

        if normalize:
            nutrients = food_item.show_facts(attribute_requirements=attributes)
            body['nutrients'] = {k: {'value': v[0], 'units': v[1]} for k, v, id in nutrients}
        else:
            nutrients = food_item.nutrition_facts(attribute_requirements=attributes)
            body['nutrients'] = {key: {'value': nutrients[key][0], 'units': nutrients[key][1]} for key in nutrients}

        return body

    try:
        if fid is not None:
            try:
                item = Food.get(fid)
                return JsonResponse(gather_data(item), json_dumps_params={'ensure_ascii': False})
            except Food.DoesNotExist:
                return HttpResponseNotFound('<h1>No matching fid</h1>')
        elif food_name:
            food_name = food_name.lower()
            food_name = re.sub("[ _]+"," ",food_name)
            symbol = food_name.replace(' ', '_')
            item = Food.objects.filter(Q(synonims__name__iexact=food_name) | Q(name=symbol)).first()
            if item is None:
                return HttpResponseBadRequest('No matching food item')
            return JsonResponse(gather_data(item), json_dumps_params={'ensure_ascii': False})
    except ObjectDoesNotExist:
        return HttpResponseBadRequest('No matching food item')


def food_hier(request):
    def hier(f):
        return hier(f.parent()) + [[f.fid, f.name]] if f.parent() else [[f.fid, f.name]]

    food_name = request.GET.get('name')
    fid = int(request.GET.get('fid')) if 'fid' in request.GET else None
    try:
        if fid is not None:
            item = Food.get(fid=fid)
        elif food_name is not None:
            item = Food.objects.filter(synonims__name=food_name.lower()).first()
            if item is None:
                return HttpResponseBadRequest('No matching food item')
        else:
            return HttpResponseBadRequest('No matching food item')
        return JsonResponse(hier(item), json_dumps_params={'ensure_ascii': False}, safe=False)
    except (ObjectDoesNotExist, Food.DoesNotExist) as e:
        return HttpResponseBadRequest('No matching food item')


def descendants(request):
    fid = int(request.GET.get('fid'))
    print(fid)
    try:
        if fid is not None:
            foods = Foods(fid, trim=False)
        else:
            return HttpResponseBadRequest()
        resp = []
        for food in foods.obj_sorted:
            names = {}
            for lang in ['en', 'he', 'cn']:
                for name, primary in zip(food.names(lang), food._primary[lang]):
                    if primary or lang not in names:
                        names[lang] = name
            resp.append(names)
        return JsonResponse(resp, json_dumps_params={'ensure_ascii': False}, safe=False)

    except SyntaxError:
        return HttpResponseBadRequest('No matching food item')


# def foods_from_free_text(request):
#     text = request.GET['text']
#     return JsonResponse(parse_free_text(text), safe=False, json_dumps_params={'ensure_ascii': False})


def edit_analysis(analysis, media, lang='en'):
    logger.info("edit_analysis input=%s",analysis)
    food_item = FoodItem.from_dict(analysis)
    all_items = food_item.flatten()
    return [item.to_json(media, lang) for item in all_items]


def analyze_food(request):
    logger.debug("hello!!!")
    lang = request.POST.get('lang', 'en')

    for filename, uploaded_file in request.FILES.items():
        if filename == 'image':
            print('analyzing image...')
            image_analyzer = ImageAnalyzer()
            image_analysis = image_analyzer.analyze(uploaded_file, metadata=request.POST)
            final_analysis = []
            for item in image_analysis:
                final_analysis.extend(edit_analysis(item, Question.IMAGE, lang))
            return JsonResponse({'foods': final_analysis})

    text = request.POST.get('text',request.GET.get('text'))
    tz = request.POST.get('tz')
    input_time = request.POST.get('input_time')
    if text:
        logger.info("nlp.analyze=%s",text)
        res = nlp.analyze(text, tz=tz, input_time=input_time)
        logger.info("NLP result: %s",res)
        if not res:
            return HttpResponseBadRequest()
        try:
            items = []
            for item in res['items']:
                if item['type'] == 'food':
                    items.extend(edit_analysis(item, Question.TEXT, lang))
                else:
                    items.append(item)
            for item in items:
                item['is_category'] = False
            
            logger.info("NLP JSON: %s", items)
            metadata = res.get("metadata", None)
            return JsonResponse({'items': items, 'metadata': metadata})
        except KeyError:
            return JsonResponse(res)

    return HttpResponseBadRequest()

def foods_csv(request):
    foods = Foods(trim=False).obj_sorted
    max_level = max(food.level() for food in foods)
    titles = CsvUtils.get_csv_titles(max_level)
    row_values = [CsvUtils.get_csv_field_values(food, max_level) for food in foods]
    csv = CsvUtils.create_csv(row_values, titles)
    response = HttpResponse(csv, content_type='application/force-download')
    response['content-disposition'] = 'attachment; filename=foods_hierarchy.csv'
    return response

def foods_csv_serving(request):
    fids_to_not_include = db.select_as_set(
        "select fid from food_attributes join food_attribute on (food_attributes.attr_id = food_attribute.id) where value in ('chinese_dishes', 'Tzameret')")
    csv = CsvUtils.create_csv_with_units(fids_set_to_exclude=fids_to_not_include)
    response = HttpResponse(csv, content_type='application/force-download')
    response['content-disposition'] = 'attachment; filename=foods_serving_size.csv'
    return response

def foods_csv_classification(request):

    for_classification = db.select_as_dict("select fid, for_classification from food")
    images_num = db.select_as_dict("select parent, sum(cnt) as i  from food_predecessor_rank join dataset_categories using(fid) group by parent having sum(cnt)>0")
    rep_num = db.select_as_dict("select parent, sum(cnt) as i  from food_predecessor_rank join tmp_food_stat using(fid) group by parent having sum(cnt)>0")

    def _for_classification(fid):
        if for_classification[fid]:
            return "V"
        return ""


    sorted_hier_sql = '''
         WITH RECURSIVE food_hh(fid,xname,lev,name) as (
              select fid,name::text,1,name from food where fid not in (select fid from food_hier)

           UNION ALL
              select nxt.fid, cur.xname || 'AAA' || food.name ::varchar,  cur.lev + 1, food.name
                from   food_hh cur, food_hier nxt, food
                where cur.fid = nxt.parent and food.fid = nxt.fid
         )
         SELECT fid, name, lev,xname from food_hh  order by xname

    '''


    csv = ""
    line = ",".join(["fid","Food"] + [""] * 8)
    csv += line  + "\n"
    for fid,name,lev,xname in db.execute(sorted_hier_sql):

        if not for_classification[fid] and images_num.get(fid,0) < 50 and rep_num.get(fid,0) < 2:
            continue

        line_data = [""] * (lev - 1) + [name] + [""]*(8-lev)
        line_data.append(str(images_num.get(fid,0)))
        line_data.append(str(rep_num.get(fid,0)))
        line_data.append(_for_classification(fid))
        line = ",".join(line_data)
        csv += line  + "\n"


    response = HttpResponse(csv, content_type='application/force-download')
    response['content-disposition'] = 'attachment; filename=foods.csv'
    return response


def chinese_csv(request):
    chinese_name = db.select_as_dict("select fid,name from food_names where lang_code='cn' order by is_primary,id desc")

    def _chinese_name(x):
        if x in chinese_name:
            return chinese_name[x]
        return ""

    eng_name = db.select_as_dict("select fid,name from food_names where lang_code='en' order by is_primary,id desc")

    def _eng_name(x,y):
        if x in eng_name:
            return eng_name[x]
        return y

    cls = db.select_as_dict('select fid, for_classification from food')
    def _cls(x):
        if cls[x]:
            return "Yes"
        else:
            return "No"


    sorted_hier_sql = '''
         WITH RECURSIVE food_hh(fid,xname,lev) as (
              select fid,name::text,1,name from food where fid not in (select fid from food_hier)
           UNION ALL
              select nxt.fid, cur.xname || 'AAA' || food.name ::varchar,  cur.lev + 1,food.name
                from   food_hh cur, food_hier nxt, food
                where cur.fid = nxt.parent and food.fid = nxt.fid and lower(food.name) not like 'tzameret%'
         )
         SELECT fid,name,lev from food_hh
         where fid not in (select fid from food_attributes where attribute='chinese_dishes' or attribute='Tzameret')
         order by xname
    '''


    csv = ""
    line = ",".join(["English Name"] + [""] * 8 + ["Is Used For Classification"])
    csv += line  + "\n"
    for fid,name,lev in db.execute(sorted_hier_sql):
        line = ",".join(list(map(str,[_eng_name(fid,name)] + [""] * (lev - 1) + [_chinese_name(fid)] + [""]*(8-lev) + [_cls(fid)])))
        csv += line  + "\n"


    response = HttpResponse(csv, content_type='application/force-download')
    response['content-disposition'] = 'attachment; filename=foods.csv'
    return response


def get_country_by_ip(ip_str):
    try:
        return geolite2.reader().get(ip_str)['country']['iso_code']
    except:
        return None


def get_images_host_by_request(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    country = get_country_by_ip(ip)
    if not country or country != 'CN':
        return ''       # Images URLs will be relative to current domain
    else:
        return 'https://foods-cn.icx-il.com'


def food_names_by_lang(request):
    lang = request.GET.get('lang')
    names = [food_name.name for food_name in FoodNames.objects.filter(lang_code__code=lang)]
    response = JsonResponse({'names': names})
    return response


def statistics(request):
    not_chinese = '''   fid not in (select fid from food_attributes where attr_id = 1)    '''
    nfoods = db.select_as_value("select count(*) from food where " + not_chinese)
    no_serving = db.select_as_value("select count(*) from food where "+not_chinese+" and fid not in (select fid from units join food_units using (unit_id) where name_en='Serving')")

    no_nutrition = db.select_as_value("select count(*) from food where " + not_chinese + " and fid not in (select fid from food_components group by fid having sum(amount)=100) "  +
                                            " and fid not in (select distinct fid from food_nutrition_refs) " )

    no_food_quantitys = db.select_as_value("select count(*) from food_units")

    resp = {
        "total_foods": nfoods,
        "foods_without_serving_size": no_serving,
        "foods_without_nutrition_facts": no_nutrition,
        "avg_food_quant" : float(no_food_quantitys) / float(nfoods),
    }

    response = JsonResponse(resp)
    return response

# def is_curated(request, fid):
#     f = Food.objects.get(pk=int(fid))
#     is_curated = bool(f.attributes().filter(attr__value="curated").first())
#     return HttpResponse(str(is_curated))


def update_nutrients(request):
    update_food_nutrients()
    redirect_str = 'home'
    return HttpResponseRedirect('/food/' + redirect_str)


def food_attributes(request):
    fid = request.GET.get('fid')
    attributes = []
    if fid is not None:
        attributes = FoodAttributes.objects.filter(fid=fid).values_list('attr__value', flat=True)
        attributes = list(attributes)
    response = JsonResponse({'attributes': attributes})
    return response


def food_category_percentage(request):
    fid = request.GET.get('fid')
    res = qattributes(fid,get_inherited= True)
    data = res['data']
    if res['inherited'] is not None:
        res['inherited'] = Food.objects.filter(fid = res['inherited']).values("fid","name")[0]
    if 'asArray' in request.GET and request.GET['asArray'] == 'True':
        temp = []
        for key in data:
            temp.append({'food_category':key,'percentage':data[key]})
        data = temp
        res['data'] = data
        return JsonResponse(res, safe=False)
    # data = db.select_as_dict('select attribute,quantity from food_qattributes where fid=%s', [fid])
    # for d in data:
    #     data[d] = float(data[d])
    return JsonResponse(data,safe=False)


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def food_category_percentage_change(request):
    fid = request.POST.get('fid')
    qset = FoodQAttributes.objects.filter(fid_id = fid)
    if len(qset)>0:
        for obj in qset:
            if obj.attribute in request.POST and not obj.quantity == float(request.POST[obj.attribute]):
                row= FoodQAttributes.objects.get(fid_id=fid, attribute=obj.attribute)
                row.quantity = float(request.POST[obj.attribute])
                UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, row)
                row.save()
    else:
        data_arr =qattributes(fid)
        for attribute in data_arr:
            if attribute in request.POST:
                row , created = FoodQAttributes.objects.get_or_create(fid_id=fid, attribute=attribute)
                row.quantity = float(request.POST[attribute])
                if created:
                    UserActivityLog.add_log(request.user, UserActivityLog.CREATE, row)
                else:
                    UserActivityLog.add_log(request.user, UserActivityLog.UPDATE, row)
                row.save()
                # FoodQAttributes.objects.filter(pk=obj.pk,attribute = obj.attribute).update(quantity = float(request.POST[obj.attribute]))
    return HttpResponseRedirect('/food/{}/#attributes'.format(request.POST.get('fid')))


def download_csv(request):
    fid = request.GET.get('fid')
    food_model = Food.objects.get(pk=fid)
    data = food_model.create_child_nutrients()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="child_nutrients.csv"'
    writer = csvwriter(response)
    header = set_nutrients_list()
    header.insert(0, "Child Name")
    writer.writerow(header)
    for child, info in data.items():
        values = [x[1] for x in info]
        values.insert(0, child)
        writer.writerow(values)
    return response


def category_portion_sizes(request):
    return JsonResponse({
        "cereals and pastry": 30,
        "nuts": 15,
        "legumes":  160,
        "dairy products":  180,
        "meat and fish":  120,
        "eggs":  60,
        "fruit":  120,
        "vegetables":  100,
        "oils": 10
    })


def category_portion_sizes_by_nutrient(request):
    return JsonResponse({
        "cereals and pastry": {'grams':15, 'of':'total_carbohydrate'},
        "nuts": {'grams':8, 'of':'total'},
        "legumes": {'grams':5, 'of':'protein'},
        "dairy products": {'grams':7, 'of':'protein'},
        "meat and fish": {'grams':100, 'of':'total'},
        "eggs": {'grams':60, 'of':'total'},
        "fruit": {'grams':15, 'of':'total_carbohydrate'},
        "vegetables": {'grams':100, 'of':'total'},
        "oils": {'grams':5, 'of':'total_fat'}
    })


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def remove_food_amount_question(request):
    fid = int(request.GET['fid'])
    food_questionn_id = int(request.GET['id'])
    o = FoodAmountQuestion.objects.get(pk=food_questionn_id)
    UserActivityLog.add_log(request.user, UserActivityLog.DELETE, o)
    o.delete()
    return HttpResponseRedirect('/food/{}/#questions'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def add_food_amount_question(request):
    fid = int(request.POST['fid'])
    questionn_id = int(request.POST['question_id'])
    q = AmountQuestion.objects.get(pk=questionn_id)
    f = Food.objects.get(pk=fid)
    o = FoodAmountQuestion(fid=f, amount_question=q)
    o.save()
    UserActivityLog.add_log(request.user, UserActivityLog.CREATE, o)
    return HttpResponseRedirect('/food/{}/#questions'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def remove_food_boolean_question(request):
    fid = int(request.GET['fid'])
    food_question_id = int(request.GET['id'])
    o = FoodBooleanQuestion.objects.get(pk=food_question_id)
    UserActivityLog.add_log(request.user, UserActivityLog.DELETE, o)
    o.delete()
    return HttpResponseRedirect('/food/{}/#questions'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def remove_food_choice_question(request):
    fid = int(request.GET['fid'])
    food_question_id = int(request.GET['id'])
    o = FoodMultipleChoiceQuestion.objects.get(pk=food_question_id)
    UserActivityLog.add_log(request.user, UserActivityLog.DELETE, o)
    o.delete()
    return HttpResponseRedirect('/food/{}/#questions'.format(fid))


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def food_choice_question(request):
    if request.method == 'POST':
        params = request.POST.copy()
        instance_id = params.pop('id', None)[0]
        instance = None
        if instance_id != 'None':
            instance = FoodMultipleChoiceQuestion.objects.get(pk=int(instance_id))

        form = ChoiceQuestionForm(params, instance=instance)
        if form.is_valid():
            choice_question = form.save()
            return HttpResponseRedirect('/food/{}/#questions'.format(choice_question.fid.fid))
    else:
        food_question_id = request.GET.get('id')
        if food_question_id:
            instance = FoodMultipleChoiceQuestion.objects.get(pk=food_question_id)
            form = ChoiceQuestionForm(instance=instance)
        else:
            fid = request.GET['fid']
            initial = {'fid': Food.objects.get(pk=fid)}
            form = ChoiceQuestionForm(initial=initial)

    return render(request, 'choice_question.html', {'form': form, 'id': request.GET.get('id')})


def attribute_types(request):
    type_id = request.GET.get('type')
    if type_id:
        try:
            types = [AttributeType.objects.get(pk=type_id)]
        except AttributeType.DoesNotExist:
            return HttpResponseBadRequest('No such attribute type')
    else:
        types = AttributeType.objects.all()
    res = [
        {
            'id': t.pk,
            'name': t.name,
            'values': [
                {
                    'id': v.pk,
                    'value': v.value,
                    'names': [n.name for n in v.attributename_set.all()]
                } for v in t.attribute_set.all()
            ]
         } for t in types
    ]
    return JsonResponse({'attribute_types': res})


def recipe_from_text(text):
    components = []
    errors = []
    for line in text.split("\n"):
        if line.strip():  # In case an empty line was entered
            analysis = nlp.analyze(line.strip())
            if analysis and len(analysis['items']) == 1:
                if analysis['items'][0]['type'] == 'food':
                    info = None
                    try:
                        info = FoodItem.from_dict(analysis['items'][0]).flatten()
                    except Exception as err:
                        errors.append("Please inform us of this error: {}".format(err))
                    components.extend(info)
                    errors.append(None)
                else:
                    components.append(None)
                    errors.append("Type is not food")
            else:
                components.append(None)
                errors.append("No such item could be recognized")
    return components, [x.strip() for x in text.split("\n") if x.strip()], errors


def nlp_recipe_component(request):
    text = request.GET['text']
    components, text_lines, errors = recipe_from_text(text)
    if components[0]:
        nlp_data = components[0].to_json()
        nlp_data.pop("nutrients")
        units = food_units_with_gram(nlp_data['fid'])
        lsUnits = [un['quantity_name'] for un in units]
        if not nlp_data['unit_type'] in lsUnits:
            nlp_data['unit_type'] = None
            nlp_data['weight'] = None
    else:
        nlp_data = None
        lsUnits = []
    return JsonResponse({"original_text": text_lines[0], "errors": errors[0], "components": nlp_data,'listUnit':lsUnits})


@transaction.atomic
def create_recipe(food_id, components, weights, units = None, units_amount= None,liquid_loss = None,user=None):
    f = Food.objects.get(pk=food_id)
    if not f.liquid_loss == liquid_loss:
        #description = "Updated: [liquid_loss: {0} => {1}]".format(f.liquid_loss,liquid_loss)
        f.liquid_loss = liquid_loss
        if user is not None:
            UserActivityLog.add_log(user, UserActivityLog.UPDATE, f,fid=f.fid)
        f.save()
    f_first_comp = f.components.first()
    if f_first_comp is not None:
        UserActivityLog.add_log(user, UserActivityLog.DELETE, f.components.first(), fid=f.fid,description="Deleted all food components.")
        f.components.all().delete()
    weights = np.array(weights)
    normalized_weights = weights / weights.sum() * 100
    resArr = [FoodComponents(fid=f, component=c, amount=w, unit = u ,unit_amount = a)
                  for c, w, u, a in zip(components, normalized_weights,units,units_amount)]
    for c in resArr:
        if user is not None:
            UserActivityLog.add_log(user, UserActivityLog.CREATE, c, fid=f.fid)
        c.save()
    return f


@login_required(redirect_field_name='home')
@permission_required('food.add_food', raise_exception=True)
def recipe(request):
    if request.method == 'GET':
        text = request.GET['recipe_text']
        food_id = request.GET['food_id']
        food = Food.objects.filter(pk=food_id).first()
        if food is None:
            return HttpResponse('<h1>Error: food id is not found</h1>')
        par = food.fid
        parents = []
        while par != 1 and par:
            parents.append(par)
            par = parent(par)
        components, text_lines, errors = recipe_from_text(text.strip())
        components = PutUnitInCommponent(components)
        return render(request, 'recipe.html', {'components': list(zip(components, text_lines, errors)), 'food_id': food_id,'liquid_loss':food.liquid_loss,'parents':parents})
    elif request.method == 'POST':
        if 'edit' in request.POST and request.POST['edit'] == "True":
            food_id = request.POST['fid']
            food = Food.objects.filter(pk=food_id).first()
            if food is None:
                return HttpResponse('<h1>Error: food id is not found</h1>')
            FC = FoodComponents.objects.filter(fid = food_id)
            components =[]
            text_lines=[]
            errors=[]
            for fc in FC:
                unamount = fc.unit_amount if fc.unit_amount is not None else 1
                print('food=',fc.component,'unit_type = ',fc.unit,'amount = ',unamount)
                components.append(FoodItem(food=fc.component,unit_type = fc.unit,amount = unamount ))
                text_lines.append("")
                errors.append("")
            components = PutUnitInCommponent(components)
            par = food.fid
            parents = []
            while par != 1 and par:
                parents.append(par)
                par = parent(par)
            return render(request, 'recipe.html', {'components': list(zip(components, text_lines, errors)), 'food_id': food_id,'liquid_loss':food.liquid_loss,'parents':parents})
        else:
            food_id = request.POST['food_id']
            weights = [float(w) for w in request.POST.getlist('weights')]
            components = [Food.objects.get(pk=int(c)) for c in request.POST.getlist('comp')]
            units = [Units.objects.filter(Q(name_en = c) |Q(name_he = c)| Q(name_cn = c) ).first() for c in request.POST.getlist('gpu')]
            units_amount = [float(c) for c in request.POST.getlist('amount')]
            liquid_loss = float(request.POST.getlist('liquid_loss')[0]) if request.POST.getlist('liquid_loss') and not request.POST['liquid_loss'] == "" else None
            f = create_recipe(food_id, components, weights, units, units_amount,liquid_loss ,user= request.user)
            return HttpResponseRedirect('/food/' + str(food_id) + '/?recipe=true')
            #return HttpResponseRedirect('/food/1/?recipe=true')

def duplicate_names(request):
    langs = Lang.objects.filter(code__in=['he', 'en'])
    names = FoodNames.objects.filter(lang_code__in=langs).select_related('fid')
    dups = defaultdict(list)
    for n in names:
        dups[n.name].append(n.fid)
    dups = {n: foods for n, foods in dups.items() if len(foods) > 1}
    return render(request, 'duplicate_names.html', {'dups': dups})

def names_list_to_food(request):
    try:
        names    = json.loads(request.POST['names'])
        fraction = float(request.POST['fraction'])
        min_n = len(names) * fraction
        #print "min_n = ",min_n

        name_counts = defaultdict(int)
        for name in names:
            name_counts[name] += 1

        sql = '''
            select P.name,rank from food_predecessor_rank join food_names using (fid) join food as P on (P.fid=food_predecessor_rank.parent)
            where food_names.name = %s
        '''

        depth_sql = 'select max(rank) from food_predecessor_rank join food_names using (fid) where name = %s'

        Count = defaultdict(int)
        Depth = dict()


        for name in name_counts:
            depth = db.select_as_value(depth_sql,[name])

            cur = db.execute(sql,[name])
            for p,rank in  cur:
                #print name, name_counts[name], ":", p, depth - rank
                Count[p] += name_counts[name]
                Depth[p] = depth - rank

        candidates = [x for x in Count.keys() if Count[x] >= min_n]
        candidates = sorted(candidates, key = lambda x: -Depth[x])
        for name in candidates:
            print(name, Count[name], Depth[name])


        return HttpResponse(candidates[0])
    except Exception as e:
        print(e)
        return HttpResponse("food - ex")

def activityLog(request):
    USL_table = UserActivityLog.objects.all()
    if 'fid' in request.GET:
        food =  Food.objects.get(pk=request.GET['fid'])
        USL_table = USL_table.filter(fid = request.GET['fid'])
    else:
        food = None
    if 'is_from' in request.GET and request.GET['is_from'] =='on':
        fromDate = dateutil.parser.parse(request.GET['from'])
        USL_table = USL_table.filter(timestamp__date__gte = fromDate)
    else:
        fromDate = None
    if 'is_until' in request.GET and request.GET['is_until'] =='on':
        untilDate = dateutil.parser.parse(request.GET['until'])
        USL_table = USL_table.filter(timestamp__date__lte=untilDate)
    else:
        untilDate = None
    if 'user' in request.GET:
        user = User.objects.get(pk=request.GET['user'])
        USL_table = USL_table.filter(user=user)
    else:
        user = None
    tablesArr = UserActivityLog.objects.all().values('table').distinct()
    tablesFilter = [obj['table'] for obj in tablesArr]
    tables = []
    if 'fromPage' in request.GET and request.GET['fromPage'] =='yes':
        for obj in tablesArr:
            if obj['table'] not in request.GET:
                tables.append({'name': obj['table'],'checked':''})
                tablesFilter.remove(obj['table'])
            else:
                tables.append({'name': obj['table'], 'checked': 'checked'})
    else:
        for obj in tablesArr:
            tables.append({'name': obj['table'], 'checked': 'checked'})
    USL_table = USL_table.filter(table__in=tablesFilter)
    USL_table = USL_table.values()
    data = [ {'id':obj['id'],
              'Table': obj['table'],
              'Food': obj['fid_id'],
              'Date': obj['timestamp'].strftime("%Y-%m-%d"),
              'User': obj['user_id'],
              'Action': UserActivityLog.CHOICES[obj['action']+1][1],
              'Description':obj['description']}
             for obj in USL_table ]
    users = { obj['id']:obj['username'] for obj in User.objects.all().values()}
    foods = { obj['fid']:obj['name'] for obj in Food.objects.all().values()}
    for obj in data:
        obj['Food'] = None if obj['Food'] not in foods else {'fid': obj['Food'], 'username': foods[obj['Food']]}
        obj['User'] = None if obj['User'] not in users else users[obj['User']]
    data.reverse()
    if len(data) > 1000:
        data = data[:1000]
    #print request.GET
    #print 'tablesFilter: ',tablesFilter
    #print datetime.strptime(request.GET['from'], "%Y-%m-%d")
    return render(request,'activitylog.html',{'food':food,
                                              'fromDate': None if fromDate is None else fromDate.strftime("%Y-%m-%d"),
                                              'untilDate': None if untilDate is None else untilDate.strftime("%Y-%m-%d"),
                                              'user': user,
                                              'tables': tables,
                                              'data':data
                                              })
def fooddb_queries(request):#for the page fooddb_queries
    if request.method == "GET":
        usd = UsdaNutrient.objects.get(name__icontains="energy")
        nutrients = UsdaNutrient.objects.filter(name__in=["energy","total_fat","protein","total_carbohydrate"])
        nodeType = FoodNodeType.getDic()
        defult = {'UsdaNutrient':{'name':usd.name, 'id':usd.id},
                  'maximal_percent':150.0,
                  'standard_deviations':2,
                  'UsdaNutrients':[{'name':obj.name, 'id':obj.id} for obj in nutrients],
                  'node_type':[{'name':nodeType['common'].name,'id':nodeType['common'].id},
                               {'name':nodeType['broad'].name,'id':nodeType['broad'].id}]
                  }
        return render(request, 'fooddb_queries.html', {'defult': defult})
    else:
        res = fooddb_querise_runFromQueryDict(request.POST)
        return JsonResponse(res,safe=False)

def fooddb_filter(request):
    if request.method == "POST":
        print('request.POST:', request.POST)
        res = fooddb_filter_runFromQueryDict(request.POST)

        return JsonResponse(res, safe=False)
    else:
        print('request.GET:',request.GET)
        return render(request, 'fooddb_filter.html', {'defult': {},'data':[]})

def barcode_scanner(request):
    return render(request, 'barcode_scanner.html')

def activity_log_json(request):
    if 'from_date' in request.GET:
        from_date = datetime.strptime(request.GET['from_date'], "%d/%m/%Y")
        sql = '''SELECT food_useractivitylog.fid,food_useractivitylog.table,food_useractivitylog.datachange
        FROM food_useractivitylog
        WHERE (food_useractivitylog.datachange)::jsonb!='{}'::jsonb
        AND (food_useractivitylog.timestamp)::date >= %s'''
        queSet = db.execute(sql,[from_date])
        activity_log  = {}
        for row in queSet:
            if row[0] not in activity_log:
                activity_log[row[0]]=[]
            activity_log[row[0]].append({'table':row[1], 'datachange':row[2]})
        DUD = default_units_data()
        FU = FoodUnits.all_inhereted()
        FidDict = defaultdict(list)
        for f in FoodNames.objects.values('fid','name','fid__name'):
            FidDict[f['name'].lower().replace(' ','_')].append(f['fid'])
            FidDict[f['fid__name'].lower().replace(' ','_')].append(f['fid'])
        UnitDict = defaultdict(list)
        Unit_IdDict = defaultdict(list)
        for u in Units.objects.values('unit_id','name_he','name_en','name_cn','plural_en','plural_he'):
            if u['name_en'] != None:
                UnitDict[u['name_en'].lower().replace(' ','_')].append(u['unit_id'])
                Unit_IdDict[u['unit_id']].append(u['name_en'].lower().replace(' ','_'))
            if u['name_he'] != None:
                UnitDict[u['name_he'].lower().replace(' ','_')].append(u['unit_id'])
                Unit_IdDict[u['unit_id']].append(u['name_he'].lower().replace(' ','_'))
            if u['name_cn'] != None:
                UnitDict[u['name_cn'].lower().replace(' ','_')].append(u['unit_id'])
                Unit_IdDict[u['unit_id']].append(u['name_cn'].lower().replace(' ','_'))
            if u['plural_en'] != None:
                UnitDict[u['plural_en'].lower().replace(' ','_')].append(u['unit_id'])
                Unit_IdDict[u['unit_id']].append(u['plural_en'].lower().replace(' ','_'))
            if u['plural_he'] != None:
                UnitDict[u['plural_he'].lower().replace(' ','_')].append(u['unit_id'])
                Unit_IdDict[u['unit_id']].append(u['plural_he'].lower().replace(' ','_'))
        gram_dic = {UnitDict['gram'][0]:1}
        FU = {k: {**v, **gram_dic} for k, v in FU.items()}
        FoodDB_data = {'activity_log':activity_log,'DUD':DUD,'FU':FU,'FidDict':FidDict,'UnitDict':UnitDict,'Unit_IdDict':Unit_IdDict}
        return JsonResponse(FoodDB_data,safe=False)
    else:
        return HttpResponse('<h1>Error: from_date is needed</h1>')

def download_tree_directoris(request,fid):
    import zipfile
    from .fooddb_queries import temp,get_dic_food
    def reqursi_generate_folders(base_path, root, children_dict, path_list, dicFood):
        base = os.path.join(base_path, "{}[{}]".format(dicFood[root]['name'], root))
        # path_list.append(base)
        # for child in children_dict[root]:
        #     reqursi_generate_folders(base, child, children_dict, path_list, dicFood)
        if root in children_dict:
            for child in children_dict[root]:
                reqursi_generate_folders(base, child, children_dict, path_list, dicFood)
        else:
            path_list.append(base)

    children_dict = get_children_dict()
    rootFid = int(fid)
    FBobj = temp(root=[rootFid])
    dicFood = get_dic_food(FBobj)
    base_path = "/"
    path_list =[]
    reqursi_generate_folders(base_path, rootFid, children_dict, path_list, dicFood)
    s = BytesIO()
    zip_filename = "%s.zip"%dicFood[rootFid]['name']
    zf = zipfile.ZipFile(s, 'w', zipfile.ZIP_DEFLATED)
    for dir in path_list:
        # zif = zipfile.ZipInfo(dir + "/")
        # zf.writestr(zif, "")
        zip_path = os.path.join(dir, "empty.txt")
        zf.write("__init__.py",zip_path)
    zf.close()
    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    return resp

