class Errors():

  @staticmethod
  def mae(y_true, y_pred):
    return np.average(np.average(np.abs(y_pred - y_true), axis=0))
  
  @staticmethod
  def mad(y_true, y_pred): 
    return np.average(np.median(np.abs(y_pred - y_true), axis=0))

  @staticmethod
  def mse(y_true, y_pred, squared=True): 
    mse = np.average(np.average((y_true - y_pred) ** 2, axis=0))
    return mse if squared else np.sqrt(mse)
    
  @staticmethod
  def mape(y_true, y_pred): 
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
