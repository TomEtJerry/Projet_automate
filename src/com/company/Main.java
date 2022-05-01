package com.company;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Scanner;
public class Main {

    public static void main(String[] args) throws IOException {
        Automate automate = Automate_affichage.lecture("automate_test.txt");
        int i=0;
        Automate_affichage.afficher_automate(automate);
        System.out.println(Automate.Test_asynchrone(automate));
        System.out.println(Automate.Test_determinisation(automate));
        System.out.println(Automate.Test_completion(automate));
        //Automate_affichage.afficher_automate(Automate.Completion(automate));
    }
}