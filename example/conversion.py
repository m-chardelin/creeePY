from path import *
from creeePY import Files, Statistics, Display, Tex
import os


###  ANALYSE DES DONNEES EBSD ##############################################

files = Files.Files(analysis, 'ZAB')

pgrm = ['bash', 'python3']
#files.SetConfig(pgrm)

# arborescence des fichiers
files.SetFolders(display = 'display', calculations = 'calculations', graphs = 'graphs', plot = 'plot', param = 'param', stats = 'stats', tex = 'tex', config = 'config', ctf = 'ctf', results = 'results', auto = True)
files.SetSubFolders(files.tex, ['figures', 'text'])


# statistiques
stats = Statistics.Statistics(files)

files.SetCats(files.calculations, '.csv')

columns = ['EGD', 'EGD', 'GOS', 'GOS', 'GOS', 'GOS', 'EGD']
values = ['manuel', 'mixte', 2, 1, 1.5, 0.5, 200]
sort = ['EGDmanuel', 'EGDmixte', 'GOS1', 'GOS2']

files.SetFiles(inp = files.display, out = files.calculations)
#stats.SetParam(sort = sort)
#stats.SortCategories(files)

stats.SetParam(columns1 = ['id', 'grod', 'kam'], table1 = 'EBSD', table2 = 'Grains', columns2 = ['id', 'EGDmanuel', 'EGDmixte', 'GOS1', 'GOS2', 'GOS1.5', 'GOS0.5', 'EGD200'], name = 'Chemistry')
#stats.Iteration(files, stats.CalculateMeanGrains)

# copie dans le dossier résultat pour archivage
files.SetSubFolders(files.results, ['xls', 'csv', 'fig', 'tables', 'fiches'])
files.CopyFiles(files.calculations, [files.csv])
files.CopyFiles(files.stats, [files.tables])

# conversion en .xls
files.SetFiles(inp = files.csv, out = files.xls)
files.SetParam(table = 'Grains', subcat = ['all', 'rex', 'porph'], sort = sort)
files.Iteration(files, files.CombineCatsXls)
files.SetParam(table = 'IntermediaryCalculations')
files.Iteration(files, files.CombineCatsXls)
#files.ConvertXls(files.txt, files.xls, extension = '.csv')

