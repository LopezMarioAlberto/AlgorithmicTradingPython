# -*- coding: utf-8 -*-
"""CryptoDashboard.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pzerbSrw4IXkT7-M94P-2wToKR3yVtyl
"""

!pip install --upgrade plotly

import datetime as dt
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as web

# Get the stock quote
crypto_currency = 'BNB'  # BTC
against_currency = 'EUR'
data_source ='yahoo'
period = 100

start = dt.datetime(2012, 1, 1)
end = dt.datetime.now()

ticket = f'{crypto_currency}-{against_currency}'

df = web.DataReader(ticket, data_source=data_source, start=start, end=end)

df.tail()

df.dtypes

df.index

df['Normalized'] = df['Close'] / df['Close'].iloc[0]
df['Normalized'].min(), df['Normalized'].argmin(), df['Normalized'].max(), df['Normalized'].argmax(), df['Normalized'].mean(), df['Normalized'].std()

df.iloc[180], df.iloc[589]

df.drop(labels=['Normalized'], axis=1, inplace=True)
df.head()

df.reset_index(inplace = True)
df.set_index(["Date"])
df.head()

sma = df['Close'].rolling(window=20).mean()  # Simple moving average (SMA)
std = df['Close'].rolling(window=20).std()  # Standard deviation
df['Upper'] = sma + (std *2)  # Bollinger band
df['Lower'] = sma - (std *2)  # Bollinger band

df['Short'] = df.Close.ewm(span=20, adjust=False).mean()  # Exponential moving average 20 days
df['Long'] = df.Close.ewm(span=50, adjust=False).mean()  # Exponential moving average 50 days

df['20MA'] = sma  # 20 moving average (20MA)
df['50MA'] = df['Close'].rolling(window=50).mean()  # 50 moving average (50MA)
df['200MA'] = df['Close'].rolling(window=200).mean()  # 200 moving average (200MA)

shortema = df.Close.ewm(span=12, adjust=False).mean()  # Exponential moving average 12 days
longema = df.Close.ewm(span=26, adjust=False).mean()  # Exponential moving average 26 days
df['MACD'] = shortema - longema  # MACD
df['Signal'] = df.MACD.ewm(span=9, adjust=False).mean()  # Exponential moving average 9 days

high14 = df['High'].rolling(14).max()
low14 = df['Low'].rolling(14).min()
df['%K'] = (df['Close'] - low14)*100/(high14 - low14)
df['%D'] = df['%K'].rolling(3).mean()

df['PClose'] = df['Adj Close'].shift()  # previous Close
df['High-Low'] = df['High'] - df['Low']  # Condition 1: High - Low
df['High-PClose'] = abs(df['High'] - df['PClose'])  # Condition 2: High - Previous Close
df['Low-PClose'] = abs(df['Low'] - df['PClose'])  # Condition 3: Low - Previous Close
df['TrueRange'] = df[['High-Low', 'High-PClose', 'Low-PClose']].max(axis=1) # True Range
df['ATR'] = df.TrueRange.rolling(window=14).mean() / df['Adj Close'] *100  # Average True Range 14 days %

df

df = df.loc[df.shape[0]-period:]
df.reset_index(inplace = True)
df.head()

fig, axs = plt.subplots(5, 1, figsize=(15, 20))

# Closed Price + 20MA + 50MA
axs[0].plot(df['Date'], df['Close'], color='blue')
axs[0].plot(df['Date'], df['20MA'], label='20MA', color='black', dashes=[3, 2])
axs[0].plot(df['Date'], df['50MA'], label='50MA', color='orange', dashes=[6, 2])
axs[0].plot(df['Date'], df['200MA'], label='200MA', color='pink', dashes=[6, 2])
axs[0].set(xticklabels=[])
axs[0].grid(True)
axs[0].legend(loc="upper right")

# Volume
axs[1].fill_between(df['Date'], df['Volume'])
axs[1].set(xticklabels=[])
axs[1].grid(True)

# ATR
axs[2].plot(df['Date'], df['ATR'], label='ATR', color='brown')
axs[2].set(xticklabels=[])
axs[2].grid(True)
axs[2].legend(loc="upper right")

# MACD
axs[3].plot(df['Date'], df['MACD'], label='MACD', color='green')
axs[3].plot(df['Date'], df['Signal'], label='Signal', color='#483040', dashes=[3, 2])
axs[3].fill_between(df['Date'], df['MACD'], color='#809C7C')
axs[3].axhline(y = 0, color = 'black', dashes=[1, 2])
axs[3].set(xticklabels=[])
axs[3].grid(True)
axs[3].legend(loc="upper right")

