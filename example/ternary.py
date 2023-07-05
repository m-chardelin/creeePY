from path import *
from creeePY import Files, Statistics, Display, Tex
import os
import numpy as np

###  ANALYSE DES DONNEES EBSD ##############################################


files = Files.Files(analysis, 'ZAB')

pgrm = ['bash', 'python3']
#files.SetConfig(pgrm)

# arborescence des fichiers
files.SetFolders(display = 'display', calculations = 'calculations', graphs = 'graphs', plot = 'plot', param = 'param', stats = 'stats', tex = 'tex', config = 'config', ctf = 'ctf', results = 'results', auto = True)
files.SetSubFolders(files.tex, ['figures', 'text'])


# statistiques
stats = Statistics.Statistics(files)

# combinaison des tables pour qu'il n'y ait plus de minéraux accesoires


files.SetCats(files.display, '.csv')

columns = ['EGD', 'EGD', 'GOS', 'GOS', 'GOS', 'GOS', 'EGD']
values = ['manuel', 'mixte', 2, 1, 1.5, 0.5, 200]
stats.SetParam(on = ['50%', 'mean', 'std'], subcat = ['all', 'neo', 'porph'], sort = ['EGDmixte', 'GOS1', 'GOS2', 'GOS1.5', 'GOS0.5', 'EGD200'], mean = True)

files.SetFiles(inp = files.stats, out = files.stats)

stats.SortCategories(files)


#stats.CombineTables(files, name = 'all', table1 = 'resume', table2 = 'samples', how = 'inner', save = True, key = 'cat', 'massif', 'lithologyDef', 'facies_EGDmixte')
stats.CombineTables(files, 'all', 'resume', 'samples', 'inner', True, 'cat', 'massif', 'lithologyDef', 'facies_EGDmixte')
stats.CombineTables(files, 'indexSamples', 'index', 'samples', 'inner', True, 'cat', 'massif', 'lithologyDef', 'facies_EGDmixte', 'XStep')

stats.ModalResume(files)



names = ['Cpx', 'PlSp', 'Amph']
values = ['Clinopyroxene', 'Plagioclase_Spinelle', 'Amphibole']
stats.SetParam(names = names, values = values, name = 'Altot')
stats.TernaryComposition(files, 'modalResume', 'ternaryCompositions')

names = ['Ol', 'Opx', 'Al']
values = ['Olivine', 'Orthopyroxene', 'Clinopyroxene_Plagioclase_Spinelle_Amphibole']
stats.SetParam(names = names, values = values, name = 'OlOpxAl')
stats.TernaryComposition(files, 'modalResume', 'ternaryCompositions')
stats.CombineTables(files, 'ternaryFinal', 'ternaryCompositions', 'samples', 'outer', True, 'cat', 'massif', 'lithologyDef', 'facies_EGDmixte')

#stats.CombineSortTables(files, 'resume', 'combSscat', ['cat', 'subcatSort'], 'sscat', ['meanSF', 'meanaspectRatio', 'meanEGD', 'pondSF', 'pondaspectRatio', 'pondEGD'])
#stats.CombineSortTables(files, 'resume', 'combSscat', ['cat', 'sscat'], 'subcatSort', ['meanSF', 'meanaspectRatio', 'meanEGD', 'pondSF', 'pondaspectRatio', 'pondEGD'])
