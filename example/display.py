from path import *
from creeePY import Files, Statistics, Display, Tex
import os

# Directories

files = Files.Files(analysis, 'ZAB')

files.SetFolders(calculations = 'calculations', display = 'display', plot = 'plot', param = 'param', stats = 'stats', ctf = 'ctf',  auto = True)

files.CopyFiles(files.calculations, [files.display], extension = 'csv')

# Display

files.SetFiles(inp = files.calculations, out = files.plot)
files.SetCats(files.display, '.csv')
disp = Display.Display(files)

columns = ['EGD', 'GOS', 'GOS', 'GOS', 'GOS', 'EGD']
values = ['mixte', 2, 1, 1.5, 0.5, 200]

labels = {'Olivine': 'Ol', 'Orthopyroxene': 'Opx', 'Clinopyroxene': 'Cpx', 'Plagioclase': 'Plg', 'Spinelle': 'Sp', 'Amphibole': 'Amph'}


for eps in [False]:
    files.SetFiles(inp = files.display, out = files.plot)
    disp.SetParam(fontFamily = 'serif', fontSize = 18, height = 30, width = 15, dpi = 400, version = 'EN', eps = eps, sort = 'EGD_200', barLegend = '100 um', grad = 6, text = None)
        
    #disp.Iteration(files, disp.PhasesMap)
    #disp.Iteration(files, disp.BoundariesMap)

    disp.SetParam(minimum = 0, maximum = 15, color = 'sscat', field = 'grod', colorbar = False, boundaries = True)
    #disp.Iteration(files, disp.FieldMap)
    #disp.Iteration(files, disp.ColorBar)

    disp.SetParam(minimum = 'all', maximum = 'all', color = 'black', field = 'area', colorbar = False, boundaries = True, all = True)
    #disp.Iteration(files, disp.FieldMap)
    #disp.Iteration(files, disp.ColorBar)

    disp.SetParam(minimum = 'all', maximum = 'all', color = 'teal', field = 'GOS', colorbar = False, boundaries = True, all = True)
    #disp.Iteration(files, disp.FieldMap)
    #disp.Iteration(files, disp.ColorBar)

    disp.SetParam(minimum = 0, maximum = 4, color = 'sscat', field = 'kam', colorbar = False, boundaries = True)
    #disp.Iteration(files, disp.FieldMap)
    #disp.Iteration(files, disp.ColorBar)

    #disp.SetParam(table = 'resumeNeighborsCompositions', sort = ['EGDmixte'], subcat = ['neo', 'porph'], cmap = 'turbo', labels = labels, on = '50%')
    #disp.Iteration(files, disp.PlotPercentBoundary)

    for s in ['EGDmixte']:
        disp.SetParam(subcat = ['neo', 'porph'], sort = s, boundaries = True)
        #disp.Iteration(files, disp.SortMap)
        disp.SetParam(sort = s, boundaries = False)
        #disp.Iteration(files, disp.SortMap)


    for col, val in zip(columns, values):

        disp.SetParam(column = col, value = val, sort = f'{col}{val}')
        #disp.Pie(files)
        #disp.PieSubcat(files)

        disp.SetParam(height = 6, width = 9, bins = 40, density = False, task = 'Grains', weight = 'area', fontSize = 14)
        disp.SetParam(field = 'EGD', legend = 'EGD (µm)')
        disp.Iteration(files, disp.Histogram, iterMineral = True)
        #disp.SetParam(field = 'shapeFactor', legend = 'Shape Factor')
        #disp.Iteration(files, disp.Histogram, iterMineral = True)
        #disp.SetParam(field = 'GOS', legend = 'GOS')
        #disp.Iteration(files, disp.Histogram, iterMineral = True)


files.CopyFiles(files.plot, [files.figures], extension = 'eps')

taskCat = ['PhasesMap', 'BoundariesMap', 'kamMap', 'grodMap', 'histEGD', 'histshapeFactor', 'histGOS', 'SortEGD', 'pieSubcat', 'pie']
files.SortFiles([files.plot], taskCat, sep = '')
