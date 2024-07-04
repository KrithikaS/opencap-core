"""
---------------------------------------------------------------------------
OpenCap: reprocessSessions.py
---------------------------------------------------------------------------

Copyright 2022 Stanford University and the Authors

Author(s): Scott Uhlrich, Antoine Falisse

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy
of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


This script reprocesses OpenCap trials collected with the web application at
app.opencap.ai. You can specify multiple sessions to reprocess, or specific
trials within a session to reprocess. Data will (optionally) be saved locally
in your <repositoryDirectory>/Data/<session_id> folder. 


This script is useful for processing a session with more accurate and higher 
resolution pose estimation settings. It is also useful for debugging failed
trials.


The example session is publicly available, but you will need login credentials
from app.opencap.ai to run this script. You can quickly create credentials
from the home page: https://app.opencap.ai. We recommend first running the 
Examples/createAuthenticationEnvFile.py script prior to running this script.
Otherwise, you will need to to login every time you run the script.


You can view the example session at:
https://app.opencap.ai/session/23d52d41-69fe-47cf-8b60-838e4268dd50
"""

import os
import sys
sys.path.append(os.path.abspath('./..'))

from utilsServer import batchReprocess
from utilsAPI import getAPIURL
from utilsAuth import getToken

API_URL = getAPIURL()
API_TOKEN = getToken()

# %% User inputs.
# Enter the identifier(s) of the session(s) you want to reprocess. This is a list of one
# or more session identifiers. The identifier is found as the 36-character string at the
# end of the session url: app.opencap.ai/session/<session_id>

# Example
# session_ids = ['23d52d41-69fe-47cf-8b60-838e4268dd50']

# Stationary
# session_ids = [
                # 'dc95f941-b377-4c0f-929f-c18fc3a202f1', # S1
                # '332f5657-efa0-454b-8f82-e63488096006', # S2
                # 'd5ff6e67-c237-4000-86a4-47b10b31e33b', # S3
                # '53a6aaea-8059-414b-84ca-f4a0f4a777d5', # S4
                # '78e028a0-a2c2-4a1a-b1c1-1013b13963ea', # S5
                # '2adc93da-0853-40ef-8a7a-6aa15e4b2e2a', # S6
                # '94cfc971-1167-419d-9474-bed0b96e5206', # S7
                # '71ca0104-9a13-44a9-a12e-e0865b4cc70f', # S8
                # '8794230e-fa8e-4f44-ba62-5868ab88fde7', # S9
                # 'a119d7e6-1628-495e-b576-8eb892c8193d', # S10
                # '44788707-43ee-4031-9e95-8724852da152', # S11
                # '1ec22e49-cbe0-4b60-a4bd-5d2ad54459a6', # S12
                # '5a3a1e42-4744-49a3-a6f6-2cc0ed53bcfe', # S13
                # '2f4d561f-c4bf-469d-9a42-bf12ef2271c8', # S14
                # '9fc09046-4247-4dbb-8bf4-98758c02211e', # S15
                # 'd8f5cdca-34de-4e23-9007-55c886616a28', # S16
                # '031dbb98-9f5d-4ab4-bdd3-d4b3c52e9bdf', # S17
                # 'ff39bfb3-8293-4d27-b9ca-41972af28692', # S18
                # '6e7901ec-23d7-4ed7-939c-a143e6d03f9f', # S21
                # '34a2a803-3ffb-4718-a2d6-040d02f5baa7', # S22
                # 'a9ec7429-fd69-4922-b4b4-4ce41b4570c9', # S23
                # '3409b96e-90cb-4ef8-a67e-b72d7407d0f4', # S24
                # '373c45d0-dc2d-4eb4-bb0e-4cc6dce6301f', # S25
                # 'b011b3e2-203a-4e98-87fd-c6ea4d95acbf', # S26
                # 'af17abef-7507-48f6-941b-25d152d317ed', # S28 - Change the neutral number of frames to 5 from 10
                # 'd10751a5-7e94-495a-94d0-2dd229ca39e0', # S29
                # 'e742eb1c-efbc-4c17-befc-a772150ca84d', # S30
                # ]

