from path import *
from creeePY import Files, Statistics, Display, Tex
import os


###  TRAITEMENT DES DONNEES EBSD, TRI DES RÉSULTATS ##########################

#### lancement de la macro en ligne de commande


# arborescence du dossier de traitement MTEX
filesTreatment = Files.Files(treatment, 'ZAB')
filesTreatment.SetFolders(data = 'data', dataClean = 'dataClean', output = 'output', auto = True)
filesTreatment.SetSubFolders(filesTreatment.output, ['total', 'lames', 'tasks'])

# nettoyage des fichiers avec le bon séparateur,
filesTreatment.CleanTxt([filesTreatment.total], [',', ';'], '&', extension = '.txt', exception = None)
filesTreatment.SetCats(filesTreatment.total, '.txt')
filesTreatment.CleanFiles([filesTreatment.lames, filesTreatment.tasks])

# copie des fichiers et classement en fonction des lames, puis en fonction des tâches effectuées
filesTreatment.CopyFiles(filesTreatment.total, [filesTreatment.lames, filesTreatment.tasks])
filesTreatment.SortFiles([filesTreatment.lames], filesTreatment.cat)
taskCat = ['PHASES', 'BANDCONTRAST', 'BOUNDARY', 'Boundaries', 'Grains', 'EBSD', 'Neighbors', 'CPO', 'ipf', 'ORIENTATIONS']
filesTreatment.SortFiles([filesTreatment.tasks], taskCat)
filesTreatment.TransferFiles(filesTreatment.tasks, [f'{filesTreatment.tasks}/divers'], extension = '.txt')
filesTreatment.TransferFiles(filesTreatment.lames, [f'{filesTreatment.lames}/divers'], extension = '.txt')
