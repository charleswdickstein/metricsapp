# The counter library used to handle number logic regarding requests
# The scraping app should use this module's functions to scrape data

import json

class MetricsMap:
    def __init__(self, id):
        self.server_id = id
        self.metrics = {}

    def createMetric(self, key):
        self.metrics[key] = 0
    
    def increment(self, metric, times=-1):
        if metric not in self.metrics:
            # metric not in the map, but added anyway for now
            print('Metric:', metric, 'was added to the counter map') # DEBUG
            if times != -1:
                self.metrics[metric] += times
            else:
                self.metrics[metric] = 1
        else:
            if times != -1:
                self.metrics[metric] += times
            else:
                self.metrics[metric] += 1

    def metricExists(self, key):
        if key in self.metrics:
            return true
        else:
            return false

    def getMetricMap(self):
        return self.metrics

    def getMetricValue(self, key):
        return self.metrics[key]

    def returnMetricsMapJSONified(self):
        # Returns a metric map as a JSON string. 
        json_str = json.dumps(self.metrics)
        return json_str

# Driver function that returns a metrics map
def createMetricsMap():
    new_metrics_map = MetricsMap()
    return new_metrics_map

# Debugging
def debug():
    tester = MetricsMap()
    tester.createMetric('test_value')
    tester.increment('test_value')
    tester.increment('test_value', 4)
    # print(tester.getMetricCount('test_value'))
    print(type(tester.returnMetricsMapJSONified()))

if __name__ == '__main__':
    debug()