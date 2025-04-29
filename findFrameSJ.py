import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import cv2
import pandas as pd
import datetime



class TrafficApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Traffic Annotation Viewer")
        
        self.video_path = None
        self.csv_path = None
        self.df = None
        self.current_index = -1
        self.display_duration_seconds = 5  # Preset Value(Adjustable after opening application)
        self.cap = None
        self.out = None
        self.last_frame = None
        
        
        # UI Elements
        self.show_popups_var = tk.BooleanVar(value=True)  # Popups are enabled by default
        
        # Create a Checkbutton as a toggle switch
        self.toggle_popup_switch = tk.Checkbutton(master, text="Popups Enabled", var=self.show_popups_var, 
                                                command=self.toggle_popups, onvalue=True, offvalue=False)
        self.toggle_popup_switch.pack()  # Adjust placement as needed
        self.load_button = tk.Button(master, text="Load Video & CSV", command=self.load_files)
        self.load_button.pack(side=tk.TOP)

        self.duration_button = tk.Button(master, text="Set Display Duration", command=self.set_display_duration)
        self.duration_button.pack(side=tk.TOP)

        self.prev_button = tk.Button(master, text="Previous Record", command=self.show_previous_record, state=tk.NORMAL)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(master, text="Next Record", command=self.show_next_record, state=tk.NORMAL)
        self.next_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(master, text="Save Current Video Segment", command=self.save_current_video_segment, state=tk.NORMAL)
        self.save_button.pack(side=tk.RIGHT)
        
        self.screenshot_button = tk.Button(master, text="Save Screenshot. Can also press 's' if paused", command=self.save_screenshot, state=tk.NORMAL)
        self.screenshot_button.pack(side=tk.TOP)

        self.validate_true_button = tk.Button(master, text="Validate TRUE", command=lambda: self.validate_record("TRUE"), state=tk.NORMAL)
        self.validate_true_button.pack(side=tk.TOP)

        self.validate_false_button = tk.Button(master, text="Validate FALSE", command=lambda: self.validate_record("FALSE"), state=tk.NORMAL)
        self.validate_false_button.pack(side=tk.TOP)

        self.save_validation_button = tk.Button(master, text="Save Validations", command=self.save_validation, state=tk.NORMAL)
        self.save_validation_button.pack(side=tk.TOP)
        
        #Gives a list of commands
        command_instructions = "Commands:\n- p: Pause/Unpause\n- q: Quit loop\n- s: Screenshot (when paused)\n- t: Validate True\n- f: Validate False"
        self.commands_label = tk.Label(master, text=command_instructions, justify=tk.LEFT, bg="lightgrey", fg="black", font=("TkDefaultFont", 10), relief=tk.RIDGE)
        self.commands_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.status_label = tk.Label(master, text="No file loaded")
        self.status_label.pack(side=tk.BOTTOM)
        
    def load_files(self):
        self.video_path = filedialog.askopenfilename(title="Select Video File", filetypes=(("MP4 files", "*.mp4"),))
        self.csv_path = filedialog.askopenfilename(title="Select CSV File", filetypes=(("CSV files", "*.csv"),))
        if self.video_path and self.csv_path:
            self.df = pd.read_csv(self.csv_path)
            self.current_index = -1
            self.total_records = len(self.df)
            self.cap = cv2.VideoCapture(self.video_path)
            if self.cap.isOpened():
                self.status_label.config(text="Files loaded. Total records: {}".format(self.total_records))
            else:
                messagebox.showerror("Error", "Failed to load the video file.")
        else:
            messagebox.showinfo("Info", "Operation cancelled or invalid file selection.")
            
    def toggle_popups(self):
        if self.show_popups_var.get():
            self.toggle_popup_switch.config(text="Popups Enabled")
        else:
            self.toggle_popup_switch.config(text="Popups Disabled")



    def update_status(self):
        self.status_label.config(text=f"Record: {self.current_index + 1}/{self.total_records}")

    def navigate_record(self, index_change):
        new_index = self.current_index + index_change
        if 0 <= new_index < self.total_records:
            self.current_index = new_index
            self.update_status()
        else:
            messagebox.showinfo("End", "No more records in this direction.")

    def show_previous_record(self):
        if self.current_index > 0:
            self.navigate_record(-1)
            self.process_current_record(save=False)

    def show_next_record(self):
        if self.current_index < self.total_records - 1:
            self.navigate_record(1)
            self.process_current_record(save=False)
            
    def set_display_duration(self):
        duration = simpledialog.askinteger("Input", "Enter the display duration (seconds):", minvalue=1, maxvalue=60)
        if duration:
            self.display_duration_seconds = duration
    def save_screenshot(self):
        if self.last_frame is not None:
            screenshot_path = f"screenshot_{self.current_index + 1}.png"
            cv2.imwrite(screenshot_path, self.last_frame)
            if self.show_popups_var.get():
                messagebox.showinfo("Success", f"Screenshot saved as {screenshot_path}.")
        else:
            messagebox.showerror("Error", "No frame available for screenshot.")



            
    def validate_record(self, validation):
        if self.df is not None and 0 <= self.current_index < len(self.df):
            self.df.at[self.current_index, 'validation'] = validation
            self.save_validation()  # Save the CSV immediately after validating
            if self.show_popups_var.get():
                messagebox.showinfo("Validation", f"Record {self.current_index + 1} marked as {validation}.")

            # Automatically move to the next record
            if self.current_index + 1 < len(self.df):
                self.current_index += 1
                self.process_current_record(False)  # Assuming False means not saving the video segment
            else:
                messagebox.showinfo("End", "You've reached the end of the records.")
        else:
            messagebox.showerror("Error", "No record selected for validation.")


    def save_validation(self):
        if self.csv_path and self.df is not None:
            self.df.to_csv(self.csv_path, index=False)
            if self.show_popups_var.get():
                messagebox.showinfo("Success", "Validations saved to CSV.")



    def process_current_record(self, save):
        if not self.cap.isOpened():
            self.cap.open(self.video_path)

        record = self.df.iloc[self.current_index]
        self.cap.set(cv2.CAP_PROP_POS_MSEC, record['time'] * 1000)

        if save:
            # Generate a unique filename for each segment
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"segment_{self.current_index}_{timestamp}.mp4"
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.out = cv2.VideoWriter(unique_filename, fourcc, fps, (frame_width, frame_height))
        
        # Display the initial frame with annotation
        ret, frame = self.cap.read()
        if ret:
            trajectory = eval(record['trajectory'].replace('null', 'None'))
            x, y, w, h = trajectory[0][:4]
            vehicle_type = record['type']
            cv2.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)), (255, 0, 0), 2)
            cv2.putText(frame, vehicle_type, (int(x), int(y - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            self.last_frame = frame  # Save for potential screenshot
            cv2.imshow('Frame', frame)
            
            if save:  # Write the initial annotated frame if saving
                self.out.write(frame)

            paused = False
            display_time_ms = 2000  # 2 seconds for initial display
            start_time = cv2.getTickCount()
            elapsed_time = 0

            while elapsed_time < display_time_ms:
                self.master.update()
                cv2.imshow('Frame', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('p'):
                    paused = not paused
                elif key == ord('s') and paused:
                    self.save_screenshot()
                elif key == ord('t'):  # Hotkey for validating True
                    self.validate_record(True)
                elif key == ord('f'):  # Hotkey for validating False
                    self.validate_record(False)
                if not paused:
                    elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency() * 1000
                else:
                    start_time = cv2.getTickCount() - elapsed_time / 1000 * cv2.getTickFrequency()

        fps = self.cap.get(cv2.CAP_PROP_FPS)
        delay = int(1000 / fps)

        # Playback loop for the video segment
        paused = False
        frame_count = 0
        total_frames = fps * self.display_duration_seconds

        while frame_count < total_frames:
            if not paused:
                ret, frame = self.cap.read()
                if not ret:
                    break
                self.last_frame = frame
                cv2.imshow('Frame', frame)
                if save:  # Continue writing frames to the video file during playback
                    self.out.write(frame)
            self.master.update()
            key = cv2.waitKey(delay) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                paused = not paused
            elif key == ord('s') and paused:
                self.save_screenshot()
            elif key == ord('t'):  # Hotkey for validating True
                self.validate_record(True)
            elif key == ord('f'):  # Hotkey for validating False
                self.validate_record(False)
            if not paused:
                frame_count += 1

        if save:
            self.out.release()  # Finalize the video file after saving the segment

            
    def play_next_frame(self):
        if self.is_paused or not self.ret:
            return  # Do not proceed if paused or if the video has ended

        self.ret, frame = self.cap.read()
        if self.ret:
            # Process the frame (e.g., draw bounding box, vehicle type)
            self.display_frame(frame)  # Apply annotations
            
            if self.save_video and self.out:
                self.out.write(frame)  # Write the frame to the video file
            
            self.frame_count += 1

        # Adjust delay based on FPS to match original video's speed
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        delay = max(int(1000 / fps), 1)
        self.master.after(delay, self.play_next_frame)





    def save_current_video_segment(self):
        self.process_current_record(save=True)
        if self.show_popups_var.get():
            messagebox.showinfo("Info", "Segment saved successfully.")

    def on_close(self):
        if self.cap:
            self.cap.release()
        if self.out:
            self.out.release()
            self.out = None
        cv2.destroyAllWindows()
        self.master.destroy()

root = tk.Tk()
app = TrafficApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_close)
root.mainloop()
