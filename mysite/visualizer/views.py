from django.http import HttpResponse
import json
# import json
from .models import Counter
import os
from django.utils import timezone
import pandas as pd
import sqlite3
import datetime
import random
from matplotlib import pyplot as plt
from io import BytesIO
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import seaborn as sns
from django.template import loader


def convert_to_seconds(x):
	d = datetime.strptime(x, "%d/%m/%Y %H:%M:%S")
 	d =  time.mktime(d.timetuple())
 	print("this is d")


def process_data(file_path):
	t = timezone.now()
	with open(file_path, 'r') as f:
		datastore = json.load(f)
		counter = datastore["counter"]
		for key, value in counter.iteritems():
			print(key, value)
			counter = Counter(key=str(key), value=int(value), pub_date=t)
			counter.save()
	
	return datastore

def home(request):
	x = 1
	
	module_dir = os.path.dirname(__file__)  # get current directory
	file_path = os.path.join(module_dir, 'data.txt')
	datastore = process_data(file_path)
	print("Data")
	
	df = pd.DataFrame(list(Counter.objects.all().values()))
	df = pd.DataFrame(list(Counter.objects.all().values('key', 'value', 'pub_date')))
	print(df.head())
	print("Print Sums By key")
	print(df.groupby("key").sum())
	sums_by_key = df.groupby("key").sum()
	print(sums_by_key)
	print("Print Sums By key And Date")
	print(df.groupby(["key", "pub_date"]).sum())
	fig=Figure()
	# ax=fig.add_subplot(111)
	# x=[]
	# y=[]
	# now=datetime.datetime.now()
	# delta=datetime.timedelta(days=1)
	# for i in range(10):
	#     x.append(now)
	#     now+=delta
	#     y.append(random.randint(0, 1000))
	# ax.plot_date(x, y, '-')
	
	# fig.autofmt_xdate()

	fig, ax = plt.subplots(figsize=(15,7))
	
	#df.groupby(['key','pub_date']).sum()['value'].plot(ax=ax)
	#ax = sns.lineplot(x="key", y="value", hue="pub_date", data=df)
	graphNum = 0
	lst = []
	#df["pub_date"] = df["pub_date"].apply(lambda x: convert_to_seconds)
	df["server"] = 1 

	for k in df.key.unique():
		plt.figure(graphNum)
		graphNum = graphNum+1
		for L in df.server.unique():
			#num = "21"+str(graphNum)
			#fig.add_subplot(5, 4,graphNum +1)
			section = df[(df["key"] == k) & (df["server"] == L)]
			plt.plot(section["pub_date"], section["value"], label=L)
			print("val")
			print(section["key"], section["value"])
		    #lst.append(plt)


		plt.title("key: " + k)
		plt.xlabel("Time")
		plt.ylabel("Counts")
		plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		plt.savefig("static/scrap" + str(graphNum)+".png")
		lst.append(plt)
		plt.close()
	#print()
	print("this is ist ")
	print(lst)
	canvas = FigureCanvas(fig)
	response = HttpResponse(content_type='image/png')
	canvas.print_png(response)
	return response



from django.shortcuts import render



def tests(request):
	latest_question_list = Counter.objects.order_by('pub_date')[:5]
	context = {'latest_question_list': latest_question_list}
	path="static"  # insert the path to your directory   
	img_list =os.listdir(path)
	print(img_list)
	context = {'latest_question_list': img_list}


	return render(request, 'visualizer/test.html', context)