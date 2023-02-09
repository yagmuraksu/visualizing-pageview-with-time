import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df.set_index('date', inplace=True)

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025))
        & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
  # Draw line plot
  num_of_rows = df.shape[0]
  fig, ax = plt.subplots(figsize=(15, 5))
  ax = sns.lineplot(data=df, x='date', y='value', color='red')
  ax.set_xlabel('Date')
  ax.set_ylabel('Page Views')
  ax.set_xticks([
    df.index.min(), df.index[num_of_rows * 25 // 100],
    df.index[num_of_rows * 50 // 100], df.index[num_of_rows * 75 // 100],
    df.index.max()
  ])
  plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
  # Copy and modify data for monthly bar plot
  df_bar = df.copy()
  df_bar['year'] = pd.DatetimeIndex(df.index).year
  df_bar['month'] = pd.DatetimeIndex(df.index).month
  df_bar = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()
  df_bar = df_bar.sort_values(['month'])
  months = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
  ]
  for i in range(0, 12):
    df_bar.loc[df_bar['month'] == i + 1, 'month'] = months[i]
  df_bar.columns = ['year', 'month', 'value']

  # Draw bar plot
  fig, ax = plt.subplots(figsize=(15, 15))
  ax = sns.barplot(data=df_bar,
                   x='year',
                   y='value',
                   hue='month',
                   palette='tab10')
  ax.set_xlabel('Years')
  ax.set_ylabel('Average Page Views')
  plt.legend(title='Months', loc='upper left')

  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig


def draw_box_plot():
  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = pd.DatetimeIndex(df.index).year
  df_box['month'] = pd.DatetimeIndex(df.index).month
  df_box = df_box.sort_values(['month'])
  months_short = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
    'Nov', 'Dec'
  ]
  for i in range(0, 12):
    df_box.loc[df_box['month'] == i + 1, 'month'] = months_short[i]

  # Draw box plots (using Seaborn)
  fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(25, 15))
  ax1 = plt.subplot(121)
  ax1 = sns.boxplot(data=df_box, x='year', y='value')
  ax1.set_title("Year-wise Box Plot (Trend)")
  ax1.set_xlabel("Year")
  ax1.set_ylabel("Page Views")
  ax2 = plt.subplot(122)
  ax2 = sns.boxplot(data=df_box, x='month', y='value')
  ax2.set_title("Month-wise Box Plot (Seasonality)")
  ax2.set_xlabel("Month")
  ax2.set_ylabel("Page Views")

  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig
