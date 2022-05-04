package com.company;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class Automate {
    private final static char [] alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
    private int nbr_symbole;
    private int nbr_etat;
    private int [] etat;
    private int nbr_etat_init;
    private int [] etat_init;
    private int nbr_etat_fin;
    private int [] etat_fin;
    private int nbr_trans;
    private String [] transition;

    public char[] getAlphabet() {
        return alphabet;
    }

    public int getNbr_etat() {
        return nbr_etat;
    }

    public int getNbr_symbole() {
        return nbr_symbole;
    }

    public String[] getTransition() {
        return transition;
    }

    public int[] getEtat() {
        return etat;
    }

    public int getNbr_etat_fin() {
        return nbr_etat_fin;
    }

    public int getNbr_etat_init() {
        return nbr_etat_init;
    }

    public int[] getEtat_fin() {
        return etat_fin;
    }

    public int[] getEtat_init() {
        return etat_init;
    }

    public int getNbr_trans() {
        return nbr_trans;
    }

    public Automate(int nbr_symbole, int nbr_etat, int [] etat, int nbr_etat_init, int[] etat_init, int nbr_etat_fin, int[] etat_fin, int nbr_trans,  String[] transition){
        this.nbr_symbole = nbr_symbole;
        this.nbr_etat = nbr_etat;
        this.etat = etat;
        this.nbr_etat_init = nbr_etat_init;
        this.etat_init = etat_init;
        this.nbr_etat_fin = nbr_etat_fin;
        this.etat_fin = etat_fin;
        this.transition = transition;
        this.nbr_trans = nbr_trans;
    }

    public static boolean Test_asynchrone(Automate automate){
        int k=0;
        while(k<automate.getNbr_trans()){
            if(automate.getTransition()[k].charAt(1) == '*') {
                return true;
            }
            k++;
        }
        return false;
    }

    public static boolean Test_determinisation(Automate automate){
        int i=0;
        int j=1;
        if (automate.nbr_etat_init > 1) {
            return false;
        }
        while(i< automate.getNbr_trans()){
            j = i + 1;
            while(j< automate.getNbr_trans()){
                //si l'état et la lettre sont les mêmes alors non déterministe
                if(automate.getTransition()[i].charAt(0) == automate.getTransition()[j].charAt(0) && automate.getAlphabet()[i] == automate.getAlphabet()[j]){
                    return false;
                }
                j++;
            }
            i++;
        }
        return true;
    }

    public static boolean Test_completion(Automate automate){
        int i = 0;
        int j = 1;
        int cpt = 0;
        // i et j comptent le nombre de fois qu'il y a un état
        while (i< automate.getNbr_trans()){
            j = i + 1;
            while (j< automate.getNbr_trans()){
                if(automate.getTransition()[i].charAt(0) == automate.getTransition()[j].charAt(0)){
                    cpt++;
                }
                j++;
            }
            // compare le nombre de fois qu'il y a un état avec le nombre de symbole (car déterministe)
            if(cpt != automate.nbr_symbole){
                return false;
            }
            i++;
        }
        return true;
    }

    public static Automate Completion(Automate automate) {
        automate.nbr_symbole += 1;
        automate.nbr_etat += 1;
        String [] transition_C = new String[50];
        automate.etat = new int[automate.nbr_etat]; //tableau statique qui contient tout les etats
        int e = 0;
        while(e<automate.nbr_etat){
            automate.etat[e] = e;
            e++;
        }
        automate.etat[automate.nbr_etat-1] = 0;  // Vérifier l'indice + modifier tableau d'entiers
        int i = 0;
        int j = 0;
        char[] alpha = automate.getAlphabet();
        char x;
        // Parcours les états
        while (i < automate.getNbr_trans()) {
            //Parcours les symboles
            while (j < automate.getNbr_symbole()) {
                x = alpha[j];
                // Si l'état possède une transition avec ce symbole ajouter au string sinon créer et ajouter
                if (automate.getTransition()[i].charAt(1) == x) {
                    transition_C[j] = String.valueOf(automate.getTransition()[i].charAt(1) + x + automate.getTransition()[i].charAt(2));
                } else {
                    automate.nbr_trans++;
                    transition_C[j] = String.valueOf(automate.getTransition()[i].charAt(1) + x + "p");
                }
                j++;
            }
            i++;
        }
        return new Automate(automate.nbr_symbole, automate.nbr_etat, automate.etat, automate.nbr_etat_init, automate.etat_init, automate.nbr_etat_fin, automate.etat_fin, automate.nbr_trans,  transition_C);
    }


    public static Automate Determinisation(Automate automate){
        int i = 1;
        //état initial
            //Concatène les états initiaux
        String letat_init_D = String.valueOf(automate.etat_init[0]);
        while(i< automate.nbr_etat_init){
            letat_init_D += automate.etat_init[i];
        }
        int nbr_etat_init_D = 1;
        int [] etat_init_D = new int[0];
        etat_init_D[0] = Integer.parseInt(letat_init_D);

        //états
        String nv_etat = ""; // Contient le nouvel état d'arrivé (transition)
        int nbr_etat_C = 1;
        int [] etat_D = new int[50];
        String [] transition_D = new String[50];
        etat_D[0] = Integer.parseInt(letat_init_D);
        transition_D[0]= letat_init_D; //Premier état
        int t = 0; // Parcours le nouveau tableau d'états (compare)
        int k; // Parcours le nouvel état (chaine de caractère en tableau)
        int a; // Parcours l'alphabet
        int u; // Parcours l'ancien tableau de transition
        int s = 0; // Parcours l'ancienne transition (chaine de caractère en tableau)
        int nbr_trans_D = 0; // Parcours le nouveau tableau de transition
        while (transition_D[t] != null){
            k =0;
            while ( k < String.valueOf(etat_D[t]).length()){ // Taille de l'état à parcourir
                u = 0;
                while (u < automate.getNbr_trans()){
                    a = 0;
                    while (a < automate.nbr_symbole){
                        if (automate.getTransition()[u].charAt(0) == String.valueOf(etat_D[t]).charAt(k)){
                            if (automate.getTransition()[u].charAt(1) == automate.getAlphabet()[a]){
                                nv_etat += automate.getTransition()[u].charAt(2);
                                transition_D[nbr_trans_D] = etat_D[t] + automate.getAlphabet()[a] + nv_etat; // Nouvelle transition
                                nbr_trans_D++;
                            }
                        }
                        a++;
                    }
                    etat_D[nbr_etat_C] = Integer.parseInt(nv_etat);
                    nv_etat = "";
                    a = 0;
                    nbr_etat_C++;
                    u++;
                }
                k++;
            }
            t++;
        }

        //Etats finaux
        int nbr_etat_fin_D = 0;
        int [] etat_fin_D = new int[50];
        int v = 0; // Parcours le nouveau tableau des états finaux (comparer)
        int c; // Parcours l'ancien tableau des états finaux
        t = 0;
        int comp; // Savoir si la valeur est dans le tableau
        while (transition_D[t] != null){
            k = 0;
            while ( k < String.valueOf(etat_D[t]).length()){
                c = 0;
                while(c < automate.etat_fin.length){
                    if(String.valueOf(etat_D[t]).charAt(k) == automate.etat_fin[c]){
                        comp = 0;
                        while(etat_fin_D[v] != 0){ // Verifie que l'état n'est pas déjà dans le tableau
                            if (etat_fin_D[v] == etat_D[t]){
                                comp ++;
                            }
                            v++;
                        }
                        if (comp == 0){
                            etat_fin_D[nbr_etat_fin_D] = etat_D[t];
                            nbr_etat_fin_D ++;
                        }
                    }
                    c++;
                }
                k++;
            }
            t++;
        }

        return new Automate(automate.nbr_symbole,nbr_etat_C , etat_D, nbr_etat_init_D, etat_init_D, nbr_etat_fin_D, etat_fin_D, nbr_trans_D, transition_D) ;
    }
}
