import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from datetime import datetime

def nice_axes(ax):
    ax.set_facecolor('.9')
    ax.tick_params(labelsize=8, length=0)
    # ax.grid(True, axis='x', color='white')
    ax.set_axisbelow(True)
    [spine.set_visible(False) for spine in ax.spines.values()]


class RacingBarChart:
    def __init__(
        self,
        data, 
        date_column_name,
        labels=None,
        title=None,
        colors=None,
        figsize=(30,30),
        dpi=144,
        fps=10,
        num_bars=None
    ):
        self.__data = data
        self.__processed_data = None
        self.__date_column_name = date_column_name
        self.__labels = labels
        self.__title = title
        self.__colors = colors
        self.__figsize = figsize
        self.__dpi = dpi
        self.__fig = plt.Figure(figsize=self.__figsize, dpi=self.__dpi)
        self.__ax = self.__fig.add_subplot()
        self.__fps = fps
        self.__num_bars = num_bars

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def _expand_data(self, insert_num_rows=10):
        data_temp = self.__data[:]
        data_temp = data_temp.reset_index()
        data_temp.index = data_temp.index*insert_num_rows

        last_idx = data_temp.index[-1]+1
        data_expanded = data_temp.reindex(range(last_idx))
        data_expanded[self.__date_column_name] = data_expanded[self.__date_column_name].fillna(method='ffill')
        data_expanded = data_expanded.set_index(self.__date_column_name)
        data_expanded_ranked = data_expanded.rank(axis=1, method='first')
        data_expanded = data_expanded.interpolate()
        data_expanded_ranked = data_expanded_ranked.interpolate()
        return data_expanded, data_expanded_ranked
    
    def _initialise_chart(self):
        self.__ax.clear()
        nice_axes(self.__ax)


    def _animate(self, idx):
        y = self.__processed_data[1].iloc[idx]
        width = self.__processed_data[0].iloc[idx]
        self.__ax.barh(y=y, width=width, color=self.__colors, tick_label=self.__labels)
        self.__ax.tick_params(axis='x', labelsize=40)
        self.__ax.tick_params(axis='y', labelsize=30)
        date_str = self.__processed_data[0].index[idx].strftime('%B %d, %Y')
        print('{} Done'.format(date_str))
        self.__ax.set_title(self.__title, fontsize='large') if self.__title is not None else None

        # set limit to display all bars
        if self.__num_bars is None:
            self.__ax.set_ylim(0, self.__processed_data[0].shape[1]+0.5)
        else:
            upper = self.__processed_data[0].shape[1]+0.5
            lower = upper - self.__num_bars
            self.__ax.set_ylim(lower, upper)

    def plot_race(self, saveas=None):
        self.__processed_data = self._expand_data()
        # print(self.__processed_data)
        anim = FuncAnimation(fig=self.__fig, func=self._animate, init_func=self._initialise_chart, frames=self.__processed_data[0].shape[0], 
                     interval=100, repeat=False, save_count=self.__processed_data[0].shape[0])

        writervideo = animation.FFMpegWriter(fps=self.__fps)
        save_name = saveas if saveas is not None else 'output_' + datetime.now().strftime('%d_%b_%Y_%H_%M_%S') + '.mp4'
        anim.save(save_name, writer=writervideo)
        plt.close()


if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    merged = pd.read_csv('F:/work_learning/Chart Animation/poc/merged3.csv', parse_dates=['Year'], index_col='Year')
    merged = merged.sort_index()


    # formatting values
    for col in merged.columns:
        # print(col)
        merged[col] = merged[col].apply(lambda x: float(x.replace(',','')))
    
    labels = merged.columns
    labels = [label.replace('_Fossil CO2Emissions(tons)', '') for label in labels]
    rbc = RacingBarChart(
        merged,
        'Year',
        labels=labels,
        title='CO2-Emissions',
        colors=plt.cm.Dark2(np.linspace(.1, .9, 15)),
        num_bars=6
    )
    rbc.plot_race()