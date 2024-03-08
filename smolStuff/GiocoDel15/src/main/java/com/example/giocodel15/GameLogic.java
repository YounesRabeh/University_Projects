package com.example.giocodel15;
import java.util.Random;

public class GameLogic {
    private final int RANDOMNESS = 1;
    private final int ROWS, COLS;
    int emptyX, emptyY;
    protected int[][] gridMatrix;

    public GameLogic(int rows, int columns) {
        this.ROWS = rows;
        this.COLS = columns;
        this.emptyX = ROWS - 1;
        this.emptyY = COLS - 1;
        gridMatrix = new int[ROWS][COLS];

    }

    protected void gridMatrixSetup(){
        int counter = 1;
        for (int row = 0; row < ROWS; row++) {
            for (int col = 0; col < COLS; col++) {
                if (!(row == ROWS - 1 && col == COLS - 1)) gridMatrix[row][col] = counter++;
            }
        }
        shuffle(gridMatrix, emptyX, emptyY, RANDOMNESS);
    }

    protected void move(int row, int col){
        int value = gridMatrix[row][col];

        if (next(gridMatrix, row, col)) {
            gridMatrix[emptyX][emptyY] = value;
            emptyX = row; emptyY = col;
            gridMatrix[row][col] = 0;
        }
    }

    private boolean next(int[][] gridMatrix, int row, int col) {
        // Define the indices of adjacent cells
        int[][] directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        // Iterate over adjacent cells
        for (int[] dir : directions) {
            int newRow = row + dir[0];
            int newCol = col + dir[1];
            // Check if the adjacent cell is within the bounds of the matrix
            if (newRow >= 0 && newRow < gridMatrix.length && newCol >= 0 && newCol < gridMatrix[0].length) {
                // Check if the adjacent cell value is 0
                if (gridMatrix[newRow][newCol] == 0) {
                    return true;
                }
            }
        }
        return false; // Return false if none of the adjacent cells are 0
    }

    private void shuffle(int[][] gridMatrix, int emptyRow, int emptyCol, int moves) {
        Random random = new Random();
        // Generate random moves and swap values with adjacent cells
        for (int i = 0; i < moves; i++) {
            // Generate a random direction (0: up, 1: down, 2: left, 3: right)
            int direction = random.nextInt(4);

            // Define the indices of adjacent cells
            int[][] directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
            int newRow = emptyRow + directions[direction][0];
            int newCol = emptyCol + directions[direction][1];

            // Check if the adjacent cell is within the bounds of the matrix
            if (newRow >= 0 && newRow < gridMatrix.length && newCol >= 0 && newCol < gridMatrix[0].length) {
                // Swap values with the adjacent cell
                int temp = gridMatrix[newRow][newCol];
                gridMatrix[newRow][newCol] = gridMatrix[emptyRow][emptyCol];
                gridMatrix[emptyRow][emptyCol] = temp;

                // Update the position of the empty cell
                emptyRow = newRow; emptyX = newRow;
                emptyCol = newCol; emptyY = newCol;
            }
        }
    }

    public boolean checkWin(){
        int counter = 1;
        for (int row = 0; row < ROWS; row++) {
            for (int col = 0; col < COLS; col++) {
                if (row == ROWS-1 && col == COLS-1) return true;
                if (gridMatrix[row][col] != counter) return false;
                counter++;
            }
        }
        System.out.println("return true 2");
        return true;
    }
}

