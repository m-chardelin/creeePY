import os
import matplotlib.pyplot as plt
from datetime import datetime


class Output():
    def __init__(self):
        
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def Describe(self, title, **kwargs):
        
        name = f'EXP_{title}'
        
        file = open(f'{title}.txt', 'w')
        
        file.write(f'{title}, {self.date} \n \n')
        
        
        for e in kwargs:
            
            if e == 'fixed':
                fixed = kwargs[e]
                file.write(f'\nFIXED PARAMETERS   : \n              Min       Max       ds       Mode \n')        
                for e in fixed.attribute:
                    gen = f'gen_{e}'
                    cha = f'cha_{e}'
                    if hasattr(fixed, gen):
                        file.write(getattr(fixed, gen))
                    if hasattr(fixed, cha):
                        file.write(getattr(fixed, cha))
                
            if e == 'stochastic':
                stochastic = kwargs[e]
                file.write(f'\nSTOCHASTIC PARAMETERS   : \n              Min       Max       Std       distribution[NbStep, NbDraw] \n')       
                for e in stochastic.attribute:
                    gen = f'gen_{e}'
                    cha = f'cha_{e}'
                    comp = f'comp_{e}'
                    if hasattr(stochastic, gen):
                        file.write(getattr(stochastic, gen))
                    if hasattr(stochastic, cha):
                        file.write(getattr(stochastic, cha))
                    if hasattr(stochastic, comp):
                        file.write(getattr(stochastic, comp)) 
                    
            if e == 'creep':
                creep = kwargs[e]
                file.write(f'\n \nCREEP LAW   : \n')
                config = getattr(creep, 'configurations')
                for element in config:
                    file.write(f'{element} \n \n ')
                    
    def SaveAttributes(self, obj, attribute = 'all'):
                
        if attribute == 'all':
            attribute = getattr(obj, 'attribute')  
                 
        for element in attribute:
            df = getattr(obj, element)            
            df.to_csv(f'{element}.txt', sep = ';')
        

    
       
        
        
        
