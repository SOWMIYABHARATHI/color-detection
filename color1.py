import numpy as np
import pandas as pd
import cv2

# Ask the user whether to use an image or the webcam
mode = (
    input("Enter 'image' for image input or 'webcam' for real-time video feed: ")
    .strip()
    .lower()
)

# Global variables to store color values and mouse position
r = g = b = xpos = ypos = 0

# Load the colors CSV file
index = ["color", "color_name", "hex", "R", "G", "B"]
df = pd.read_csv(
    "d:/VSC/Color-Detection-master/Color-Detection-master/Data/colors.csv",
    names=index,
    header=None,
)


# Function to get the closest color name from the CSV
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(df)):
        d = (
            abs(R - int(df.loc[i, "R"]))
            + abs(G - int(df.loc[i, "G"]))
            + abs(B - int(df.loc[i, "B"]))
        )
        if d < minimum:
            minimum = d
            cname = df.loc[i, "color_name"] + "   Hex=" + df.loc[i, "hex"]
    return cname


# Function to identify the color at a given position
def identify_color(event, x, y, flags, param):
    global b, g, r, xpos, ypos
    if event == cv2.EVENT_LBUTTONDOWN:  # Only act on left button click
        xpos, ypos = x, y
        b, g, r = frame[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


# Create a window
cv2.namedWindow("image")
cv2.setMouseCallback("image", identify_color)

# Get screen resolution to resize the image or webcam feed to fit the display
screen_width = 1536  # Your screen width
screen_height = 864  # Your screen height


# Helper function to resize the frame to fit both width and height constraints
def resize_frame_to_screen(frame, screen_width, screen_height):
    frame_height, frame_width = frame.shape[:2]

    # Calculate scaling factors for width and height
    width_ratio = screen_width / frame_width
    height_ratio = screen_height / frame_height

    # Choose the smallest ratio to ensure the image fits on screen
    scale_factor = min(width_ratio, height_ratio)

    # Resize the frame
    new_width = int(frame_width * scale_factor)
    new_height = int(frame_height * scale_factor)

    return cv2.resize(frame, (new_width, new_height))


# If the user chooses to input an image
if mode == "image":
    # Ask for the image file path
    image_path = input("Enter the path of the image file: ").strip()

    # Load the image
    frame = cv2.imread(image_path)
    if frame is None:
        print("Error: Could not load the image.")
    else:
        # Resize the image to fit the screen while maintaining the aspect ratio
        frame = resize_frame_to_screen(frame, screen_width, screen_height)

        while True:
            # Display the image with color info
            cv2.rectangle(frame, (20, 20), (800, 60), (b, g, r), -1)
            text = (
                getColorName(b, g, r)
                + "   R="
                + str(r)
                + " G="
                + str(g)
                + " B="
                + str(b)
            )
            cv2.putText(frame, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            # Adjust text color for light backgrounds
            if r + g + b >= 600:
                cv2.putText(frame, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

            # Display the image
            cv2.imshow("image", frame)

            # Exit on pressing the 'Esc' key
            if cv2.waitKey(20) & 0xFF == 27:
                break

# If the user chooses to use the webcam
elif mode == "webcam":
    camera = cv2.VideoCapture(0)

    while True:
        # Capture frame from the webcam
        (grabbed, frame) = camera.read()

        # Resize the webcam frame to fit within both width and height constraints
        frame = resize_frame_to_screen(frame, screen_width, screen_height)

        # Draw a rectangle and display color information
        cv2.rectangle(frame, (20, 20), (800, 60), (b, g, r), -1)
        text = (
            getColorName(b, g, r) + "   R=" + str(r) + " G=" + str(g) + " B=" + str(b)
        )
        cv2.putText(frame, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # Adjust text color for light backgrounds
        if r + g + b >= 600:
            cv2.putText(frame, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        # Display the webcam feed
        cv2.imshow("image", frame)

        # Exit on pressing the 'Esc' key
        if cv2.waitKey(20) & 0xFF == 27:
            break

    # Release the camera and close windows
    camera.release()

# Cleanup
cv2.destroyAllWindows()
