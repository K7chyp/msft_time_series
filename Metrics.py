class Metrics:

    def __init__(self, dataframe):
        self.dataframe = dataframe.copy()

    def get_min_max(self, column):
        return min(self.dataframe[column].to_list()), max(
            self.dataframe[column].to_list()
        )

    def get_average(self, column):
        sum_ = 0
        for value in self.dataframe[column]:
            sum_ = value
        return sum_ / len(self.dataframe)

    def more_less_avg(self, column):

        avg = self.get_average(column)
        more_than_avg = 0
        less_than_avg = 0

        for value in self.dataframe[column].to_list():
            if value >= avg:
                more_than_avg += 1
            else:
                less_than_avg += 1

        return more_than_avg, less_than_avg
    
    def get_mode(self, column):

        mode_ = max(
            set(self.dataframe[column].to_list()),
            key=self.dataframe[column].to_list().count,
        )

        return mode_

    def get_stat(self, column):

        min_, max_ = self.get_min_max(column)
        avg_ = self.get_average(column)
        mta, lta = self.more_less_avg(column)
        mode_ = self.get_mode(column)

        return print(
            f"Minimum {min_}",
            f"Maximum {max_}",
            f"Average {avg_}",
            f"Mode {mode_} ",
            f"More than average {mta}",
            f"Less than averange {lta} ",
            sep="\n",
        )
