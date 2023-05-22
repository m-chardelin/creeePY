from path import *
from creeePY import Files, Statistics, Display, Tex
import os
import pandas as pd

###  ANALYSE DES DONNEES EBSD ##############################################


files = Files.Files(analysis, 'ZAB')

pgrm = ['bash', 'python3']
#files.SetConfig(pgrm)

# arborescence des fichiers
files.SetFolders(display = 'display', calculations = 'calculations', graphs = 'graphs', plot = 'plot', param = 'param', stats = 'stats', tex = 'tex', config = 'config', ctf = 'ctf', results = 'results', auto = True)

# statistiques
stats = Statistics.Statistics(files)
files.SetCats(files.display, '.csv')

stats.SetParam(on = ['50%'], sort = ['EGDmixte'])
files.SetFiles(inp = files.calculations, out = files.stats)
#stats.Iteration(files, stats.AreaResume)

stats.resume = pd.read_csv(f'{files.stats}/resume.csv', sep = '&')
files.cat = list(set(stats.resume['cat']))

stats.ModalResume(files)
#stats.SetParam(names = ['Cpx', 'PlSp', 'Amph'], values = ['areaClinopyroxene', 'areaPlagioclase_areaSpinelle', 'areaAmphibole'])
#stats.modalResume = stats.TernaryComposition(stats.modalResume)

#stats.SetParam(names = ['Ol', 'Opx', 'Al'], values = ['areaOlivine', 'areaOrthopyroxene', 'CpxPlSpAmph'])
#stats.modalResume = stats.TernaryComposition(stats.modalResume)

#stats.modalResume.to_csv(f'{files.stats}/final.csv', sep = '&')

stats.SortCategories(files)
