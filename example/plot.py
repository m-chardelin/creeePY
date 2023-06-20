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
       
plot.SetParam(fontFamily = 'serif', fontSize = 18, height = 10, width = 15, dpi = 400, version = 'EN', eps = False, s = 100)

plot.GetParam()
        
plot.PlotTernary(files, 'Ol', 'Opx', 'Al', 'ternaryFinal', 'massif', 'lithologyDef', 'facies_EGDmixte')
plot.PlotTernary(files, 'Cpx', 'PlSp', 'Amph', 'ternaryFinal', 'massif', 'lithologyDef', 'facies_EGDmixte', labels = False)

plot.PlotScatterXYSave(files, 'pondGOSrexEGDmixte', 'pondaspectRatioporphEGDmixte', 'combSort', 'sscat', 'sscat', 'sscat', 'sscat', ';', sort = 'sscat_Olivine')
plot.PlotScatterXYSave(files, 'pondGOSrexEGDmixte', 'pondaspectRatioporphEGDmixte', 'combSort', 'sscat', 'sscat', 'sscat', 'sscat', ';', sort = 'sscat_Orthopyroxene')
plot.PlotScatterXYSave(files, 'J', 'BA', 'index', 'sscat', 'sscat', 'sscat', 'sscat', '&', xlim = [0, 15], ylim = [0, 1], sort = 'subcat_all')
plot.PlotScatterXYSave(files, 'J', 'BA', 'index', 'sscat', 'sscat', 'sscat', 'sscat', '&', xlim = [0, 15], ylim = [0, 1], sort = 'sscat_Olivine')
plot.PlotScatterXYSave(files, 'J', 'BA', 'index', 'sscat', 'sscat', 'sscat', 'sscat', '&', xlim = [0, 15], ylim = [0, 1], sort = 'sscat_Orthopyroxene')
    
plot.PlotScatterXYSave(files, 'BA', 'J', 'index', 'sscat', 'sscat', 'facies_EGDmixte', 'sscat', '&', xlim = [0, 1], ylim = [0, 15], sort = 'sscat_Olivine', c = 'no', cmap = 'sscat')

plot.PlotScatterXYSave(files, 'pondSFOlivine', 'pondSFOrthopyroxene', 'combSscat', 'massif', 'lithologyDef', 'facies_EGDmixte', 'massif', ';', sort = 'sort_EGDmixte')
plot.PlotScatterXYSave(files, 'pondGOSOlivine', 'pondGOSOrthopyroxene', 'combSscat', 'massif', 'lithologyDef', 'facies_EGDmixte', 'massif', ';', sort = 'sort_EGDmixte')
plot.PlotScatterXYSave(files, 'pondaspectRatioOlivine', 'pondaspectRatioOrthopyroxene', 'combSscat', 'massif', 'lithologyDef', 'facies_EGDmixte', 'massif', ';', sort = 'sort_EGDmixte')

plot.PlotScatterXYSave(files, 'BA', 'J', 'indexMerge2', 'massif', 'lithologyDef', 'facies_EGDmixte', 'massif', '&', xlim = [0, 1], ylim = [0, 15], sort = 'sscat_Olivine')
    
plot.Combine(files, 'cat', 'massif', 'lithologyDef', 'facies_EGDmixte')

plot.SetParam(fontFamily = 'serif', fontSize = 18, height = 35, width = 30, dpi = 400, version = 'EN', eps = False, s = 100)
plot.IterationPlot(files)
