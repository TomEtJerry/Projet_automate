package com.company;

import java.lang.reflect.Array;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

public class Automate {
    private final static char [] alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
    private final int nbr_symbole;
    private int nbr_etat;
    private int [] etat;
    private final int nbr_etat_init;
    private final int [] etat_init;
    private final int nbr_etat_fin;
    private final int [] etat_fin;
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
        int j;
        if (automate.nbr_etat_init > 1) {
            return false;
        }
        while(i< automate.getNbr_trans()){
            j=0;
            while(j< automate.getNbr_trans()){
                //si l'état et la lettre sont les mêmes alors non déterministe
                if(automate.getTransition()[i].charAt(0) == automate.getTransition()[j].charAt(0) && automate.getTransition()[i].charAt(1) == automate.getTransition()[j].charAt(1) && i != j){
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
        int j;
        int cpt;

        while (i< automate.getNbr_etat()){
            j=0;
            cpt = 0;
            while (j< automate.getNbr_trans()){
                if(automate.getTransition()[j].charAt(0) == automate.getEtat()[i]){
                    cpt += 1;
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

    public void completion() {
        this.nbr_etat += 1;
        String [] transition_C = new String[50];
        this.etat = new int[this.nbr_etat]; //tableau statique qui contient tout les etats avec l'etat poubelle en plus
        int e = 0;
        while(e<this.nbr_etat){
            this.etat[e] = e;
            e++;
        }
        this.etat[this.nbr_etat-1] = -1;  // Vérifier l'indice + modifier tableau d'entiers
        int i = 0;
        int j;
        int l;
        int k = 0; //k va s'incrementer pour le nouveau tableau de transition
        boolean test; //sert à savoir si la transition contient l'un des symbole
        int nbr_transition = this.nbr_trans;

        while(i < this.nbr_etat-1){
            j=0;
            while(j < nbr_symbole){
                l=0;
                test = false;
                while(l < nbr_transition){
                    if(this.etat[i] == Integer.parseInt(String.valueOf(this.transition[l].charAt(0))) && this.getAlphabet()[j] == this.transition[l].charAt(1)){
                        transition_C[k] = this.transition[l];
                        k++;
                        test = true;
                        break;
                    }
                    l++;
                }
                if(!test){
                    transition_C[k] = String.valueOf(i) + this.getAlphabet()[j] + "p";
                    k++;
                }
                j++;
            }
            i++;
        }
        j=0;
        while(j < nbr_symbole){
            transition_C[k] = "-1" + this.getAlphabet()[j] + "p";
            k++;
            j++;
        }

        this.nbr_trans = k;
        this.transition = transition_C;
    }


    public Automate determinisation(){
        int i = 0;
        //état initial
        //Concatène les états initiaux
        String letat_init_D = "";
        while(i < this.nbr_etat_init){
            letat_init_D += String.valueOf(this.etat_init[i]);
            i++;
        }
        int nbr_etat_init_D = 1;
        int [] etat_init_D = {Integer.parseInt(""+letat_init_D)};


        //états
        int nbr_etat_D = 1;
        int [] etat_D = new int[50];
        Arrays.fill(etat_D, -1);
        etat_D[0] = Integer.parseInt(letat_init_D); // premier etat qui est l'etat initial fait avant

        int nbr_trans_D = 0; // nouveau nbr de transitions
        String [] transition_D = new String[50]; // nouveau tableau de transition

        i = 0; // parcours le nouveau tableau d'état
        int j; // parcours
        int k; //
        int l;

        String nv_etat; // Contient le nouvel état d'arrivé (transition)
        while(etat_D[i] != -1){
            j=0;
            while(j < this.nbr_symbole){
                k=0;
                nv_etat = "";
                while (k < this.nbr_trans){
                    l=0;
                    while (l < String.valueOf(etat_D[i]).length()){
                        if(transition[k].charAt(0) == String.valueOf(etat_D[i]).charAt(l) && transition[k].charAt(1) == alphabet[j]){
                            nv_etat += transition[k].charAt(2);
                        }
                        l++;
                    }
                    k++;
                }
                if(!nv_etat.equals("") && !Arrays.toString(etat_D).contains(nv_etat)){
                    etat_D[nbr_etat_D] = Integer.parseInt(nv_etat);
                    nbr_etat_D += 1;
                    transition_D[nbr_trans_D] = String.valueOf(etat_D[i])+alphabet[j]+nv_etat;
                    nbr_trans_D += 1;
                }
                else if(!nv_etat.equals("")){
                    transition_D[nbr_trans_D] = String.valueOf(etat_D[i])+alphabet[j]+nv_etat;
                    nbr_trans_D += 1;
                }
                j++;
            }
            i++;
        }

        //etat finaux
        i = 0; //parcours des nouveaux état
        j = 0; // parcours des chiffres de l'état pour savoir si un d'eux est fina
        int nbr_etat_fin_D = 0;
        int [] temp = new int[50];

        while(i < nbr_etat_D){
            j=0;
            while (j < String.valueOf(etat_D[i]).length()){
                if (Arrays.toString(etat_fin).contains(String.valueOf(String.valueOf(etat_D[i]).charAt(j)))){ // si on trouve un des caracteres dans le tableau d'etat finaux de base, on met en sortie
                    temp[nbr_etat_fin_D] = etat_D[i];
                    nbr_etat_fin_D += 1;
                    break;
                }
                j++;
            }
            i++;
        }

        k=0; //remplissage du tableau d'etat finaux
        int [] etat_fin_D = new int[nbr_etat_fin_D];
        while(k < nbr_etat_fin_D){
            etat_fin_D[k] = temp[k];
            k++;
        }

        return new Automate(this.nbr_symbole, nbr_etat_D , etat_D, nbr_etat_init_D, etat_init_D, nbr_etat_fin_D, etat_fin_D, nbr_trans_D, transition_D);
    }
}
