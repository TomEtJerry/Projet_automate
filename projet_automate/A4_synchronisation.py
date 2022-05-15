from A4_transition import Transition


def recup_epsilon(automate):
    for lettre in automate.alphabet.lettres:
        if lettre.epsilon:
            return lettre

    return None


# Retourne tous les états connectés avec une transition d’état vide
def recup_etats_asynchrones(etat, epsilon=None, parents=None):
    if parents is None:
        parents = set()
    elif etat in parents:
        return set()

    if epsilon is None:
        epsilon = recup_epsilon(etat.automate)
        if epsilon is None:  # Si abs de epsilon Alors abs de transition epsilon
            return set()

    etats_asynchrones = set()

    # Ajoute chaque état connecté avec une transition epsilon à un état asynchrone (se fait récursivement)
    for etat_asynchrones in etat.obtention_etat_suiv(epsilon):
        etats_asynchrones.add(etat_asynchrones)
        if etat_asynchrones not in parents:  # Permet d'éviter les boucles infinies
            etats_asynchrones.update(recup_etats_asynchrones(etat_asynchrones, parents.union({etat, })))

    return etats_asynchrones


def recup_recursivement_etat_suiv(etat, lettre, parents=None):
    if parents is None:
        parents = set()
    elif etat in parents:
        return set()

    etat_suiv = etat.obtention_etat_suiv(lettre)

    # Ajoute tous les états comportants des transitions "lettre" et "epsilon"
    for etat_suivant in etat_suiv.copy():
        etat_suiv.update(recup_etats_asynchrones(etat_suivant))

    # Trouve tous les états similaires (se fait récursivement)
    for etat_asynchrones in recup_etats_asynchrones(etat):
        if etat_asynchrones not in parents:  # Permet d'éviter les boucles infinies
            etat_suiv.update(recup_recursivement_etat_suiv(etat_asynchrones, lettre, parents.union({etat, })))

    return etat_suiv


# Cette fonction retourne true s’il y a une ou plusieurs transitions epsilon de n’importe quel état initial vers l’état donné
def epsilon_etat_initial(etat, parents=None):
    if etat.initial:
        return True
    if parents is None:
        parents = set()
    elif etat in parents:
        return False

    epsilon = recup_epsilon(etat.automate)
    if epsilon is None:  # Si abs de epsilon Alors abs de transition epsilon
        return

    for etat_asynchrones in etat.obtention_etat_precedent(epsilon):
        if etat_asynchrones not in parents and epsilon_etat_initial(etat_asynchrones, parents.union({etat, })):
            return True

    return False


# Cette fonction retourne true s’il y a une ou plusieurs transitions epsilon de l’état donné à n’importe quel état terminal
def epsilon_etat_terminal(etat, parents=None):
    if etat.terminal:
        return True
    if parents is None:
        parents = set()
    elif etat in parents:
        return False

    epsilon = recup_epsilon(etat.automate)
    if epsilon is None:  # Si abs de epsilon Alors abs de transition epsilon
        return

    for etat_asynchrones in etat.obtention_etat_suiv(epsilon):
        if etat_asynchrones not in parents and epsilon_etat_terminal(etat_asynchrones, parents.union({etat, })):
            return True

    return False


def synchroniser(automate, file=None):
    # Copie l’automate pour ne pas perdre les références de l'originel
    automate_synchrone = automate.copy()

    if not automate.est_un_automate_asynchrone(file=file):
        return automate

    # Trouve tous les symboles autres que epsilon
    lettres = []
    for lettre in automate_synchrone.alphabet.lettres:
        if not lettre.epsilon:
            lettres.append(lettre)

    for etat in automate_synchrone.etats:
        for lettre in lettres:
            # Pour chaque état, trouve ceux qui sont connectés via epsilon et ajoute une transition directe entre eux
            etat_suiv = recup_recursivement_etat_suiv(etat, lettre)
            etat_suiv -= etat.obtention_etat_suiv(lettre)

            for etat_suivant in etat_suiv:
                Transition(etat, etat_suivant, lettre)

        # Si l’état est connecté à un état initial via les transitions epsilon entrantes, le marque comme initial
        if epsilon_etat_initial(etat):
            etat.initial = True
            automate_synchrone.etats_initial.add(etat)

        # Si l’état est connecté à un état terminal via les transitions epsilon entrantes, le marque comme terminal
        if epsilon_etat_terminal(etat):
            etat.terminal = True
            automate_synchrone.etats_terminal.add(etat)

    # Supprime toutes les transitions epsilon
    for transition in automate_synchrone.transitions.copy():
        if transition.lettre.epsilon:
            transition.remove()

    return automate_synchrone
