import os
import re

from A4_automate import Automate
from A4_determinisation import determiniser
from A4_completion import completer
from A4_complementarisation import complement
from A4_reconnaissance import reconnaissance

FORMAT_FICHIER = "A4-%d.txt"


def main():
    automate_as = set()
    for file in os.listdir("."):
        match = re.match(FORMAT_FICHIER.replace(r"%d", r"(\d+)"), file)
        if match:
            automate_as.add(int(match.group(1)))

    automate_list = ", ".join(map(str, sorted(automate_as)))

    try:
        while True:  # boucle principal
            automate_id = None  # id de l'automate(numero de l'automate)
            while automate_id is None or automate_id not in automate_as:  # si le numero n'est pas bon, c'est le cas au debut, on fait la suite
                if automate_id is not None:  # si l'id n'est pas nul mais pas dans la liste d'automate
                    automate_id = input("Le numero est invalide, recommencez \n%s: \n" % automate_list)
                else:  # si l'id est nul, on affiche ça
                    automate_id = input(
                        "quel automate voulez-vous utiliser ? (q pour quitter) --> %s: \n" % automate_list)

                try:
                    automate_id = int(automate_id)  # si c'est bon, on transforme ce qu'a mis l'utilisateur en int
                except ValueError:
                    if automate_id.lower() in ["quit", "exit", "end", "q"]:  # commande pour quitter
                        break

            if not automate_id in automate_as:  # au cas ou
                break

            print()
            print("-Lecture et affichage de l'automate :")
            chemin_fichier = FORMAT_FICHIER % automate_id  # on remplace le numero de format fichier par celui du user
            automate = Automate.lecture_automate(chemin_fichier)
            automate.afficher_automate()

            print()
            reconnaissance(automate)

            print()
            print("-Determinisation :")
            automate = determiniser(automate)
            print()
            print("-Completion :")
            automate = completer(automate)
            print()
            print("-Apres determinisation et completion")
            automate.est_un_automate_asynchrone()
            automate.est_un_automate_deterministe()
            automate.est_un_automate_complet()
            print()
            automate.afficher_automate()

            print()
            reconnaissance(automate)

            print()
            print("-Langage complémentaire :")
            automate = complement(automate)
            automate.afficher_automate()

            print()
            reconnaissance(automate)

    except KeyboardInterrupt:
        print()
        pass

    print("Sortie...")


if __name__ == "__main__":
    main()
