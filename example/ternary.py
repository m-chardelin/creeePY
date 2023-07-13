from path import *
from creeePY import Files, Statistics, Display, Tex
import os
import numpy as np

###  ANALYSE DES DONNEES EBSD ##############################################


files = Files.Files(analysis, 'ZAB')

# arborescence des fichiers
files.SetFolders(display = 'display', calculations = 'calculations', graphs = 'graphs', plot = 'plot', param = 'param', stats = 'stats', tex = 'tex', config = 'config', ctf = 'ctf', auto = True)
files.SetSubFolders(files.tex, ['figures', 'text'])

# statistiques
stats = Statistics.Statistics(files)

# combinaison des tables pour qu'il n'y ait plus de minéraux accesoires

files.SetCats(files.display, '.csv')

stats.SetParam(on = ['50%', 'mean', 'std'], subcat = ['all', 'neo', 'porph'], sort = ['EGDmixte', 'GOS1', 'GOS2', 'GOS1.5', 'GOS0.5', 'EGD200'], mean = True)

files.SetFiles(inp = files.stats, out = files.stats)

stats.SortCategories(files)

#stats.CombineTables(files, name = 'all', table1 = 'resume', table2 = 'EBSD', how = 'inner', save = True, key = 'cat', 'massif', 'lithologyDef', 'facies_EGDmixte')
resume = stats.Load(f'{files.input}/resume.csv')
resume = resume[(resume['sscat'] == 'Olivine') & (resume['subcat'] == 'neo') & (resume['sort'] == 'EGDmixte')]
resume = resume[['id', 'cat', 'sscat', 'subcat', 'sort', '%catArea', '%sscatArea', 'meanEGD', 'pondEGD']]
resume.columns = ['id', 'cat', 'sscat', 'subcat', 'sort', 'Ol%catArea', 'Ol%sscatArea', 'OlmeanEGD', 'OlpondEGD']
resume.to_csv(f'{files.input}/neoProp.csv', sep = ';', index = None)

stats.CombineTables(files, 'EBSD', 'EBSD', 'neoProp', 'left', True, 'cat', 'Ol%catArea', 'Ol%sscatArea', 'OlmeanEGD', 'OlpondEGD')
stats.CombineTables(files, 'EBSD', 'EBSD', 'samples', 'left', True, 'sample', 'triEGD', 'massif')
stats.CombineTables(files, 'all', 'resume', 'EBSD', 'inner', True, 'cat', 'lithologyDef', 'facies_EGDmixte', 'massif')
stats.CombineTables(files, 'indexSamples', 'index', 'EBSD', 'inner', True, 'cat', 'lithologyDef', 'facies_EGDmixte', 'XStep', 'massif')


stats.ModalResume(files)

names = ['Cpx', 'PlSp', 'Amph']
values = ['Clinopyroxene', 'Plagioclase_Spinelle', 'Amphibole']
stats.SetParam(names = names, values = values, name = 'Altot')
stats.TernaryComposition(files, 'modalResume', 'ternaryCompositions')

names = ['Ol', 'Opx', 'Al']
values = ['Olivine', 'Orthopyroxene', 'Clinopyroxene_Plagioclase_Spinelle_Amphibole']
stats.SetParam(names = names, values = values, name = 'OlOpxAl')
stats.TernaryComposition(files, 'modalResume', 'ternaryCompositions')

stats.CombineTables(files, 'article-final', 'modalResume', 'EBSD', 'left', True, 'cat', 'facies_EGDmixte', 'lithologyDef', 'massif', 'Ol%sscatArea', 'OlpondEGD')

stats.CombineTables(files, 'ternaryCompositions', 'ternaryCompositions', 'neoProp', 'left', True, 'cat', 'Ol%catArea', 'Ol%sscatArea', 'OlmeanEGD', 'OlpondEGD')
stats.CombineTables(files, 'ternaryFinal', 'ternaryCompositions', 'EBSD', 'outer', True, 'cat', 'lithologyDef', 'facies_EGDmixte', 'massif')


values = ['pondSF', 'pondEGD', 'pondGOS', 'pondaspectRatio']
stats.CombineSortTables(files, 'resume', 'CombSort', ['subcat', 'sort'], values = values)
stats.CombineSortTables(files, 'resume', 'CombAll', ['sscat', 'subcat', 'sort'], values = values)
stats.CombineSortTables(files, 'resume', 'CombSScat', ['sscat'], values = values)

stats.CombineTables(files, 'combAll', 'combAll', 'EBSD', 'left', True, 'cat', 'massif', 'facies_EGDmixte', 'lithologyDef', 'Ol%catArea', 'Ol%sscatArea', 'OlmeanEGD', 'OlpondEGD')
stats.CombineTables(files, 'combSort', 'combSort', 'EBSD', 'left', True, 'cat', 'lithologyDef', 'facies_EGDmixte', 'massif', 'Ol%catArea', 'Ol%sscatArea', 'OlmeanEGD', 'OlpondEGD')
stats.CombineTables(files, 'combSscat', 'combSscat', 'EBSD', 'left', True, 'cat', 'massif', 'lithologyDef', 'facies_EGDmixte', 'Ol%catArea', 'Ol%sscatArea', 'OlmeanEGD', 'OlpondEGD')
stats.CombineTables(files, 'indexSamples', 'indexSamples', 'neoProp', 'left', True, 'cat', 'Ol%catArea', 'Ol%sscatArea', 'OlmeanEGD', 'OlpondEGD')



