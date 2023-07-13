from path import *
from creeePY import Files, Statistics, Display, Tex
import os
import numpy as np

###  ANALYSE DES DONNEES EBSD ##############################################


files = Files.Files(analysis, 'ZAB')

pgrm = ['bash', 'python3']
#files.SetConfig(pgrm)

# arborescence des fichiers
files.SetFolders(display = 'display', calculations = 'calculations', graphs = 'graphs', plot = 'plot', param = 'param', stats = 'stats', tex = 'tex', config = 'config', ctf = 'ctf', auto = True)
files.SetSubFolders(files.tex, ['figures', 'text'])


# statistiques
stats = Statistics.Statistics(files)

# combinaison des tables pour qu'il n'y ait plus de minéraux accesoires


files.SetCats(files.display, '.csv')

columns = ['EGD', 'GOS', 'GOS', 'GOS', 'GOS', 'EGD']
values = ['mixte', 2, 1, 1.5, 0.5, 200]
stats.SetParam(on = ['50%', 'mean', 'std'], subcat = ['all', 'neo', 'porph'], sort = ['EGDmixte', 'GOS1', 'GOS2', 'GOS1.5', 'GOS0.5', 'EGD200'], mean = True)

files.SetFiles(inp = files.calculations, out = files.calculations)
stats.Iteration(files, stats.Neighbors)
stats.Iteration(files, stats.NeighborsCompoStatistics)

files.SetFiles(inp = files.calculations, out = files.calculations)

stats.SetParam(column = 'sscat', table = 'GrainsNeighbors')
stats.Iteration(files, stats.Split)
stats.SetParam(column = 'sscat', table = 'NeighborsCompositions')
stats.Iteration(files, stats.Split)

stats.SetParam(column = 'EGD', table = 'GrainsNeighbors')
stats.Iteration(files, stats.GetMaximumColumn)
stats.SetParam(column = 'EGD', table = 'GrainsNeighbors', maxi = stats.maximumColumn, mini = 0, step = 100, stepType = 'nb', roundo = 0)
stats.Iteration(files, stats.SortSlices)
stats.SetParam(column = 'EGD', table = 'NeighborsCompositions', maxi = stats.maximumColumn, mini = 0, step = 100, stepType = 'nb')
stats.Iteration(files, stats.SortSlices)


####### SORT EGD/GOS stats
stats.SetParam(table = 'GrainsNeighbors', stat = 'GrainsNeighborsStats')
stats.Iteration(files, stats.Describe)
stats.SetParam(table = 'GrainsNeighbors', stat = 'GrainsNeighborsStats', intermediaryCalculations = 'IntermediaryCalculationsGrainsNeighbors')
stats.Iteration(files, stats.IntermediaryCalculations, iterMineral = True)
stats.SetParam(table = 'IntermediaryCalculationsGrainsNeighbors', stat = 'IntermediaryCalculationsGrainsNeighborsStats')
stats.Iteration(files, stats.Describe)
stats.SetParam(grainsStat = 'GrainsNeighborsStats', intermediaryCalculationsStats = 'IntermediaryCalculationsGrainsNeighborsStats', resumeName = 'resumeGrainsNeighbors', ponderation = False)
stats.Iteration(files, stats.Resume)

stats.SetParam(table = 'NeighborsCompositions', stat = 'NeighborsCompositionsStats')
stats.Iteration(files, stats.Describe)
stats.SetParam(table = 'NeighborsCompositions', stat = 'NeighborsCompositionsStats', intermediaryCalculations = 'IntermediaryCalculationsNeighborsCompositions', ponderation = False)
stats.Iteration(files, stats.IntermediaryCalculations, iterMineral = True)
stats.SetParam(table = 'IntermediaryCalculationsNeighborsCompositions', stat = 'IntermediaryCalculationsNeighborsCompositionsStats')
stats.Iteration(files, stats.Describe)
stats.SetParam(grainsStat = 'NeighborsCompositionsStats', intermediaryCalculationsStats = 'IntermediaryCalculationsNeighborsCompositionsStats', resumeName = 'resumeNeighborsCompositions')
stats.Iteration(files, stats.Resume)


####### SORT SLICED EGD

subcat = list(np.linspace(0, stats.maximumColumn, 100, endpoint = True))
subcat.append('all')
sort = [f'slicedEGD--0-{stats.maximumColumn}--100nb']
stats.SetParam(on = ['50%', 'mean', 'std'], subcat = subcat, sort = sort, mean = True)

stats.SetParam(table = 'GrainsNeighbors', stat = 'GrainsNeighborsStats')
stats.Iteration(files, stats.Describe)
stats.SetParam(table = 'GrainsNeighbors', stat = 'GrainsNeighborsStats', intermediaryCalculations = 'IntermediaryCalculationsGrainsNeighbors')
stats.Iteration(files, stats.IntermediaryCalculations, iterMineral = True)
stats.SetParam(table = 'IntermediaryCalculationsGrainsNeighbors', stat = 'IntermediaryCalculationsGrainsNeighborsStats')
stats.Iteration(files, stats.Describe)
stats.SetParam(grainsStat = 'GrainsNeighborsStats', intermediaryCalculationsStats = 'IntermediaryCalculationsGrainsNeighborsStats', resumeName = 'resumeGrainsNeighbors', ponderation = False)
stats.Iteration(files, stats.Resume)

stats.SetParam(table = 'NeighborsCompositions', stat = 'NeighborsCompositionsStats')
stats.Iteration(files, stats.Describe)
stats.SetParam(table = 'NeighborsCompositions', stat = 'NeighborsCompositionsStats', intermediaryCalculations = 'IntermediaryCalculationsNeighborsCompositions', ponderation = False)
stats.Iteration(files, stats.IntermediaryCalculations, iterMineral = True)
stats.SetParam(table = 'IntermediaryCalculationsNeighborsCompositions', stat = 'IntermediaryCalculationsNeighborsCompositionsStats')
stats.Iteration(files, stats.Describe)
stats.SetParam(grainsStat = 'NeighborsCompositionsStats', intermediaryCalculationsStats = 'IntermediaryCalculationsNeighborsCompositionsStats', resumeName = 'resumeNeighborsCompositions')
stats.Iteration(files, stats.Resume)


files.TransferFiles(files.calculations, [files.stats], extension = 'resume')
