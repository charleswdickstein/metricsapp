# Metriculous
## Counter Library, Scraper, and Data Visualization Application
### Github: 
(This document may also be accessed at the README.md in the repository)

## Project Use

### The project is running on three Google Cloud instances. Two separate Google Cloud instances run Scalica, which contain implemented the counter library. Another instance runs the scraper/visualizer application. 

Access Scalica at the following links:
Server 1: http://35.237.169.40:8000/micro/
Server 2: http://35.230.185.22:8000/micro/

Access Metriculous Scraper at the following link:
Server: http://35.223.174.169:8000/

The Scalica instances have counters to track (separate per server) the following variables (since the counter was running). For visibility’s sake, we limited the number of metrics:
total-views : total number of page views
page-home : number of times the home page was viewed
user-created : number of times a new user was created
page-index : total number of times index (login) was viewed

Project Specifications

This project is in two distinct parts, discussed in their separate sections. Generally the counters are a library that can be imported to be used in any Django web application and the Scraper/Visualizer is a Django application to gather the counts from the various servers and produce graphs. The counter library is in python while the scraper/visualizer application uses python and javascript. Both parts of the project use Django. The scraper requires SQLite, Pandas, and MatplotLib.



## Counter Library

The main counter library file is called `metrics_counter.py`. Place this in the same folder as your Django app, with file `views.py`. In `views.py`, we can import the module and create a counter object:
	`from .counter_metrics import MetricsMap`
	`metrics_map = MetricsMap()`
Once the object is created, we can utilize the class functions to work with the dictionary attribute of the counter object. Here is an example where we record the number of times users view the index route of our application, in `views.py`:
	`metrics_map = MetricsMap()`
	`def index(request):
	    metrics_map.simpleIncrement('index')`

The class functions of counter_metrics.py can be viewed in the source code, but a high level overview is given here:
` createSimpleCounters(key)` takes in a list as an argument and creates keys, with values initialized to 0, for the object dictionary attribute.
` simpleIncrement(metric, optional count)` increments the metric given by the first argument, and increments it by an optional value in the second argument. 
` mapReset()` clears the object dictionary.
` serveMetricsMap()` returns a Django HTTP response, with the metrics dictionary as the content.

For our projects, we serve the counter JSON response at `ip/stats`. So for Scalica, we have:
 Server 1: ` http://35.237.169.40:8000/micro/stats `
 Server 2: ` http://35.230.185.22:8000/micro/stats `
	

## Scraper/Visualizer Application

Github Repository: https://github.com/charleswdickstein/metricsapp

#### How to Run:
Clone the repository
From the main directory: “metrify” in the terminal run the following commands:
# Install Required Libraries
```
$ pip install django
$ pip install pandas
$ pip install matplotlib
$ pip install seaborn
```
### Create database and run from the directory ‘metrify/scraper_visualizer’
From metrify:
Create Database. Install missing libraries as needed 
```
$ cd scraper_visualizer
$ python manage.py makemigrations
$ python manage.py migrate
```
# Run the application on localhost at ‘metrify/scraper_visualizer’
`$python manage.py runserver`

Input variables are set in the Configuration.txt file. This sets the time between scrapes (how long to wait), number of time intervals to show in the most recent intervals graph (as opposed to the graphs over all time), and the links to the JSON files in the server locations you want to read from. The configuration file has some leniency for trailing spaces but do not change the order of, add or remove lines in the file. Example values are given.

Graphs will be saved into the following directory: ‘metrify/scraper_visualizer/static’

All servers must have the same keys. The key’s value may be 0 for any of the servers but must be present for the scraper to record a value of 0. The scraper will assume that keys with the same name over different servers are the same count over different servers. As such, the graphs are grouped by and ordered by the key names. Each graph will have a version over the total time of running the scraper and only the most recent time intervals (depends on configuration settings). Note that the most recent time intervals will not be shown if the total time does not exceed the number of time intervals. 


The following graphs will be produced (per unique key name):

Counts for key per server - The raw number of counts at different time intervals, one line per server containing at least one count on the same graph.

Aggregate of counts for key over all servers - The raw number of counts for a key from all listed servers added together at different time intervals.

Change in counts for key per server - The change in counts in the current and previous time interval, plotted over time. This has one line per server with at least one count on the same graph.

Aggregate of the change in counts for key over all servers - The change in the aggregate of the counts from all servers for a key in current and previous time interval, plotted over time.

JSON File should be in this format:
```
	{
		"key1":"2",
		"key2":"2",
		"key3":"3",
		...
	}

```
### Model
```
class Counter(models.Model):
    key = models.CharField(max_length=200)
    value = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.key
```
## Demo Instructions
### Run the following commands from the mysite directory in terminal to build DB:
```
$ python manage.py migrate.  
$ python manage.py makemigrations visualizer
```
### Run command to start server. Then go to localhost:8000
```
$ python manage.py runserver
 ```

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
