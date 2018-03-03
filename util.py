import matplotlib.pyplot as plt
import numpy as np
from pylab import savefig
from datetime import datetime
from cryptocompy import price
from sklearn.preprocessing import normalize
import pandas as pd
import time

class plot_every_hour:
    def __init__(self):
        self.filename = './data/XRP_ETH_BTC.csv'
    
    def run(self,minutes=1,save=None):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        
        XRP,ETH,BTC = self.get_data(minutes)        
        
        XRP['XRP']=(XRP.close+XRP.open)/2
        ETH['ETH']=(ETH.close+ETH.open)/2
        BTC['BTC']=(BTC.close+BTC.open)/2

        df_XRP_min = pd.DataFrame(XRP)
        df_ETH_min = pd.DataFrame(ETH)
        df_BTC_min = pd.DataFrame(BTC)
        df_combined_min = pd.concat([ETH.time,df_XRP_min.XRP,df_ETH_min.ETH,df_BTC_min.BTC],axis=1)

        if save=='save':
            timestr = time.strftime("%Y%m%d-%H%M%S")
            filename = './data/ARCHIVE/time_{}.csv'.format(timestr)
        else:
            filename = self.filename
       
        df_combined_min.to_csv(filename, sep='\t', header=False, index=False)
        pd.DataFrame.from_csv(filename).append(df_combined_min).drop_duplicates().to_csv(filename,sep='\t',header=False, index=False)
        
        print('saving {}...'.format(filename))
    
    def get_data(self,minutes):
        xrp = price.get_historical_data('XRP', 'KRW', 'minute', e='Bithumb',aggregate=minutes, limit=2000)
        eth = price.get_historical_data('ETH', 'KRW', 'minute', e='Bithumb',aggregate=minutes, limit=2000)
        btc = price.get_historical_data('BTC', 'KRW', 'minute', e='Bithumb',aggregate=minutes, limit=2000)
        XRP = pd.DataFrame(xrp)
        ETH = pd.DataFrame(eth)
        BTC = pd.DataFrame(btc)
        return XRP,ETH,BTC
    
    def plot_func(self):
        filename = self.filename

        df0 = pd.DataFrame.from_csv(filename,sep='\t',header=None,index_col=False)
        df = df0.iloc[1:,:]
        df.reset_index(level=0,col_level=0)
        df.columns = ['BTC','ETH','XRP','time']
        
        normalized_ETH = normalize([df.ETH]).ravel()
        normalized_XRP = normalize([df.XRP]).ravel()
        normalized_BTC = normalize([df.BTC]).ravel()

        d_axis =  [int(datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S').timestamp()) for x in df.time]

        self.plot_combined(d_axis,normalized_ETH,normalized_XRP,normalized_BTC)
        
    def plot_combined(self,d_axis,ETH,XRP,BTC):            
        fig=plt.figure(figsize=(28, 14))
        ax2=fig.add_subplot(1,1,1)
        ax2.plot(d_axis,ETH,'r',label='ethereum')
        ax2.plot(d_axis,BTC,'b',label='bitcoin')
        ax2.plot(d_axis,XRP,'y',label='ripple')
        ax2.legend()

        filename = './data/combined_EXB.png'
        savefig(filename)