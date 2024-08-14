import cv2
import numpy as np
import time

def initialize_camera():
    """Initialize webcam and allow it to warm up."""
    capture = cv2.VideoCapture(0)
    time.sleep(3)
    return capture

def capture_background(capture, frames=30):
    """Capture and return the background frame."""
    for _ in range(frames):
        ret, bg = capture.read()
    return np.flip(bg, axis=1)

def create_mask(hsv_frame, lower_bound, upper_bound):
    """Create and refine mask for the given color range."""
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))
    return mask

def apply_invisibility_effect(frame, background, mask):
    """Apply the invisibility effect by replacing masked areas with the background."""
    inverse_mask = cv2.bitwise_not(mask)
    foreground = cv2.bitwise_and(frame, frame, mask=inverse_mask)
    background_part = cv2.bitwise_and(background, background, mask=mask)
    return cv2.addWeighted(foreground, 1, background_part, 1, 0)

def main():
    capture = initialize_camera()
    background = capture_background(capture)

    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        frame = np.flip(frame, axis=1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([94, 80, 2])
        upper_blue = np.array([126, 255, 255])
        blue_mask = create_mask(hsv, lower_blue, upper_blue)
        output_frame = apply_invisibility_effect(frame, background, blue_mask)

        cv2.imshow('Invisibility Cloak', output_frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Invisibility Cloak', cv2.WND_PROP_VISIBLE) < 1:
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
