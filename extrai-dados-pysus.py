#%%
from pysus import SIH
import pandas as pd

#%%
sih = SIH().load() # Loads the files from DATASUS

files = sih.get_files("RD", uf="PB", year=2024)
parquets = sih.download(files)

# %%
df = pd.DataFrame()
for parquet in parquets:
    df = pd.concat([df, parquet.to_dataframe()])

# %%
df.to_csv('dados/dados_sih_pb_2024.csv', index=False)

# %%
