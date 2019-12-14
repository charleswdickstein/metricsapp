# The counter library used to handle number logic regarding requests
# The scraping app should use this module's functions to scrape data

'''
to import this file (from same directory):
from .this_module import MetricsMap()
'''

import json
from django.http import JsonResponse

class MetricsMap:
    def __init__(self):
        # Metrics dictionary has key: metric and value: count
        self.metrics = {}

    def createSimpleCounters(self, keys):
        # keys is list type
        if type(keys) is list:
            for key in keys:
                if key not in self.metrics:
                    self.metrics[key] = 0
                else:
                    continue
        else:
            print('createSimpleCounters accepts one argument of list type.')
            return

    def simpleIncrement(self, metric, count = 1):
        if type(count) is int:
            if metric not in self.metrics:
                print('Metric %s was created at increment time' % (metric))
                self.metrics[metric] = count
            else:
                self.metrics[metric] = self.metrics[metric] + count
        else:
            print('simpleIncrement count argument was not an integer')
            return

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

    def mapReset(self):
        self.metrics.clear()

    def getMetricsMapJSONified(self):
        # Returns metrics dict as a JSON string. 
        ret = json.dumps(self.metrics)
        return ret

    def serveMetricsMap(self):
        # Returns HTTP response with Json object as body
        return JsonResponse(self.metrics)

# Debugging
def debug():
    pass

if __name__ == '__main__':
    debug()
