SIMPLE.py script automatically detects any image files in the folder it has been run from and tries to split them into smaller pieces by edge and empty area detection. Starts from the top left goes towards bottom right. Then creates and Output (if it does not exist already) folder and puts every image with their original filename along with an incremental suffix. Works best with white backgrounds and / or white grids.

Optional_Grid.py does the same but when run through the "Run_Optional_Grid.bat" it asks the user the source image's grid /bg  colour and adjusts the detection threshold accordingly.

Available grid color options are;
1. White
2. Gray
3. Black
4. Red
5. Green
6. Blue
7. Yellow
