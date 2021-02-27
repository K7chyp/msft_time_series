class Preprocessing():

  def  __init__(self, dataframe): 
    self.dataframe = dataframe.copy()
  
  def weighted_average(self, column, weights):
    result = 0.0
    weights.reverse()
    series = self.dataframe[column]
    for n in range(len(weights)):
        result += series.iloc[-n-1] * weights[n]
    return float(result) 
  
  def exponential_smoothing(self, column, alpha):
    series = self.dataframe[column]
    result = [series[0]] 
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result

  def double_exponenitial_smoothing(self, column, alpha, beta):

    series = self.dataframe[column]
    result = [series[0]]
    for n in range(1, len(series)+1):
        if n == 1:
            level, trend = series[0], series[1] - series[0]
        if n >= len(series): # forecasting
            value = result[-1]
        else:
            value = series[n]
        last_level, level = level, alpha*value + (1-alpha)*(level+trend)
        trend = beta*(level-last_level) + (1-beta)*trend
        result.append(level+trend)
    return result