#import requests #Using requests module for webbscraping
import yfinance as yf
import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

win_res = (600,500)
tickers =['SEK=X','ERIC','ELUX-B.ST','ASTR','TSLA']

main_layout=[
  [sg.Button('1D',key='1d'),sg.Button('7D',key='7d'),sg.Button('30D',key='30d'),sg.Button('1 Year',key='1y'),sg.Button('USD/SEK',key='SEK=X'),sg.Button('ERICSSON',key='ERIC'),sg.Button('ELECTROLUX',key='ELUX-B.ST'),sg.Button('ASTRA ZENECA',key='AZN.ST'),sg.Button('TESLA',key='TSLA') ,sg.Button('Quit',key='Quit')],
  [sg.Text('Enter a ticker'), sg.InputText(key='keyword'),sg.Button('Search',key='search'),sg.Button('help',key='help')],
  [sg.Canvas(size=win_res,key='canvas'),sg.VerticalSeparator(),sg.MLine(size=(35, 35),key='mline')]
  ]

help_layout=[
  [sg.Button('Back',key='back')],
  [sg.Text('This is a program developed by Wilmer Liljenström.')],
  [sg.Text('In this program you can view some common stocks aswell as search for whatever stock you wish.', )],
  [sg.Text('The program will also calculate and show some basic fundamental and technical analytics.')],
  [sg.Text('In the search bar you can enter whatever stock or index symbol that you may find on Yahoo Finance.')],
  [sg.Text('Type in the symbol and press search, if you have typed correctly the stock should show up.')],
  [sg.Text('Betavalue is calculated with respec to the SP500(^GSPC) index.')],
  [sg.Text('Wilmer Liljenström 2023')]
]
layout = [
  [
   sg.pin(sg.Column(main_layout, key='main_layout')),
   sg.pin(sg.Column(help_layout, key='help_layout',visible=False,element_justification='c'))
  ]
]
window = sg.Window('Stock Analysis',layout,location=(0,0),element_justification='left',finalize=True)
window["mline"].Widget.configure(bg='#62768a')


# fetch_data will scrape Yahoo finance 
def fetch_data(event,length):
  symbol = yf.Ticker(event)
  prices = symbol.history(interval="1h",period=length)
  del prices["Dividends"],prices["Stock Splits"],prices["Open"],prices["High"],prices["Low"],prices["Volume"]
  return prices

def beta_value(prices,period):                        # Betavalue is defined as return of the stock divided by return of the market over the some time period
  prices = prices.to_numpy()                          # Convert dataframe to numpy array
  market = fetch_data('^GSPC',period)                 # fetch returns for market (uses SP500)
  market = market.to_numpy()
  return_of_market = market[len(market)-1]-market[0]  # always latest market day minus beginning of period
  return_of_stock = prices[len(prices)-1]-prices[0]
  beta = return_of_stock / return_of_market
  beta = round(float('.'.join(str(elem) for elem in beta)),5) # Convert tuple to float and rounds
  return str(beta)


def technical_analysis(prices):
  prices = prices.to_numpy()
  returns_over_period = (prices[len(prices)-1]-prices[0])/prices[0]
  returns_over_period = str(round(100*float('.'.join(str(elem) for elem in returns_over_period)),2))  # Goes from numpy tuple to float in order to be rounded and then to a string
  prices = np.sort(prices)  # sort in ascending order
  lowest_price = prices[0]
  lowest_price = str(round(float('.'.join(str(elem) for elem in lowest_price)),2))
  highest_price = prices[len(prices)-1]
  highest_price = str(round(float('.'.join(str(elem) for elem in highest_price)),2))
  return [returns_over_period,str(lowest_price),str(highest_price)] 

def fundamental_analysis(event):   #Solidity, p/e och p/s
  #fund = yf.Ticker(event).info  # Currently bugged, yfinance fails to decrypt Yahoo response
  event = event

   

def draw_figure(prices,canvas):    # Method to plot and draw price history on Tkinter canvas object
    plt.plot(prices)
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.title('Value of stock Over Time')
    plot = plt.gcf()
    if not hasattr(draw_figure, 'canvas_packed'):
        draw_figure.canvas_packed = {}
    figure_canvas_agg = FigureCanvasTkAgg(plot, canvas)
    figure_canvas_agg.draw()
    widget = figure_canvas_agg.get_tk_widget()
    if widget not in draw_figure.canvas_packed:
        draw_figure.canvas_packed[widget] = plot
        widget.pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    draw_figure.canvas_packed.pop(figure_agg.get_tk_widget())
    plt.close('all')

