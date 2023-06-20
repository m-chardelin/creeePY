from path import *
from creeePY import Files, Statistics, Display, Tex
import os


###  TRAITEMENT DES DONNEES EBSD, TRI DES RÉSULTATS ##########################

#### lancement de la macro en ligne de commande


# arborescence du dossier de traitement MTEX
filesTreatment = Files.Files(treatment, 'ZAB')
filesTreatment.SetFolders(data = 'data', dataClean = 'dataClean', output = 'output', auto = True)
filesTreatment.SetSubFolders(filesTreatment.output, ['total', 'total_indexed', 'total_notIndexed', 'lames', 'tasks'])


filesTreatment.CopyFiles(filesTreatment.total_indexed, [filesTreatment.total])

# nettoyage des fichiers avec le bon séparateur,
filesTreatment.CleanTxt([filesTreatment.total], [',', '&'], ';', extension = '.csv', exception = None)
filesTreatment.SetCats(filesTreatment.total, '.csv')
filesTreatment.CleanFiles([filesTreatment.lames, filesTreatment.tasks])

# copie des fichiers et classement en fonction des lames, puis en fonction des tâches effectuées
filesTreatment.CopyFiles(filesTreatment.total, [filesTreatment.lames, filesTreatment.tasks])
filesTreatment.SortFiles([filesTreatment.lames], filesTreatment.cat, sep = '_')
taskCat = ['PHASES', 'BANDCONTRAST', 'BOUNDARY', 'Boundaries', 'CPO', 'Grains', 'EBSD', 'Neighbors', 'NeighborsPairs', 'CPO', 'CPOporph', 'CPOall', 'CPOoppgporph', 'CPOoppgall', 'CPOoppg', 'IPF', 'ORIENTATIONS']
filesTreatment.SortFiles([filesTreatment.tasks], taskCat, sep = '.')
filesTreatment.TransferFiles(filesTreatment.tasks, [f'{filesTreatment.tasks}/divers'], extension = '.csv')
filesTreatment.TransferFiles(filesTreatment.lames, [f'{filesTreatment.lames}/divers'], extension = '.csv')
