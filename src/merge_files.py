import pandas as pd
import os

directory_path = os.getcwd()+'/results/transactions'
files = os.listdir(directory_path)

df_all = pd.DataFrame()

for file in files:
   if os.path.isfile(os.path.join(directory_path, file)):
      print("Opening file: ", os.path.join(directory_path, file))

      try:
         df = pd.read_csv(os.path.join(directory_path, file), sep=',')
         print(df.head())
         df_all = pd.concat([df_all, df])
      except Exception as e:
         print(e)

CSV_FILE = f"results/Aave-V2-all.csv"
print(len(df_all.index))
df_all.to_csv(CSV_FILE, index=False)


