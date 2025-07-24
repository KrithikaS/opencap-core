import os
import sys
import numpy as np
import pandas as pd

thisDir = os.path.dirname(os.path.realpath(__file__))
repoDir = os.path.abspath(os.path.join(thisDir,'../'))
sys.path.append(repoDir)

from utils import getTrialNameIdMapping, postMotionData, writeMediaToAPI
from utilsServer import getResultsPath
from utilsAPI import getAPIURL
from main import main

API_URL = getAPIURL()

# Define session/trial details
session_id = '881ebd52-c1e7-4844-984d-7cc3ad5ec2b1'
dynamic_trialNames = ['ddj1_1']
cameras_to_use = ['all_available']

trialNames = getTrialNameIdMapping(session_id)
dynamic_ids = [trialNames[name]['id'] for name in dynamic_trialNames]
# dynamic_ids = dynamic_trialNames

print('Processing ' + session_id)

dataDir = os.path.join(thisDir, '')

for i_trial, dID in enumerate(dynamic_ids):
    main(session_id, dynamic_trialNames[i_trial], dID, 
        dataDir=dataDir,
        genericFolderNames=True,
        poseDetector='hrnet',
        cameras_to_use=cameras_to_use)
    
    # Write results to django
    session_path = os.path.join(dataDir, 'Data', session_id)
    postMotionData(dID,session_path,trial_name=dynamic_trialNames[i_trial],isNeutral=False,
                    poseDetector='hrnet')
    
    # Write visualizer jsons to django
    visualizerJson_path = getResultsPath(session_id, dID, 
                                            resultType='visualizerJson', 
                                            isDocker=False)
    writeMediaToAPI(API_URL,visualizerJson_path,dID,
                    tag="visualizerTransforms-json",deleteOldMedia=True)