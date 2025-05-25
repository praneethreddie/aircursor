# Air Cursor - Hand Gesture Control System

Air Cursor is a Python-based application that allows you to control your computer's cursor and perform window management actions using hand gestures captured through your webcam. It utilizes computer vision and hand tracking technology to create a touchless interface for your computer.

## Features

- **Cursor Control**: Move your index finger to control the cursor position
- **Click Action**: Perform a pinch gesture (bring thumb and index finger together) to click
- **Window Minimize**: Bring all fingers together to minimize the active window
- **Window Close**: Show the back of your hand to close the active window
- **Smooth Movement**: Implemented cursor smoothing for better control
- **Real-time Visualization**: See hand tracking landmarks in real-time

## Requirements

- Python 3.x
- Webcam
- Required packages (listed in requirements.txt):
  - opencv-python
  - mediapipe
  - pyautogui
  - numpy
  - pywin32

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/praneethreddie/aircursor
   cd aircursor
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python air_cursor.py
   ```

2. Position yourself in front of the webcam

3. Use the following gestures:
   - Move your index finger to control the cursor
   - Pinch (thumb and index finger) to click
   - Bring all fingers together and hold to minimize the current window
   - Show the back of your hand and hold to close the current window

4. Press 'q' to quit the application

## Gesture Guide

- **Cursor Movement**: Point your index finger and move it in the direction you want the cursor to go
- **Click**: Bring your thumb and index finger together (pinch gesture)
- **Minimize Window**: Bring all your fingers together and hold the gesture
- **Close Window**: Show the back of your hand to the camera and hold the gesture

## Configuration

You can adjust the following parameters in `air_cursor.py` to fine-tune the experience:

- `PINCH_THRESHOLD`: Sensitivity of the pinch gesture detection
- `FINGERS_TOGETHER_THRESHOLD`: Sensitivity of the minimize gesture detection
- `HAND_FLIP_THRESHOLD`: Sensitivity of the close gesture detection
- `GESTURE_HOLD_FRAMES`: Number of frames to hold a gesture before triggering an action
- `MOVEMENT_THRESHOLD`: Threshold for detecting hand movement
- `FPS_TARGET`: Target frames per second for processing

## Troubleshooting

1. If the cursor movement is too sensitive:
   - Adjust the smoothing factor in the code
   - Modify the coordinate mapping range

2. If gestures are not being detected:
   - Ensure good lighting conditions
   - Adjust the threshold values in the code
   - Keep your hand within the camera frame

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
