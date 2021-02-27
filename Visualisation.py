from Train import Train
from Metrics import Metrics
from Prerpocessing import Prerpocessing

class Visualisation(Train, Metrics, Preprocessing):

    def plot_more_less_avg(self):

        more_than_avg, less_than_avg = self.more_less_avg()

        labels = ["More than average", "Less than average"]
        values = [more_than_avg, less_than_avg]

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

        return fig.show()

    def plot_hist(self, column):
        plt.hist(self.dataframe[column], 5, color="Blue")
        plt.title(column)
        return plt.show()

    def plot_common_hist(self):
        for column in self.dataframe.columns.to_list():
            self.plot_hist(column)

    def plot_graphs(self):

        for column in self.dataframe.columns.to_list():
            plt.plot(self.dataframe[column])
            plt.ylabel(column)
            plt.show()

    def plot_moving_average(self, column,
                            window, plot_intervals=False, 
                            scale=1.96):

      rolling_mean = self.dataframe[column].rolling(window=window).mean()
      series = self.dataframe[column]
      plt.figure(figsize=(15,5))

      plt.title("Moving average\n window size = {}".format(window))
      plt.plot(rolling_mean, "g", label="Rolling mean trend")

      # Plot confidence intervals for smoothed values
      if plot_intervals:
          mae =self.mae(series[window:], rolling_mean[window:])
          deviation = np.std(series[window:] - rolling_mean[window:])
          lower_bond = rolling_mean - (mae + scale * deviation)
          upper_bond = rolling_mean + (mae + scale * deviation)
          plt.plot(upper_bond, "r--", label="Upper Bond / Lower Bond")
          plt.plot(lower_bond, "r--")
          
      plt.plot(series[window:], label="Actual values")
      plt.legend(loc="upper left")
      plt.grid(True)
    
    def plot_exponential_smoothing(self, column, alphas):
      series = self.dataframe[column]
      with plt.style.context('seaborn-white'):    
          plt.figure(figsize=(15, 7))
          for alpha in alphas:
              plt.plot(self.exponential_smoothing(column, alpha), 
                       label="Alpha {}".format(alpha))
          plt.plot(series.values, "c", label = "Actual")
          plt.legend(loc="best")
          plt.axis('tight')
          plt.title("Exponential Smoothing")
          plt.grid(True);

    def plot_double_exponenitial_smoothing(self, column, alphas, betas):
      series = self.dataframe[column]
      with plt.style.context('seaborn-white'):    
          plt.figure(figsize=(20, 8))
          for alpha in alphas:
              for beta in betas:
                  plt.plot(self.double_exponenitial_smoothing(column, alpha, beta), 
                                  label="Alpha {}, beta {}".format(alpha, beta))
          plt.plot(series.values, label = "Actual")
          plt.legend(loc="best")
          plt.axis('tight')
          plt.title("Double Exponential Smoothing")
          plt.grid(True)
    
    def plot_Holt_Winters(self, column, plot_intervals=False, plot_anomalies=False):
      """
          series - dataset with timeseries
          plot_intervals - show confidence intervals
          plot_anomalies - show anomalies 
      """
      series = self.dataframe[column]
      model = self.pred(column, self.dataframe)

      plt.figure(figsize=(20, 10))
      plt.plot(model.result, label = "Model")
      plt.plot(series.values, label = "Actual")
      error = self.mape(series.values, model.result[:len(series)])
      plt.title("Mean Absolute Percentage Error: {0:.2f}%".format(error))
      
      if plot_anomalies:
          anomalies = np.array([np.NaN]*len(series))
          anomalies[series.values<model.LowerBond[:len(series)]] = \
              series.values[series.values<model.LowerBond[:len(series)]]
          anomalies[series.values>model.UpperBond[:len(series)]] = \
              series.values[series.values>model.UpperBond[:len(series)]]
          plt.plot(anomalies, "o", markersize=10, label = "Anomalies")
      
      if plot_intervals:
          plt.plot(model.UpperBond, "r--", alpha=0.5, label = "Up/Low confidence")
          plt.plot(model.LowerBond, "r--", alpha=0.5)
          plt.fill_between(x=range(0,len(model.result)), y1=model.UpperBond, 
                          y2=model.LowerBond, alpha=0.2, color = "grey")    
          
      plt.vlines(len(series), ymin=min(model.LowerBond), ymax=max(model.UpperBond), linestyles='dashed')
      plt.axvspan(len(series)-20, len(model.result), alpha=0.3, color='lightgrey')
      plt.grid(True)
      plt.axis('tight')
      plt.legend(loc="best", fontsize=13);

     