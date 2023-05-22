from path import *
from creeePY import Files, Statistics, Display, Plot, Tex
import os

# Directories

files = Files.Files(analysis, 'ZAB')

files.SetFolders(raw = 'raw', data = 'data', fig = 'figures', param = 'param', stats = 'stats', tex = 'tex', config = 'config', ctf = 'ctf', results = 'results', auto = True)

files.SetCats(files.data, '.txt')

# Display


files.SetFiles(inp = files.stats, out = files.fig)

plot = Plot.Plot(files)
       
plot.SetParam(fontFamily = 'serif', fontSize = 18, height = 30, width = 15, dpi = 400, version = 'EN', eps = False, s = 100)

plot.GetParam()
        
#df = pd.read_csv('/storage/emulated/0/scripts/tests/ternaryPlot/test.txt', sep = '/')

#plot.PlotTernary(files, 'Ol', 'Opx', 'Al', df, 'massif', 'massif', 'facies_EGDmixte')
#plot.PlotTernary(files, 'CpxAl', 'PlSpAl', 'TrAl', df, 'massif', 'massif', 'facies_EGDmixte')

plot.PlotScatterXYSave(files, 'pondGOSrexEGDmixte', 'pondaspectRatioporphEGDmixte', 'comb', 'sscat', 'sscat', 'sscat', 'sscat', ';', sort = 'sscat_Olivine')

plot.SetParam(fontFamily = 'serif', fontSize = 18, height = 42, width = 30, dpi = 400, version = 'EN', eps = False, s = 100)

plot.IterationPlot(files)
