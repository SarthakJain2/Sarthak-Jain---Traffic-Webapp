import cv2
import pandas as pd
import csv
import keyboard

# Read the CSV file containing the timestamps
df = pd.read_csv('traffic.csv')
print(df)

# Open the video file
cap = cv2.VideoCapture('002530_0013_20231129_104301.mp4')
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Set the initial frame number to 0
frame_number = 0

text = 0
# Define the font type and size
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1

# Define the text color and thickness
color = (0, 0, 255) # BGR format
thickness = 2

# Define the text position
org = (50, 50) # bottom-left corner of the text string

while True:
    # Get the next frame number from the CSV file
    if frame_number < len(df):
        if 'time' in df:
            next_timestamp = df.iloc[frame_number]['time']
            text = df.iloc[frame_number]['type']
        else:
            break
    else:
        break

    # Set the video position to the specified timestamp
    cap.set(cv2.CAP_PROP_POS_MSEC, next_timestamp * 1000)

    # Read the frame at the specified position
    success, image = cap.read()
    image = cv2.putText(image, text, org, font, font_scale, color, thickness)

    if success:
        # Display the frame
        cv2.imshow('Frame', image)
        
        # Wait for a key press
        key = cv2.waitKey(0)
        
        # If the space bar is pressed, add "TRUE" to the CSV file
        if key == ord(' '):
            df.loc[df['time'] == next_timestamp, 'Validation'] = 'TRUE'
            df.to_csv('traffic.csv', index=False)
            frame_number += 1

        # If the 'n' key is pressed, advance to the next timestamp
        elif key == ord('d'):
            frame_number += 1

        elif key == ord('a'):
            frame_number -= 1

        # If any other key is pressed, exit the loop
        else:
            break
    else:
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()