# This script trims a specific camera's video and corresponding pose pkl file to the same start and end times

'''
NOTE: DO NOT UPLOAD THESE VIDEOS TO THE SERVER AT THIS TIME,
      OR YOU MIGHT LOSE THE ORIGINALS FOREVER - OR AT LEAST 
      SAVE THEM SOMEWHERE MEMORABLE

NOTE: Before reprocessing your data, rename the generated trimmed files
      to get rid of the "trimmed_" prefix

NOTE: To test if it's working okay, try: different start/stop times 
      (including stop time as None), frequencies, and activities
'''
# Load libraries
import sys
import os
sys.path.append(os.path.abspath('./..'))

import pickle
import shutil
import subprocess

# ======== HELPER FUNCTIONS - Written with GPT-4o help ========
def duplicate_files_with_prefix(file_directory, prefix):
    # file_directory is a path containing all the files to be modified
    # prefix is a string that will be added to the front of all the existing filenames

    for filename in os.listdir(file_directory):
        old_file_path = os.path.join(file_directory, filename)
    
        # Check if it's a file (not a directory)
        if os.path.isfile(old_file_path):
            # Create the new file name by adding the prefix
            new_filename = prefix + filename
            
            # Create full new file path
            new_file_path = os.path.join(file_directory, new_filename)
            
            # Rename the file
            shutil.copy(old_file_path, new_file_path)
            print(f"Renamed {filename} to {new_filename}")
        else:
            print(f"{filename} is not a file -- skipping")

    print("All files have been renamed.")

def seconds_to_hhmmss(seconds):
    # To simplify user's work - trim times should just be provided in seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{int(hours):02}:{int(minutes):02}:{secs:06.3f}"

def get_closest_keyframe_info(input_file, time_in_s, is_before = True): ## Not used anymore - okay to delete
    """
    Finds the frame index of the nearest keyframe before the given time
    is_before = False finds the nearest keyframe after the given time
    """

    # Extract all frames with their types and timestamps
    cmd = [
        'ffprobe',
        '-v', 'warning', # Set the output level to warnings and above
        '-select_streams', 'v:0',
        '-show_entries', 'frame=pts_time,pict_type',
        '-of', 'csv=p=0',
        '-print_format', 'csv',
        input_file
    ]

    try:
        # Note: subprocess.PIPE allows saving the output to a variable that would otherwise be directly printed to the terminal
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        lines = result.stdout.strip().split('\n')

        last_keyframe_index = None
        last_keyframe_time = None

        if is_before:
            for frame_index, line in enumerate(lines):
                if not line: # Skips empty lines
                    continue
                line_parts = line.split(',') # Expecting to see an output like [## frame, timestamp, frametype, extra4, entry5] or [## frame, timestamp, frametype]
                time_str = line_parts[1]
                pict_type = line_parts[2]
                if pict_type == 'I':
                    time = float(time_str)
                    if time <= time_in_s:
                        last_keyframe_index = frame_index
                        last_keyframe_time = time
                    else:
                        break
        else:
            for frame_index, line in reversed(list(enumerate(lines))):
                if not line: # Skips empty lines
                    continue
                line_parts = line.split(',') # Expecting to see an output like [## frame, timestamp, frametype, extra4, entry5] or [## frame, timestamp, frametype]
                time_str = line_parts[1]
                pict_type = line_parts[2]
                if pict_type == 'I':
                    time = float(time_str)
                    if time >= time_in_s:
                        last_keyframe_index = frame_index
                        last_keyframe_time = time
                    else:
                        break

        if last_keyframe_index is not None:
            print(f"Video will be cut at keyframe #{last_keyframe_index}, time={last_keyframe_time:.3f} sec")
            return last_keyframe_index, last_keyframe_time
        else:
            print("No keyframe found before the target time.")
            return None

    except subprocess.CalledProcessError as e:
        print("Error running ffprobe:", e.stderr)
        return None

