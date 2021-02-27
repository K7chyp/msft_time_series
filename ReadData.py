class ReadData(): 

  def __init__(self, dataframe, column): 
    self.dataframe = dataframe.copy()
    self.series = self.dataframe[column]