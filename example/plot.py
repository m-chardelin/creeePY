from path import *
from creeePY import Files, Statistics, Display, Plot, Tex
import os

# Directories

files = Files.Files(analysis, 'ZAB')

files.SetFolders(data = 'data', graphs = 'graphs', param = 'param', stats = 'stats', tex = 'tex', config = 'config', ctf = 'ctf', auto = True)

files.SetCats(files.data, '.txt')

# Display


files.SetFiles(inp = files.stats, out = files.graphs)

plot = Plot.Plot(files)
       
plot.SetParam(fontFamily = 'serif', fontSize = 18, height = 10, width = 15, dpi = 400, version = 'EN', eps = False, s = 100)

plot.GetParam()
        
#plot.PlotTernary(files, 'Ol', 'Opx', 'Al', 'ternaryFinal', 'massif', 'lithologyDef', 'facies_EGDmixte')
#plot.PlotTernary(files, 'Cpx', 'PlSp', 'Amph', 'ternaryFinal', 'massif', 'lithologyDef', 'facies_EGDmixte', labels = False)

plot.PlotTernary(files, 'Ol', 'Opx', 'Al', 'ternaryFinal', 'massif', 'lithologyDef', 'massif', 'massif', c = 'Ol%sscatArea', cmap = 'facies_EGDmixte', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte')
plot.PlotTernary(files, 'Cpx', 'PlSp', 'Amph', 'ternaryFinal', 'massif', 'lithologyDef', 'massif', 'massif', c = 'Ol%sscatArea', cmap = 'facies_EGDmixte', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte', labels = False)


plot.SimplePlot(files, 'neoEGDmixte_pondGOS', 'porphEGDmixte_pondGOS', 'combSort', 'massif', 'lithologyDef', 'massif', 'massif', ';', sortType = 'inner', sort = 'sscat', values = 'Olivine', c = 'Ol%sscatArea', cmap = 'facies_EGDmixte', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte')
plot.SimplePlot(files, 'neoEGDmixte_pondaspectRatio', 'porphEGDmixte_pondaspectRatio', 'combSort', 'massif', 'lithologyDef', 'massif', 'massif', ';', sortType = 'inner', sort = 'sscat', values = 'Orthopyroxene', c = 'Ol%sscatArea', cmap = 'facies_EGDmixte', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte')
plot.SimplePlot(files, 'neoEGDmixte_pondGOS', 'porphEGDmixte_pondGOS', 'combSort', 'massif', 'lithologyDef', 'massif', 'massif', ';', sortType = 'inner', sort = 'sscat', values = 'Clinopyroxene', c = 'Ol%sscatArea', cmap = 'facies_EGDmixte', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte')

plot.SimplePlot(files, 'J', 'BA', 'index', 'sscat', 'subcat', 'sscat', 'sscat', ';', xlim = [0, 15], ylim = [0, 1], sortType = 'inner', sort = 'subcat', values = 'all')

plot.SimplePlot(files, 'J', 'BA', 'index', 'sscat', 'sscat', 'sscat', 'sscat', ';', xlim = [0, 15], ylim = [0, 1], sortType = 'inner', sort = 'sscat', values = 'Orthopyroxene', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte')
plot.SimplePlot(files, 'BA', 'J', 'indexSamples', 'sscat', 'subcat', 'massif', 'massif', ';', xlim = [0, 1], ylim = [0, 6], sortType = 'inner', sort = 'sscat', values = 'Olivine', c = 'Ol%sscatArea', cmap = 'facies_EGDmixte', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte')


plot.SimplePlot(files, 'OlivineporphEGDmixte_pondSF', 'OrthopyroxeneporphEGDmixte_pondSF', 'CombAll', 'massif', 'lithologyDef', 'massif', 'massif', ';', sortType = None, xlim = [1.4, 4], ylim = [1.4, 4], c = 'Ol%sscatArea', cmap = 'facies_EGDmixte', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte')
plot.SimplePlot(files, 'OlivineporphEGDmixte_pondGOS', 'OrthopyroxeneporphEGDmixte_pondGOS', 'CombAll', 'massif', 'lithologyDef', 'massif', 'massif', ';', sortType = None, xlim = [1, 8], ylim = [1, 8], c = 'Ol%sscatArea', cmap = 'facies_EGDmixte', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte')
plot.SimplePlot(files, 'OlivineporphEGDmixte_pondaspectRatio', 'OrthopyroxeneporphEGDmixte_pondaspectRatio', 'CombAll', 'massif', 'lithologyDef', 'massif', 'massif', ';', sortType = None, xlim = [1.5, 3.3], ylim = [1.5, 3.3], c = 'Ol%sscatArea', cmap = 'facies_EGDmixte', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte')
plot.SimplePlot(files, 'OlivineporphEGDmixte_pondEGD', 'OrthopyroxeneporphEGDmixte_pondEGD', 'CombAll', 'massif', 'lithologyDef', 'massif', 'massif', ';', sortType = None, xlim = [0, 2500], ylim = [0, 2500],  c = 'Ol%sscatArea', cmap = 'facies_EGDmixte', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte')

plot.SimplePlot(files, 'BA', 'J', 'indexSamples', 'massif', 'lithologyDef', 'massif', 'massif', ';', xlim = [0, 1], ylim = [0, 15], c = 'Ol%sscatArea', cmap = 'facies_EGDmixte', sortType = 'inner', sort = 'sscat_subcat', values = 'Olivine_all', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte')
    

plot.SimplePlot(files, 'OlivineneoEGDmixte_pondEGD', 'Ol%sscatArea', 'CombAll', 'massif', 'lithologyDef', 'massif', 'massif', ';', sortType = None, c = 'Ol%sscatArea', cmap = 'facies_EGDmixte', vmin = 'facies_EGDmixte', vmax = 'facies_EGDmixte')

plot.SetParam(fontFamily = 'serif', fontSize = 18, height = 35, width = 30, dpi = 400, version = 'EN', eps = False, s = 100)
#plot.IterationPlot(files)
