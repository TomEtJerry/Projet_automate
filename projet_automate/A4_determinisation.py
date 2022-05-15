
from A4_automate import Automate
from A4_etat import Etat
from A4_transition import Transition
from A4_synchronisation import synchroniser

def determiniser(automate, file=None):
	# Copier l’automate synchrone
	automate = synchroniser(automate, file=file)

	if automate.est_un_automate_deterministe(file=file):
		return automate

	# Créer un nouvel automate
	determiniser_automate = Automate(automate.alphabet)
	pour_traitement = [(None, None, automate.etats_initial)]

	# Commence par regrouper tout les noeuds d'entrées puis regroupe chaque destination de cet état et recommence 
	while pour_traitement:
		depuis_etat, depuis_lettre, traitement = pour_traitement.pop(0)
		nouv_etat_num = ",".join(sorted(map(lambda etat: etat.numero_etat, traitement)))

		# Créer un nouvel état unique à partir de la liste des états précédents
		nouv_etat = determiniser_automate.obtention_etat(nouv_etat_num)
		traiter = True
		if nouv_etat is None:
			traiter = False
			nouv_etat = Etat(determiniser_automate, nouv_etat_num)

		# transition entrante
		if depuis_etat is not None and depuis_lettre is not None:
			Transition(depuis_etat, nouv_etat, depuis_lettre)
		else:
			nouv_etat.initial = True
			determiniser_automate.etats_initial.add(nouv_etat)

		# Si ce nouveau statut "groupe" vient d’être créé, analysez ses transitions sortantes
		if traiter:
			continue

		# Stockez toutes les transitions dans un dico {[lettre] : set([transition])}
		nouv_transition = {}
		for etat in traitement:
			# Si au moins un des états précédents du groupe est terminal, le groupe est terminal
			if etat.terminal:
				nouv_etat.terminal = True
				determiniser_automate.etats_terminal.add(nouv_etat)

			# Pour chaque état précédent dans le groupe, et chaque transition de ces états, stockez-les dans le dictionnaire
			for transition in etat.transition_0:
				if transition.lettre not in nouv_transition:
					nouv_transition[transition.lettre] = set()

				nouv_transition[transition.lettre].add(transition.etat_1)

		#  A partir du dictionnaire, reconstruisez les groupes qui doivent être faits et ajoutez-les au tableau en attente
		for lettre, etat_suiv in nouv_transition.items():
			pour_traitement.append((nouv_etat, lettre, etat_suiv))

	return determiniser_automate
