from django.shortcuts import render
import counter

# Create your views here.
def index(request):
    counter1 = counter.createMetricsMap(1)
    print("shit kinda worked")
    return counter1.serveMetricsMap()