def program_loop():
  period = '30d'
  while (True):
    event, values = window.read()

    if event =='SEK=X':
      if 'figure_agg' in locals(): delete_figure_agg(figure_agg)
      prices = fetch_data(event,period)
      beta = beta_value(prices,period)
      tech_analysis = technical_analysis(prices)
      fund_analysis = fundamental_analysis(event)
      window['mline'].update(value='TECHNICAL ANALYSIS'+'\n\nReturns for the period is: '+tech_analysis[0]+'%\n\n'+'Beta value is: '+beta+'\n\nLowest price for the period: '+tech_analysis[1]+'\n\nHighest price for the period: '+tech_analysis[2])
      figure_agg=draw_figure(prices, window['canvas'].TKCanvas)

    elif event=='ERIC':
      if 'figure_agg' in locals(): delete_figure_agg(figure_agg)
      prices = fetch_data(event,period)
      beta = beta_value(prices,period)
      tech_analysis = technical_analysis(prices)
      fund_analysis = fundamental_analysis(event)
      window['mline'].update(value='TECHNICAL ANALYSIS'+'\n\nReturns for the period is: '+tech_analysis[0]+'%\n\n'+'Beta value is: '+beta+'\n\nLowest price for the period: '+tech_analysis[1]+'\n\nHighest price for the period: '+tech_analysis[2])
      figure_agg=draw_figure(prices, window['canvas'].TKCanvas)

    elif event=='ELUX-B.ST':
      if 'figure_agg' in locals(): delete_figure_agg(figure_agg)
      prices = fetch_data(event,period)
      beta = beta_value(prices,period)
      tech_analysis = technical_analysis(prices)
      fund_analysis = fundamental_analysis(event)
      window['mline'].update(value='TECHNICAL ANALYSIS'+'\n\nReturns for the period is: '+tech_analysis[0]+'%\n\n'+'Beta value is: '+beta+'\n\nLowest price for the period: '+tech_analysis[1]+'\n\nHighest price for the period: '+tech_analysis[2])
      figure_agg=draw_figure(prices, window['canvas'].TKCanvas)

    elif event=='AZN.ST':
      if 'figure_agg' in locals(): delete_figure_agg(figure_agg)
      prices = fetch_data(event,period)
      beta = beta_value(prices,period)
      tech_analysis = technical_analysis(prices)
      fund_analysis = fundamental_analysis(event)
      window['mline'].update(value='TECHNICAL ANALYSIS'+'\n\nReturns for the period is: '+tech_analysis[0]+'%\n\n'+'Beta value is: '+beta+'\n\nLowest price for the period: '+tech_analysis[1]+'\n\nHighest price for the period: '+tech_analysis[2])
      figure_agg=draw_figure(prices, window['canvas'].TKCanvas)

    elif event=='TSLA':
      if 'figure_agg' in locals(): delete_figure_agg(figure_agg)
      prices = fetch_data(event,period)
      beta = beta_value(prices,period)
      tech_analysis = technical_analysis(prices)
      fund_analysis = fundamental_analysis(event)
      window['mline'].update(value='TECHNICAL ANALYSIS'+'\n\nReturns for the period is: '+tech_analysis[0]+'%\n\n'+'Beta value is: '+beta+'\n\nLowest price for the period: '+tech_analysis[1]+'\n\nHighest price for the period: '+tech_analysis[2])
      figure_agg=draw_figure(prices, window['canvas'].TKCanvas)

    elif event=='search':
      search = values['keyword']
      try: prices = fetch_data(search,period)
      except:continue
      if 'figure_agg' in locals(): delete_figure_agg(figure_agg)
      beta = beta_value(prices,period)
      tech_analysis = technical_analysis(prices)
      fund_analysis = fundamental_analysis(search)
      window['mline'].update(value='TECHNICAL ANALYSIS'+'\n\nReturns for the period is: '+tech_analysis[0]+'%\n\n'+'Beta value is: '+beta+'\n\nLowest price for the period: '+tech_analysis[1]+'\n\nHighest price for the period: '+tech_analysis[2])
      figure_agg=draw_figure(prices, window['canvas'].TKCanvas)

    elif event=='help':
      window['main_layout'].update(visible=False)
      window['help_layout'].update(visible=True)
      event, values = window.read()
      if event=='back':
        window['main_layout'].update(visible=True)
        window['help_layout'].update(visible=False)
        
    elif event=='1d'or'7d'or'30d': 
      period = event
      print("Please reselect the stock you wish to view to update period")

    if event in (sg.WIN_CLOSED, 'Quit'):
            break
    
program_loop()
window.close()
