import numpy as np
import pandas as pd

class Data():
    def __init__(self, filename):
    
        file = open(filename, 'r')                                                           # open config file
        
        self.fixedDict = {}                                                                 # create dictionaries for both fixed and stochastic parameters
        self.stoDict = {}
        
        self.variables = []
    
        for line in file:
            if not line.startswith('###') and 'sto' not in line and 'nb' not in line:      # lines wich begin by 'sto' or 'nb' are affected to the stochastic dictionariy
                k, v = line.strip().split('=')
                try:
                    self.fixedDict[k.strip()] = float(v.strip())                             # convert numbers to float for further calculations...
                except ValueError:
                    self.fixedDict[k.strip()] = v.strip()

            if line.startswith('sto') or 'nb' in line:
                k, v = line.strip().split('=')
                try:
                    self.stoDict[k.strip()] = float(v.strip())
                except ValueError:
                    self.stoDict[k.strip()] = v.strip()
        file.close()
        
    def SetVariable(self, var, newVar, clear = False):     
        if clear == True:
            self.variables = []
        # dupplicate an attribute under another name 
        setattr(self, var, getattr(self, newVar))
        self.variables.append(f'{var}_{newVar}')
        
        
    
    
class Fixed(Data):
    def __init__(self, filename = 'config'):
        super().__init__(filename)
        
        self.attribute = []                                                                 # keep a trace of the name of the variables generated for output
        
        for k, v in self.fixedDict.items():                                                  # update the class attribute with dictionary keys
            setattr(self, k, v)

    def GenerateVariable(self, mode = 'uniform', **kwargs):                                 # generate variables by three different manners ('uniform' or 'linearSpace' better, to make the number of stress values correspond to the number of points wanted)
        
        if len(kwargs) == 0:                                                                # take the attributes of the class
            Min = self.Min
            Max = self.Max
            ds = self.ds
            name = self.name
            
        else:                                                                               # take the kwargs (possibility to create other variables manually if all the wanted kwargs are declared)
            Min = kwargs['Min']
            Max = kwargs['Max']
            ds = kwargs['ds']
            name = kwargs['name']
    
        if mode == 'range':
            var = np.arange(Min, Max, ds)
            
        if mode == 'linearSpace':
            var = np.linspace(Min, Max, num = ds)
    
        if mode == 'uniform':
            ds = int(ds)
            var = Min + np.random.uniform(0, 1, ds) * (Max - Min) 
            var = np.sort(var)
            
        self.mode = mode
        self.attribute.append(name)

        setattr(self, name, var)

        txt = f'{name} :    {Min}  {Max}  {ds}  {mode} \n'                                
        
        tname = f'gen_{name}'                                                        
        setattr(self, tname, txt)       

        print(f'Attribute "{name}" set.')
    
    
class Stochastic(Data):
    def __init__(self, filename = 'config'):
        super().__init__(filename)
        
        for k, v in self.stoDict.items():
            setattr(self, k, v)
            
        self.attribute = []
        
    def GenerateSeed(self, **kwargs):                                           
    
        if len(kwargs) == 0:
            Min = self.stoMin
            Max = self.stoMax
            Std = self.stoStd
            NbStep = int(self.nbStep)    
            NbDraw = int(self.nbDraw)
            name = self.stoName
            
        else:
            Min = kwargs['Min']
            Max = kwargs['Max']
            Std = kwargs['Std']
            NbStep = int(kwargs['nbStep'])
            NbDraw = int(kwargs['nbDraw'])
            name = kwargs['name']

            
        self.tab = pd.DataFrame()
        
        strainStoch = 0        
        for i in range(0, NbStep):    
            for j in range(1, NbDraw+1):        
                varStoch = 0
                misvalues = 0
                while (varStoch >= Max) or (varStoch <= Min):         
                    varStoch = Min + np.random.standard_normal() * Std
                    
                #if NbStep < 1000 and NbDraw < 1000 :
                #    self.values[i, j] = varStoch
                #else:
                #    misvalue = (misvalues + varStoch /j)
                
                
                misfit = func(stress, varStoch) - strainStoch
                strainStoch = strainStoch + misfit / j
        
        
        self.tab[i, f'{calib}_{name}'] = strainStoch
        
        self.attribute.append(name)
                              
        setattr(self, name, self.tab)        

        txt = f'{name} :    {Min}  {Max}  {Std}  normal[{NbStep}, {NbDraw}] \n'
        
        tname = f'gen_{name}'
        setattr(self, tname, txt)

        print(f'Stochastic seed "{name}" set')
        
        
    def GenerateCompositeSeed(self):                                                
        
        tab = pd.DataFrame()
        p = ''
        
        for e in range(1, int(self.stoDistrib) +1):                                
            
            prop = f'stoProp{e}'                                                       
            snbdraw = self.nbDraw * getattr(self, prop)                                        
            smin = str(f'stoMin{e}')                                                 
            smax = str(f'stoMax{e}')
            sstd = str(f'stoStd{e}')
            sname = str(f'stoName{e}')
            
            self.GenerateSeed(Min = getattr(self, smin),                             
                              Max = getattr(self, smax), 
                              Std = getattr(self, sstd), 
                              nbDraw = snbdraw, 
                              nbStep = self.nbStep,
                              name = getattr(self, sname))
            
            self.tab.columns = [f'{e}_{col}' for col in self.tab.columns]          
            tab = pd.concat([tab, self.tab], axis = 1)                              
            
            p = p + f'             {getattr(self, sname)}, {getattr(self, prop)}\n'  
            
            
        self.attribute.append(self.stoNameComp)                                        
        
        setattr(self, self.stoNameComp, tab) 
        
        txt = f'{self.stoNameComp} : \n' + p                                           
        
        tname = f'comp_{self.stoNameComp}'
        setattr(self, tname, txt)
                  
        print(f'   --->  added to the stochastic seed {self.stoNameComp} \n')

    def CharacteriseSeed(self,                                                       
                  calculation = ['min', 'max', 'std', 'mean', 'median', 'mad'], 
                  quantile = [0.2, 0.4, 0.6, 0.8],
                  option = 1, **kwargs):
    
        if len(kwargs) == 0:
            df = self.tab
            name = self.stoName
            
        else:
            df = kwargs['df']
            name = kwargs['name']
    
        for element in calculation:

            if element == 'min':
                df[element] = df.min(axis = option)

            if element == 'mean':
                df[element] = df.mean(axis = option)

            if element == 'max':
                df[element] = df.max(axis = option)

            if element == 'var':
                df[element] = df.var(axis = option)   

            if element == 'std':
                df[element] = df.std(axis = option)
        
            if element == 'median':
                df[element] = df.median(axis = option)
        
            if element == 'mad':
                df[element] = df.mad(axis = option)


        for q in quantile:
            df[f'q{q}'] = df.quantile(q, axis = option)
        
                    
        setattr(self, f'{name}', df) 
               
        txt = f'Characterised by : \n parameters {calculation}, quantiles {quantile} on {option}'
        tname = f'cha_{name}'
        setattr(self, tname, txt)                                                      

        print(f'Characterisation of stochastic seed "{name}" made')
