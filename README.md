# Metric Counter App
## Install Django 
pip install Django 

## Scraper 
Reads Data from a generic file called data.txt
containing JSON and saves it to the database

JSON File should be in this format:
```
{"counter": 
	{
		"key1":"2",
		"key2":"2",
		"key3":"3",
		...
	}
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
$ python manage.py migrate
$ python manage.py makemigrations visualizer
```
### Run command to start server. Then go to localhost:8000
```
$ python manage.py runserver
 ```

## TODO:
### Counter application to create Dictionary and exposed JSON file which the scraper will read. 
### Read Data from SQLite DB for data visualization

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