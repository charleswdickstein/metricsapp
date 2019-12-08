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
import numpy as np


from django.shortcuts import render

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

def get_graphs(testData):
	keys = "key" #Holds the string names of the keys
	serv = "server" #Holds the string names of the server location
	vlaues = "value" #Holds the values of the counts
	time = "pub_date" #Holds the time stamps

	showPlot = True #Runs the plt.show() command if this is True (should be set false)
	graphNum = 0
	print("50")
	for k in testData.key.unique():
		plt.figure(graphNum)
		graphNum = graphNum+1
	    
	    #Gets the aggragate values for all servers per key
		aggra = np.zeros(len(testData[(testData[keys] == k) 
	                & (testData[serv] == testData.server.unique()[0])][vlaues].values))
	    #Get the change in values for the aggragate
		change = np.zeros(len(aggra))
	    #An array to hold the change in values (serperate per server)
		changeLocArr = []
	    #Get the time stamp to use for the x axis
		timeAxis = testData[(testData[keys] == k) & (testData[serv] == testData.server.unique()[0])][time]
		print('64')
		for L in testData.server.unique():
			section = testData[(testData[keys] == k) & (testData[serv] == L)]
			#Add plot line to seperated values
			plt.plot(timeAxis, section[vlaues], label=L)
			#Update the aggragate change in values and change in values (the temp arr)
			a = section[vlaues].values
			change[0] = change[0] + a[0]
			changeTemp = np.zeros(len(a))
			changeTemp[0] = a[0]
			for i in range(1, len(change)):
			    change[i] = change[i] + (a[i] - a[i-1])
			    changeTemp[i] = a[i] - a[i-1]
			changeLocArr.append(changeTemp)
			#Get the aggragate values
			aggra = aggra + a
			plt.close()
	    
		print("82")
	    #Plot the seperated values
		plt.title("key: " + k)
		plt.xlabel("Time")
		plt.ylabel("Counts")
		plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		plt.savefig("static/scrap" + str(graphNum) + ".png")
		# if(showPlot == True):
		#     plt.show()
		# plt.close()
		print("91")
		#Plot the aggragate
		plt.figure(graphNum)
		graphNum = graphNum+1
		print("95")
		plt.plot(timeAxis, aggra)
		plt.title("key: " + k + " aggregate")
		plt.xlabel("Time")
		plt.ylabel("Counts")
		plt.savefig("static/scrapAgg" + str(graphNum) + ".png")
		
		plt.close()
		print("104")
		#Plot the change in values
		plt.figure(graphNum)
		graphNum = graphNum+1

		L = testData.server.unique()

		for i in range(0, len(changeLocArr)):
		    plt.plot(timeAxis, changeLocArr[i], label=L[i])
		print("113")
		plt.title("Change in key: " + k)
		plt.xlabel("Time")
		plt.ylabel("Counts")
		plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
		plt.savefig("static/ascrapChange" + str(graphNum) + ".png")
		
		plt.close()
		print("122")
		#Plot the aggragate change in values
		plt.figure(graphNum)
		graphNum = graphNum+1

		plt.plot(timeAxis, change)
		plt.title("Change in key: " + k + " aggregate")
		plt.xlabel("Time")
		plt.ylabel("Counts")
		plt.savefig("mysite/static/scrapAggChange" + str(graphNum) + ".png")
		
		plt.close()
	plt.close()
		

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

	fig, ax = plt.subplots(figsize=(15,7))
	
	
	graphNum = 0
	lst = []
	df["server"] = 1 
	print("this is ist ")
	print()
	get_graphs(df)
	print("after get")
	canvas = FigureCanvas(fig)
	response = HttpResponse(content_type='image/png')
	canvas.print_png(response)
	path = "static"  # insert the path to your directory   
	img_list =os.listdir(path)
	print("img list")
	print(img_list)
	context = {'latest_question_list': img_list}
	print(request)
	plt.close()
	return render(request, 'visualizer/test.html', context)
	





def tests(request):
	latest_question_list = Counter.objects.order_by('pub_date')[:5]
	#context = {'latest_question_list': latest_question_list}
	path="static"  # insert the path to your directory   
	img_list =os.listdir(path)
	# print(img_list)
	context = {'latest_question_list': img_list}
	return render(request, 'visualizer/test.html', context)