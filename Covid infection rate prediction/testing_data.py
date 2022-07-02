import pandas as pd

link = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=newCasesBySpecimenDate&format=csv'
data =  pd.read_csv(link)

data.drop(columns = ['areaCode', 'areaName', 'areaType'], inplace = True)
data.columns = ['date', 'newCases']
data = data.reindex(index = data.index[::-1]).reset_index(drop = True)

data['activeCases'] = data.newCases.rolling(10, min_periods=1).sum()
pd.set_option('display.max_rows', 1000)

data.to_excel('C:\\Users\\adama\\Desktop\\GitHub Files\\Covid infection rate prediction\\data.xlsx')