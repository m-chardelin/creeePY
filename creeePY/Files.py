import os
import sys
import shutil
import pandas as pd
from itertools import product, combinations, chain


class Files():
    def __init__(self, folder, name):
        
        self.folder = folder
        self.name = name


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
                    if os.path.exists(f'{files.input}/{c}_{ssc}_{self.table}.txt'):
                        func(files, c, ssc)

    
    def SetFolders(self, auto = True, **kwargs):
        """création des dossier nécessaires à la lecture des données et des résultats
        auto = True : dans le dossier principal
        auto = False : dans les dossiers indiqués (nécessité de préciser le chemin absolu / ou la variable système"""
        keys = [key for key in kwargs.keys() if key != 'auto']
        for key in keys:
                if auto == True:
                    value = f'{self.folder}/{kwargs[key]}'
                else:
                    value = kwargs[key]
                setattr(self, key, value)
                os.makedirs(getattr(self, key), exist_ok = True)
                
                
    def SetSubFolders(self, folder, subFolders):
        """Crée des ramifications à partir d'un dossier"""
        for subFolder in subFolders:
            os.makedirs(f'{folder}/{subFolder}', exist_ok = True)
            setattr(self, f'{subFolder}', f'{folder}/{subFolder}')
        
    
    def SetConfig(self, pgrm, config):
        """création d'un fichier spécial config avec :
            - liste des programmes utilisés pour la compilation
            - liste des librairies python et leurs versions
            - composition du hardware de l'ordinateur (inxi, neofetch)"""
        os.system(f'uname -a >> {config}/PgrmVersions.txt')
        for p in pgrm:
            os.system(f'{p} --version >> {config}/PgrmVersions.txt')
        os.system(f'pip3 freeze >> {config}/PythonRequirements.txt')
        # os.system('make')


    def SetFiles(self, inp, out, **kwargs):
        """crée les entrées input et output pour l'utilisation des autres somposantes de la librairie"""
        self.input = inp
        self.output = out

    
    def SetCats(self, folder, dat, cat = '', sscat = ''):
        """crée la liste des catégories (cat) et des sous catégories (sscat), puisque les fichiers sont nommés sous la forme :
        
                            MASSIF_LAME_MINERAL_CLASSE_TACHE.ext
                            EXP_COMBINAISON_ITERATION_TRI_TACHE.ext
                            
                            
                             -1     0    1     2      3
                            SUPCAT_CAT_SSCAT_SUBCAT_TASK(_detail).ext
                            detail = précisions sur le tri des lames ou le tri des grains
        
            - cat = expérience ADELI, ou lame
            - sscat = une itération dans le cas d'ADELI, un minéral... dépend de la convention de nommage qui est sensées rester la même
            
            todo : attention au niveau de nommage, trop ne sera pas assez précis """
        if cat == '':
            a = files = [file.replace(dat, '') for file in os.listdir(folder) if file.endswith(dat)]
            self.cat = set([file.split('_')[0] for file in files if file.count('_') > 1])
        else:
            self.cat = cat
        if sscat == '':
            files = [file.replace(dat, '') for file in os.listdir(folder) if file.endswith(dat)]
            self.sscat = set([file.split('_')[1] for file in files if file.count('_') > 1])
        else:
            self.sscat = sscat

   
    def SortFiles(self, folders, liste):
        """tri des données selon la liste de clefs données en argument :
            - vérifie parmi tous les fichiers d'un dossier ceux content les éléments
            - crée un dossier s'il n'existe pas déjà
            - transfère les fichiers chosis
            
            ==> permet de classer la multitude de fichiers de sortie en des dossiers facilement consultables"""
        for folder in folders:
            for lis in liste:
                files = [file for file in os.listdir(folder) if lis in file]
                for file in files:
                    os.makedirs(f'{folder}/{lis}', exist_ok = True)
                    try:
                        shutil.move(f'{folder}/{file}', f'{folder}/{lis}')
                    except:
                        os.remove(f'{folder}/{lis}/{file}')  #écrase le fichier s'il existe déjà, puis refait la copie
                        shutil.move(f'{folder}/{file}', f'{folder}/{lis}')


    def TransferFiles(self, source, destinations, extension = None, exception = None):
        """transfère les fichiers d'un dossier à l'extension données ou pas dans un autre, en ne sélectionnant que ceux qui ne comportent pas les flags"""
        for destination in destinations:
            if extension == None:
                files = [file for file in os.listdir(source)]
            else:
                files = [file for file in os.listdir(source) if file.endswith(extension)]

            if exception != None:
                for e in exception:
                    files = [file for file in files if e not in file]
                
            os.makedirs(destination, exist_ok = True)
            
            for file in files:
                try:
                    shutil.move(f'{source}/{file}', f'{destination}')
                except:
                    os.remove(f'{destination}/{file}')
                    shutil.move(f'{source}/{file}', f'{destination}')


    def CopyFiles(self, source, destinations, extension = None, exception = None):
        """transfère les fichiers d'un dossier à l'extension données ou pas dans un autre, en ne sélectionnant que ceux qui ne comportent pas les flags"""
        for destination in destinations:
            if extension == None:
                files = [file for file in os.listdir(source)]
            else:
                files = [file for file in os.listdir(source) if file.endswith(extension)]

            if exception != None:
                for e in exception:
                    files = [file for file in files if e not in file]
                
            os.makedirs(destination, exist_ok = True)
            
            for file in files:
                try:
                    shutil.copy(f'{source}/{file}', f'{destination}')
                except:
                    os.remove(f'{destination}/{file}')
                    shutil.copy(f'{source}/{file}', f'{destination}')
                
                
    def CleanFiles(self, folders, extension = None, exception = None):
        """supprime le contenu d'un dossier selon l'extension et les exception choisies"""
        for folder in folders:
            if extension == None:
                files = [file for file in os.listdir(folder)]
            else:
                files = [file for file in os.listdir(folder) if file.endswith(extension)]

            if exception != None:
                for e in exception:
                    files = [file for file in files if e not in file]
                    
            for file in files:
                try:
                    os.remove(f'{folder}/{file}')
                except:
                    shutil.rmtree(f'{folder}/{file}')
                    
                    
    def CleanTxt(self, folders, txtInput, txtOutput, extension = None, exception = None):
        """Nettoie tous les séparateurs pour un seul"""
        for folder in folders:
            if extension == None:
                files = [file for file in os.listdir(folder)]
            else:
                files = [file for file in os.listdir(folder) if file.endswith(extension)]

            if exception != None:
                for e in exception:
                    files = [file for file in files if e not in file]
                    
            for file in files:
                try:
                    a = f'{folder}/{file}'
                    with open(f'{folder}/{file}', 'r') as file:
                        text = file.read()
                        file.close()
                        for txt in txtInput:
                            text = text.replace(txt, txtOutput)
                         
                    with open(a, 'w') as newFile:
                        newFile.write(text)
                except:
                    pass


    def CombineCatsXls(self, files, cat):
        """Convertit en xls les tables avec les catégories et les sous catégories voulues"""
        
        try:
            writer = pd.ExcelWriter(f'{files.output}/{cat}_{self.table}.xlsx', engine='xlsxwriter')
                
            c = [cat]
            
            sscat = sorted(files.sscat, reverse = True)
            subcat = sorted(files.subcat)
            sort = sorted(files.sort)
            
            for it in list(product(c, sscat, subcat, sort)):
                    
                names = {'id': f'{it[1]}_{it[2]}_{it[3]}', 'cat': it[0], 'sscat': it[1], 'subcat': it[2], 'sort': it[3]}

                    
                if os.path.exists(f'{files.input}/{it[0]}_{it[1]}_{self.table}.txt'):
                    self.Load(f'{files.input}/{it[0]}_{it[1]}_{self.table}.txt')
                    
                    if names['subcat'] == 'all':
                        names['id'] = f'{it[1]}_{it[2]}'
                        self.df.to_excel(writer, sheet_name=names['id'], index = None)
                                    
                    elif names['subcat'] != 'all':
                        df = self.df[self.df[names['sort']] == names['subcat']]
                        df.to_excel(writer, sheet_name=names['id'], index = None)
            
            writer.close()
        except:
            pass

            
    def ConvertXls(self, source, destination, extension = None, exception = None):
        """Convertit en xls toutes les tables d'un fichier"""
        
        if extension == None:
            files = [file for file in os.listdir(source)]
        else:
            files = [file for file in os.listdir(source) if file.endswith(extension)]

        if exception != None:
            for e in exception:
                files = [file for file in files if e not in file]
                
        for file in files:
            file = file.replace('.txt', '')
            try:
                writer = pd.ExcelWriter(f'{destination}/{file}.xlsx', engine='xlsxwriter')
                self.Load(f'{source}/{file}')
                self.df.to_excel(writer, sheet_name='data', index = None)
                writer.close()
            except:
                pass
