#!/bin/python

import json
from time import time

def get_stats():
  with open('../web/data.json') as f:
    data = json.load(f)

    # Store some stats while parsing through
    lastTime = 0
    lastWeight = 0
    high = -999
    low = 999
    averageWeight = 0
    totalWeights = 0

    current = time()
    previousMonth = (current - (60 * 60 * 24 * 30)) * 1000

    for key in data:
      value = float(data[key])

      # Set last weight based on last time (handles incorrectly sorted lists)
      if int(key) > lastTime:
        lastTime = int(key)
        lastWeight = value

      # Only keep track of the past month of averages
      if int(key) >= previousMonth:
        if value < low:
          low = value

        if value > high:
          high = value

        averageWeight += value
        totalWeights += 1

    if lastWeight > 0:
      lastWeight = round(lastWeight, 1)
    else:
      lastWeight = '?'

    if averageWeight > 0 and totalWeights > 0:
      averageWeight = round(averageWeight / totalWeights, 1)
    else:
      averageWeight = '?'

    if low < 999:
      low = round(low, 1)
    else:
      low = '?'

    if high > -999:
      high = round(high, 1)
    else:
      high = '?'

    stats = {
      'averageWeight': averageWeight,
      'high': high,
      'lastWeight': lastWeight,
      'low': low
    }

    with open('../web/stats.json', 'w') as s:
      json.dump(stats, s, sort_keys=True, indent=2)

    print "last weight: " + str(lastWeight)
    print "30 day average: " + str(averageWeight)
    print "30 day low: " + str(low)
    print "30 day high: " + str(high)
