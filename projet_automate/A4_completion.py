
from A4_etat import Etat
from A4_transition import Transition
from A4_synchronisation import synchroniser


def completer(automate, file=None):
	# Copier l’automate synchrone
	automate = synchroniser(automate, file=file)

	if automate.est_un_automate_complet(file=file):
		return automate

	# Création de l'etat poubelle necessaire a la completion
	etat_poubelle = Etat(automate, "P")

	for etat in automate.etats:
		# Pour chaque état, trouver les lettres qui n’ont pas de transition sortante 
		transition_sortante = set()
		for transition in etat.transition_0.copy():
			transition_sortante.add(transition.lettre)

		# Ajouter une transition à l’état de la corbeille pour chaque transition manquante, sauf celles d’epsilon
		for lettre in set(automate.alphabet.lettres) - transition_sortante:
			if not lettre.epsilon:
				Transition(etat, etat_poubelle, lettre)

	return automate