# Traversing
session_ids = [
                # '1443ed48-3cbe-4226-a2cc-bc34e21a0fb3', # S1 - Change the neutral number of frames to 5 from 10
                '5249a0b7-282d-4339-bef2-8e3b3dc88372', # S2
                # '9c1b5be7-cf95-4f0f-abc2-5f117b134123', # S3
                # '26c51f1d-6b16-4a80-af35-de61818a2c85', # S4
                # '81121c4c-f197-4323-b4c5-a7649a5c5f93', # S5
                # '1b365060-f439-406d-a98d-cbd1be79966b', # S6
                # 'b09da98f-df14-4285-8b24-a3b3e4df05d6', # S7
                # 'd353fa2a-1c02-40f7-9a1c-f4dbe5d02a83', # S8
                # 'aa735c89-e43f-4a0f-8a6b-117c5d854d79', # S9
                # '09a91af3-de83-488c-ae98-9201af866e95', # S10
                # 'b07c0de4-d081-4dda-a941-ceca43522c7b', # S11
                # '263c4a4e-2c18-4157-a276-a8a8d1842b35', # S12
                # '064ff969-08ab-4aad-9cfc-973b70b19c37', # S13
                # '89214e8a-b2f3-45b5-b3ed-91115cf5e69a', # S14
                # '1e5aae82-9380-4d7a-9d9f-89ff240fc987', # S15
                # '76d371ba-3c89-4383-aa19-7971e82fe718', # S16
                # '7b3f02d6-cecc-4a5f-9314-a32d81d695c3', # S17
                # '2b80cdd6-1f4c-4f08-91e9-7670694a91d3', # S18
                # 'a4007d87-5cef-446a-b2d7-d6581e1cd63e', # S21
                # '6fdffc2c-eade-4ddc-b8d5-dc047f5dd488', # S22
                # '379fb610-90ed-459a-ae9d-d0b7070ec4a8', # S23
                # '238f41ce-0e35-4594-b4cd-df5042628a2f', # S24
                # '1fc766fc-c103-4116-a1ee-9fc7a1c62e5d', # S25
                # 'c8ec5277-0adc-4afb-a7c0-a767dc9fa5d6', # S26
                # 'f09528a1-0992-409f-9f8f-e7e852b8e4e8', # S28
                # 'eb517e30-17c8-4b00-a46b-8d564a53b5f8', # S29
                # '9fd8370e-4fd3-4caa-a085-42c29eb497b5', # S30
                ]

# In-the-wild
session_ids = [
                # '4218da28-7720-4994-8b0d-7eb99c38877f', # S1
                # '24192a02-5d1c-4302-834d-c620415575af', # S2
                # '748397dc-2524-4bc1-ab3a-fbe01047e466', # S3
                # '1328dbe4-f7cc-4ed0-9a0f-33fd9738e926', # S4
                # '02dcf8d9-8d97-49ee-952b-9b9b9c446f44', # S5
                # '322fb9dc-dfda-4ee0-a6e2-af48c6c51816', # S6
                # 'fde40b93-2f34-4a13-90ed-10f8d59ab7d8', # S7
                # '6e845fec-c30b-4434-ac7c-096cbcfb70c3', # S8
                # '88a9849d-bfce-4e93-94e4-4c35e8293c20', # S9
                # 'cee26815-b3e8-4ad7-a016-cd506ff31a29', # S10
                # 'a6525d1-42dc-4af1-9dc6-6414894ee78a', # S11
                # 'd9f9ee36-5584-4d4b-b31b-fa6150034b92', # S12
                # 'be0fb943-4606-4878-ad71-6d7ccb102f0f', # S13
                # '72a31a2a-5d01-4818-bb2d-77719a26d334', # S14
                # '1c01a02b-5450-4219-9ea7-31d034ad6ac3', # S15
                # '8ce12017-1d1c-47c3-bc0b-cb75948a9938', # S16
                # 'dfce5643-dfc0-471a-8c6b-caf746c6e003', # S17
                # '2028197a-c1c8-4d09-ad43-8cf8fc6fa657', # S18
                # '70bcbb66-fcab-45f0-9ea8-b23912200cb7', # S21
                # 'e1d50e78-a98f-481d-b130-dba286ae76ff', # S22
                # '5adf2b4d-cabe-4c8b-84d5-2ecac62a44ab', # S23
                # '02159c08-3dc0-43bb-9173-a3fdf1fc6886', # S24
                # '60dbf22c-d84a-48c2-af89-f88e934e96c3', # S25
                # '21db7e28-9123-46e0-9cb6-02a9c76cd8b9', # S26
                '07732617-ea7d-4243-be1c-327cf33cf14f', # S28
                # 'b1642639-d9e1-499f-a7eb-82f55c9a2dd5', # S29
                # 'eeb943ec-7f94-4472-aa2a-86bfdd203577', # S30
                ]

