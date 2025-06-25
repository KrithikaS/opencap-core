import os
import sys
import numpy as np
import pandas as pd

thisDir = os.path.dirname(os.path.realpath(__file__))
repoDir = os.path.abspath(os.path.join(thisDir,'..'))
sys.path.append(repoDir)

from utils import getTrialNameIdMapping
from main import main

# Define session/trial details
session_id = 'b09da98f-df14-4285-8b24-a3b3e4df05d6'
dynamic_trialNames = ['C90_L1']
cameras_to_use = ['Cam0', 'Cam1', 'Cam2']

trialNames = getTrialNameIdMapping(session_id)
# dynamic_ids = [
#     trialNames[name]['id'] if name in trialNames else 'UNKNOWN_ID'
#     for name in dynamic_trialNames
# ]

dynamic_ids = [trialNames[name]['id'] for name in dynamic_trialNames]

print('Processing ' + session_id)

dataDir = os.path.join(thisDir, '')

for i_trial, dID in enumerate(dynamic_ids):
    main(session_id, dynamic_trialNames[i_trial], dID, 
        dataDir=dataDir,
        genericFolderNames=True,
        poseDetector='hrnet',
        cameras_to_use=cameras_to_use)

def getTrialNameIdMapping(session_id):
    trials = getSessionJson(session_id)['trials']
    
    # dict of session name->id and date
    trialDict = {}
    for t in trials:
        trialDict[t['name']] = {'id':t['id'],'date':t['created_at']}
        
    return trialDict