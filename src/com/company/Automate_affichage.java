package com.company;
import javax.swing.*;
import java.io.*;
import java.util.Scanner;

public class Automate_affichage {
    public static Automate lecture(String nom_fichier) throws FileNotFoundException {
        int i; //pour les boucles

        // ouverture du fichier + creation du scanner
        FileInputStream file = new FileInputStream(nom_fichier);
        Scanner scanner = new Scanner(file);

        //variable avec toutes les composantes de l'automate
        int nbr_symbole = Integer.parseInt(scanner.nextLine()); //ligne 1, nextline passe a la suivante
        int nbr_etat = Integer.parseInt(scanner.nextLine());
        int [] etat = new int[nbr_etat]; //tableau statique qui contient tout les etats
        //remplissage du tableau :
        i = 0;
        while(i<nbr_etat){
            etat[i] = i;
            i++;
        }
        int nbr_etat_init = Integer.parseInt(scanner.next()); //recuperation du nombre d'etats initiaux
        int [] etat_init = new int[nbr_etat_init];
        //remplissage
        i = 0;
        while(i<nbr_etat_init){
            etat_init[i] = Integer.parseInt(scanner.next());
            i++;
        }
        int nbr_etat_fin = Integer.parseInt(scanner.next()); //recuperation du nombre d'etats finaux
        int [] etat_fin = new int[nbr_etat_init];
        //remplissage
        i = 0;
        while(i<nbr_etat_fin){
            etat_fin[i] = Integer.parseInt(scanner.next());
            i++;
        }
        int nbr_trans = Integer.parseInt(scanner.next()); //nbr de transition
        //remplissage du tableau des transitions
        i=0;
        String [] transition = new String[50];
        while(i<nbr_trans){
            transition[i] = scanner.next();
            i++;
        }
        scanner.close();

        //creation de l'automate
        return new Automate(nbr_symbole, nbr_etat, etat, nbr_etat_init, etat_init, nbr_etat_fin, etat_fin, nbr_trans, transition);
    }

    public static void afficher_automate(Automate automate){
        int i=0;
        int j;
        int k;
        char [] alpha = automate.getAlphabet();
        //premiere ligne avec les transitions
        System.out.print("          etat      ");
        while(i<automate.getNbr_symbole()){
            System.out.print(alpha[i]+"         ");
            i++;
        }
        System.out.print("epsilon"); //rajout d'epsilon à la fin, seulement si automate asynchrone(a faire plus tard)
        System.out.print("\n");
        //les ligne suivantes
        i=0;
        String ES;
        while(i<automate.getNbr_etat()){ //boucle pour toutes les lignes
            ES = ""; //variable qui va contenir le fait que l'etat est une entré ou sortie
            // TEST DES ENTREE SORTIE EN COMPARANT AU TABLEAU DE CHACUN
            for (int value: automate.getEtat_init()) {
                if(value==automate.getEtat()[i]){
                    ES += "E";
                    break;
                }
            }
            for (int value: automate.getEtat_fin()) {
                if(value==automate.getEtat()[i]){
                    ES+="S";
                    break;
                }
            }
            if(ES.equals("ES")){
                System.out.print(ES+"        ");
            }
            else if(ES.equals("E") || ES.equals("S")){
                System.out.print(ES+"         ");
            }
            else{
                System.out.print("          ");
            }
            // FIN DES TEST ENTREE SORTIE

            //COLONNE ETAT - ATTENTION : Marche seulement si c'est entre 0 et 9, au dessus ça decalera d'un car un espace en trop
            System.out.print(automate.getEtat()[i]+"         ");

            // LES TRANSITIONS
            j = 0;
            String trans;
            String epsilon = "";
            while(j<automate.getNbr_symbole()){ // boucle pour faire tout les symbole  de l'alphabet
                trans = "";
                k=0;
                while(k<automate.getNbr_trans()) { // boucle qui va parcourir les transitions et tester si on ajoute à la table la transition
                    //si le caractere  du milieu = le symbole de la colonne et si l'etat correspond à l'etat de la ligne alors on l'ajouteà la case
                    if(automate.getTransition()[k].charAt(1) == automate.getAlphabet()[j] && Integer.parseInt(String.valueOf((automate.getTransition()[k].charAt(0)))) == automate.getEtat()[i]){
                        trans += automate.getTransition()[k].charAt(2);
                    }
                    else if(automate.getTransition()[k].charAt(1) == '*' && Integer.parseInt(String.valueOf((automate.getTransition()[k].charAt(0)))) == automate.getEtat()[i] && j == 0) {
                        epsilon += automate.getTransition()[k].charAt(2);
                    } // pour Epsilone, ATTENTION : repetition de la transition a cause de la boucle
                    k++;
                }

                switch (trans.length()) { //print des transition
                    case 0 -> System.out.print("-         ");
                    case 1 -> System.out.print(trans + "         ");
                    case 2 -> System.out.print(trans + "        ");
                    case 3 -> System.out.print(trans + "       ");
                    case 4 -> System.out.print(trans + "      ");
                    case 5 -> System.out.print(trans + "     ");
                }
                j++;
            }

            if(epsilon.equals("")) {
                System.out.print("-"); //print si pas de transition epsilon
            }
            else{
                System.out.print(epsilon); //print des transition epsilon
            }

            System.out.print("\n");
            i++;
        }
    }

}
