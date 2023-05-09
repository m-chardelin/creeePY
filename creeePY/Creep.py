import numpy as np
import pandas as pd
import os

class Creep():
    def __init__(self, **kwargs):
        
        self.__dict__.update(kwargs)
        
        self.attribute = []                                                   # attribute created
        self.configurations = []
        
        self.R = 8.3145
        self.e = 2.718281828459045
        
        
    def SetCalibration(self, calib, process, condition, clear = []):       # read the wanted dataframe and the line associated to the right deformation process and the right condition  
        df = pd.read_csv(f'/home/Marialine/RhEoVOLUTION/CODES/SCRIPTS/creeepy/creeepy/calibration/{calib}.txt', sep = ';')
        df = df[df['process'] == process]
        df = df[df['condition'] == condition] 
        df.reset_index(drop = True, inplace = True)
        
        self.name = calib
        self.calibration = df
        self.process = process
        self.condition = condition
        self.listParam = self.calibration.columns
        
        if len(clear) >= 1:                                                     # clean parameters between two loadings
            for e in range(2, len(self.listParam)):
                attr = self.listParam[e]
                if hasattr(self, attr) and attr not in clear:
                    delattr(self, attr)
        
        
    def SetParams(self, fixed, stochastic):
        self.txt = f'Paramters used in the law {self.name}, for {self.condition} {self.process} : \n'
        
        for e in self.listParam:
            if 'process' not in e and 'condition' not in e:                          
                if hasattr(fixed, e):
                    setattr(self, e, getattr(fixed, e))
                    self.txt = self.txt + f'{e} = see tables      fixed \n'           

                elif hasattr(stochastic, e):
                    setattr(self, e, getattr(stochastic, e))
                    self.txt = self.txt + f'{e} = see tables      stochastic \n'
            
                elif hasattr(self, e):
                    self.txt = self.txt + f'{e} = {getattr(self, e)}      set manually \n'
            
                else:
                    var = float(self.calibration.loc[0, e])
                    setattr(self, e, var)
                    self.txt = self.txt + f'{e} = {getattr(self, e)}      from calibration \n'
        
        self.varSto = stochastic.variables
        self.varFix = fixed.variables
        
        self.txt = self.txt + f'\nFixed array : {", ".join(self.varFix)}'
        self.txt = self.txt + f'\nStochastic array : {", ".join(self.varSto)}\n\n'
        
        self.configurations.append(self.txt)
        
    
    def SetVariables(self, variable, values):        
        setattr(self, variable, values)
        
        
    def StochasticCreep(self, tab, variable, func, prop = 0):            
   
        self.stoS = pd.DataFrame()
                
        for col in range(0, tab.shape[1]):
            
            var = tab.iloc[:,col]
            self.SetVariables(variable, var)
            func()
            self.stoS[tab.columns[col]] = self.S
                       
        columns = self.stoS.columns
        self.stoS['meanSeed'] = self.stoS.mean(axis = 1) 
        
        if prop >= 0:
            for e in range(1, prop+1):
                col = b = [x for x in columns if x.startswith(f'{e}_')]              
                self.stoS[f'meanSubSeed{e}'] = self.stoS.loc[:, col].mean(axis = 1)
            
        
    def RegularCreep(self, func):    
        if hasattr(self, 'rS') == False:
            self.rS = pd.DataFrame()         
            self.rS['s'] = self.s            
        func()        
        self.rS[f'r_{self.name}'] = self.S
        
        
    def SetPercentage(self, df, col1, total):        
        df[f'{total}_percent'] = df[col1]/df[total]
     
        
    def Esperance(self, tab, col):
        
        for j in range(1, len(tab.index)):
            tab.loc[j, f'{col}_esp'] = sum(tab.loc[0:j, col])/(j)
        return tab
        
    def TotalCreep(self, a, b, prop = 0):  
        
        df = self.rS.copy()
        df[f'sto_{self.name}'] = self.stoS['meanSeed']
        
        if prop >= 0:
            for e in range(1, prop+1):          
                df[f'sto_{self.name}_SubSeed{e}'] = self.stoS[f'meanSubSeed{e}']
            
        
        columns = list(df.columns)
        
        for i in range(0, len(a)):
            ind1 = columns.index(a[i])
            ind2 = columns.index(b[i])            
            df[f't{ind1}-{ind2}'] = df.iloc[:,ind1] + df.iloc[:,ind2]
            
            self.SetPercentage(df, columns[ind1], f't{ind1}-{ind2}')
            df = self.Esperance(df, f't{ind1}-{ind2}') 
        
        var = '-'.join(self.varSto)
        name = f'S_{var}_{self.T}'
        self.attribute.append(name)
        setattr(self, name, df)
                  
                    
                    
                    
#####################################################################################################
                    
    def Hirth2003(self, kwargs['Min']):
        '''
        Creep law associated to the review of G. Hirth and D. Kohlstedt, 2003. 
        
        Arguments : 
            s      stress                    [MPa]
            var    variable value (d)        [μm]
            T      temperature               [Kelvin]
                   
        Output : 
            S      strain rate               [s-1]
        '''
        
        
        self.S = self.A * self.s**self.n * (1/self.d)**self.p  * self.fH2O**self.r * np.exp(self.alpha*self.phi) * np.exp( -self.Q /(self.R * self.T)) 
        
        return self.S
    
    
    def Gouriet2018(self): 
        '''
        Creep law associated to disocation creep. 
        
        Arguments : 
            s      stress                    [MPa]
            var    variable value (d)        [μm]
            T      temperature               [Kelvin]
                   
        Output : 
            S      strain rate               [s-1]
        '''       
        
        self.S =  self.A * ( self.s*1e6/self.mu )**self.n * np.exp((-self.Q/(self.R*self.T)) * ( 1 - ( self.s*1e6/self.s_P )**self.p )**self.q)   
    
            
                
                
                
                
                
                
        
