import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import datetime
from matplotlib import pyplot as plt
import seaborn as sns

#data load
filepath = r"C:\Users\user\Desktop\신희진\경찰청\화성시 Data_교통"
file = '\화성시방향별교통량5분_5월.csv'

raw_df = pd.read_csv(filepath+file,encoding='CP949')
raw_df['time']=pd.to_datetime(raw_df['time'])
raw_df['time'] = raw_df['time'].apply(lambda dt: datetime.datetime(dt.year,dt.month, dt.day,dt.hour))
raw_df_loc=raw_df.loc[:,['IntersectionSeq','AvenueSeq','MovementType','time','COUNT(*)']]

#key별 데이터(176)
pri_intersection = raw_df_loc['IntersectionSeq'].unique()
pri_Avenue = raw_df_loc['AvenueSeq'].unique()
pri_Movement = raw_df_loc['MovementType'].unique()
df=[]
a=0
for i in range(len(pri_intersection)):
    for j in range(len(pri_Avenue)):
        for k in range(len(pri_Movement)):
            globals()['pre_df{}'.format(a)] = raw_df_loc[(raw_df['IntersectionSeq']==pri_intersection[i]) & (raw_df_loc['AvenueSeq']==pri_Avenue[j]) & (raw_df_loc['MovementType']==pri_Movement[k])]
            if not globals()['pre_df{}'.format(a)].empty:
                df.append('pre_df{}'.format(a))
            a=a+1
#결과
result=[]
for i in range(len(df)):
    #1시간 단위
    data=eval(df[i]).groupby("time")['COUNT(*)'].sum()
    data=pd.DataFrame(data)

    #print(data)

    #ARIMA
    from statsmodels.tsa.arima_model import ARIMA
    import statsmodels.api as sm
    from statsmodels.graphics.tsaplots import plot_predict
    # (AR = 2, 차분 =1, MA=2) 파라미터로 ARIMA 모델을 학습한다.
    model = sm.tsa.ARIMA(data, order = (1,2,1))
    #model = ARIMA(data, order=(1, 1, 1))
    model_fit = model.fit()
    #print(model_fit.summary())
    forecast=model_fit.forecast(steps=1)
    data=data.reset_index()
    result_time=data.iloc[-1,0]+datetime.timedelta(hours=1)
    result.append([int(eval(df[i])['IntersectionSeq'].unique()),int(eval(df[i])['AvenueSeq'].unique()),int(eval(df[i])['MovementType'].unique()),result_time,int(forecast)])
print(result)
pd.DataFrame(result)
import openpyxl
result_df = pd.DataFrame(result,columns=['IntersectionSeq','AvenueSeq','MovementType','Time','forecast'])
print(result_df)
print("---------------------------------------------------------")
result_df.to_excel('C:/Users/user/Desktop/신희진/경찰청/result.xlsx', sheet_name='result', index=False)