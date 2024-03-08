package com.example.giocodel15;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.Priority;
import javafx.stage.Stage;

public class Game15Grid extends Application {
    //APP CONSTANTS:
    final int ROWS = 4;
    final int COLS = 4;
    GameLogic gameLogic = new GameLogic(ROWS, COLS);
    GridPane gridPane = new GridPane();
    Scene scene = new Scene(gridPane, 400, 400);


    @Override
    public void start(Stage primaryStage) {
        // BACK-END:
        gameLogic.gridMatrixSetup();
        // GRID:
        gridSetup(gridPane);
        // SCENE:
        scene.getStylesheets().add(getClass().getResource("Styles.css").toExternalForm());
        primaryStage.setScene(scene);
        stageSetup(primaryStage);
        primaryStage.show();
    }

    private void gridSetup(GridPane gridPane){
        gridPane.setPadding(new Insets(10));
        gridPane.setHgap(5); gridPane.setVgap(5);

        for (int row = 0; row < ROWS; row++) {
            for (int col = 0; col < COLS; col++) {
                Button button = new Button();
                button.setMinSize(100, 100); // Set button size
                button.setMaxSize(Double.MAX_VALUE, Double.MAX_VALUE); // Make button resizable with grid
                GridPane.setRowIndex(button, row); GridPane.setColumnIndex(button, col);
                GridPane.setHgrow(button, Priority.ALWAYS); GridPane.setVgrow(button, Priority.ALWAYS);
                if (gameLogic.gridMatrix[row][col] == 0) { button.setOpacity(0);}
                button.setText(String.valueOf(gameLogic.gridMatrix[row][col]));
                button.setText(String.valueOf(gameLogic.gridMatrix[row][col]));
                button.setOnAction(event -> printButtonNumber(button));
                button.setFocusTraversable(false);
                gridPane.getChildren().add(button);
            }
        }
    }

    private void stageSetup(Stage stage){
        stage.setTitle("Gioco Del 15");
        stage.setMinWidth(500);
        stage.setMinHeight(500);
    }

    // FUNCTIONS:
    private void printButtonNumber(Button button) {
        gameLogic.move(GridPane.getRowIndex(button), GridPane.getColumnIndex(button));
        gridPane.getChildren().clear();
        gridSetup(gridPane);

        if (gameLogic.checkWin()) {
            winScreen();
        }


    }

    private void winScreen() {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle("Congratulations");
        alert.setHeaderText(null);
        alert.setContentText("You have won the game!");
        alert.showAndWait();
    }

    // DRIVER CODE:
    public static void main(String[] args) {
        launch(args);
    }
}
