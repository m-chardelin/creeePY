from creeepy import Files, Statistics, Display, Plot, Tex
import os

# Directories
folder = '/Users/marialinechardelin/save/2021-2023/current/Zabargad/3_4_deformation/4_analysis'

files = Files.Files(folder, 'ZAB')

files.SetFolders(raw = 'raw', data = 'data', fig = 'figures', param = 'param', stats = 'stats', tex = 'tex', config = 'config', ctf = 'ctf', results = 'results', auto = True)
files.SetSubFolders(files.tex, ['figures', 'text'])

files.SetCats(files.data, '.txt')

# Display

files.SetFiles(inp = files.stats, out = files.figures)
plot = Plot.Plot(files)
        
files.cat = ['85ZA1c', '85ZA7bc']
        
plot.GetParam()

plot
