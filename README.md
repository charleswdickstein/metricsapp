# metrify
## Install Django 
pip install Django 

## Scraper 
Reads Data from a generic file called data.txt
containing JSON and saves it to the database

JSON File should be in this format:
{"counter": 
	{
		"key1":"2",
		"key2":"2",
		"key3":"3",
		...
	}
}

### Model
'''
class Counter(models.Model):
    key = models.CharField(max_length=200)
    value = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.key
'''
## Demo Instructions
### Run the following commands from the mysite directory in terminal to build DB:
#### $ python manage.py migrate
#### $ python manage.py makemigrations visualizer

### Run command to start server. Then go to localhost:8000
#### $ python manage.py runserver


## TODO:
### Counter application to create Dictionary and exposed JSON file which the scraper will read. 
### Read Data from SQLite DB for data visualization

### Resources:
### https://docs.djangoproject.com/en/2.2/intro/