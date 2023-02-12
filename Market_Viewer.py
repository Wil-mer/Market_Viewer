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



"""
def teknisk(Val):
  if Val=="1":
    with open('EricssonKursdata', 'r') as a:
      print("\n"+"————Teknisk analys för Ericsson—————")
      temp = a.read().split(",")
      kurs = []
      for ele in temp:
        a = ele.replace("[","")
        b = a.replace("]","")
        c = float(b)
        kurs.append(c)
      kursUtv = (kurs[len(kurs)-1] - kurs[0])*100/kurs[0]
      print("Kursutveckling senaste 30 dagarna: " + str(round(kursUtv, 1))+"%")
      beta = betaVärde(Val)
      print("Betavärde " + str(beta))
      print("lägsta kurs(30 senaste dagarna) "+str(round(min(kurs), 1)))
      print("Högsta kurs(30 senaste dagarna) "+str(round(max(kurs), 1))+"\n")
  elif Val == "2":
    print("\n"+"————Teknisk analys för Electrolux")
    with open('ElectroluxKursdata', 'r') as a:
      temp = a.read().split(",")
      kurs = []
      for ele in temp:
        a = ele.replace("[","")
        b = a.replace("]","")
        c = float(b)
        kurs.append(c)
      kursUtv = (kurs[len(kurs)-1] - kurs[0])*100/kurs[0]
      print("Kursutveckling senaste 30 dagarna: " + str(round(kursUtv, 1))+"%")
      beta = betaVärde(Val)
      print("Betavärde " + beta)
      print("lägsta kurs(30 senaste dagarna) "+str(round(min(kurs), 1)))
      print("Högsta kurs(30 senaste dagarna) "+str(round(max(kurs), 1))+"\n")
  elif Val == "3":
    print("\n"+"————Teknisk analys för AstraZeneca—————")
    with open('AstraKursdata', 'r') as a:
      temp = a.read().split(",")
      kurs = []
      for ele in temp:
        a = ele.replace("[","")
        b = a.replace("]","")
        c = float(b)
        kurs.append(c)
      kursUtv = (kurs[len(kurs)-1] - kurs[0])*100/kurs[0]
      print("Kursutveckling senaste 30 dagarna: " + str(round(kursUtv,1))+"%")
      beta = betaVärde(Val)
      print("Betavärde " + beta)
      print("lägsta kurs(30 senaste dagarna) "+str(round(min(kurs), 1)))
      print("Högsta kurs(30 senaste dagarna) "+str(round(max(kurs), 1))+"\n")
  elif Val == "4":
    print("\n"+"————Teknisk analys för Tesla—————")
    with open('TeslaKursdata', 'r') as a:
      temp = a.read().split(",")
      kurs = []
      for ele in temp:
        a = ele.replace("[","")
        b = a.replace("]","")
        c = float(b)
        kurs.append(c)
      kursUtv = (kurs[len(kurs)-1] - kurs[0])*100/kurs[0]
      print("Kursutveckling senaste 30 dagarna: " + str(round(kursUtv,1))+"%")
      beta = betaVärde(Val)
      print("Betavärde " + beta)
      print("lägsta kurs(30 senaste dagarna) "+str(round(min(kurs), 1)))
      print("Högsta kurs(30 senaste dagarna) "+str(round(max(kurs), 1))+"\n")
  else: print("Felaktig inmatning, försök igen")
"""

"""
def fundamental(Val):   #Utskrivning av fundamental analys
  if Val=="1":
    with open('Fundamental.txt', 'r') as a:
      print("\n"+"—————Fundamental analys för Ericsson————–")
      data = a.read().split(",")          #Hämta data från fil
      del data[4:16]                      #Ta bort data för övriga aktier 
      print("Företagets soliditet är "+data[1] + "%")    
      if float(data[2])<0: print("Företagets p/e-tal är negativt")
      else: print("Företagets p/e-tal är positivt")        #Printa data
      print("Företagets p/s tal är "+data[3]+"\n")
  elif Val=="2":
    print("\n"+"—————Fundamental analys för Electrolux————–")
    with open('Fundamental.txt', 'r') as a:
      data = a.read().split(",")
      del data[0:4]
      del data[4:16]
      print("Företagets soliditet är "+data[1] + "%")
      if float(data[2])<0: print("Företagets p/e-tal är negativt")
      else: print("Företagets p/e-tal är positivt")
      print("Företagets p/s tal är "+data[3]+"\n")
  elif Val=="3":
    print("\n"+"—————Fundamental analys för AstraZeneca————–")
    with open('Fundamental.txt', 'r') as a:
      data = a.read().split(",")
      del data[0:8]
      del data[12:16]
      print("Företagets soliditet är "+data[1] + "%")
      if float(data[2])<0: print("Företagets p/e-tal är negativt")
      else: print("Företagets p/e-tal är positivt")
      print("Företagets p/s tal är "+data[3]+"\n")
  elif Val=="4":
    print("\n"+"—————Fundamental analys för Tesla————–")
    with open('Fundamental.txt', 'r') as a:
      data = a.read().split(",")
      del data[0:12]
      print("Företagets soliditet är "+data[1] + "%")
      if float(data[2])<0: print("Företagets p/e-tal är negativt")
      else: print("Företagets p/e-tal är positivt")
      print("Företagets p/s tal är "+data[3]+"\n")
  else: print("Felaktig inmatning, försök igen")
"""