# Select which trials to reprocess. You can reprocess all trials in the session 
# by entering None in all fields below. The correct calibration and static
# trials will be automatically selected if None, and all dynamic trials will be
# processed if None. If you do not want to process one of the trial types, 
# enter []. If you specify multiple sessions above, all of the fields
# below must be None or []. If you selected only one session_id above, you may
# select specific trials. Only one trial (str) is allowed for calib_id and
# static_id. A list of strings is allowed for dynamic_trialNames.

calib_id = [] # None (auto-selected trial), [] (skip), or string of specific trial_id
static_id = None # None (auto-selected trial), [] (skip), or string of specific trial_id
dynamic_trialNames = None # None (all dynamic trials), [] (skip), list of trial names, or
                              # list of activities out of ['DJ', 'LS', 'DC', 'TH', 'C9'] for drop-jump, leg-squat, drop-cut, triple-hop, cut-90

# Select which pose estimation model to use; options are 'OpenPose' and 'hrnet'.
# If the same pose estimation model was used when collecting data with the web
# app and if (OpenPose only) you are not reprocessing the data with a different
# resolution, then the already computed pose estimation results will be used and
# pose estimation will not be re-run. Please note that we do not provide support
# for running 'hrnet' locally. If you want to use 'hrnet', you will need to have
# selected 'hrnet' when collecting data with the web app. You can however re-
# process data originally collected with 'hrnet' with 'OpenPose' if you have 
# installed OpenPose locally (see README.md for instructions).
poseDetector = 'hrnet'

# OpenPose only:
# Select the resolution at which the videos are processed. There are no
# resolution options for hrnet and resolutionPoseDetection will be ignored.
# The finer the resolution the more accurate the results (typically) but also
# the more GPU memory is required and the more time it takes for processing.
# OpenCap supports the following four resolutionPoseDetection options (ordered
# from lower to higher resolution/required memory):
#   - 'default': 1x368 resolution, default in OpenPose (we were able to run with a GPU with 4GB memory).
#   - '1x736': 1x736 resolution, default in OpenCap (we were able to run with a GPU with 4GB memory).
#   - '1x736_2scales': 1x736 resolution with 2 scales (gap = 0.75). (may help with people larger in the frame. (we were able to run with a GPU with 8GB memory)
#       - Please visit https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/include/openpose/flags.hpp#L112
#         to learn more about scales. The conversation in this issue is also
#         relevant: https://github.com/CMU-Perceptual-Computing-Lab/openpose/issues/622
#   - '1x1008_4scales': 1x1008 resolution with 4 scales (gap = 0.25). (we were only able to run with a GPU with 24GB memory)
#       - This is the highest resolution/settings we could use with a 24GB
#         GPU without running into memory issues.
resolutionPoseDetection = '1x736'


# Set deleteLocalFolder to False to keep a local copy of the data. If you are 
# reprocessing a session that you collected, data will get written to the database
# regardless of your selection. If True, the local copy will be deleted.
deleteLocalFolder = False
      

# %% Process data.
batchReprocess(session_ids,calib_id,static_id,dynamic_trialNames,
               poseDetector=poseDetector,
               resolutionPoseDetection=resolutionPoseDetection,
               deleteLocalFolder=deleteLocalFolder,
               cameras_to_use=['all_available'])
