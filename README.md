# NJ Transit Vehicle Detection System

## Project Overview
This application was engineered for **NJ Transit** to identify vehicles that stop on railroad crossings using **computer vision** techniques. The system detects and validates over **500+ vehicles** across various datasets, helping improve safety at critical intersections.

## Key Features
- 🚗 **Vehicle Detection**  
  Utilized **OpenCV** to create bounding boxes around **3,000+ vehicles** of interest for robust validation.

- 🛤 **Railroad Stop Validation**  
  Developed algorithms to detect and flag vehicles that stop on tracks, enhancing operational monitoring.

- 🎨 **User-Friendly Interface**  
  Designed a **responsive UI** using **Tkinter** for:
  - Setting video clip durations
  - Navigating through clips efficiently
  - Validating stops with easy-to-use controls

## Technologies Used
- Python
- OpenCV
- Tkinter

## How It Works
1. **Video Input**  
   The system ingests traffic footage from NJ Transit cameras.

2. **Object Detection**  
   Vehicles are detected using computer vision models, and bounding boxes are drawn around potential violators.

3. **Clip Generation and Review**  
   Users can adjust clip durations, navigate through frames, and validate whether a vehicle actually stopped.

4. **Validation Interface**  
   Operators use the custom Tkinter UI to quickly validate detected stops and export results for reporting.

## Project Impact
- Successfully processed and validated over **500 vehicles** stopped at railroad crossings.
- Enhanced the safety monitoring systems for NJ Transit using **AI-powered visual analysis**.
- Streamlined the manual review process through an intuitive and responsive UI.