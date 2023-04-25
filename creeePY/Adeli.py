# -*- coding: utf-8 -*-

import os

class Iterations():
    def __init__(self, nameExp, param, files):
        
        self.iType = 'model/iType'  # Load ifile type with good number of materials and laws
        self.jType = 'model/jType'  # Load jfile
        self.adeliMessage = 'model/ADELI3d.MESSAGES' # Laod Adeli message
        self.script = 'model/scriptType'  # Load script
        
        with open(f'{files.preproc}varIType') as file:   # Load list of variables to change
            self.listVar = file.readlines()     
            self.listVar = [a.replace('\n', '') for a in self.listVar]
        
        for i in range(0, param.iter.shape[0]):
            print(i)
            os.makedirs(f'{files.runs}{nameExp}_{i}/', exist_ok=True)  
            
        with open(self.jType) as jType:  # Load jfile
            self.jTxt = jType.read()
            
        with open(self.adeliMessage) as adeliMessage: # Laod Adeli message
            self.aTxt = adeliMessage.read()
            
        with open(self.iType) as iType :  # Load ifile type with good number of materials and laws
            self.iTxt = iType.read() 
            
        with open(self.script) as sType:    # Load script
            sTxt = sType.read()
            sTxt = sTxt.replace('nameExp', files.nameExp)
            
            if param.version == 'classic':   # Change bin path in function of Adeli version
                sTxt = sTxt.replace('binAdeli', files.bin3p9)
            else:
                sTxt = sTxt.replace('binAdeli', files.bin3p9Sto)                              # TO DO : WRITE THE IFILE.STO
            
            self.sTxt = sTxt.replace('binVtk', files.binVtk)    # Change the bin path for vtk extraction from the pfile
            
            #for line in range(0, param.iter.shape[0]):
            for line in range(0, 15):
                txt = self.iTxt
                
                for var in self.listVar:    # Replace the variables with the values loaded from the config file
                    var2 = eval(f'param.{var}')        
                    var2 = str(var2)
                    txt = txt.replace(var, var2) 
                
                for var in param.iter.columns:   # Replace the rheological values for law 1 and 2 with values of the iterations
                    txt = txt.replace(f'var{var}', str(param.iter.loc[line, var]))
                
                with open(f'{files.runs}{nameExp}_{line}/i{files.nameExp}', 'w') as iFile:  # Write ifile
                    iFile.write(txt)
                    
                with open(f'{files.runs}{nameExp}_{line}/j{files.nameExp}', 'w') as jFile:  # write jfile
                    jFile.write(self.jTxt)
                    
                with open(f'{files.runs}{nameExp}_{line}/ADELI3d.MESSAGES', 'w') as aFile:  # Write Adeli message 
                    aFile.write(self.aTxt)
                    
                with open(f'{files.scripts}SCRIPT', 'w') as script:   # Write SCRIPT
                    script.write(self.sTxt)
                    
            if param.varNGRAV == 1 :    # If lithostatic pressure is applied to the model : write an extra configuration with no stress
                txt = self.iTxt
                txt = txt.replace('varNVFIX', '0')
                txt = txt.replace('tabVITESSES', '    '.join(param.stress.columns))
     
                for var in self.listVar:
                    var2 = eval(f'param.{var}')
                    var2 = str(var2)
                    txt = txt.replace(var, var2) 
                
                for var in param.iter.columns:
                    txt = txt.replace(f'var{var}', str(param.iter.loc[0, var]))
                
                os.makedirs(f'{files.runs}test_Plitho/', exist_ok=True)
                with open(f'{files.runs}test_Plitho/i{files.nameExp}', 'w') as iFile:
                    iFile.write(txt)
                    
                with open(f'{files.runs}test_Plitho/j{files.nameExp}', 'w') as jFile:
                    jFile.write(self.jTxt)
                    
                with open(f'{files.runs}test_Plitho/ADELI3d.MESSAGES', 'w') as aFile:
                    aFile.write(self.aTxt)

            
