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
    
    def plot_func(self,save=None):
        filename = self.filename

        df0 = pd.DataFrame.from_csv(filename,sep='\t',header=None,index_col=False)
        df = df0.iloc[1:,:]
        df.reset_index(level=0,col_level=0)
        df.columns = ['BTC','ETH','XRP','time']
        
        normalized_ETH = normalize([df.ETH]).ravel()
        normalized_XRP = normalize([df.XRP]).ravel()
        normalized_BTC = normalize([df.BTC]).ravel()

        d_axis =  [int(datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S').timestamp()) for x in df.time]
        
        fig=plt.figure(figsize=(28, 14))
        ax1 = fig.add_subplot(1,2,1)
        
        ax1.scatter(normalized_XRP, normalized_ETH ,c=normalize([d_axis]).ravel())

        min_val = np.min([np.min(normalized_XRP),np.min(normalized_ETH)])
        max_val = np.max([np.max(normalized_XRP),np.max(normalized_ETH)])
        
        ax2 = fig.add_subplot(1,2,2)
        ax2.scatter(normalized_BTC, normalized_ETH ,c=normalize([d_axis]).ravel())

        min_val = np.min([np.min(normalized_BTC),np.min(normalized_ETH)])
        max_val = np.max([np.max(normalized_BTC),np.max(normalized_ETH)])
        
        if save=='save':
            timestr = time.strftime("%Y%m%d-%H%M%S")
            filename = './data/ARCHIVE/normalized_correlation_{}.png'.format(timestr)
        else:
            filename = './data/normalized_correlation.png'#.format(timestr)
        
        savefig(filename,bbox_inches='tight')

        self.plot_combined(d_axis,normalized_ETH,normalized_XRP,normalized_BTC,save)
        
    def plot_combined(self,d_axis,ETH,XRP,BTC,save):            
        fig=plt.figure(figsize=(28, 14))
        ax=fig.add_subplot(2,1,1)
        ax.scatter(d_axis,ETH,c=d_axis, label='ethereum',marker='>',s=80)
        ax.scatter(d_axis,BTC,c=d_axis,label='bitcoin',marker='+',s=40)
        ax.scatter(d_axis,XRP,c=d_axis,label='ripple',marker=(5,0),s=10)
        ax.legend()
        ax2=fig.add_subplot(2,1,2)
        ax2.plot(d_axis,ETH,'r',label='ethereum')
        ax2.plot(d_axis,BTC,'b',label='bitcoin')
        ax2.plot(d_axis,XRP,'y',label='ripple')
        ax2.legend()
        if save=='save':
            timestr = time.strftime("%Y%m%d-%H%M%S")
            filename = './data/ARCHIVE/combined_EXB_{}.png'.format(timestr)
        else:
            filename = './data/combined_EXB.png'#.format(timestr)
        savefig(filename)
        #fig.close()
     
    def plot_static(self,minutes = 1):
        XRP,ETH,BTC = self.get_data(minutes)
        
        normalized_ETH = normalize([ETH.close]).ravel()
        direction=np.sign(ETH.close-ETH.open)
        vol = direction*(ETH.volumeto - ETH.volumefrom)
        normalized_ETH_VOL = [vol]
        c_data =  [int(datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S').timestamp()) for x in ETH.time]
        plt.scatter(normalized_ETH,np.cumsum(normalized_ETH_VOL),c=c_data)
      
        min_val = np.min(normalized_ETH)
        max_val = np.max(normalized_ETH)
        plt.colorbar()
        plt.xlim(min_val,max_val)
        filename = './data/ETH.png'
        savefig(filename)
        plt.close()
        
    def plot_static2(selfminutes = 1):
        XRP,ETH,BTC = self.get_data(minutes)
        
        normalized_ETH = [ETH.close]
        direction=np.sign(ETH.close-ETH.open)
        vol = direction*(ETH.volumeto - ETH.volumefrom)
        normalized_ETH_VOL = [vol]
        c_data =  [int(datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S').timestamp()) for x in ETH.time]
        plt.scatter(normalized_ETH,np.cumsum(normalized_ETH_VOL),c=c_data)
        plt.colorbar()
        min_val = np.min(normalized_ETH)
        max_val = np.max(normalized_ETH)
   
        plt.xlim(min_val,max_val)
        filename = './data/ETH2.png'
        savefig(filename)
        plt.close
    
    def get_coins(self,minutes=1):
        XRP,ETH,BTC = self.get_data(minutes)
        coins=[XRP,ETH,BTC]
        return coins
    
    def plot_static3(self,minutes=1,save=None):
        coins = self.get_coins(minutes)
        self.plot_resistant(coins,minutes,save)
    
    def get_vol(self,coin):
        direction=np.sign(coin.close-coin.open)
        vol = direction*(coin.volumeto)# - coin.volumefrom)
        color_data =  [int(datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S').timestamp()) for x in coin.time]
        return vol,color_data
    
    def safe_div(self,x,y):
        if y == 0:
            return 0
        return x / y
    
    def plot_resistant(self,coins,minutes,save):
        line_thk = 0.6
        if minutes == 1: 
            markersize = 30
        else:
            markersize = 150
        fig=plt.figure(figsize=(40, 50))
        ax=fig.add_subplot(4,3,1)
        for i,coin in enumerate(coins):
            vol,c_data = self.get_vol(coin)
            normalized_coin = coin.close#normalize([coin.close]).ravel()
            cum_vol = np.cumsum(vol)#[1000:])
                  
            ax=fig.add_subplot(4,3,i+1)
            ax.plot(normalized_coin,cum_vol,zorder=2,linewidth=line_thk)#[1000:],cum_vol,zorder=2,linewidth=line_thk)
            ax.scatter(np.array(normalized_coin),cum_vol,c=np.array(c_data),s=markersize,zorder=1)#[1000:]),cum_vol,c=np.array(c_data[1000:]),s=markersize,zorder=1)
            min_val = np.min(normalized_coin)
            max_val = np.max(normalized_coin)
   
        ax2=fig.add_subplot(4,3,2)
        for i,coin in enumerate(coins):
            vol,c_data = self.get_vol(coin)
            normalized_coin = coin.close#normalize([coin.close]).ravel()
            ax2=fig.add_subplot(4,3,i+4)
            ax2.plot(np.array(normalized_coin),np.array(vol),zorder=1,linewidth=line_thk)#[1000:]),np.array(vol[1000:]),zorder=1,linewidth=line_thk)
            ax2.scatter(np.array(normalized_coin),np.array(vol),c=np.array(c_data),s=markersize,zorder=2)#[1000:]),np.array(vol[1000:]),c=np.array(c_data[1000:]),s=markersize,zorder=2)
            min_val = np.min(normalized_coin)
            max_val = np.max(normalized_coin)

        ax3=fig.add_subplot(4,3,3)
        for i,coin in enumerate(coins):
            coin_names = ['XRP','ETH','BTC']
            vol,c_data = self.get_vol(coin)
            cum_vol = np.cumsum(vol)#[1000:])
            cum_vol1 = np.cumsum(cum_vol)
            #cum_vol2 = np.cumsum(cum_vol1)
            #cum_vol3 = np.cumsum(cum_vol2)
            normalized_coin = np.log(coin.close)#normalize([coin.close]).ravel()       
            ax3=fig.add_subplot(4,3,i+7)
            ax3.plot(np.array(normalized_coin),cum_vol1,zorder=1,linewidth=line_thk)#[1000:]),cum_vol1,zorder=1,linewidth=line_thk)
            ax3.scatter(np.array(normalized_coin),cum_vol1,c=np.array(c_data),s=markersize,zorder=2)#[1000:]),cum_vol1,c=np.array(c_data[1000:]),s=markersize,zorder=2)    
            if save=='save':
                timestr = time.strftime("%Y%m%d-%H%M%S")
                filename = './data/ARCHIVE/{}_{}.csv'.format(coin_names[i],timestr)

                df = pd.concat([pd.DataFrame(normalized_coin),pd.DataFrame(cum_vol1),pd.DataFrame(c_data)],axis=1)
                df.to_csv(filename, sep=',', header=False, index=False)
                print('saving {}...'.format(filename))  
            
        ax4=fig.add_subplot(4,3,3)
        for i,coin in enumerate(coins):
            vol,c_data = self.get_vol(coin)
            cum_vol = np.cumsum(vol)#[1000:])
            cum_vol1 = np.cumsum(cum_vol)
            normalized_coin = coin.close#normalize([coin.close]).ravel() 
            slope = [self.safe_div(x,y) for x,y in zip(np.diff(cum_vol1),(np.diff(np.array(normalized_coin))))]#[1000:]))))]
            ax4=fig.add_subplot(4,3,i+10)
            #ax4.plot(c_data[1001:],slope)
            #print(len(c_data[1:]),len(slope))
            ax4.scatter(c_data[1:],slope,c=np.array(c_data[1:]),s=markersize)#[1001:],slope,c=np.array(c_data),s=markersize)
            #ax4.plot(np.array(normalized_coin[1000:]),cum_vol1,zorder=1,linewidth=line_thk) 
            
        if save=='save':
            timestr = time.strftime("%Y%m%d-%H%M%S")
            filename = './data/ARCHIVE/slope_{}.png'.format(timestr)
        else:
            filename = './data/slope.png'
        
        savefig(filename)
        
   # def plot_history(self):
        