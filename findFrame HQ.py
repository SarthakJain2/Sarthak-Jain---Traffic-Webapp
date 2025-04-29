import cv2
import pandas as pd
import time
import pyautogui 
import numpy as np


# Read the CSV file containing the timestamps
csv_path = "2021_0609_105130_001A.csv"
df = pd.read_csv(csv_path)
print(df.head())

# Open the video file
cap = cv2.VideoCapture('09012023.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)

# Set the initial frame number to 0
rid = 0

text = 0
# Define the font type and size
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1.5

# Define the text color and thickness
color = (0, 0, 255) # BGR format
thickness = 4

# Define the text position
org = (50, 50) # bottom-left corner of the text string
time_org = (200, 50) # bottom-left corner of the text string
text = "a: previous, d: next, space: stop-playing/true, s: slow, other: quit"

# video segment offset in sec
offset = 30

while True:
    # Get the next frame number from the CSV file
    if rid < len(df):
        next_vid_timestamp = df.iloc[rid]['time_since_start']
        next_timestamp = df.iloc[rid]['time']

    else:
        break
    
    # define the start frame and the end frame of the video segment to review
    segment_range = (int((next_vid_timestamp - 60 * (next_vid_timestamp / 86400)) * fps), int((next_vid_timestamp) * fps))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    time_text = next_timestamp.split(".")[0]
    # Set the video position to the specified timestamp
    cap.set(cv2.CAP_PROP_POS_FRAMES, segment_range[0])
    

    # play the video segment
    for _ in range(segment_range[0], segment_range[1]):
        success, image = cap.read()
        if success:
            # time.sleep(0.01) # video streaming speed controller
            # image = cv2.putText(image, text, org, font, font_scale, color, thickness)
            image = cv2.putText(image, time_text, time_org, font, font_scale, color, thickness)
            cv2.imshow('Frame', image)
        if cv2.waitKey(25) & 0xFF == ord(' '):
            break

        
    # Wait for a key press
    key = cv2.waitKey(0)
    
    # If the space bar is pressed, add "TRUE" to the CSV file
    if key == ord(' '):
        df.loc[df['time'] == next_timestamp, 'Validation'] = 'TRUE'
        df.to_csv(csv_path, index=False)
        rid += 1
    elif key == ord('s'):
        df.loc[df['time'] == next_timestamp, 'Validation'] = 'SLOW'
        df.to_csv(csv_path, index=False)
        rid += 1
    # If the 'a' or 'd' key is pressed, advance to the next timestamp
    elif key == ord('d'):
        rid += 1
    elif key == ord('a'):
        rid -= 1
    #add a screenshot
    elif key == ord('p'):
        cv2.imwrite(df.iloc[rid]['_id'].strip('"') + ".png", image)
        rid += 1
    # If any other key is pressed, exit the loop
    else:
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()