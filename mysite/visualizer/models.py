from django.db import models

class Counter(models.Model):
    key = models.CharField(max_length=200)
    value = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.key

  