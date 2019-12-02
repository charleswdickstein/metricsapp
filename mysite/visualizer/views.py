from django.http import HttpResponse
import json
# import json
from .models import Counter
import os
from django.utils import timezone

def process_data(file_path):
	with open(file_path, 'r') as f:
		datastore = json.load(f)
		counter = datastore["counter"]
		for key, value in counter.iteritems():
			print(key, value)
			counter = Counter(key=str(key), value=int(value), pub_date=timezone.now())
			counter.save()
	print(Counter.objects.all())
	return datastore

def home(request):
	x = 1
	
	module_dir = os.path.dirname(__file__)  # get current directory
	file_path = os.path.join(module_dir, 'data.txt')
	datastore = process_data(file_path)
	return HttpResponse(datastore["counter"])