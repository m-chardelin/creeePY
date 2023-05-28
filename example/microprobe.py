from path import *
from creeePY import Files, Statistics, Display, Tex
import os

# Directories

files = Files.Files(analysis, 'ZAB')

files.SetFolders(display = 'display', calculations = 'calculations', graphs = 'graphs', plot = 'plot', param = 'param', stats = 'stats', tex = 'tex', config = 'config', ctf = 'ctf', results = 'results', verif = 'verif', auto = True)

files.SetSubFolders(files.tex, ['figures', 'text'])

files.CopyFiles(files.calculations, [files.display], extension = 'csv')

# Display

files.SetFiles(inp = files.display, out = files.plot)
files.SetCats(files.display, '.csv')
disp = Display.Display(files)

columns = ['EGD', 'EGD', 'GOS', 'GOS', 'GOS', 'GOS', 'EGD']
values = ['manuel', 'mixte', 2, 1, 1.5, 0.5, 200]

files.cat = ['85ZA1', '85ZA22A', '85ZA37', '85ZA45-new', '85ZA48', '85ZA11']


for eps in [False, True]:
    files.SetFiles(inp = files.display, out = files.plot)
    disp.SetParam(fontFamily = 'serif', fontSize = 18, height = 30, width = 15, dpi = 400, version = 'EN', eps = eps, sort = 'EGD_200', barLegend = '12 mm', grad = 6, text = None)
        
    #disp.Iteration(files, disp.SelectPoints)
    #disp.SetParam(quadri = True)
    #disp.Iteration(files, disp.PointsMap)
    disp.SetParam(quadri = False)
    disp.Iteration(files, disp.PointsMap)
