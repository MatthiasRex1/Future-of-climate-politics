import pandas as pd

clima=pd.read_csv('999.csv',sep=';')
codes=pd.read_csv('country_codes_V202301.csv',sep=',')

for i in range(clima.shape[0]):
    clima['country'][i]=codes[codes['country_code']==clima['country'][i]]['country_name_full'].tolist()[0]

clima.to_csv('999 decoded.csv',sep=';',index=False)
