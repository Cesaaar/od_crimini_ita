
# coding: utf-8

# # Criminalità Italia - Data Analysis
# 
# ## KPI
# 
# 1. Distribuzione omicidi volontari per Regione Italiana
# 2. Distribuzione omicidi volontari per Città Italiana
# 3. Distribuzione omicidi volontari per Paese zona Euro
# 4. Distribuzione omicidi volontari per Città zona Euro
# 
# ## Open Data
# 1. Istat
#     - http://dati.istat.it/Index.aspx
# 2. Eurostat
#     - http://ec.europa.eu/eurostat/data/database
#     - http://ec.europa.eu/eurostat/web/json-and-unicode-web-services/getting-started/query-builder
#     - http://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=LST_CLS_DLD&StrNom=NUTS_2013L&StrLanguageCode=EN&StrLayoutCode=HIERARCHIC#
#    
# ## Librerie
# 1. Jsonstat
#     - (ISTAT) http://jsonstatpy.readthedocs.io/en/latest/notebooks/istat_house_price_index.html
#     - (EUROSTAT) https://github.com/26fe/jsonstat.py/blob/master/docs/notebooks/eurostat.rst
# 

# In[66]:

# Import librerie per analisi dati (Pandas) e dati Istat
import os
import pandas as pd
import numpy as np
from IPython.core.display import HTML
import istat
import jsonstat


# In[67]:

# cache dir per velocizzare analisi in locale
cache_dir = os.path.abspath(os.path.join("..", "tmp", "istat_cached"))
istat.cache_dir(cache_dir)
istat.lang(0)  # lingua italiano
print("cache_dir is '{}'".format(istat.cache_dir()))


# In[68]:

# Lista delle aree di analisi disponibili
# istat.areas()


# In[69]:

# AREA Giustizia e Sicurezza
istat_area_lab = istat.area('JUS')

# Lista dei datasets dell'area
# istat_area_lab.datasets()


# In[70]:

# DATASET delitti http://dati.istat.it/Index.aspx?DataSetCode=dccv_delittips
istat_dataset_taxdisoccu = istat_area_lab.dataset('DCCV_DELITTIPS')
istat_dataset_taxdisoccu


# In[71]:

# Lista di tutte le Dimensioni
# istat_dataset_taxdisoccu.dimensions()


# In[72]:

# es. spec: Numero crimini registrati dalla polizia(Data Type) per Anno 2014 (Year) su tutto il Territorio Italia (Territory), Omicidi Intenzionali (Type of crime)
spec = {
    "Tipo dato":1,                      # 1 -> number of crimes reported by the police forces to the judicial authority (per 100.000 abitanti)
    "Anno":2167,                        # 2167 -> 2014
    #"Territory":,                      # 0 -> ALL
    #"Type of crime":,                  # 0 -> ALL   
    "Identità autore nota":3,           # 3 Total
    "Periodo del commesso delitto":2    # 2 -> during the reference year
}

collection = istat_dataset_taxdisoccu.getvalues(spec)


# In[73]:

# Lista dei dataset presenti nella collection
# collection


# In[74]:

# Leggo il primo e unico dataset
ds = collection.dataset(0)
# ds


# In[75]:

# Trasformo il dataset in DataFrame
df = ds.to_data_frame('Territorio')


# In[76]:

# Tengo solo Omicidi Volontari, perchè sono gli stessi comunicati in EURO
df_fil = df[
            #(df['Tipo di delitto']=='strage') | 
            #(df['Tipo di delitto']=='infanticidi') |
            # (df['Tipo di delitto']=='omicidi preterintenzionali') |
            (df['Tipo di delitto'].str.contains('omicidi volontari'))
            # (df['Tipo di delitto'].str.contains('omicidi colposi'))
           ]
df_fil = df_fil.drop('Tipo di delitto', 1)


# In[77]:

# Reset index per group-by
df_fil.reset_index(level=0, inplace=True)


# In[78]:

# Raggruppo i valori per Territorio 
df_fil_agg = df_fil.groupby('Territorio',as_index=False)
df_fil_agg = df_fil_agg.agg({'Value' : np.max})


# In[79]:

# writer = pd.ExcelWriter('TerritorioItalia.xlsx')
# df_fil_agg.to_excel(writer,'territorio')
# writer.save()


