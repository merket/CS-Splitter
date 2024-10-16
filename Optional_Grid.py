import os
import cv2
import numpy as np
import warnings
from PIL import Image

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module='cv2')

def get_threshold_values(color_choice):
    # Define threshold values based on the chosen grid color
    if color_choice == 1:  # White
        return 240, 255, cv2.THRESH_BINARY_INV
    elif color_choice == 2:  # Gray
        return None, None, cv2.THRESH_BINARY_INV  # Dynamic thresholding for gray
    elif color_choice == 3:  # Black
        return 40, 255, cv2.THRESH_BINARY
    elif color_choice == 4:  # Red
        return 100, 255, cv2.THRESH_BINARY_INV
    elif color_choice == 5:  # Green
        return 100, 255, cv2.THRESH_BINARY_INV
    elif color_choice == 6:  # Blue
        return 100, 255, cv2.THRESH_BINARY_INV
    elif color_choice == 7:  # Yellow
        return 200, 255, cv2.THRESH_BINARY_INV
    else:
        raise ValueError("Invalid color choice")

def calculate_dynamic_threshold(gray_image):
    # Calculate dynamic threshold based on the average pixel value
    average_value = np.mean(gray_image)
    threshold_value = int(average_value * 0.8)  # Set threshold at 80% of average
    return threshold_value

def split_image(image_path, output_folder, threshold_value, max_value, threshold_type):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use dynamic thresholding for gray
    if threshold_value is None:
        threshold_value = calculate_dynamic_threshold(gray)

    # Apply a threshold to create a binary image
    _, thresh = cv2.threshold(gray, threshold_value, max_value, threshold_type)

    # Morphological operations to enhance contours
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.dilate(thresh, kernel, iterations=1)

    # Find contours of the images
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours from left to right, then top to bottom
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])
    rectangles = [cv2.boundingRect(c) for c in contours]

    # Create output images from detected rectangles
    for i, (x, y, w, h) in enumerate(rectangles):
        # Set a minimum crop size based on area
        if w >= 50 and h >= 50:  # Adjust minimum size if needed
            cropped_image = image[y:y+h, x:x+w]

            # Save the cropped image
            output_path = os.path.join(output_folder, f"{os.path.basename(image_path).split('.')[0]}_{i + 1}.png")
            cv2.imwrite(output_path, cropped_image)

def extract_prompt(image_path):
    # Open the image file to extract metadata
    try:
        with Image.open(image_path) as img:
            # Extract metadata
            metadata = img.info.get("parameters", None)
            if metadata is None:
                metadata = img.info.get("text", "No prompt found.")
                if metadata == "No prompt found.":
                    # Print the entire metadata for debugging
                    print(f"Metadata for {image_path}: {img.info}")
            return metadata
    except Exception as e:
        print(f"Error reading metadata from {image_path}: {e}")
        return "Error reading metadata."

def main():
    # Get the current directory
    current_dir = os.getcwd()

    # Create a directory for output images
    output_dir = os.path.join(current_dir, "split_images")
    os.makedirs(output_dir, exist_ok=True)

    # Supported image formats
    supported_formats = (".png", ".jpg", ".jpeg", ".bmp")

    # Prompt user for grid color choice
    print("Select a grid color:")
    print("1. White")
    print("2. Gray")
    print("3. Black")
    print("4. Red")
    print("5. Green")
    print("6. Blue")
    print("7. Yellow")

    try:
        color_choice = int(input("Enter the number corresponding to your choice: "))
        threshold_value, max_value, threshold_type = get_threshold_values(color_choice)
    except (ValueError, IndexError):
        print("Invalid choice. Please run the script again and select a valid option.")
        return

    # List to store prompts for all processed images
    prompts = []

    # Process each image file in the current directory
    for filename in os.listdir(current_dir):
        if filename.lower().endswith(supported_formats):
            image_path = os.path.join(current_dir, filename)
            split_image(image_path, output_dir, threshold_value, max_value, threshold_type)
            prompt = extract_prompt(image_path)
            prompts.append(f"{os.path.basename(image_path)}: {prompt}")

    # Write all prompts to a single text file
    prompts_file_path = os.path.join(output_dir, "prompts.txt")
    with open(prompts_file_path, "w", encoding="utf-8") as f:
        for prompt in prompts:
            f.write(prompt + "\n")

    print(f'Prompts extracted to {prompts_file_path}')

if __name__ == "__main__":
    main()
