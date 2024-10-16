import cv2
import os
import numpy as np

def split_image(image_path, output_folder):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply a threshold to create a binary image
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

    # Find contours of the images
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours from left to right, then top to bottom
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])
    rectangles = [cv2.boundingRect(c) for c in contours]

    # Create output images from detected rectangles
    for i, (x, y, w, h) in enumerate(rectangles):
        cropped_image = image[y:y+h, x:x+w]

        # Save the cropped image
        output_path = os.path.join(output_folder, f"{os.path.basename(image_path).split('.')[0]}_{i + 1}.png")
        cv2.imwrite(output_path, cropped_image)

def main():
    # Get the current directory
    current_dir = os.getcwd()

    # Create a directory for output images
    output_dir = os.path.join(current_dir, "split_images")
    os.makedirs(output_dir, exist_ok=True)

    # Supported image formats
    supported_formats = (".png", ".jpg", ".jpeg", ".bmp")

    # Process each image file in the current directory
    for filename in os.listdir(current_dir):
        if filename.lower().endswith(supported_formats):
            image_path = os.path.join(current_dir, filename)
            split_image(image_path, output_dir)

if __name__ == "__main__":
    main()
