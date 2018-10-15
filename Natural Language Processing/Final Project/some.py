import pandas as pd

df2 = pd.read_csv('Flight.csv')
df_Flight_test = df2[2615:]
print(len(df_Flight_test['text'].tolist()))