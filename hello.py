import sqlite3
import requests
import pandas as pd

r = requests.get(
    'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-8561BA50-5DAB-405D-9A90-D4C424DB2928&format=JSON')
data = r.json()["records"]["location"]
df = pd.DataFrame()
df["location"] = data
# df.head()
result = []
for i in data:
    dic = {}
    dic["locationName"] = i["locationName"]
    dic["startTime"] = i["weatherElement"][0]["time"][2]["startTime"]
    dic["endTime"] = i["weatherElement"][0]["time"][2]["endTime"]
    dic["parameterName"] = i["weatherElement"][0]["time"][2]["parameter"]["parameterName"]
    dic["parameterValue"] = i["weatherElement"][0]["time"][2]["parameter"]["parameterValue"]
    result.append(dic)

df = pd.DataFrame(result)

conn = sqlite3.connect('weather.db')
df.to_sql('weather', conn, if_exists='replace', index=False)
pd.read_sql('select * from weather', conn)