# Bolinger
axs[4].fill_between(df['Date'], df['Upper'], df['Lower'], color='silver')
axs[4].plot(df['Date'], df['Close'], color='gold', lw=3, label='Close Price')
axs[4].plot(df['Date'], df['Short'], color='brown', dashes=[1, 2], lw=3, label='Short')
axs[4].plot(df['Date'], df['Long'], color='orange', dashes=[1, 2], lw=3, label='Long')
axs[4].tick_params(axis='x', rotation=90)
axs[4].grid(True)
axs[4].legend(loc="upper right")

# fig.tight_layout()
plt.show()

# Stochastic oscillator
fig, ax = plt.subplots(figsize=(15, 10))
df[['%K', '%D']].plot(ax=ax)
ax.axhline(80, c='r', alpha=0.3)
ax.axhline(20, c='r', alpha=0.3)
df['Close'].plot(ax=ax, alpha=0.3, secondary_y=True)

import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.options.plotting.backend = "plotly"

Closed_Price = go.Scatter(
    x=df['Date'],
    y=df['Close'],
    name='Price',
    line_color='blue',
)
MA20 = go.Scatter(
    x=df['Date'],
    y=df['20MA'],
    name='20MA',
    line_color='black',
)
MA50 = go.Scatter(
    x=df['Date'],
    y=df['50MA'],
    name='50MA',
    line_color='orange',
)
MA200 = go.Scatter(
    x=df['Date'],
    y=df['200MA'],
    name='200MA',
    line_color='pink',
)
Short = go.Scatter(
    x=df['Date'],
    y=df['Short'],
    name='Short',
    line_color='green',
    line_dash='dot',
)
Long = go.Scatter(
    x=df['Date'],
    y=df['Long'],
    name='Long',
    line_color='green',
    line_dash='dash',
)
Upper = go.Scatter(
    x=df['Date'],
    y=df['Upper'],
    name='Upper',
    line_color='silver',
)
Lower = go.Scatter(
    x=df['Date'],
    y=df['Lower'],
    name='Lower',
    fill='tonexty', # fill area between
    mode='lines',
    line_color='silver',
)
data = [Closed_Price, MA20, MA50, MA200, Short, Long, Upper, Lower]
layout = go.Layout(yaxis=dict())
fig = go.Figure(data=data, layout=layout)
fig.update_layout(
    title='Closed Price',
    yaxis_title='Price',
    xaxis_title='Dates',
    legend_title='Indicator',
    )
fig.show()

Volume = go.Scatter(
    x=df['Date'],
    y=df['Volume'],
    name='Volume',
    line_color='blue',
    fill='tonexty', # fill area between
    mode='lines',
)
layout = go.Layout(yaxis=dict())
fig = go.Figure(data=Volume, layout=layout)
#fig.add_hline(y=0, line_color="green")
fig.update_layout(
    title='Volume',
    yaxis_title='Operations',
    xaxis_title='Dates',
    xaxis_tickangle=-90,
    legend_title='Indicator',
    )
fig.show()

ATR = go.Scatter(
    x=df['Date'],
    y=df['ATR'],
    name='ATR',
    line_color='brown',
    )
layout = go.Layout(yaxis=dict())
fig = go.Figure(data=ATR, layout=layout)
fig.update_layout(
        title='ATR',
        yaxis_title='ATR %',
        xaxis_title='Dates',
        legend_title='Indicator',
)
fig.show()

MACD = go.Scatter(
    x=df['Date'],
    y=df['MACD'],
    name='MACD',
    line_color='green',
    fill='tonexty', # fill area between
    mode='lines',
)
Signal = go.Scatter(
    x=df['Date'],
    y=df['Signal'],
    name='Signal',
    line_color='purple',
    line_dash='dot',
)
data = [MACD, Signal]
layout = go.Layout(yaxis=dict())
fig = go.Figure(data=data, layout=layout)
fig.add_hline(y=0, line_color="green")
fig.update_layout(
    title='MACD',
    yaxis_title='MACD',
    xaxis_title='Dates',
    legend_title='Indicator',
    )
fig.show()

# data2 = web.get_data_stooq(ticket, start)
# nasdaq_sym = web.get_nasdaq_symbols()
# nasdaq_sym.loc['AAPL']

df['%-chg'] = df['Close'].pct_change()
df.head()

df['Log returns'] = np.log(df['Close']/df['Close'].shift())
df.head()

dpy = 252  # Working days per year
volatility = df['Log returns'].std()*dpy**.5
volatility