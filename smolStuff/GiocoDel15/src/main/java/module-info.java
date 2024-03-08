module com.example.giocodel15 {
    requires javafx.controls;
    requires javafx.fxml;

    requires org.controlsfx.controls;
    requires net.synedra.validatorfx;

    opens com.example.giocodel15 to javafx.fxml;
    exports com.example.giocodel15;
}