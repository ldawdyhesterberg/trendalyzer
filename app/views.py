from flask import render_template, request, Response
from app import app
from defs import *
from gensim import corpora, models, similarities
from gensim.models import Word2Vec
from gensim.models import Phrases
from gensim import matutils
import logging
import pygal
import mimetypes

from pygal.style import Style
custom_style = Style(background='transparent', plot_background='#cfd1d2', foreground='#000000', foreground_light='#0cabb5', foreground_dark='#07676d', opacity='.5', opacity_hover='.9', transition='100ms ease-in', colors=('#6fd7ff', '#19a5da', '#00719c', '#00415a', '#001f2b'))


mimetypes.add_type('image/svg+xml', '.svg')

#import os
logging.basicConfig(level=logging.DEBUG)

#cur_wd = os.getcwd()
#logging.debug("curdwd = %s" % cur_wd)

model = Word2Vec.load_word2vec_format('./app/data/GoogleNews-vectors-negative300.bin', binary=True)
logging.debug("Loaded full model")


trend_words = []
with open("./app/data/google_trends.txt", "r") as f:
    for line in f:
        trend_words.append(line)
f.close()

trend_words=trend_words[1:]

trend_words_cleaned = []
for item in trend_words:
    newitem = item.replace("\n", "")
    newitem = newitem.split("\t")
    trend_words_cleaned.append(newitem)




@app.route('/')
@app.route('/input')
def trend_input():
  return render_template("input.html")

@app.route('/output')
def trend_output():
  #pull 'Category' from input field and store it
  category = str(request.args.get('Category'))
  if ' ' in category:
  	cat_upper_join = '_'.join(string.capwords(category).split(' '))
  	cat_lower_join = '_'.join(category.lower().split(' '))
  	cat_lower = category.split(' ')
  	cat_split = category.split(' ')
  	if (cat_upper_join in model or cat_lower_join in model or all(x in model for x in cat_lower) or all(x in model for x in cat_split)):
  		toplist = extract_points(find_weighted_best_trends(category, trend_words_cleaned, model))
  		topcats = toplist[0]
  		topsims = toplist[1]
  		topurls = toplist[2]
  		category = string.capwords(category)
  		horizontalbar_chart = pygal.HorizontalBar(title = category, style=custom_style, title_font_size=40, x_title_font_size=24, x_title='Similarity', legend_box_size=28, legend_font_size=28, legend_at_bottom=True, truncate_legend=12, label_font_size=22, x_label_font_size=18, major_label_font_size=22, show_x_guides=False, x_labels_major_count=5, show_minor_x_labels=False)
  		horizontalbar_chart.add(topcats[4],topsims[4])
  		horizontalbar_chart.add(topcats[3],topsims[3])
  		horizontalbar_chart.add(topcats[2], topsims[2])
  		horizontalbar_chart.add(topcats[1], topsims[1])
  		horizontalbar_chart.add(topcats[0], topsims[0])
  		horizontalbar_chart.value_formatter = lambda x: "%.2f" % x
  		horizontalbar_chart.render_to_file('./app/static/images/%s.svg' % '_'.join(category.split()))
  		image_url = "/static/images/" + '_'.join(category.split()) + ".svg"
  		return render_template("output.html", topcats=topcats, topsims=topsims, category=category, image_url=image_url)
  	else:
  		error = "Sorry, category input not found. Please try another category."
  		return render_template("input.html", error=error)
  if ' ' not in category:
  	if category not in model:
  		error = "Sorry, category input not found. Please try another category."
  		return render_template("input.html", error=error)
  	else:
			toplist = extract_points(find_weighted_best_trends(category, trend_words_cleaned, model))
			topcats = toplist[0]
			topsims = toplist[1]
			topurls = toplist[2]
			category = string.capitalize(category)
			horizontalbar_chart = pygal.HorizontalBar(title = category, style=custom_style, title_font_size=40, x_title_font_size=24, x_title='Similarity', legend_box_size=28, legend_font_size=28, legend_at_bottom=True,  truncate_legend=12, label_font_size=22,  major_label_font_size=22, x_label_font_size=18, show_x_guides=False, x_labels_major_count=5, show_minor_x_labels=False)
			horizontalbar_chart.add(topcats[4],topsims[4])
			horizontalbar_chart.add(topcats[3],topsims[3])
			horizontalbar_chart.add(topcats[2], topsims[2])
			horizontalbar_chart.add(topcats[1], topsims[1])
			horizontalbar_chart.add(topcats[0], topsims[0])
			horizontalbar_chart.value_formatter = lambda x: "%.2f" % x
			horizontalbar_chart.render_to_file('./app/static/images/%s.svg' %category)
			image_url = "/static/images/" + category + ".svg"
			return render_template("output.html", topcats=topcats, topsims=topsims, topurls=topurls, category=category, image_url=image_url)


@app.route('/slides')
def slides():
    return render_template("slides.html")

@app.route('/about')
def about():
    return render_template("about.html")
