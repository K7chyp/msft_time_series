from sklearn.model_selection import TimeSeriesSplit 
from scipy.optimize import minimize   

from ReadData import ReadData
from Errors import Errors

class Train(ReadData, Errors): 

  def timeseriesCVscore(self, params, column, slen=10):

      # errors array
      errors = []
      alpha, beta, gamma = params
      values = self.series.values
  
      
      # set the number of folds for cross-validation
      tscv = TimeSeriesSplit(n_splits=10) 
      
      # iterating over folds, train model on each, forecast and calculate error
      for train, test in tscv.split(values):

          model = HoltWinters(self.dataframe, column, slen=slen, 
                              alpha=alpha, beta=beta, 
                              gamma=gamma, n_preds=len(test))
          model.triple_exponential_smoothing()
          
          predictions = model.result[-len(test):]
          actual = values[test]
          error = self.mae(actual, predictions)
          errors.append(error)
          
      return np.mean(np.array(errors))
  
  def pred(self, data, column): 

    # initializing model parameters alpha, beta and gamma
    x = [0, 0, 0] 

    # Minimizing the loss function 
    opt = minimize(self.timeseriesCVscore,
                   args = (column), 
                   x0=x,  
                  method="TNC", 
                   bounds = ((0, 1), (0, 1), (0, 1))
                  )
    
    alpha_final, beta_final, gamma_final = opt.x
    print(alpha_final, beta_final, gamma_final, sep='\n')

    model = HoltWinters(data, column=column,
                        slen = 10, 
                        alpha = alpha_final, 
                        beta = beta_final, 
                        gamma = gamma_final, 
                        n_preds = 10, scaling_factor = 3)

    model.triple_exponential_smoothing()