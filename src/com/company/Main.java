package com.company;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) throws FileNotFoundException {
        Automate automate = Automate_affichage.lecture("automate_test.txt");
        Automate_affichage.afficher_automate(automate);
        System.out.println(Automate.Test_determinisation(automate));
        Automate auto_det = automate.determinisation();
        System.out.println(auto_det.getTransition()[1]);



        //Automate_affichage.afficher_automate(Automate.Completion(automate));
    }
}
