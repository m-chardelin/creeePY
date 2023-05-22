import os
import sys
import pandas as pd
import numpy as np
import PIL
from PIL import Image
from PyPDF2 import PdfMerger
    
class Tex():
    def __init__(self, files, **kwargs):
                        
        self.__dict__.update(kwargs)

        self.area = pd.read_csv(f'{files.stats}/resume.csv', sep = '&')

        #### Functions
    
    def Load(self, table, sort = False):
        self.df = pd.read_csv(table, sep = ',')
        
        if sort == True:
            self.subcat = set(self.df[self.sort])


    def SetParam(self, **kwargs):
        self.__dict__.update(kwargs)

    
    def GetTxt(self, files, file):
        with open(f'{files.input}/{file}.tex', 'r') as file:
            self.txt = file.read()
        return self.txt

    
    def Save(self, files, file):
        with open(f'{files.output}/{file}.tex', 'w') as file:
            file.write(self.text)
            
            
    def Convert(files, inputFormat, outputFormat):
        os.system(f'for file in *.{inputFormat}; do convert $file "`basename $file .{inputFormat}`.{outputFormat}"; done')
            
    def ConvertDVI(files):
        os.system('for file in *.dvi; do dvipdf $file ; done')
    
    def Iteration(self, files, func, iterMineral = False):
        for c in files.cat:
            if iterMineral == False:
                func(files, c)

            if iterMineral == True:
                for ssc in files.sscat:
                    if os.path.exists(f'{files.input}/{c}_{ssc}_{self.task}.csv'):
                        func(files, c, ssc)


    def addTEXT(self, files, name, cat, subcat, iter, rep = '', begin = 1):
    
        if hasattr(self, 'ts') == False:
            self.ts = self.area[self.area['cat'] == cat]
            self.ts = self.ts[self.ts['subcat'] == subcat]
            self.ts = self.ts.sort_values(by = ['%catArea'], ascending=False)
            self.ts.index = np.arange(0, len(self.ts['sscat']), 1)
        
        text = ''
        if iter == 1 :
            end = len(self.ts['sscat'])
        else:
            end = len(self.ts['sscat'])
            
        while begin < end:
            add = self.GetTxt(files, name)
            add = add.replace('SUBCAT', subcat)
            add = add.replace('CAT', cat)
            add = add.replace(f'MINERAL1', self.ts.loc[begin, 'sscat'])
            if begin + 1 in self.ts.index:
                add = add.replace(f'MINERAL2', self.ts.loc[begin + 1, 'sscat'])
            else:
                add = add.replace('rep', 'blank_hist.eps')
            text = text + add
            begin += iter
        return text
        
        
    def GetParam(self, files, cat, name):
        img = PIL.Image.open(f'{files.figures}/{cat}_{name}.eps')
        width, height = img.size
            
        if width / height > 1:
            PARAM = 'width = \\linewidth'
            rotAngle = 0
        elif width / height < 1:
            PARAM = 'width = \\linewidth, angle = 90'
            rotAngle = 90
        elif width / height == 1:
            PARAM = 'height = 0.45\\paperheight'
            rotAngle = 0
            
        return PARAM, rotAngle


    def Area(self, files, sort):
        
        for c in files.cat:
        
            try:
                print(c)
                text = self.GetTxt(files, 'areaType')
            
                PARAM, rotAngle = self.GetParam(files, c, f'Sort{sort}NoboundariesMap')
                
                text = text.replace('CAT', c)
                text = text.replace('PARAM', PARAM)
                text = text.replace('FIGURESDIR', files.figures)
                text = text.replace('rotAngle', str(rotAngle))
                
                self.text = text
                self.Save(files, 'ts')
                
                os.system(f'cd {files.tex}')
                os.chdir(f'{files.tex}')
                os.system('pwd')
                os.system(f'latex -jobname={c}_{sort} ts.tex')
                #os.system(f'dvipdf {c}_{sort}.dvi')
            except:
                pass
    

    def ThinSection(self, files):
        
        for c in files.cat:
            text = self.GetTxt(files, 'lameType')
            
            PARAM, rotAngle = self.GetParam(files, c, 'PhasesMap')
            
            text = text.replace('CAT', c)
            text = text.replace('PARAM', PARAM)
            text = text.replace('FIGURESDIR', files.figures)
            text = text.replace('rotAngle', str(rotAngle))
            
            cpo = self.addTEXT(files, 'addCPO', c, 'all', 1)
            hist = self.addTEXT(files, 'addHIST', c, 'all', 2, 'CAT_MINERAL2_subcat_histEGDweightareaEGDmixte.eps')
            
            text = text.replace('CPO', cpo)
            text = text.replace('HIST', hist)

            self.text = text
            self.Save(files, 'ts')
            
            os.system(f'cd {files.tex}')
            os.chdir(f'{files.tex}')
            os.system('pwd')
            os.system(f'latex -jobname={c} ts.tex')
            os.system(f'dvipdf {c}.dvi')
            

    def Merge(self, files):

        pdfs = [f'{c}.pdf' for c in files.cat]
        
        merger = PdfMerger()

        for pdf in pdfs:
            merger.append(pdf)
        merger.write("lames.pdf")
        merger.close()
        
        merger = PdfMerger()
        for c in files.cat:
            #os.system(f'cd {files.output}')
            #os.system(f'cd /Users/marialinechardelin/Zabargad/figures')
            #os.system(f'pdflatex {files.output}/{c}.tex')
            #os.system(f'dvipdf {files.output}/{file}.dvi')
            merger.append(f'{c}.pdf')
        self.merger.write("areaZabargad.pdf")
        merger.close()
