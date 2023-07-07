import pandas as pd
from itertools import product


df = pd.read_csv('/storage/emulated/0/toDo/Zabargad/3_4_deformation/4_analysis/stats/resume.csv', sep = ';')
samples = pd.read_csv('/storage/emulated/0/toDo/Zabargad/3_4_deformation/4_analysis/stats/EBSD.csv', sep = ';')

ddf = pd.DataFrame()

cat = list(set(df['cat']))
sscat = list(set(df['sscat']))
subcat = list(set(df['subcat']))
sort = list(set(df['sort']))


prop = ['pondaspectRatio', 'pondSF', 'pondGOS', 'pondEGD']

i = 0
for c, ssc in list(product(cat, sscat)):
    ddff = df[(df['cat'] == c) & (df['sscat'] == ssc) ]
    
    for sub, s in list(product(subcat, sort)):

        d = ddff[(ddff['subcat'] == sub) & (ddff['sort'] == s) ]
        for pro in prop:
            if d.shape[0] == 1:
                pp = d[pro]
                ddf.loc[i, f'{pro}{sub}{s}'] = pp[pp.index[0]]
                ddf.loc[i, 'cat'] = c
                ddf.loc[i, 'sscat'] = ssc

            elif d.shape[0] == 0:
                ddf.loc[i, f'{pro}{sub}{s}'] = 0
                ddf.loc[i, 'cat'] = c
                ddf.loc[i, 'sscat'] = ssc

    i += 1

samp = samples[['cat', 'facies_EGDmixte', 'massif', 'lithologyDef']]

ddf = ddf.merge(samp, on = 'cat', how = 'outer')
ddf.to_csv('/storage/emulated/0/toDo/Zabargad/3_4_deformation/4_analysis/stats/combSort.csv', sep = ';')


df = pd.read_csv('/storage/emulated/0/toDo/Zabargad/3_4_deformation/4_analysis/stats/resume.csv', sep = ';')

cat = list(set(df['cat']))
sscat = list(set(df['sscat']))
subcat = list(set(df['subcat']))
sort = list(set(df['sort']))

ddf = pd.DataFrame()

i = 0
for c, sub, s in list(product(cat, subcat, sort)):
    ddff = df[(df['cat'] == c) & (df['subcat'] == sub) & (df['sort'] == s) ]
    for ssc in sscat:
        d = ddff[ddff['sscat'] == ssc]
        for pro in prop:
            if d.shape[0] == 1:
                pp = d[pro]
                ddf.loc[i, f'{pro}{ssc}'] = pp[pp.index[0]]
                ddf.loc[i, 'cat'] = c
                ddf.loc[i, 'subcat'] = sub
                ddf.loc[i, 'sort'] = s

            elif d.shape[0] == 0:
                ddf.loc[i, f'{pro}{ssc}'] = 0
                ddf.loc[i, 'cat'] = c
                ddf.loc[i, 'subcat'] = sub
                ddf.loc[i, 'sort'] = s
    i += 1

ddf = ddf.merge(samp, on = 'cat', how = 'outer')
ddf.to_csv('/storage/emulated/0/toDo/Zabargad/3_4_deformation/4_analysis/stats/combSscat.csv', sep = ';')
