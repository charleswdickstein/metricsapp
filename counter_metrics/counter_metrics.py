# The counter library used to handle number logic regarding requests
# The scraping app should use this module's functions to scrape data

'''
to import this file and serve a json response:
from this_module import MetricsMap
x = MetricsMap(id)
# add to dict here... 
res = x.serveMetricsMap()
# res is an entire http response
return res
'''

import datetime
import json
from django.http import HttpResponse
from django.http import JsonResponse

class MetricsMap:
    def __init__(self, id):
        # Metrics dictionary has key: metric and value: list of (x), where x can be anything (we are thinking a tuple of (timestamp, count))
        self.id = id
        self.metrics = {}

    def createSimpleCounter(self, key, initial_count=1):
        if key not in self.metrics:
            self.metrics[key] = initial_count
        else:
            self.metrics[key] = self.metrics[key] + 1

    def simpleIncrement(self, metric, count = 1):
        if metric not in self.metrics:
            print('Metric %s was created at increment time' % (metric))
            self.metrics[metric] = 1
        else:
            self.metrics[metric] = self.metrics[metric] + count

    def metricExists(self, key):
        if key in self.metrics:
            return True
        else:
            return False

    def getMetricsDict(self):
        return self.metrics

    def getMetricValue(self, key):
        # returns value of metric
        return self.metrics[key]

    def getMetricsMapJSONified(self):
        # Returns metrics dict as a JSON string. 
        # TODO: Do we want server ID in the json object?
        temp_metrics_dict_with_id = self.metrics.copy()
        temp_metrics_dict_with_id['id'] = self.id 
        json_str = json.dumps(temp_metrics_dict_with_id)
        return json_str

    def serveMetricsMap(self):
        # Returns HTTP response with Json object as content
        # TODO: Do we want server ID in the json object?
        temp_metrics_dict_with_id = self.metrics.copy()
        temp_metrics_dict_with_id['id'] = self.id 
        return JsonResponse(temp_metrics_dict_with_id)

# Debugging
def debug():
    print('abcdefg##############\n\n\n')
    my_map = MetricsMap('1')
    my_map.simpleIncrement('key1')
    my_map.createSimpleCounter('key2')
    my_map.simpleIncrement('key1', 33)
    print(my_map.getMetricsMapJSONified())

if __name__ == '__main__':
    debug()