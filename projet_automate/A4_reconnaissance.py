def impasse(etat, parents=None):
    if parents is None:
        parents = set()
    elif etat in parents:
        return True

    # si on trouve un état terminal l'état n'est pas une impasse
    if etat.terminal:
        return False

    #  verifiez toutes les transitions sortantes, s'il y a au moins une non-impasse, cet etat n est pas une impasse
    for transition in etat.transition_0:
        if transition.etat_1 not in parents and not impasse(transition.etat_1, parents=parents.union({etat})):
            return False

    #  si tous les états sont des impasses, cet état est une impasse
    return True


def reconnaissance(automate):

    while True:
        mot = input("mot à tester (s pour continuer): ")

        # ferme la fonction si l'utilisateur entre le mot quitter
        if mot.lower() in ["suivant", "s", "suiv"]:
            break

        # demarrer avec un etat initial
        etats_actifs = automate.etats_initial

        for i, caractere in enumerate(mot):
            # prend une lettre dans l'alphabet qui correspond avec ce que l'utilisateur a tapé
            lettre = automate.alphabet.get_lettre(caractere)

            # si la lettre n'existe pas dans l'alphabet, le mot ne sera pas reconnu
            if lettre is None:
                etats_actifs = set()
                print("la lettre \"%s\" n'est pas dans l'alphabet." % caractere)
                break

            # pour chaque etat actif, trouver ceux qu'il active avec cette lettre et les stocker
            prochains_etats_actifs = set()
            for etat_actif in etats_actifs:
                for next_etat in etat_actif.obtention_etat_suiv(lettre):
                    prochains_etats_actifs.add(next_etat)

            # remplace les anciens etats actifs (au temps T) par les nouveaux (au temps T+1)
            etats_actifs = prochains_etats_actifs

            # si aucun etat actif ne presente de sortie, on est sur que l'automate ne sera pas reconnu et on s'arrete la
            for etat_actif in etats_actifs:
                if not impasse(etat_actif):
                    break
            else:
                break

        # si au moins un etat actif a la fin du mot est terminal, alors le mot sera reconnu
        for etat_actif in etats_actifs:
            if etat_actif.terminal:
                print("Le mot \"%s\" est reconnue par l'automate." % mot)
                break
        else:
            print("le mot \"%s\" , n'est pas reconnue par l'automate." % mot)