def trim_video(input_video, output_video, start_time_in_s, duration_in_s = None):
    # Note: if end_time is specified, the cropped video will NOT include the frame at end_time
    start_time = seconds_to_hhmmss(start_time_in_s)
    
    # Build the ffmpeg command
    if duration_in_s is not None:
        duration = seconds_to_hhmmss(duration_in_s)
        command = [
            'ffmpeg',
            '-i', input_video,  # Input file
            '-ss', start_time,  # Start time
            '-t', duration,  # Duration
            '-q', '0', # Re-encode at highest quality
            '-v', 'warning', # Set the output level to warnings and above
            output_video
        ]
    else:
        command = [
        'ffmpeg',
        '-i', input_video,  # Input file
        '-ss', start_time,  # Start time
        '-q', '0', # Re-encode at highest quality
        '-v', 'warning', # Set the output level to warnings and above
        output_video
    ]

    # Run the ffmpeg command
    try:
        subprocess.run(command, check = True)
    except subprocess.CalledProcessError as e:
        print("Error: ", e)

def trim_pkl(input_pkl, output_pkl, start_frame, stop_frame):
    open_file = open(input_pkl, "rb")
    frames = pickle.load(open_file)
    print(f'Number of frames in original: {len(frames)}')
    open_file.close()

    if stop_frame is not None:
        trimmed_frames = frames[start_frame:stop_frame]
    else:
        trimmed_frames = frames[start_frame:]

    print(f'Number of frames in trimmed: {len(trimmed_frames)}')

    with open(output_pkl, 'wb') as pkl_file:
        pickle.dump(trimmed_frames, pkl_file)

# ========================================================

# ====================== SETUP ===========================
# Setup which files to modify
session_ID = '2a8af4cc-4167-42c3-a847-281fb08e4cae'
camNumber = 'Cam2'
start_time = 17.5 # in seconds - NOTE: The video length needs to start within 2s of the other videos to proceed with syncing
duration = None # Duration from start_time in seconds; None will crop to the end from start_time
framerate = 60
trialName = 'sdj_r2_1'

# Setup paths
baseDir = os.getcwd()
dataDir = os.path.abspath(os.path.join(baseDir,'Data'))
videoDir = os.path.join(dataDir, session_ID, 'Videos', camNumber, 'InputMedia', trialName)
pklDir = os.path.join(dataDir, session_ID, 'Videos', camNumber, 'OutputPkl_mmpose_0.8', trialName)

# =================== MAIN LOGIC =======================
# First find existing files and copy+rename them
duplicate_files_with_prefix(videoDir, 'orig_')
duplicate_files_with_prefix(pklDir, 'orig_')

# Now crop all the videos
for file in os.listdir(videoDir):
    if not os.path.isfile(os.path.join(videoDir, file)):
        print(f"Skipping {file} because it is not a file")
        continue
    if 'orig' in file: # We just created these copies
        continue

    trim_video(os.path.join(videoDir, file), os.path.join(videoDir, 'trimmed_' + file), start_time, duration)
    if duration is not None: print(f'{file} has been cropped from {start_time}s to {start_time + duration}s')
    else: print(f'{file} has been cropped from {start_time}s to end')

for file in os.listdir(pklDir):
    if not os.path.isfile(os.path.join(pklDir, file)):
        print(f"Skipping {file} because it is not a file")
        continue
    if 'orig' in file: # We just created these copies
        continue

    start_frame = round(start_time * framerate)
    if duration is not None: stop_frame = round(start_frame + (duration * framerate))
    else: stop_frame = None

    trim_pkl(os.path.join(pklDir, file), os.path.join(pklDir, 'trimmed_' + file), start_frame, stop_frame)
    if duration is not None: print(f'{file} has been cropped from frames {start_frame} to {stop_frame}')
    else: print(f'{file} has been cropped from frame {start_frame} to end')