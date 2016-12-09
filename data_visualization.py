
# coding: utf-8

# # Criminalità Italia - Data Visualization
# 
# 
# ## Librerie
# 1. Folium
#     - conda install -c conda-forge folium=0.2.1

# In[18]:

# Librerie
import os
import pandas as pd
import numpy as np
import folium
import matplotlib.pyplot as plt
plt.style.use('ggplot')
get_ipython().magic('pylab inline')


# In[19]:

# Cartelle Input/Output
dir_df = os.path.join(os.path.abspath(''),'stg')
dir_out = os.path.join(os.path.abspath(''),'output')


# ### Totale Omicidi Volontari Italia

# In[20]:

df_reg.sum()


# ### Distribuzione Omicidi Volontari per Regione Italiana

# In[21]:

df_reg_filename = r'df_reg.pkl'
df_reg_fullpath = os.path.join(dir_df, df_reg_filename)
df_reg = pd.read_pickle(df_reg_fullpath)

regioni_geo_filename = r'regioni.geojson'
regioni_geo = os.path.join(dir_df, regioni_geo_filename)

reg_map = folium.Map(location=[42, 12], zoom_start=5)
reg_map.choropleth(geo_path=regioni_geo, data=df_reg,
                  columns=['Territorio', 'Value'],
                  key_on='feature.properties.NOME_REG',
                  fill_color='YlOrRd')

reg_map.save(os.path.join(dir_out,r'omicidi_volontari.html'))
reg_map


# ### Top 3 Regioni Pericolose - Numero Omicidi Volontari

# In[22]:

# Top 3 Regioni
df_reg_top3=df_reg.sort_values(by='Value',ascending=False).head(3)
df_reg_top3.to_csv(os.path.join(dir_out,r'Top3_Regioni.csv'),header=True, index=False)
df_reg_top3


# ### Top 10 Città Pericolose

# In[33]:

df_cit_top_filename = r'df_cit_top.pkl'
df_cit_top_fullpath = os.path.join(dir_df, df_cit_top_filename)
df_cit_top = pd.read_pickle(df_cit_top_fullpath)
# Report
tp = df_cit_top.plot(
        x=df_cit_top['Territorio'],
        kind='bar',
        legend = False)
for p in tp.patches:
    tp.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005), ha='center', va='center', xytext=(10, 5), textcoords='offset points')
    tp.plot()

fig_prj = tp.get_figure()
fig_prj.tight_layout()
fig_prj.savefig(os.path.join(dir_out,'topcitta.png'), format='png', dpi=300)


# ### 2. Paesi Unione Europea

# In[24]:

df_eur_filename = r'df_eur.pkl'
df_eur_fullpath = os.path.join(dir_df, df_eur_filename)
df_eur = pd.read_pickle(df_eur_fullpath)


# In[25]:

europa_geo_filename = r'euro.geojson'
europa_geo = os.path.join(dir_df, europa_geo_filename)

eur_map = folium.Map(location=[48, 10], zoom_start=4)
eur_map.choropleth(geo_path=europa_geo, data=df_eur,
                  columns=['geo', 'Value'],
                  key_on='feature.properties.iso_a2',
                  fill_color='YlOrRd')
eur_map


# In[26]:

# Top 3 Paesi
df_eur_top3=df_eur.sort_values(by='Value',ascending=False).head(3)
df_eur_top3


# In[27]:

dir_out = os.path.join(os.path.abspath(''),'output')
eur_map.save(os.path.join(dir_out,r'omicidi_volontari_eu.html'))


# ### Top Città Europee Pericolose - (Dati Eurostat non sembrani Buoni)

# In[28]:

df_eur_cit_filename = r'df_eur_cit.pkl'
df_eur_cit_fullpath = os.path.join(dir_df, df_eur_cit_filename)
df_eur_cit = pd.read_pickle(df_eur_cit_fullpath)
# Report
tp1 = df_eur_cit.plot(
        x=df_eur_cit['City name'],
        kind='bar',
        legend = False)
for p in tp1.patches:
    tp1.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005), ha='center', va='center', xytext=(10, 5), textcoords='offset points')
    tp1.plot()

fig_eur = tp1.get_figure()
fig_eur.tight_layout()
fig_eur.savefig(os.path.join(dir_out,'topeurcitta.png'), format='png', dpi=300)

