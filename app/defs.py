import numpy
import string
from gensim import corpora, models, similarities
from gensim.models import Word2Vec
from gensim.models import Phrases
from gensim import matutils
import math

def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v1)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)


def array_sum(trend, model):
    array_sum = [0] * 300
    for index, word in enumerate(trend):
        array_sum = array_sum + model[trend[index]]
    return array_sum


def get_weighted_sim(cat, trend, weight, model):
    trend_add = array_sum(trend, model)
    sim = 0
    if ' ' in cat:
        cat_join = '_'.join(cat.split(' '))
        cat_lower_join = '_'.join(cat.lower().split(' '))
        cat_lower = cat.lower().split(' ')
        cat_split = cat.split()
        if cat_lower_join in model:
            sim = cosine_similarity(trend_add, model[cat_lower_join])
        elif cat_join in model:
            sim = cosine_similarity(trend_add, model[cat_join])
        elif all(x in model for x in cat_lower):
            cat_add = array_sum(cat_lower, model)
            sim = cosine_similarity(trend_add, cat_add)
        elif all(x in model for x in cat_split):
            cat_add = array_sum(cat_split, model)
            sim = cosine_similarity(trend_add, cat_add)
    else:
        sim = cosine_similarity(trend_add, model[cat.lower()])
    weighted_sim = sim * 1/(1+0.003*int(weight))
    return weighted_sim


def find_weighted_best_trends(cat, trend_list, model):
    vec_list = {}
    for trend in trend_list:
        vec_list[trend[3]] = get_weighted_sim(cat, trend[3].split(" "), trend[0], model)
    return pretty_print(sorted(vec_list.items(), key=lambda x: x[1], reverse=True)[:5])


def pretty_print(vec_list):
    pretty_list = []
    for item in vec_list:
        trend = item[0]
        weight = item[1]
        if '_' in trend:
            trend = trend.replace('_', ' ')
        if trend[0].islower():
            trend = string.capwords(trend)
        pretty_list.append([trend, weight])
    return pretty_list


def extract_points(best_list):
    cats = []
    sims = []
    for i in best_list:
        cats.append(i[0])
        sims.append(i[1])
    return cats, sims

