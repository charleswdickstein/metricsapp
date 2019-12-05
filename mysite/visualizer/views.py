from django.http import HttpResponse
import json
# import json
from .models import Counter
import os
from django.utils import timezone
import pandas as pd
import sqlite3


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
	print("Print Sums By key And Date")
	print(df.groupby(["key", "pub_date"]).sum())
	return HttpResponse("Write Successful")