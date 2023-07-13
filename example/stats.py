from path import *
from creeePY import Files, Statistics, Display, Tex
import os


###  ANALYSE DES DONNEES EBSD ##############################################


files = Files.Files(analysis, 'ZAB')

pgrm = ['bash', 'python3']
#files.SetConfig(pgrm)

# arborescence des fichiers
files.SetFolders(display = 'display', calculations = 'calculations', graphs = 'graphs', plot = 'plot', param = 'param', stats = 'stats', tex = 'tex', config = 'config', ctf = 'ctf', auto = True)
files.SetSubFolders(files.tex, ['figures', 'text'])
files.CleanFiles([files.calculations, files.display, files.graphs, files.ctf, files.stats])

# copie des fichiers utiles dans les répertoires
files.CopyFiles(dataClean, [files.ctf], extension = '.ctf', exception = ['-r.ctf'])
files.CopyFiles(f'{tasks}/Grains', [files.display], exception = ['Antigorite', 'Antigorite2', 'Antigorite3', 'Pargasite', 'Pargasite2', 'Phlogopite', 'Anorthite', 'Tremolite', 'Bytownite', 'Hornblende', 'notIndexed'])
files.CopyFiles(f'{tasks}/EBSD', [files.display], extension = 'csv', exception = ['Antigorite', 'Antigorite2', 'Antigorite3', 'Pargasite', 'Pargasite2', 'Phlogopite', 'Anorthite', 'Tremolite', 'Bytownite', 'Hornblende', 'png', 'eps', 'notIndexed'])
files.CopyFiles(f'{tasks}/Boundaries', [files.display], extension = 'csv', exception = ['Antigorite', 'Antigorite2', 'Antigorite3', 'Pargasite', 'Pargasite2', 'Phlogopite', 'Anorthite', 'Tremolite', 'Bytownite', 'Hornblende'])
#files.CopyFiles(f'{tasks}/Neighbors', [files.display], extension = 'csv')
files.CopyFiles(f'{tasks}/NeighborsPairs', [files.display], extension = 'csv')
files.CopyFiles(f'{tasks}/divers', [files.stats], extension = 'csv')
#files.CopyFiles(f'{tasks}/CPOcombined', [files.figures], extension = 'eps')
#files.CopyFiles(f'{tasks}/ipf', [files.figures], extension = 'eps')

files.SetCats(f'{tasks}/Grains', '.csv')

# statistiques
stats = Statistics.Statistics(files)

# combinaison des tables pour qu'il n'y ait plus de minéraux accesoires

for table in ['Grains', 'EBSD']:
    files.SetFiles(inp = f'{tasks}/{table}', out = files.display)
    stats.SetParam(inp = ['Antigorite', 'Antigorite2', 'Antigorite3', 'Pargasite', 'Pargasite2', 'Phlogopite', 'Tremolite', 'Hornblende'], out = 'Amphibole', table = table)
    stats.Iteration(files, stats.Combine)
    stats.SetParam(inp = ['Anorthite', 'Bytownite'], out = 'Plagioclase')
    stats.Iteration(files, stats.Combine)
    files.SetCats(files.display, '.csv')
    files.SetFiles(inp = files.display, out = files.display, table = 'Grains')
    stats.SetParam(inp = files.sscat, out = 'all')
    stats.Iteration(files, stats.Combine)

#stats.SetParam(columns1 = ['id', 'grod', 'kam'], table1 = 'EBSD', table2 = 'Grains', columns2 = ['all'], name = 'Chemistry')
#stats.Iteration(files, stats.CalculateMeanGrains)

files.CopyFiles(files.display, [files.calculations], exception = ['r_', 'Boundaries'])

files.SetCats(files.display, '.csv')

# table des résolutions pour les ctf
stats.Iteration(files, stats.GetRes)
stats.Res(files)

#stats.BoundariesLength(files)

# tri des porphyroclastes et des néoblastes

columns = ['EGD', 'GOS', 'GOS', 'GOS', 'GOS', 'EGD']
values = ['mixte', 2, 1, 1.5, 0.5, 200]

files.SetFiles(inp = files.calculations, out = files.calculations)
for i in range(0, len(columns)):
    stats.SetParam(sortRes = False, grainSize = 3, table = 'Grains', column = columns[i], value = values[i])
    stats.Iteration(files, stats.SortGrains, iterMineral = True)
    
# statistiques sur les grains
files.SetFiles(inp = files.calculations, out = files.calculations)
stats.SetParam(subcat = ['all', 'neo', 'porph'], sort = ['EGDmixte', 'GOS1', 'GOS2', 'GOS1.5', 'GOS0.5', 'EGD200'], stat = 'GrainsStats', table = 'Grains')
stats.Iteration(files, stats.Describe)

# calculs intermédiaires pour pondérer les champs par la surface des grains
stats.SetParam(table = 'Grains', stat = 'GrainsStats', intermediaryCalculations = 'IntermediaryCalculations')
stats.Iteration(files, stats.IntermediaryCalculations, iterMineral = True)
stats.SetParam(stat = 'IntermediaryStats', table = 'IntermediaryCalculations')
stats.Iteration(files, stats.Describe)

# écriture d'un table résumant les principales caractéristiques géométriques des grains, des rapports de surface et des champs pondérés
stats.SetParam(on = ['50%', 'mean', 'std'])
files.SetFiles(inp = files.calculations, out = files.stats)
stats.SetParam(grainsStat = 'GrainsStats', intermediaryCalculationsStats = 'IntermediaryStats', resumeName = 'resume', ponderation = False)
stats.Iteration(files, stats.Resume)

stats.SortCategories(files)