# ### 1. Dataset -  Numero Omicidi Italia 2014

# In[80]:

# Directory dove salvare i file, da utilizzare in data_visualization
dir_df = os.path.join(os.path.abspath(''),'stg')


# In[81]:

df_ita=df_fil_agg[(df_fil_agg['Territorio']=='Italia')]
# df_ita


# In[82]:

df_ita_filename = r'df_ita.pkl'
df_ita_fullpath = os.path.join(dir_df, df_ita_filename)
df_ita.to_pickle(df_ita_fullpath)


# ### 2. Dataset - Numero Omicidi Regioni 2014

# In[83]:

df_reg=df_fil_agg[(df_fil_agg['Territorio']=='Abruzzo') |
                  (df_fil_agg['Territorio']=='Basilicata') |
                  (df_fil_agg['Territorio']=='Calabria') |
                  (df_fil_agg['Territorio']=='Campania') |
                  (df_fil_agg['Territorio']=='Emilia-Romagna') |
                  (df_fil_agg['Territorio']=='Friuli-Venezia Giulia') |
                  (df_fil_agg['Territorio']=='Lazio') |
                  (df_fil_agg['Territorio']=='Liguria') |
                  (df_fil_agg['Territorio']=='Lombardia') |
                  (df_fil_agg['Territorio']=='Marche') |
                  (df_fil_agg['Territorio']=='Molise') |
                  (df_fil_agg['Territorio']=='Piemonte') |
                  (df_fil_agg['Territorio']=='Puglia') |
                  (df_fil_agg['Territorio']=='Sardegna') |
                  (df_fil_agg['Territorio']=='Sicilia') |
                  (df_fil_agg['Territorio']=='Toscana') |
                  (df_fil_agg['Territorio']=='Umbria') |
                  (df_fil_agg['Territorio']=='Veneto') |
                  (df_fil_agg['Territorio'].str.contains('Trentino Alto Adige')) |
                  (df_fil_agg['Territorio'].str.contains('''Valle d'Aosta'''))
                 ]


# In[84]:

df_reg_filename = r'df_reg.pkl'
df_reg_fullpath = os.path.join(dir_df, df_reg_filename)
df_reg.to_pickle(df_reg_fullpath)


# In[85]:

# Directory dove salvare gli output per il Sito
dir_out = os.path.join(os.path.abspath(''),'output')
df_reg.to_csv(os.path.join(dir_out,r'regioni.csv'))


# ### 3. Dataset - Numero Omicidi Città 2014

# In[86]:

df_cit=df_fil_agg[(df_fil_agg['Territorio']!='Abruzzo') &
                  (df_fil_agg['Territorio']!='Basilicata') &
                  (df_fil_agg['Territorio']!='Calabria') &
                  (df_fil_agg['Territorio']!='Campania') &
                  (df_fil_agg['Territorio']!='Emilia-Romagna') &
                  (df_fil_agg['Territorio']!='Friuli-Venezia Giulia') &
                  (df_fil_agg['Territorio']!='Lazio') &
                  (df_fil_agg['Territorio']!='Liguria') &
                  (df_fil_agg['Territorio']!='Lombardia') &
                  (df_fil_agg['Territorio']!='Marche') &
                  (df_fil_agg['Territorio']!='Molise') &
                  (df_fil_agg['Territorio']!='Piemonte') &
                  (df_fil_agg['Territorio']!='Puglia') &
                  (df_fil_agg['Territorio']!='Sardegna') &
                  (df_fil_agg['Territorio']!='Sicilia') &
                  (df_fil_agg['Territorio']!='Toscana') &
                  (df_fil_agg['Territorio']!='Veneto') &
                  (df_fil_agg['Territorio']!='Umbria') &
                  (df_fil_agg['Territorio']!='Italia') &
                  (df_fil_agg['Territorio']!='Nord-ovest') &
                  (df_fil_agg['Territorio']!='Sud') &
                  (df_fil_agg['Territorio']!='Centro') &
                  (df_fil_agg['Territorio']!='Nord-est') &
                  (df_fil_agg['Territorio']!='Isole')
                 ]


# In[87]:

