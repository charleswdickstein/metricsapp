from django.db import models

class Counter(models.Model):
    key = models.CharField(max_length=200)
    value = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    #url = models.CharField(max_length=200, default="none")
    def __str__(self):
        return self.key
	
	class Meta:
		db_table = 'COUNTERS'
	
	def to_dict(self):
		return {
			'key': self.key,
			'y': [self.value, self.pub_date]
		}



  