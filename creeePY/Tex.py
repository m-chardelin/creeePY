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

        self.area = pd.read_csv(f'{files.stats}/resume.csv', sep = ';')

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


    def addTEXT(self, files, name, cat, subcat, task, rep = '', re = '', begin = 1):

        ts = self.area[(self.area['cat'] == cat) & (self.area['subcat'] == 'all')]
        ts = ts.sort_values(by = ['%catArea'], ascending=False)
        ind = np.arange(0, len(ts['sscat']), 1)
        ts.index = ind
        print(ts)
  
        end = ts.shape[0]
        
        add = self.GetTxt(files, name)
        
        for i in np.arange(begin, len(ts['sscat']), 1):
            mineral = ts.loc[i, 'sscat']
            print(f'{files.figures}/{cat}_{mineral}_{subcat}_{task}.eps')
            mine = f'MINERAL{i}'
            if os.path.exists(f'{files.figures}/{cat}_{mineral}_{subcat}_{task}.eps'):
                add = add.replace(mine, mineral)
                
        for ii in np.arange(begin, len(files.sscat), 1):
            print('blank')
            mine = f'MINERAL{ii}'
            if mine in add:
                for r, ree in zip(rep, re):
                    print(r, ree)
                    ee = r.replace('mine', mine)
                    add = add.replace(ee, f'blank_{ree}.eps')
        
        print(add)
        add = add.replace('SUBCAT', subcat)
        add = add.replace('CAT', cat)
        text = add
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
            try:
                print(c)
                text = self.GetTxt(files, 'lameType')
                
                PARAM, rotAngle = self.GetParam(files, c, 'PhasesMap')
                
                text = text.replace('CAT', c)
                text = text.replace('PARAM', PARAM)
                text = text.replace('FIGURESDIR', files.figures)
                text = text.replace('rotAngle', str(rotAngle))
                
                cpo = self.addTEXT(files, 'addCPO', c, 'all', 'CPO', rep = ['CAT_mine_SUBCAT_CPO.eps', 'CAT_mine_SUBCAT_IPF.eps'], re = ['CPO', 'IPF'])
                
                hist = self.addTEXT(files, 'addHIST', c, 'subcat', 'histEGDweightareaEGDmixte', rep = ['CAT_mine_SUBCAT_histEGDweightareaEGDmixte.eps'], re = ['histEGDweightareaEGDmixte'])
                
                text = text.replace('CPO', cpo)
                text = text.replace('HIST', hist)

                self.text = text
                self.Save(files, 'ts')
                
                os.system(f'cd {files.tex}')
                os.chdir(f'{files.tex}')
                os.system('pwd')
                os.system(f'latex -jobname={c} ts.tex')
                #os.system(f'dvipdf {c}.dvi')
            except:
                pass
            

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




    #def addTEXT(self, files, name, cat, subcat, task, iter, rep = '', re = '', begin = 1):

        #ts = self.area[(self.area['cat'] == cat) & (self.area['subcat'] == 'all')]
        #ts = ts.sort_values(by = ['%catArea'], ascending=False)
        #ts.index = np.arange(0, len(ts['sscat']), 1)
        #print(ts)
        
        #text = ''
        #end = ts.shape[0]
        
        #while begin < end:
        #    add = self.GetTxt(files, name)
        #    mineral = ts.loc[begin, 'sscat']
        #    print(f'{files.figures}/{cat}_{mineral}_{subcat}_{task}.eps')
            
        #    if os.path.exists(f'{files.figures}/{cat}_{mineral}_{subcat}_{task}.eps'):
        #        add = add.replace('MINERAL1', mineral)
        #        print(add)
        #    else:
        #        for r, re in zip(rep, res):
        #            add = add.replace(r, f'blank_{re}.eps')
        #            print(f'blank_{re}.eps')

        #    if begin + 1 in self.ts.index:
        #        add = add.replace(f'MINERAL2', self.ts.loc[begin + 1, 'sscat'])
        #    else:
        #        for r, re in zip(rep, res):
        #            add = add.replace(r, f'blank_{re}.eps')
        #            print(f'blank_{re}')
                    
            #add = add.replace('CAT', cat)
            #add = add.replace('SUBCAT', subcat)
            #text = text + add
            #begin += iter
        #return text