# Top 10 Città pericolose
df_cit_top=df_cit.sort_values(by='Value',ascending=False).head(10)
df_cit_top_filename = r'df_cit_top.pkl'
df_cit_top_fullpath = os.path.join(dir_df, df_cit_top_filename)
df_cit_top.to_pickle(df_cit_top_fullpath)


# ### 3. Dataset - Numero Omicidi Paesi Euro

# In[88]:

# url costruito via Query Builder di Euro Stat
url_1 = 'http://ec.europa.eu/eurostat/wdds/rest/data/v1.1/json/en/crim_off_cat?precision=1&iccs=ICCS0101&unit=NR'
file_name_1 = r'eurostat-omicidi.json'
file_path_1 = os.path.join(dir_df, file_name_1)
jsonstat.download(url_1, file_path_1)


# In[89]:

collection_1 = jsonstat.from_file(file_path_1)
collection_1


# In[90]:

crim_off_cat = collection_1.dataset('crim_off_cat')
crim_off_cat


# In[91]:

# Dimensioni Geo e Time
df_eur = crim_off_cat.to_table(content='id',rtype=pd.DataFrame)


# In[92]:

# Filtro solo 2014
df_eur=df_eur[(df_eur['time']=='2014')]
# df_eur.head(10)


# In[93]:

#writer = pd.ExcelWriter('ZonaEuro.xlsx')
#df_eur.to_excel(writer,'Euro')
#writer.save()


# In[94]:

df_eur = df_eur.drop('iccs', 1)
df_eur = df_eur.drop('unit', 1)
df_eur = df_eur.drop('time', 1)


# In[95]:

df_eur_filename = r'df_eur.pkl'
df_eur_fullpath = os.path.join(dir_df, df_eur_filename)
df_eur.to_pickle(df_eur_fullpath)


# ### 4. Dataset Omicidi volontari principali città Europee

# In[96]:

# url costruito via Query Builder di Euro Stat
url_2 = 'http://ec.europa.eu/eurostat/wdds/rest/data/v1.1/json/en/crim_hom_ocit?unit=NR&precision=1'
file_name_2 = r'eurostat-omicidi_citta.json'
file_path_2 = os.path.join(dir_df, file_name_2)
jsonstat.download(url_2, file_path_2)


# In[97]:

collection_2 = jsonstat.from_file(file_path_2)
collection_2


# In[98]:

crim_hom_ocit = collection_2.dataset('crim_hom_ocit')
crim_hom_ocit


# In[99]:

# Dimensioni Geo e Time
df_eur_cit = crim_hom_ocit.to_table(content='id',rtype=pd.DataFrame)


# In[100]:

# Filtro solo 2014
df_eur_cit=df_eur_cit[(df_eur_cit['time']=='2014')]


# In[101]:

df_eur_cit = df_eur_cit.drop('time', 1)
df_eur_cit = df_eur_cit.drop('unit', 1)


# In[102]:

# Top 10 Città pericolose
df_eur_cit_top10per=df_eur_cit.sort_values(by='Value',ascending=False).head(10)
# df_eur_cit_top10per


# In[103]:

df_name = pd.read_excel(os.path.join(dir_df, 'NUTS3.xls'), sheetname='Local information')


# In[104]:

# df_name.head(5)


# In[105]:

df_name = df_name.drop('NUTS0', 1)
df_name = df_name.drop('NUTS 3 ID (2010)', 1)
df_name = df_name.drop('NUTS 3 2010 code and name', 1)
df_name = df_name.drop('UA city in NUTS 3', 1)
df_name = df_name.drop('Functional Urban Zone code', 1)
df_name = df_name.drop('Port in NUTS 3', 1)
df_name = df_name.drop('Port ID', 1)
df_name = df_name.drop('Name of the port', 1)
df_name = df_name.drop('Remark', 1)


# In[106]:

# df_name.head(5)


# In[107]:

df = pd.merge(df_eur_cit_top10per, df_name, how='left',left_on='cities', right_on='City code')
df = df[pd.notnull(df['City name'])]
#df


# In[108]:

df_eur_cit_filename = r'df_eur_cit.pkl'
df_eur_cit_fullpath = os.path.join(dir_df, df_eur_cit_filename)
df.to_pickle(df_eur_cit_fullpath)

