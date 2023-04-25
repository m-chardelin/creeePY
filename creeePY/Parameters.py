# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import copy
from itertools import product, combinations, chain


class Param():
    def __init__(self, config, files):
        
        self.listParam = [x for x in dir(config) if "__" not in x]
        
            
        # Duration of the experiences and number of steps
        
        self.varNTIME = config.NTIME
        self.varTFIN = config.TFIN
        
        
        # Mesh used in the experiences, actualisation of the depth value 
        
        self.varMESH = f'../../config/mesh/{config.mesh}'
        
        with open(f'{files.mesh}/{config.mesh}') as mesh:
            lines = mesh.readlines()
            ind = [index for index in range(len(lines)) if lines[index] == '// PROFONDEUR = 2e3\n']
            self.varPROF = '-'+lines[ind[0]].split()[-1]
            
            
        # Reading ifile.sto if required
    
        if config.version == 'stochastic':
            self.isto = 0                                                                                    # TO DO : READ THE PDF PARAMETERS AND WRITE THE IFILE.STO
        else:
            print("Classic version of ADELI used, ifile.Sto not read")
        
        self.version = config.version
        
        # Param for visco-elastic behaviour
        
        if config.A[0] == 'pm':
            self.A = np.arange(config.A[1] - config.A[2], config.A[1] + config.A[2] + config.A[2], config.A[2])
        if config.A[0] == 'range':
            self.A = np.arange(config.A[1], config.A[2], config.A[3])
        if config.A[0] == "value":
            self.A = config.A[1]        
        
        if config.Q[0] == "pm":
            self.Q = np.arange(config.Q[1] - config.Q[2], config.Q[1] + config.Q[2] + config.Q[2], config.Q[2]) 
        if config.Q[0] == "range": 
            self.Q = np.arange(config.Q[1], config.Q[2], config.Q[3]) 
        if config.Q[0] == "value": 
            self.Q = config.Q[1] 

        if config.mu[0] == "pm": 
            self.mu = np.arange(config.mu[1] - config.mu[2], config.mu[1] + config.mu[2] + config.mu[2], config.mu[2]) 
        if config.mu[0] == "range": 
            self.mu = np.arange(config.mu[1], config.mu[2], config.mu[3]) 
        if config.mu[0] == "value": 
            self.mu = [config.mu[1]]

        if config.n[0] == "pm": 
            self.n = np.arange(config.n[1] - config.n[2], config.n[1] + config.n[2] + config.n[2], config.n[2]) 
        if config.n[0] == "range": 
            self.n = np.arange(config.n[1], config.n[2], config.n[3]) 
        if config.n[0] == "value": 
            self.n = [config.n[1]]

        if config.p[0] == "pm": 
            self.p = np.arange(config.p[1] - config.p[2], config.p[1] + config.p[2] + config.p[2], config.p[2]) 
        if config.p[0] == "range": 
            self.p = np.arange(config.p[1], config.p[2], config.p[3]) 
        if config.p[0] == "value": 
            self.p = config.p[1] 

        if config.q[0] == "pm": 
            self.q = np.arange(config.q[1] - config.q[2], config.q[1] + config.q[2] + config.q[2], config.q[2]) 
        if config.q[0] == "range": 
            self.q = np.arange(config.q[1], config.q[2], config.q[3]) 
        if config.q[0] == "value": 
            self.q = config.q[1] 

        if config.s_dev[0] == "pm": 
            self.s_dev = np.arange(config.s_dev[1] - config.s_dev[2], config.s_dev[1] + config.s_dev[2] + config.s_dev[2], config.s_dev[2]) 
        if config.s_dev[0] == "range": 
            self.s_dev = np.arange(config.s_dev[1], config.s_dev[2], config.s_dev[3]) 
        if config.s_dev[0] == "value": 
            self.s_dev = config.s_dev[1] 

        if config.s_peierls_fix[0] == "pm": 
            self.s_peierls_fix = np.arange(config.s_peierls_fix[1] - config.s_peierls_fix[2], config.s_peierls_fix[1] + config.s_peierls_fix[2] + config.s_peierls_fix[2], config.s_peierls_fix[2]) 
        if config.s_peierls_fix[0] == "range": 
            self.s_peierls_fix = np.arange(config.s_peierls_fix[1], config.s_peierls_fix[2], config.s_peierls_fix[3]) 
        if config.s_peierls_fix[0] == "value": 
            self.s_peierls_fix = config.s_peierls_fix[1] 
            
        if config.T_fix[0] == "pm": 
            self.T_fix = np.arange(config.T_fix[1] - config.T_fix[2], config.T_fix[1] + config.T_fix[2] + config.T_fix[2], config.T_fix[2]) 
        if config.T_fix[0] == "range": 
            self.T_fix = np.arange(config.T_fix[1], config.T_fix[2], config.T_fix[3]) 
        if config.T_fix[0] == "value": 
            self.T_fix = config.T_fix[1] 
            
        if config.T_cut[0] == "pm": 
            self.T_cut = np.arange(config.T_cut[1] - config.T_cut[2], config.T_cut[1] + config.T_cut[2] + config.T_cut[2], config.T_cut[2]) 
        if config.T_cut[0] == "range": 
            self.T_cut = np.arange(config.T_cut[1], config.T_cut[2], config.T_cut[3]) 
        if config.T_cut[0] == "value": 
            self.T_cut = [config.T_cut[1]]
            
        
        # Param for elastic behaviour
        
        self.Young = [2e11]
        self.Poisson = [0.25]
        self.rho0 = [3.0e3]
        
                
        # Materials and behaviour definition
        
        self.varMAT = config.MAT
        self.varLAW = config.LAW
        
        with open('/Users/marialinechardelin/scripts/creeepy/creeepy/model/iSource') as file:
            lines = file.readlines()
        
        if len(config.MAT) == 1:
            self.varMAT = config.MAT[0]
            self.varLAW = config.LAW[0]
            with open('/Users/marialinechardelin/scripts/creeepy/creeepy/model/iType', 'w') as file : file.write(''.join(lines))
        else:
            ind = [index for index in range(len(lines)) if lines[index] == '   varMAT    varLAW   2.0\n']
            a = ''
            self.add = ''.join([a + lines[i] for i in range(ind[0], ind[0]+7)])
            with open('/Users/marialinechardelin/scripts/creeepy/creeepy/model/iSource') as file: self.txt = file.read()
            self.txt = self.txt.replace('varMAT', self.varMAT[0])
            self.txt = self.txt.replace('varLAW', self.varLAW[0])
            for i in range(1, len(self.varMAT)):
                self.txt = self.txt.replace('VITESSES IMPOSEES\n', self.add)
                self.txt = self.txt.replace('varMAT', self.varMAT[i])
                self.txt = self.txt.replace('varLAW', self.varLAW[i])
            with open('/Users/marialinechardelin/scripts/creeepy/creeepy/model/iType', 'w') as file : file.write(self.txt)
            
            
        # Limit speed conditions 
        
        self.stress = pd.read_csv('/Users/marialinechardelin/scripts/creeepy/creeepy/model/vitesses.csv', sep = ';')
        if config.Stress == True:
            self.varNVFIX = self.stress.shape[0]
            with open('/Users/marialinechardelin/scripts/creeepy/creeepy/model/vitesses.csv') as file: self.tabVITESSES = file.read().replace(';', '    ')
        else:
            self.varNVFIX = 0
            self.tabVITESSES = '    '.join(self.stress.columns)
            
        
        # Lithostatic stress conditions (if required, will test a configuration without stress)
        
        self.pressure = pd.read_csv(f'{files.config}/contraintesLitho.csv', sep = ';')
        if config.Plitho == True:
            self.varNPRES = self.pressure.shape[0]
            self.varNGRAV = 1
            self.varISOSTRS = 1
            with open(f'{files.config}/contraintesLitho.csv') as file: self.tabCONTRAINTESLITHO = file.read().replace(';', '    ')
        else:
            self.varNGRAV = 0
            self.varNPRES = 0
            self.varISOSTRS = 0
            self.tabCONTRAINTESLITHO = '    '.join(self.pressure.columns)
            
            
        # Param for fixed temperature or gradient        
        
        self.Tgrad = pd.read_csv(f'{files.config}/temperature.csv', sep = ',')
        if config.Tgrad == True: 
            self.T_fix = [0, 0]
            self.varTEMP = self.Tgrad.shape[0]
            with open(f'{files.config}/temperature.csv') as file: self.tabTEMP = file.read().replace(',', '    ')
        else:
            self.varTEMP = 1
            self.tabTEMP = '    '.join(self.Tgrad) + '\n' + 'varPROF     varT_fix     2'

        
        ################################################################################################################################################

        self.table = list(product(self.A, self.Q, self.mu, self.n, self.p, self.q, self.s_dev, self.s_peierls_fix, self.T_cut, self.Young, self.Poisson, self.rho0, self.T_fix))
        self.iter = pd.DataFrame(self.table, columns = ['A', 'Q', 'mu', 'n', 'p', 'q', 's_dev', 's_Peierls_fix', 'T_cut', 'Young', 'Poisson', 'Rho0', 'T_fix'])
        self.iter = self.iter.drop_duplicates()
        self.iter.index = range(0, self.iter.shape[0])
        self.iter.to_csv(f'{files.config}/iterations.csv', sep = ";")
