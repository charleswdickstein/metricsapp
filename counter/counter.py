# The counter library used to handle number logic regarding requests
# The scraping app should use this module's functions to scrape data

import datetime
import json

# List of all metrics maps, key = (server) ID, value = dict
# list_of_all_metrics_maps = {}

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
        # returns array of metric items
        return self.metrics[key]

    def getMetricsMapJSONified(self):
        # Returns metrics dict as a JSON string. 
        # TODO: Do we want server ID in the json object?
        temp_metrics_dict_with_id = self.metrics.copy()
        temp_metrics_dict_with_id['id'] = self.id 
        json_str = json.dumps(temp_metrics_dict_with_id)
        return json_str

# Driver function that returns a metrics map
def createMetricsMap(id):
    new_metrics_map = MetricsMap(id)
    # list_of_all_metrics_maps[id] = new_metrics_map
    return new_metrics_map

# Debugging
def debug():
    dict1 = MetricsMap(1)
    dict1.simpleIncrement('key1')
    dict1.simpleIncrement('key1')
    print(dict1.getMetricsMapJSONified())

if __name__ == '__main__':
    debug()