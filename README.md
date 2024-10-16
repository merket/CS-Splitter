
# Character Sheet Splitter

This is a very basic script to split the photo grids, like character sheets, into smaller separate files. 



## Python Scripts

- SIMPLE.py script automatically detects any image files in the folder it has been run from and tries to split them into smaller pieces by edge and empty area detection. Starts from the top left goes towards bottom right. Then creates and Output (if it does not exist already) folder and puts every image with their original filename along with an incremental suffix. Works best with white backgrounds and / or white grids.

- Optional_Grid.py does the same but when run through the "Run_Optional_Grid.bat" it asks the user the source image's grid /bg colour and adjusts the detection threshold accordingly.

Available grid color options are;

    White
    Gray
    Black
    Red
    Green
    Blue
    Yellow




## Settings
Below is the main detection threshold settings. You can change the values for different results.
```
cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
```


## Example Character Sheet

![App Screenshot](https://raw.githubusercontent.com/merket/CS-Splitter/refs/heads/main/Example%20Character%20Sheet.png)


## Examples of Split Images

![App Screenshot](https://raw.githubusercontent.com/merket/CS-Splitter/refs/heads/main/split_images/ECS%20(10).png)
![App Screenshot](https://raw.githubusercontent.com/merket/CS-Splitter/refs/heads/main/split_images/ECS%20(3).png)


# How to use

1. Copy the files into the folder of the images you wish to split.
2. Shift + Right click to the folder window and select "Open PowerShell window"
3. Then type "python simple.py" and press enter. The script will detect all the images, split them and put them into a new folder called "split_images".
4. Optionally, if you have images with different grid colours than white, double click and run the "Run_Optional_Grid.bat" to be able to select the available grid / background colours.

Note: Try not to run the scripts from a folder with various coloured images or you will get undesired effects and files.

