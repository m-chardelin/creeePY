from itertools import product, combinations, chain
import pandas as pd
import numpy as np
import math
import os
import linecache

    
class Statistics():
    def __init__(self, files, **kwargs):
        
        self.__dict__.update(kwargs)

        self.samples = pd.read_csv(f'{files.folder}/samples.csv', sep = '&', index_col = 'cat')
        
        with open(f'{files.folder}/resolution.csv', 'w') as file:
            file.write('cat\tdata\tvalue\n')
     
    def Load(self, table, sort = False):
        self.df = pd.read_csv(table, sep = '&')
        if sort == True:
            self.sort = set(self.df[self.sort])
        return self.df
            

    def SetParam(self, **kwargs):
        self.__dict__.update(kwargs)


    def Iteration(self, files, func, iterMineral = False):
        """Itération sur les nom des catégories et des sous catégories, possibilité d'itération sur les subcatégories"""
        for c in files.cat:
            if iterMineral == False:
                func(files, c)

            if iterMineral == True:
                for ssc in files.sscat:
                    if os.path.exists(f'{files.input}/{c}_{ssc}_{self.task}.csv'):
                        func(files, c, ssc)
                        
                        
    def GetRes(self, files, cat):
        """Crée une table des tailles des échantillons en longueur et en largeur, avec les résolutions"""
        for i in [5, 6, 7, 8]:
            try:
                line = linecache.getline(f'{files.ctf}/{cat}.ctf', i)
                with open(f'{files.folder}/resolution.csv', 'a') as file:
                    file.write(f'{cat}\t{line}')
            except:
                pass
                
                
    def Res(self, files):
        """Inclu la table des résolutions à la table des échantillons principaux"""
        df = pd.read_csv(f'{files.folder}/resolution.csv', sep = '\t')
        ind = []
        for i in df.index:
            ind.append(str(df.loc[i, 'cat']) + '_' + str(df.loc[i, 'data']))
        df.index = ind
        for cat in set(df['cat']):
            for d in set(df['data']):
                self.samples.loc[cat, d] = df.loc[f'{cat}_{d}', 'value']
        self.samples.to_csv(f'{files.folder}/samples.csv', sep = '&')
        self.samples = pd.read_csv(f'{files.folder}/samples.csv', sep = '&', index_col = 'cat')
        
        
    def Combine(self, files, cat):
        """Combine les tables des sous catégories données en une même table avec le nom donné"""
        grains = pd.DataFrame()
            
        if type(self.inp) == 'str':
            input = [self.inp]
        else:
            pass
            
        for inp in self.inp:
            if os.path.exists(f'{files.input}/{cat}_{inp}_{self.table}.csv'):
                self.Load(f'{files.input}/{cat}_{inp}_{self.table}.csv')
                if self.out == 'all':
                    self.df['sscat'] = inp
                grains = pd.concat([grains, self.df])

        if grains.shape[0] > 0:
            grains.sort_values(by = ['id'])
            grains.to_csv(f'{files.output}/{cat}_{self.out}_{self.table}.csv', sep = '&', index = None)



    def Calculate(self, files, cat, sortRes):
        """Calcul des colonnes voulues sur les tables """
    
        self.df['EGD'] = self.df.equivalentRadius *2

        r = np.sqrt(self.df.area/np.pi)
        self.df['SF'] = self.df.perimeter/(2*np.pi*r)
        
        if sortRes == True:
            res = self.samples.loc[cat, 'XStep']
            self.df = self.df[self.df['EGD'] >= 1.5*res]
        return self.df


    def Sort(self, files, cat, sscat):
        """Tri des recristallisations et des porphyroclastes selon les valeurs indiquées et les colonnes indiquées"""
        self.Load(f'{files.input}/{cat}_{sscat}_Grains.csv')
        
        if 'EGD' not in self.df.columns:
            self.df = self.Calculate(files, cat, self.sortRes)

        if self.value == 'manuel':
            self.val = self.samples.loc[cat, f'tri{self.column}']
            self.crit = 'manuel'
        elif self.value == 'mixte':
            self.crit = 'mixte'
            self.df.loc[self.df['GOS'] > 1, f'{self.column}{self.crit}'] = 'porph'
            self.df.loc[self.df['GOS'] <= 1, f'{self.column}{self.crit}'] = 'rex'
            self.df.loc[self.df['EGD'] > 400, f'{self.column}{self.crit}'] = 'porph'
            self.df.to_csv(f'{files.output}/{cat}_{sscat}_Grains.csv', sep = '&', index = None)
        else:
            self.crit = self.value
            self.val = self.value

        if self.crit != 'mixte':
            self.df.loc[self.df[self.column] > self.val, f'{self.column}{self.crit}'] = 'porph'
            self.df.loc[self.df[self.column] <= self.val, f'{self.column}{self.crit}'] = 'rex'
            self.df.to_csv(f'{files.output}/{cat}_{sscat}_Grains.csv', sep = '&', index = None)
            
        if sscat == 'Amphibole':
            self.df[f'{self.column}{self.crit}'] = 'rex'
            self.df.to_csv(f'{files.output}/{cat}_{sscat}_Grains.csv', sep = '&', index = None)


    def DescribeDf(self, df):
        """Fait le résumé statistique du dataframe voulu, ajout de la somme des valeurs"""
        d = df.describe()
        for col in d.columns:
            d.loc['sum', col] = np.sum(df[col])
        return d
        
        
    def Describe(self, files, cat):
        """Crée une table annexe dans laquelles sont résumées les statistiques par sous catégorie, catégorie, par échantillon avec la bonne indexation pour un futur résumé"""
        
        self.stats = pd.DataFrame()
        
        c = [cat]
        
        for it in list(product(c, files.sscat, self.subcat, self.sort)):
            
            names = {'id': f'{it[0]}_{it[1]}_{it[2]}_{it[3]}', 'cat': it[0], 'sscat': it[1], 'subcat': it[2], 'sort': it[3]}
            
            if os.path.exists(f'{files.input}/{it[0]}_{it[1]}_{self.table}.csv'):
                self.Load(f'{files.input}/{it[0]}_{it[1]}_{self.table}.csv')
                 
                if names['subcat'] == 'all':
                    describe = self.DescribeDf(self.df)
                    names['id'] = f'{it[0]}_{it[1]}_{it[2]}'
                    names['sort'] = 'all'
                    
                elif names['subcat'] != 'all':
                    self.df = self.df[self.df[names['sort']] == names['subcat']]
                    describe = self.DescribeDf(self.df)
                    
                for key in names.keys():
                    describe[key] = names[key]
                        
                describe['operation'] = describe.index
                self.stats = pd.concat([self.stats, describe])
        
        self.stats = self.stats.drop_duplicates(keep = 'last')
        self.stats.to_csv(f'{files.output}/{cat}_{self.stat}.csv', sep = '&', index = None)
        
        
    def IntermediaryCalculations(self, files, cat, sscat):
        """Calcule les valeurs d'un champ * les coefficients de l'aire pour chaque grain, garde en mémoire les tri effectués"""
        
        grains = self.Load(f'{files.input}/{cat}_{sscat}_Grains.csv')
        
        area = pd.read_csv(f'{files.input}/{cat}_GrainsStats.csv', sep = '&')
        area = area[area['operation'] == 'sum']
        area.index = area['id']
        
        self.calculations = pd.DataFrame()
            
        self.calculations['id'] = grains['id']
        self.calculations['area'] = grains['area']
        self.calculations['catArea'] = area.loc[f'{cat}_all_all', 'area']
        self.calculations['pondArea'] = self.calculations['area']/self.calculations['catArea']
            
        if hasattr(self, 'ponderation') == False:
            col = [c for c in grains.columns if c not in self.sort]
            col = [c for c in col if c not in ['sscat', 'id']]
            setattr(self, 'ponderation', col)
                
        for s in self.sort:
            self.calculations[f'{s}'] = grains[f'{s}']
            
        for p in self.ponderation:
            self.calculations[f'pond{p}'] = grains[p]*self.calculations['pondArea']
            
        self.calculations.to_csv(f'{files.output}/{cat}_{sscat}_IntermediaryCalculations.csv', sep = '&', index = None)
        

    def AreaResume(self, files, cat):
        """Concatène les tables pour une opération statistique données, avec les bons index, calcule les rapports de surface selon les différentes catégories et calcule les variables pondérées par la surface"""
    
        if os.path.exists(f'{files.output}/resume.csv'):
            self.resume = pd.read_csv(f'{files.output}/resume.csv', sep = '&')
        else:
            self.resume = pd.DataFrame()
     
        intStats = self.Load(f'{files.input}/{cat}_IntermediaryStats.csv')
        grainsStats = self.Load(f'{files.input}/{cat}_GrainsStats.csv')
        
        sum = grainsStats[grainsStats['operation'] == 'sum']
        intStats = intStats[intStats['operation'] == 'sum']
        
        add = pd.DataFrame()
        for c in ['id', 'cat', 'sscat', 'subcat', 'sscat', 'sort', 'area']:
            add[c] = sum[c]
        
        sum.index = sum.id
        intStats.index = intStats.id
    
        for o in self.on:
            dfOn = grainsStats[grainsStats['operation'] == o]
            cols = [col for col in dfOn.columns if col not in ['cat', 'sscat', 'subcat', 'sscat', 'sort', 'operation']]
            df = dfOn[cols]
            for c in cols:
                if c != 'id':
                    df = df.rename(columns = {c: f'{o}{c}'})
            add = add.merge(df, on = 'id', how = 'outer')

        add.loc[add['cat'] == cat, 'catArea'] = sum.loc[f'{cat}_all_all', 'area']
        
        sscat = list(set(add.sscat))
        for ssc in sscat:
            add.loc[add['sscat'] == ssc, 'sscatArea'] = sum.loc[f'{cat}_{ssc}_all', 'area']
            add.loc[(add['sscat'] == ssc) & (add['sort'] == 'all'), 'subcatArea'] = sum.loc[f'{cat}_all_all', 'area']

        subcat = ['rex', 'porph']
        for it in list(product(subcat, self.sort)):
            add.loc[(add['subcat'] == f'{it[0]}') & (add['sort'] == f'{it[1]}'), 'subcatArea'] = sum.loc[f'{cat}_all_{it[0]}_{it[1]}', 'area']

        for c in ['catArea', 'sscatArea', 'subcatArea']:
            add[f'%{c}'] = add['area']/add[c]


        self.resume = pd.concat([self.resume, add])
        self.resume.index = self.resume.id

        if hasattr(self, 'ponderation'):
            for p in self.ponderation:
                for i in self.resume.index:
                    try:
                        self.resume.loc[i, f'pond{p}'] = intStats.loc[i, f'pond{p}'] / intStats.loc[i, 'pondArea']
                    except:
                        pass
                        
        self.resume.to_csv(f'{files.output}/resume.csv', sep = '&', index = None)

  
    def SortCategories(self, files):
        """Trie les catégories de lames selon les critères définis"""
        
        self.resume = pd.read_csv(f'{files.output}/resume.csv', sep = '&', index_col = 'id')
        
        for it in list(product(files.cat, self.sort)):
        
            cat = it[0]
            sort = it[1]

            try:
                all = self.resume.loc[f'{cat}_Clinopyroxene_all', '%catArea'] + self.resume.loc[f'{cat}_Orthopyroxene_all', '%catArea'] + self.resume.loc[f'{cat}_Olivine_all', '%catArea']
                
                if self.resume.loc[f'{cat}_Olivine_all', '%catArea'] / all < 0.4:
                    self.samples.loc[cat, 'lithologyDef'] = 'pyroxenite'
                else:
                    self.samples.loc[cat, 'lithologyDef'] = 'peridotite'
            except:
                pass
            
            try:
                if self.resume.loc[f'{cat}_Amphibole_all', '%catArea'] > 0.8:
                    self.samples.loc[cat, 'lithologyDef'] = 'amphibolite'
            except:
                pass

            try:
                if self.resume.loc[f'{cat}_Olivine_rex_{sort}', '%sscatArea'] <= 0.15 :
                    if self.resume.loc[f'{cat}_Olivine_rex_{sort}', 'pondEGD'] <= 100:
                        self.samples.loc[cat, f'facies_{sort}'] = 'protomylonite BT'
                    elif self.resume.loc[f'{cat}_Olivine_rex_{sort}', 'pondEGD'] > 100:
                        self.samples.loc[cat, f'facies_{sort}'] = 'mylonite HT'
            except:
                pass
                
            try:
                if self.resume.loc[f'{cat}_Olivine_rex_{sort}', '%sscatArea'] > 0.15 and self.resume.loc[f'{cat}_Olivine_rex_{sort}', '%sscatArea'] <= 0.5:
                    self.samples.loc[cat, f'facies_{sort}'] = 'mylonite BT'
            except:
                pass
                
            try:
                if self.resume.loc[f'{cat}_Olivine_rex_{sort}', '%sscatArea'] > 0.5:
                    self.samples.loc[cat, f'facies_{sort}'] = 'ultramylonite'
            except:
                pass

            #try:
            #    if self.resume.loc[f'{cat}_all_rex_{sort}', '%catArea'] <= 0.1 and self.resume.loc[f'{cat}_all_rex_{sort}', '%catArea'] <= 800:
            #        self.samples.loc[cat, f'facies_{sort}'] = 'protomylonite BT'
            #except:
            #    pass
                
        self.samples.to_csv(f'{files.output}/samples.csv', sep = '&')


    def CalculateMeanGrains(self, files, cat):
        """Calcule les grandeurs moyennes à partir des pixels pour chaques grains, ne garde que les colonnes voulues """
        for ssc in files.sscat:
            if os.path.exists(f'{files.input}/{cat}_{ssc}_{self.table1}.csv'):
                table1 = self.Load(f'{files.input}/{cat}_{ssc}_{self.table1}.csv')
                print(f'{files.input}/{cat}_{ssc}_{self.table1}.csv')
                
                df = pd.DataFrame()
                id = list(set(table1['grain']))
                
                for i in id:
                    sub = table1[table1['grain'] == i]
                    mean = sub.mean(numeric_only=True)
                    mean = pd.DataFrame(mean)
                    mean = mean.T
                    
                    df = pd.concat([df, mean])
                    
                df['id'] = df['grain'].astype(int)
                
                columns = [c for c in table1.columns if c not in self.columns1]
                for c in columns:
                    try:
                        del df[c]
                    except:
                        pass
                    
                table2 = self.Load(f'{files.input}/{cat}_{ssc}_{self.table2}.csv')
                
                table2['id'] = table2['id'].astype(int)
                
                if self.columns2[0] != 'all':
                    table2 = table2[self.columns2]
                else:
                    pass
                
                table2 = table2.merge(df, on = 'id', how = 'outer')
            
                table2.to_csv(f'{files.output}/{cat}_{ssc}_{self.name}.csv', sep = '&', index = None)
                    

    # COMBINER DES DATAFRAMES EN NE GARDANT QUE LES BONNES COLONNES

    # COMBINER DES DATAFRAMES AVEC LES SOUS CATEGORIES
    
    # LES VOISINS !
