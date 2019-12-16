# Metriculous
## Counter Library, Scraper, and Data Visualization Application
### Github: https://github.com/charleswdickstein/metricsapp

## Project Use

### The project is running on three Google Cloud instances. Two separate Google Cloud instances run Scalica, which contain implementations of the counter library. Another instance runs the scraper/visualizer application. 

Access Scalica at the following links: <br/>
Server 1: http://35.237.169.40:8000/micro/ <br/>
Server 2: http://35.230.185.22:8000/micro/

For our projects, we serve the counter JSON response for the scraper to read at
 `<IP Address>/stats`. So for Scalica, we have:<br/>
Server 1: http://35.237.169.40:8000/micro/stats<br/>
Server 2: http://35.230.185.22:8000/micro/stats

Access Metriculous, the Scraper/Visualizer application, at the following link:<br/>
Server: http://35.223.174.169:8000/


The Scalica instances have counters to track developer pre-defined variables per server. For demonstration purposes we have used the following variables:<br/>
total-views : total number of page views<br/>
page-home : number of times the home page was viewed<br/>
user-created : number of times a new user was created<br/>
page-index : total number of times index (login) was viewed

## Project Specifications

The project consists of two distinct parts, discussed in their separate sections. The counter portion of the project is a library that can be imported into any Django web application. The Scraper/Visualizer is a Django application to gather the counts from the various servers and produce graphs from those counts. The counter library is in Python while the scraper/visualizer application uses Python, and Javascript. The scraper requires libraries Django, SQLite, Pandas, apscheduler, seaborn and MatplotLib.

# IMPORTANT NOTE: 
In the demo application, we scrape every 30 seconds. After modifying data on Scalica, it will take 30 seconds to reflect in the scraper_visualizer web page. 

# Counter Library

The main counter library file is called `metrics_counter.py`. Place this in the same folder as your Django app’s `views.py` file. In `views.py`, we can import the module and create a counter object:<br/>
	```from .counter_metrics import MetricsMap
	metrics_map = MetricsMap()```
Once the object is created, we can utilize the class functions to work with the dictionary attribute of the counter object. Here is an example where we record the number of times users view the index route of our application, in `views.py`:<br/>
```	metrics_map = MetricsMap()
	def index(request):
	    metrics_map.simpleIncrement('index')
```

The class functions of counter_metrics.py can be viewed in the source code, but a high level overview is given here:<br/>

`createSimpleCounters(key)` takes in a list as an argument and creates keys with values initialized to 0 for the object dictionary attribute.<br/>

`simpleIncrement(metric, optional count)` increments the metric given by the first argument, and increments it by an optional value in the second argument. <br/>

`mapReset()` clears the object dictionary. <br/>

`serveMetricsMap()` returns a Django HTTP response, with the metrics dictionary as the content.
	

	

# Scraper/Visualizer Application

## How to Run:
Clone the repository
From the main directory: “metrify” in the terminal run the following commands:<br/>
# Install Required Libraries
```
$ pip install django
$ pip install pandas
$ pip install matplotlib
$ pip install seaborn
$ pip install apscheduler
```
## Create database and run from the directory ‘metrify/scraper_visualizer’
From metrify:
Create Database. Install missing libraries as needed 
```
$ cd scraper_visualizer
$ python manage.py makemigrations
$ python manage.py migrate
```
## Run the application on localhost at ‘metrify/scraper_visualizer’
`$python manage.py runserver`

Input variables are set in the Configuration.txt file. This sets the time between scrapes (how long to wait), number of time intervals to show in the most recent intervals graph (as opposed to the graphs over all time), and the links to the JSON files in the server locations you want to read from. The configuration file has some leniency for trailing spaces but do not change the order of, add or remove lines in the file. Example values are given.

Graphs will be saved into the following directory: ‘metrify/scraper_visualizer/static’

On a local machine, the visualizer will display the graphs at the root path of localhost:8000.

### Specifications

All servers must have the same keys. The key’s value may be 0 for any of the servers, but must be present for the scraper to record a value of 0. The scraper will assume that keys with the same name over different servers are the same count over different servers. 
The graphs are grouped by and ordered by the key names. Each graph will have a version over the total time of running the scraper and only the most recent time intervals (depends on configuration settings). Note that the most recent time intervals will not be shown if the total time does not exceed the number of time intervals. 

### Graphs

The following graphs will be produced (per unique key name):

Counts for key per server - The raw number of counts at different time intervals, one line per server containing at least one count on the same graph.

Aggregate of counts for key over all servers - The raw number of counts for a key from all listed servers added together at different time intervals.

Change in counts for key per server - The change in counts in the current and previous time interval, plotted over time. This has one line per server with at least one count on the same graph.

Aggregate of the change in counts for key over all servers - The change in the aggregate of the counts from all servers for a key in current and previous time interval, plotted over time.


### Resources:
### https://docs.djangoproject.com/en/2.2/intro/

'''
MIT License

Copyright (c) 2019 Charles Dickstein et al.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
