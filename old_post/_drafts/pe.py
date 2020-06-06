import pandas as pd
import numpy as np
from tqdm import tqdm
from tqdm import trange
import tushare as ts
import plotly.express as px

ts.set_token('2ecdcdc049841ad3c28d13653925f79d41da86fe73dd49f5897f1ec4')
pro = ts.pro_api()

class ewPE(object):
    def __init__(self,index_date, index_code):
        self.index_date = index_date
        self.index_code = index_code

    def Pull(self):
        con_list = pro.index_weight(start_date=self.index_date, end_date=self.index_date, index_code=self.index_code)
        con_info_list = []
        for con in trange(len(con_list['con_code'].values)):
            con_info = pro.daily_basic(ts_code=con, trade_date=self.index_date, fields='ts_code,pe_ttm,pb')
            con_info_list.append(con_info)

        pe_df = pd.concat(con_info_list).dropna()
        pe_df['ROR'] = 1/pe_df['pe_ttm']

        return pe_df
        
    def Ewpe(self):
        return self.df['pe_ttm'].count()/self.df['ROR'].sum()
    
    def Quantile(self):
        return self.df.quantile(np.arange(0,1.1,0.1)).transpose()

    def Frequency(self):
        # 设置12个值，历史峰值为70
        listBins = [0, 10, 20, 30, 40, 50, 60, 70, 9999]

        # 对应11个区间
        listLabels = ['0<=10','10<=20','20<=30','30<=40','40<=50','50<=60','60<=70','>70']
        s = pd.cut(pe_df['pe_ttm'].values,bins=listBins, labels=listLabels)
        freq = s.value_counts()
        freq_df = pd.DataFrame(freq,columns=['frequency'])
        freq_df['pct'] = freq_df['frequency'] / freq_df['frequency'].sum()
        freq_df['accumulative_pct'] = freq_df['pct'].cumsum()
 
        self.frequency = freq_df


    def Freqbar(self):
        fig = px.bar(self.frequency, 
            y='accumulative_pct', 
            x=self.frequency.index, 
            color='accumulative_pct',
            title='Accumulative PE Percentile')
        fig.show()

    def Freqpie(self):
        fig = px.pie(self.frequency.sort_values('pct'), 
                    values='pct',
                    names=self.frequency.index,
                    title='Percentage of PE Percentile')
        fig.show()

pe = ewPE('20200301', 000905.SH')
df = pe.Pull()
