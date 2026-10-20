
# Hand Gesture Control

A Python-based application that uses computer vision to control
screen brightness and system volume through hand gestures.

## Features

- Real-time hand tracking using MediaPipe
- Finger-distance-based control
- Screen brightness adjustment
- Windows system volume adjustment
- Smoothed gesture input for more stable control
- On-screen percentage bar and control-mode indicator
- Keyboard shortcuts for switching modes and exiting

## Technologies Used

- Python
- OpenCV
- MediaPipe
- Screen Brightness Control
- Pycaw
- Comtypes

## How It Works

The application detects hand landmarks through a webcam and
measures the distance between the thumb tip and index fingertip.
This distance is mapped to a percentage from 0 to 100.

The percentage is used to adjust screen brightness or system
volume, depending on the selected control mode.

## Requirements

- Python 3.10
- A webcam
- Windows for system volume control
- A display supported by `screen-brightness-control`

## Installation

1. Clone this repository:

   ```bash
   https://github.com/AjayKumar366/Hand_Gesture-Control.git
   ```

2. Navigate to the project folder:

   ```bash
   cd Hand_Gesture-Control
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

4. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   python main.py
   ```

## Controls

| Key | Action |
| --- | --- |
| B | Brightness mode |
| V | Volume mode |
| Q | Quit the application |

## Notes

- Brightness is limited to a minimum of 10%.
- Volume can range from 0% to 100%.
- Control responsiveness depends on camera quality,
  lighting, and hand position.
- Brightness support depends on the display and its drivers.

## Future Improvements

- Configurable gesture calibration
- Improved visual interface
- Additional gesture-based actions
- Performance and responsiveness improvements

