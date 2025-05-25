import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import win32gui
import win32con

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Get screen size
screen_width, screen_height = pyautogui.size()

# Constants for pinch detection and stability
PINCH_THRESHOLD = 0.08  # Increased threshold for more deliberate pinches
PINCH_HOLD_FRAMES = 5  # Increased frames for more stable click detection
PINCH_RELEASE_THRESHOLD = 0.12  # Separate threshold for releasing pinch
FINGERS_TOGETHER_THRESHOLD = 0.04  # Threshold for detecting fingers together
HAND_FLIP_THRESHOLD = 0.3  # Threshold for detecting hand flip
GESTURE_HOLD_FRAMES = 10  # Frames to hold gesture before action
FPS_TARGET = 30  # Target frames per second

# Initialize state variables
pinch_clicked = False
pinch_frames = 0
gesture_frames = 0
last_frame_time = 0
MOVEMENT_THRESHOLD = 0.02  # Threshold for movement detection
last_index_x = 0
last_index_y = 0
last_gesture = None

def minimize_active_window():
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

def close_active_window():
    hwnd = win32gui.GetForegroundWindow()
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

def detect_hand_gesture(hand_landmarks):
    # Get all finger tip coordinates
    finger_tips = [
        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    ]
    
    # Check if all fingers are together
    max_distance = 0
    for i in range(len(finger_tips)):
        for j in range(i + 1, len(finger_tips)):
            distance = np.sqrt(
                (finger_tips[i].x - finger_tips[j].x)**2 +
                (finger_tips[i].y - finger_tips[j].y)**2
            )
            max_distance = max(max_distance, distance)
    
    # Get wrist and middle finger positions for hand orientation
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    hand_direction = middle_finger.z - wrist.z
    
    if max_distance < FINGERS_TOGETHER_THRESHOLD:
        return 'minimize'
    elif hand_direction > HAND_FLIP_THRESHOLD:
        return 'close'
    return None

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set webcam dimensions
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Smoothing factor for cursor movement
smoothing = 0.5
prev_x, prev_y = 0, 0

def map_coordinates(hand_x, hand_y):
    # Convert hand coordinates to screen coordinates
    screen_x = np.interp(hand_x, [0.2, 0.8], [0, screen_width])
    screen_y = np.interp(hand_y, [0.2, 0.8], [0, screen_height])
    
    # Apply smoothing
    global prev_x, prev_y
    curr_x = prev_x + (screen_x - prev_x) * smoothing
    curr_y = prev_y + (screen_y - prev_y) * smoothing
    
    prev_x, prev_y = curr_x, curr_y
    return int(curr_x), int(curr_y)

try:
    while True:
        # Control frame rate
        current_time = cv2.getTickCount()
        if current_time - last_frame_time < cv2.getTickFrequency() / FPS_TARGET:
            continue
        last_frame_time = current_time

        # Read frame from webcam
        success, frame = cap.read()
        if not success:
            print("Failed to capture frame")
            continue

        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process hand tracking
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Detect gestures
                current_gesture = detect_hand_gesture(hand_landmarks)
                
                if current_gesture == last_gesture and current_gesture is not None:
                    gesture_frames += 1
                    if gesture_frames >= GESTURE_HOLD_FRAMES:
                        if current_gesture == 'minimize':
                            minimize_active_window()
                            gesture_frames = 0
                        elif current_gesture == 'close':
                            close_active_window()
                            gesture_frames = 0
                else:
                    gesture_frames = 0
                    last_gesture = current_gesture
                
                # Get finger coordinates for cursor control
                index_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                thumb_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                
                # Calculate distance between thumb and index finger
                pinch_distance = np.sqrt((index_x - thumb_x)**2 + (index_y - thumb_y)**2)
                
                # Calculate movement since last frame
                movement = np.sqrt((index_x - last_index_x)**2 + (index_y - last_index_y)**2)
                last_index_x, last_index_y = index_x, index_y
                
                # Map coordinates and move cursor
                cursor_x, cursor_y = map_coordinates(index_x, index_y)
                pyautogui.moveTo(cursor_x, cursor_y)
                
                # Enhanced pinch gesture detection with movement check
                if pinch_distance < PINCH_THRESHOLD and movement < MOVEMENT_THRESHOLD:
                    pinch_frames += 1
                    if pinch_frames >= PINCH_HOLD_FRAMES and not pinch_clicked:
                        pyautogui.click()
                        pinch_clicked = True
                elif pinch_distance > PINCH_RELEASE_THRESHOLD:
                    pinch_frames = 0
                    pinch_clicked = False
        
        # Display frame
        cv2.imshow('Air Cursor', frame)
        
        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    hands.close()