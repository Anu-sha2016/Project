import cv2
import numpy as np

def cartoonify_image(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter to reduce noise and keep edges sharp
    gray = cv2.bilateralFilter(gray, d=9, sigmaColor=300, sigmaSpace=300)

    # Apply edge detection using adaptive thresholding
    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 2)

    # Convert the frame to a color image
    color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Combine the color image with the edges
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon

def capture_and_cartoonify():
    # Open the default camera (camera index 0)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Check if the frame was read successfully
        if not ret:
            print("Error: Could not read frame.")
            break

        # Cartoonify the frame
        cartoon_frame = cartoonify_image(frame)

        # Display the cartoonified frame
        cv2.imshow('Cartoonifier', cartoon_frame)

        # Capture an image when the 'c' key is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            # Save the captured frame to a file
            cv2.imwrite('cartoonized_photo.jpg', cartoon_frame)
            print("Cartoonized photo captured!")

        # Break the loop if 'q' key is pressed
        elif key == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()

if _name_ == "_main_":
    capture_and_cartoonify()