from path import *
from creeePY import Files, Statistics, Display, Tex
import os

# Directories
files = Files.Files(analysis, 'ZAB')

files.SetFolders(display = 'display', calculations = 'calculations', graphs = 'graphs', plot = 'plot', param = 'param', stats = 'stats', tex = 'tex', config = 'config', ctf = 'ctf', auto = True)

files.SetSubFolders(files.tex, ['figures', 'text'])

# Display

files.SetFiles(inp = files.tex, out = files.tex)
files.SetCats(files.display, '.csv')

## LaTeX

files.SetFiles(inp = files.text, out = files.tex)
tex = Tex.Tex(files)

#tex.Area(files, sort = 'EGDmixte')
tex.ThinSection(files)
