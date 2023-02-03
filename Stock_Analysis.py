import requests #Using requests module for webbscraping
import os
stock_list=['https://query1.finance.yahoo.com/v7/f3inance/download/%5EOMX?period1=1577379442&period2=1609001842&interval=1d&events=history&includeAdjustedClose=true', 'https://query1.finance.yahoo.com/v7/finance/download/ERIC-B.ST?period1=1577379535&period2=1609001935&interval=1d&events=history&includeAdjustedClose=true', 'https://query1.finance.yahoo.com/v7/finance/download/ELUX-B.ST?period1=1577379500&period2=1609001900&interval=1d&events=history&includeAdjustedClose=true', 'https://query1.finance.yahoo.com/v7/finance/download/AZN.ST?period1=1577379559&period2=1609001959&interval=1d&events=history&includeAdjustedClose=true', 'https://query1.finance.yahoo.com/v7/finance/download/TSLA?period1=1578194536&period2=1609816936&interval=1d&events=history&includeAdjustedClose=true']
stock_name=['OMXS30','Astra','Ericsson','Electrolux','Tesla']

def fetch_data():
  for i in range(len(stock_list)):
    req = requests.get(stock_list[i])
    url_content = req.content
    csv_file = open(stock_name[i],'wb')
    csv_file.write(url_content)
    csv_file.close()

def cleanup_data():
  for i in range(len(stock_list)):
    with open(stock_name[i]) as f:
      temp = f.read().split(",")
      del temp [0:1369]
      i = 4
      list=[]
      while (i<len(temp)-1):
        list.append(temp[i])
        i=i+6
      kurser=[]
      for ele in list:        
        a = ele.replace("'","")
        kurser.append(float(a))
      open(stock_name[i],'w')
      with open(stock_name[i], 'w') as f:
        f.write(str(kurser))

def betaVärde(Val):     #Beräkning av betavärden
  if Val=="1":
    with open('EricssonKursdata') as list:
      temp = []
      data = list.read().split(",")
      for ele in data:
        a = ele.replace("[","")
        b = a.replace("]","")
        c = float(b)
        temp.append(c)
      kvotAktie = temp[len(temp)-1]/temp[0]
      with open('omx') as list:
        temp=[]
        data = list.read().split(",")
        for ele in data:
          a = ele.replace("[","")       
          b = a.replace("]","")
          c = float(b)
          temp.append(c)
        kvotReferens = temp[len(temp)-1]/temp[0]
      beta = kvotAktie/kvotReferens
      beta = round(beta,3)
      return "Ericsson: " +str(beta)
  elif Val=="2":
    with open('ElectroluxKursdata') as list:
      temp = []
      data = list.read().split(",")
      for ele in data:
        a = ele.replace("[","")
        b = a.replace("]","")
        c = float(b)
        temp.append(c)
      kvotAktie = temp[len(temp)-1]/temp[0]
      with open('omx') as list:
        temp=[]
        data = list.read().split(",")
        for ele in data:
          a = ele.replace("[","")
          b = a.replace("]","")
          c = float(b)
          temp.append(c)
        kvotReferens = temp[len(temp)-1]/temp[0]
      beta = kvotAktie/kvotReferens
      beta = round(beta,3)
      return "Electrolux: "+str(beta)
  elif Val=="3":
    with open('AstraKursdata') as list:
      temp = []
      data = list.read().split(",")
      for ele in data:
        a = ele.replace("[","")
        b = a.replace("]","")
        c = float(b)
        temp.append(c)
      kvotAktie = temp[len(temp)-1]/temp[0]
      with open('omx') as list:
        temp=[]
        data = list.read().split(",")
        for ele in data:
          a = ele.replace("[","")
          b = a.replace("]","")
          c = float(b)
          temp.append(c)
        kvotReferens = temp[len(temp)-1]/temp[0]
      beta = kvotAktie/kvotReferens
      beta = round(beta,3)
      return "AstraZeneca: "+str(beta)
  elif Val =="4":
    with open('TeslaKursdata') as list:
      temp = []
      data = list.read().split(",")
      for ele in data:
        a = ele.replace("[","")
        b = a.replace("]","")
        c = float(b)
        temp.append(c)
      kvotAktie = temp[len(temp)-1]/temp[0]
      with open('omx') as list:
        temp=[]
        data = list.read().split(",")
        for ele in data:
          a = ele.replace("[","")
          b = a.replace("]","")
          c = float(b)
          temp.append(c)
        kvotReferens = temp[len(temp)-1]/temp[0]
      beta = kvotAktie/kvotReferens
      beta = round(beta,3)
      return "Tesla: "+str(beta)
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
def fundamental(Val): 
  if Val=="1":
    with open('Fundamental.txt', 'r') as a:
      print("\n"+"—————Fundamental analys för Ericsson————–")
      data = a.read().split(",")    
      del data[4:16]                    
      print("Företagets soliditet är "+data[1] + "%")    
      if float(data[2])<0: print("Företagets p/e-tal är negativt")
      else: print("Företagets p/e-tal är positivt")   
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
hämtaKurser()  
while (True):
  print("     -------------------Meny-------------------\n"+" 1.Fundamental analys (Vid långsiktigt aktieinnehav)\n"+" 2.Teknisk analys (Vid kort aktieinnehav)\n"+" 3.Rangordning av aktier med avseende på dess betavärde\n"+" 4.Avsluta")
  val = input(" Vilket alternativ vill du välja? ")     
  if val == "1":
    print("\nEn fundamental analys kan utföras på följande aktier:\n"+" 1.Ericsson\n"+" 2.Electrolux\n"+" 3.AstraZeneca\n"+" 4.Tesla")
    Val= input("Vilken aktie vill du göra fundamental analys på? ")
    fundamental(Val)    
  elif val == "2":
    print("\nEn teknisk analys kan utföras på följande aktier:\n"+" 1.Ericsson\n"+" 2.Electrolux\n"+" 3.AstraZeneca\n"+" 4.Tesla")
    Val= input("Vilken aktie vill du göra teknisk analys på? ")
    teknisk(Val)   
  elif val == "3":
    temp= []
    Val="3"
    for i in range(1,5):    
      temp.append(betaVärde(str(i)))        
    temp = sorted(temp,reverse=True)  
    for ele in temp:            
      print(ele)        
    print("\n")
  elif val == "4":
    os.system('clear')
    break   
  else:
    print("Felaktig inmatning, försök igen")
