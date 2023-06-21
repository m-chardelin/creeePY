from itertools import product, combinations, chain
import pandas as pd
import numpy as np
import math
import os
import linecache

    
class Statistics():
    def __init__(self, files, **kwargs):
        
        self.__dict__.update(kwargs)

        self.samples = pd.read_csv(f'{files.folder}/samples.csv', sep = ';', index_col = 'cat')
        
        with open(f'{files.folder}/resolution.csv', 'w') as file:
            file.write('cat\tdata\tvalue\n')
     
    def Load(self, table, sort = False):
        self.df = pd.read_csv(table, sep = ';')
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
                    if os.path.exists(f'{files.input}/{c}_{ssc}_{self.table}.csv'):
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
        self.samples.to_csv(f'{files.folder}/samples.csv', sep = ';')
        self.samples = pd.read_csv(f'{files.folder}/samples.csv', sep = ';', index_col = 'cat')
        
        
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
            grains.to_csv(f'{files.output}/{cat}_{self.out}_{self.table}.csv', sep = ';', index = None)


    def Split(self, files, cat):

        df = self.Load(f'{files.input}/{cat}_all_{self.table}.csv')

        sort = list(set(df[self.column]))

        for s in sort:
            d = df[df[self.column] == s]
            if d.shape[0] > 0:
                del d[self.column]
                d.to_csv(f'{files.output}/{cat}_{s}_{self.table}.csv', sep = ';', index = None)



    def Calculate(self, files, cat, sortRes):
        """Calcul des colonnes voulues sur les tables """
    
        self.df['EGD'] = self.df.equivalentRadius *2

        r = np.sqrt(self.df.area/np.pi)
        self.df['SF'] = self.df.perimeter/(2*np.pi*r)
        
        if sortRes == True:
            res = self.samples.loc[cat, 'XStep']
            self.df = self.df[self.df['EGD'] >= 1.5*res]
        return self.df


    def SortGrains(self, files, cat, sscat):
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
            self.df.loc[self.df['GOS'] <= 1, f'{self.column}{self.crit}'] = 'neo'
            self.df.loc[self.df['EGD'] > 400, f'{self.column}{self.crit}'] = 'porph'
            self.df.to_csv(f'{files.output}/{cat}_{sscat}_Grains.csv', sep = ';', index = None)
        else:
            self.crit = self.value
            self.val = self.value

        if self.crit != 'mixte':
            self.df.loc[self.df[self.column] > self.val, f'{self.column}{self.crit}'] = 'porph'
            self.df.loc[self.df[self.column] <= self.val, f'{self.column}{self.crit}'] = 'neo'
            self.df.to_csv(f'{files.output}/{cat}_{sscat}_Grains.csv', sep = ';', index = None)
            
        if sscat == 'Amphibole':
            self.df[f'{self.column}{self.crit}'] = 'neo'
            self.df.to_csv(f'{files.output}/{cat}_{sscat}_Grains.csv', sep = ';', index = None)


    def DescribeDf(self, df):
        """Fait le résumé statistique du dataframe voulu, ajout de la somme des valeurs"""
        d = df.describe()
        for col in d.columns:
            d.loc['sum', col] = np.sum(df[col])
        return d
        
        
    def Describe(self, files, cat):
        """Crée une table annexe dans laquelles sont résumées les statistiques par sous catégorie, catégorie, par échantillon avec la bonne indexation pour un futur résumé"""
        
        
        if os.path.exists(f'{files.output}/{cat}_{self.stat}.csv'):
            stats = pd.read_csv(f'{files.output}/{cat}_{self.stat}.csv', sep = ';')
        else:
            stats = pd.DataFrame()
        
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
               
                stats = pd.concat([stats, describe])
        
        stats = stats.drop_duplicates(subset = ['cat', 'sscat', 'subcat', 'sort', 'id', 'operation'], keep = 'last')
        stats.to_csv(f'{files.output}/{cat}_{self.stat}.csv', sep = ';', index = None)
        
        
    def IntermediaryCalculations(self, files, cat, sscat):
        """Calcule les valeurs d'un champ * les coefficients de l'aire pour chaque grain, garde en mémoire les tri effectués"""
        

        grains = self.Load(f'{files.input}/{cat}_{sscat}_{self.table}.csv')
        
        area = pd.read_csv(f'{files.input}/{cat}_{self.stat}.csv', sep = ';')
        area = area[area['operation'] == 'sum']
        area.index = area['id']
        

        if os.path.exists(f'{files.output}/{cat}_{sscat}_{self.intermediaryCalculations}.csv'):
            self.calculations = pd.read_csv(f'{files.output}/{cat}_{sscat}_{self.intermediaryCalculations}.csv', sep = ';')
        else:
            self.calculations = pd.DataFrame()
            self.calculations['id'] = grains['id']
            self.calculations['area'] = grains['area']
            self.calculations['catArea'] = area.loc[f'{cat}_all_all', 'area']
            self.calculations['pondArea'] = self.calculations['area']/self.calculations['catArea']
            
        if hasattr(self, 'ponderation') == False :
            col = [c for c in grains.columns if c not in self.sort]
            col = [c for c in col if c not in ['sscat', 'id']]
            col = [c for c in col if grains.dtypes[c] != 'object']
            setattr(self, 'colPonderation', col)
        elif hasattr(self, 'ponderation') == True and self.ponderation == False:
            col = [c for c in grains.columns if c not in self.sort]
            col = [c for c in col if c not in ['sscat', 'id']]
            col = [c for c in col if grains.dtypes[c] != 'object']
            setattr(self, 'colPonderation', col)
    
        col = [c for c in grains.columns if grains.dtypes[c] == 'object']
        for c in col:
            self.calculations[c] = grains[c]
    
        for p in self.colPonderation:
            self.calculations[f'pond{p}'] = grains[p]*self.calculations['pondArea']
        
        self.calculations.to_csv(f'{files.output}/{cat}_{sscat}_{self.intermediaryCalculations}.csv', sep = ';', index = None)


    def Resume(self, files, cat):
        """Concatène les tables pour une opération statistique données, avec les bons index, calcule les rapports de surface selon les différentes catégories et calcule les variables pondérées par la surface"""
    
        if os.path.exists(f'{files.output}/{self.resumeName}.csv'):
            self.resume = pd.read_csv(f'{files.output}/{self.resumeName}.csv', sep = ';')
        else:
            self.resume = pd.DataFrame()
     
        intStats = self.Load(f'{files.input}/{cat}_{self.intermediaryCalculationsStats}.csv')
        grainsStats = self.Load(f'{files.input}/{cat}_{self.grainsStat}.csv')
       
        with open(f'{files.output}/control.txt', 'a') as file:
            file.write(f'{files.input}/{cat}_{self.intermediaryCalculationsStats}.csv\n')

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

        subcat = [val for val in self.subcat if val != 'all']
        for it in list(product(subcat, self.sort)):
            add.loc[(add['subcat'] == f'{it[0]}') & (add['sort'] == f'{it[1]}'), 'subcatArea'] = sum.loc[f'{cat}_all_{it[0]}_{it[1]}', 'area']

        for c in ['catArea', 'sscatArea', 'subcatArea']:
            add[f'%{c}'] = add['area']/add[c]


        self.resume = pd.concat([self.resume, add])
        self.resume.index = self.resume.id

        if hasattr(self, 'colPonderation'):
            for p in self.colPonderation:
                for i in self.resume.index:
                    try:
                        self.resume.loc[i, f'pond{p}'] = intStats.loc[i, f'pond{p}'] / intStats.loc[i, 'pondArea']
                    except:
                        pass
                        
        self.resume.to_csv(f'{files.output}/{self.resumeName}.csv', sep = ';', index = None)

 
    def CombineTables(self, files, name, table1, table2, how, save,  key, *fields):

        table1 = self.Load(f'{files.input}/{table1}.csv')
        table2 = self.Load(f'{files.input}/{table2}.csv')

        keys = [key]
        for e in fields:
            keys.append(e)
            
        table1 = table1.merge(table2[keys], on=key, how=how)       
        for c in table1.columns:
            try:
                table1[c] = table1[c].astype(float)
            except:
                pass

        if save == True:
            table1.to_csv(f'{files.output}/{name}.csv', sep = ';')
        return table1


    def CombineSortTables(self, files, df, name, sortColumns, splitColumns, columnsTransfert):

        df = self.Load(f'{files.input}/{df}.csv')

        for i in df.index:
            s = df.loc[i, 'sort'] 
            sub = df.loc[i, 'subcat']
            df.loc[i, 'subcatSort'] = f'{sub}_{s}'
        
        for col in sortColumns:
            cvalues = list(set(df[col]))
            setattr(self, col, cvalues)

        
        a = getattr(self, sortColumns[0])
        b = getattr(self, sortColumns[1])
        split = list(set(df[splitColumns]))

        ttt = pd.DataFrame()
        i = 0
        for aa, bb in list(product(a, b)):

            dd = df.copy()
            dd = dd[(dd[sortColumns[0]] == aa) & (dd[sortColumns[1]] == bb)]
            
            for sp in split:

                ddf = dd[dd[splitColumns] == sp]
                
                for ct in columnsTransfert:
                    if ddf.shape[0] == 1:
                        pp = ddf[ct]
                        ttt.loc[i, f'{ct}{sp}'] = pp[pp.index[0]]
                        ttt.loc[i, sortColumns[0]] = aa
                        ttt.loc[i, sortColumns[1]] = bb
                    elif ddf.shape[0] == 0:
                        ttt.loc[i, f'{ct}{sp}'] = 0
                        ttt.loc[i, sortColumns[0]] = aa
                        ttt.loc[i, sortColumns[1]] = bb

        i += 1

        ttt.to_csv(f'{files.output}/{name}.csv', sep = ';', index = None)


    def ModalResume(self, files):

        self.resume = self.Load(f'{files.stats}/resume.csv')
        self.resume.index = self.resume['id']
        self.modalResume = pd.DataFrame()

        for c, ssc in list(product(files.cat, files.sscat)):
        
            try:
                a = self.resume[(self.resume['cat'] == c) & (self.resume['sscat'] == ssc) & (self.resume['subcat'] == 'all')]
                a = a['%catArea']
                b = self.resume[(self.resume['cat'] == c) & (self.resume['sscat'] == ssc) & (self.resume['subcat'] == 'all')]
                b = b['area']
                
                self.modalResume.loc[c, f'%{ssc}'] = a[0]
                self.modalResume.loc[c, f'area{ssc}'] = b[0]
                self.modalResume.loc[c, 'cat'] = c
            except:
                self.modalResume.loc[c, f'%{ssc}'] = 0
                self.modalResume.loc[c, f'area{ssc}'] = 0
                self.modalResume.loc[c, 'cat'] = c


        self.modalResume = self.samples.merge(self.modalResume, on = 'cat', how = 'outer')


       # to correct 

        #df = self.modalResume

        #df['tAl'] = df['areaClinopyroxene'] + df['areaPlagioclase'] + df['areaSpinelle'] + df['areaAmphibole']
        #df['tCpx'] = df['areaClinopyroxene'] / df['tAl']
        #df['tPlSp'] = (df['areaPlagioclase'] + df['areaSpinelle']) / df['tAl']
        #df['tAmph'] = df['areaAmphibole'] / df['tAl']
        
        #df['tOlOpxAl'] = df['areaOlivine'] + df['areaOrthopyroxene'] + df['tAl']
        #df['tOl'] = df['areaOlivine'] / df['tOlOpxAl']
        #df['tOpx'] = df['areaOrthopyroxene'] / df['tOlOpxAl']
        #df['tCpxPlSpAmph'] = df['tAl'] / df['tOlOpxAl']

        #self.modalResume = df

        self.modalResume.to_csv(f'{files.output}/modalResume.csv', sep = ';', index = None)
     

    def TernaryComposition(self, files, dfInput, dfOutput):

        df = self.Load(f'{files.output}/{dfInput}.csv')

        if hasattr(self, 'ternaryCompositions') == False:
            dd = pd.DataFrame()
        else:
            dd = self.ternaryCompositions


        if hasattr(self, 'name'):
            name = self.name
        else:
            name = ''.join(self.names)

        for i, j in zip(['a', 'b', 'c'], self.names):
            setattr(self, i, j)
            
        for i, j in zip(['va', 'vb', 'vc'], self.values):
            if '_' in j:
                elements = j.split('_')
                ee = elements[0]
                dd[j] = df[f'area{ee}']
                for e in range(1, len(elements)):
                    ele = elements[e]
                    dd[j] = dd[j] + df[f'area{ele}']
                setattr(self, i, j)
            else:
                setattr(self, i, j)
                dd[j] = df[f'area{j}']

        dd['cat'] = df['cat']
        dd[name] = dd[self.va] + dd[self.vb] + dd[self.vc]

        for i, j in zip([self.a, self.b, self.c], [self.va, self.vb, self.vc]):
            dd[i] = dd[j]/dd[name]

        dd[f'control{name}'] = dd[self.a] + dd[self.b] + dd[self.c]
            
        self.ternaryCompositions = dd

        dd.to_csv(f'{files.output}/{dfOutput}.csv', sep = ';', index = None)


    def SortCategories(self, files):
        """Trie les catégories de lames selon les critères définis"""
        
        self.resume = pd.read_csv(f'{files.output}/resume.csv', sep = ';', index_col = 'id')
        
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
                    if self.resume.loc[f'{cat}_Olivine_neo_{sort}', '%sscatArea'] <= 0.15 :
                        if self.resume.loc[f'{cat}_Olivine_neo_{sort}', 'pondEGD'] <= 100:
                            self.samples.loc[cat, f'facies_{sort}'] = 'protomylonite BT'
                        elif self.resume.loc[f'{cat}_Olivine_neo_{sort}', 'pondEGD'] > 100:
                            self.samples.loc[cat, f'facies_{sort}'] = 'mylonite HT'
            except:
                pass
                
            try:
                if self.resume.loc[f'{cat}_Olivine_neo_{sort}', '%sscatArea'] > 0.15 and self.resume.loc[f'{cat}_Olivine_neo_{sort}', '%sscatArea'] <= 0.5:
                    self.samples.loc[cat, f'facies_{sort}'] = 'mylonite BT'
            except:
                pass
                
            try:
                if self.resume.loc[f'{cat}_Olivine_neo_{sort}', '%sscatArea'] > 0.5:
                    self.samples.loc[cat, f'facies_{sort}'] = 'ultramylonite'
            except:
                pass

            #try:
            #    if self.resume.loc[f'{cat}_all_neo_{sort}', '%catArea'] <= 0.1 and self.resume.loc[f'{cat}_all_neo_{sort}', '%catArea'] <= 800:
            #        self.samples.loc[cat, f'facies_{sort}'] = 'protomylonite BT'
            #except:
            #    pass
                
        self.samples.to_csv(f'{files.output}/samples.csv', sep = ';')


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
            
                table2.to_csv(f'{files.output}/{cat}_{ssc}_{self.name}.csv', sep = ';', index = None)
                    

    def Neighbors(self, files, cat):
        '''Calculate the mean values of the parameters of the neighbors of each grain, keeps the id of the neighbors used in calculations, keep the subcat if available for further statistics
        
        INPUT :

            cat      : sample name

            (sort)   ; columns for sorting grains in Sort function

        
        OUTPUT :

            [GrainsNeighbors]
            | id | id_neighbors | area | perimeter | neighbors{parameters}  |... | sscat | sort | 

        '''

        neighbors = self.Load(f'{files.input}/{cat}_NeighborsPairs.csv')
        grains = self.Load(f'{files.input}/{cat}_all_Grains.csv')
        
        ids = list(set(grains['id']))
            
        AllNeighbors = pd.DataFrame()


        for e in range(0, 15):

            i = ids[e]
                    
            gn1 = neighbors[neighbors['grain1'] == i]
            gn2 = neighbors[neighbors['grain2'] == i]

            neighbor = list(gn1['grain2']) + list(gn2['grain1'])
            segNumber = len(neighbor)
            neighbor = list(set(neighbor))

            neighDf = grains[grains['id'].isin(neighbor)]
            neighDf = neighDf.mean(numeric_only=True)
            neighDf = pd.DataFrame(neighDf)
            neighDf = neighDf.T
            del neighDf['id']

            for c in neighDf.columns:
                if c != 'id':
                    neighDf = neighDf.rename(columns = {c: f'neighbors{c}'})
                    
            neighDf['id_neighbors'] = '_'.join(str(nn) for nn in neighbor)
            neighDf['id'] = i
            neighDf['segNumber'] = segNumber
            neighDf['neighborsNumber'] = len(neighbor)

            AllNeighbors = pd.concat([AllNeighbors, neighDf])
            
        if hasattr(self, 'sort'):
            a = ['id', 'sscat', 'EGD', 'area', 'perimeter']
            for s in self.sort:
                a.append(s)
            AllNeighbors = AllNeighbors.merge(grains[a], on = 'id', how = 'left')

        AllNeighbors.to_csv(f'{files.output}/{cat}_all_GrainsNeighbors.csv', sep = ';', index = None)

        

    def NeighborsCompoStatistics(self, files, cat):
        ''' Calculate the length and the corresponding percentage of each grain shared with the phasis of the neighbors
            Return a complete table of neighbors pairs from grains and ebsd table (with mean x and y from ebsd merging)

        INPUT :

            cat      : sample name

            (sort)   ; columns for sorting grains in Sort function

        
        OUTPUT :

            [NeighborsCompositions]
            | id | sscat | area | perim | segLength{sscat} | %boundary{sscat} |


            [NeighborsPairs]
            | grain1 | grain2 | ebsd1 | ebsd2 | x | y | mineral1 | mineral2 | {orientation parameters} | 

        '''


        neighbors = self.Load(f'{files.input}/{cat}_NeighborsPairs.csv')
        grains = self.Load(f'{files.input}/{cat}_all_Grains.csv')
        ebsd = self.Load(f'{files.input}/{cat}_all_EBSD.csv')

        for i in [1, 2]:
            neighbors = neighbors.merge(grains[['id', 'sscat']], left_on = f'grain{i}', right_on = 'id', how = 'left')
            neighbors[f'mineral{i}'] = neighbors['sscat']
            del neighbors['id']
            del neighbors['sscat']
        
        print('grains')
        for i in [1, 2]:
            neighbors = neighbors.merge(ebsd[['id', 'x', 'y']], left_on = f'ebsd{i}', right_on = 'id', how = 'left')
            neighbors[f'x{i}'] = neighbors['x']
            neighbors[f'y{i}'] = neighbors['y']
            del neighbors['id']
            del neighbors['x']
            del neighbors['y']
        
        for e in ['x', 'y']:
            neighbors[e] = (neighbors[f'{e}1'] + neighbors[f'{e}2'])/2
            for f in [1, 2]:
                del neighbors[f'{e}{f}']

        print('x y')

        neighbors.to_csv(f'{files.output}/{cat}_NeighborsPairs.csv', sep = ';', index = None)

        neigh = grains[['id', 'sscat', 'perimeter', 'area', 'GOS', 'EGD']]
        sscat = list(set(grains.sscat))
        ids = list(set(neigh['id']))
        idd = ids[0:30]

        for a in list(product(idd, sscat)):
            print(a)
            g1 = neighbors[(neighbors['grain1'] == a[0]) & (neighbors['mineral2'] == a[1])]
            g2 = neighbors[(neighbors['grain2'] == a[0]) & (neighbors['mineral1'] == a[1])]
            s1 = np.sum(g1['segLength'])
            s2 = np.sum(g2['segLength'])

            mine = a[1]
            neigh.loc[neigh['id'] == a[0], f'segLength{mine}'] = s1 + s2
        
        for ssc in sscat:
            neigh[f'%boundary{ssc}'] = neigh[f'segLength{ssc}']/neigh['perimeter']


        if hasattr(self, 'sort'):
            a = ['id']
            for s in self.sort:
                a.append(s)
            neigh = neigh.merge(grains[a], on = 'id', how = 'left')

        neigh.to_csv(f'{files.output}/{cat}_all_NeighborsCompositions.csv', sep = ';', index = None)


        
    def SortSlices(self, files, cat):
        ''' Return a new dataframe with classes defined from a minimum and maximum value with a step. Dataframe is sliced and mean parameters are calculated in order to compare variations with the classes in the wanted column. Ieteration over m and M, down and upper boundary of the class.

        INPUT :

            cat      : sample name

            table    ; name of the dataframe to slice
        
        OUTPUT :

            [{cat}_{sscat}_sliced{table}]
            | columns | m | M | sliced{column} |

        '''

        for ssc in files.sscat:
            if os.path.exists(f'{files.input}/{cat}_{ssc}_{self.table}.csv'):
                df = self.Load(f'{files.input}/{cat}_{ssc}_{self.table}.csv')

                if self.maxi == 'auto':
                    self.end = np.max(df[self.column])
                else:
                    self.end = self.maxi
                if self.mini == 'auto':
                    self.begin = np.min(df[self.column])
                else:
                    self.begin = self.mini

                if self.stepType == 'step':
                    values = np.arange(self.begin, self.end, self.step)
                if self.stepType == 'nb':
                    values = np.linspace(self.begin, self.end, self.step, endpoint=True)

                if type(self.roundo) == 'int':
                    roundo = self.roundo
                else:
                    roundo = 0

                values = [round(val, roundo) for val in values]

                dd = pd.DataFrame()

                for i in range(1, len(values)):
                    m = values[i-1]
                    M = values[i]
                    d = df[(df[self.column] >= m) & (df[self.column] < M)]
                    if d.shape[0] > 0:
                        d[f'sliced{self.column}--{self.mini}-{self.maxi}--{self.step}{self.stepType}'] = f'{m}_{M}'
                        d[f'sliced{self.column}--{self.mini}-{self.maxi}--{self.step}{self.stepType}Value'] = (m + M) /2
                        dd = pd.concat([dd, d])

                dd.to_csv(f'{files.output}/{cat}_{ssc}_{self.table}.csv', sep = ';', index = None)


    def GetMaximumColumn(self, files, cat):

        for ssc in files.sscat:
            if os.path.exists(f'{files.input}/{cat}_{ssc}_{self.table}.csv'):
                df = self.Load(f'{files.input}/{cat}_{ssc}_{self.table}.csv')
                
                a = np.max(df[self.column])
                if hasattr(self, 'maximumColumn') == False:
                    setattr(self, 'maximumColumn', a)
                elif hasattr(self, 'maximumColumn') == True and a > self.maximumColumn:
                    self.maximumColumn = a

        self.maximumColumn = (round(self.maximumColumn, 0)) + 1
                    

