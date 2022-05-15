import re

from A4_lettre import Lettre
from A4_alphabet import Alphabet
from A4_etat import Etat
from A4_transition import Transition

LETTRES = "abcdefghijklmnopqrstuvwxyz" # lettre de l'alphabet
ETATS = list(map(str, range(100))) # etat de base dans l'ordre croissant

class Automate(object):
	def __init__(self, alphabet=None, etats=None, transitions=None, etats_initial=None, etats_terminal=None):
		super(Automate, self).__init__()

		# On initialise l'objet
		self.alphabet = alphabet if alphabet is not None else Alphabet()
		self.etats = etats if etats is not None else set()
		self.transitions = transitions if transitions is not None else set()
		self.etats_initial = etats_initial if etats_initial is not None else set()
		self.etats_terminal = etats_terminal if etats_terminal is not None else set()

	def copy(self, alphabet=None):
		if alphabet is None:
			alphabet = self.alphabet

		automate_copie = Automate(alphabet)

		for etat in self.etats:
			etat.copy(automate_copie)

		for transition in self.transitions:
			transition.copy(automate_copie)

		return automate_copie

	def obtention_etat(self, numero_etat):
		for etat in self.etats:
			if etat.numero_etat == numero_etat:
				return etat

		return None

	# Pour verifier si un automate est asynchrone on regarde s'il a un * dans ses transitions
	def est_un_automate_asynchrone(self, file=None):
		for transition in sorted(self.transitions, key=lambda transition: (transition.etat_0.numero_etat, transition.etat_1.numero_etat, transition.lettre.caractere)): # sorted est une fonction qui construit une nouvelle liste trier depuis un itérable 
			if transition.lettre.epsilon:
				print("Cet automate est asynchrone.", file=file)
				return True

		print("Cet automate est synchrone.", file=file)
		return False

	def est_un_automate_deterministe(self, file=None):
		# Il doit y avoir maximum une seule entrée par etat
		if len(self.etats_initial) > 1:
			print("Cet automate est non-deterministe car il a %d états initiaux." % len(self.etats_initial), file=file)
			return False

		association = set()
		for transition in sorted(self.transitions, key=lambda transition: (transition.etat_0.numero_etat, transition.etat_1.numero_etat, transition.lettre.caractere)):
			membre = (transition.etat_0, transition.lettre)
			if membre in association: # Chaque pair de transition de l'automate doit d'être unique
				print("Cet automate n'est pas deterministe", file=file)
				return False

			association.add(membre)

		print("Cet automate est déterministe.", file=file)
		return True

	def est_un_automate_complet(self, file=None):
		association = set()

		for transition in self.transitions:
			if transition.lettre.epsilon: # Un automate complet doit etre synchrone
				print("Cet automate ne peut pas être compléter car il est asynchrone.", file=file)
				return False

			association.add((transition.etat_0, transition.lettre))

		cpt_lettre = 0
		for lettre in self.alphabet.lettres:
			if not lettre.epsilon:
				cpt_lettre += 1

		if len(association) >= len(self.etats) * cpt_lettre: 
			# Il doit y avoir au moins une pair (etat, lettre)
			print("Cet automate est complet.", file=file)
			return True
		else:
			print("Cet automate n'est pas complet", file=file)
			return False

	def afficher_automate(self, file=None):
		print("---Affichage---")
		# Affichage des lettres de l'alphabet sans epsilon
		lettres = []
		for lettre in self.alphabet.lettres:
			if not lettre.epsilon:
				lettres.append(lettre.caractere)
		lettres.sort()
		print("Alphabet:", *lettres, file=file) # * = espace

		# Affichage des etats initiaux
		etats_initial = []
		for etat in self.etats_initial:
			etats_initial.append(etat.numero_etat)
		etats_initial.sort()
		print("Etats initiaux:", *etats_initial, file=file)

		# Affichage des etats finaux
		etats_terminal = []
		for etat in self.etats_terminal:
			etats_terminal.append(etat.numero_etat)
		etats_terminal.sort()
		print("Etats terminaux : ", *etats_terminal, file=file)

		# affiche une table de transition
		print("Table de transition :", file=file)

		# on garde que les lettres qui sont utilisées
		lettres = []
		for lettre in self.alphabet.lettres: # on parcours les lettres de l'alphabet de l'automate
			for transition in self.transitions: #on parcours les transitions
				if transition.lettre == lettre:  # si la lettre est dans les transitions on l'ajoute, sinon on fait rien
					lettres.append(lettre)
					break

		# Calcul la largeur de chaques colonnes
		largeur_colonnes = [0] * (len(lettres) + 1) # largeur des colonnes en fonction des lettres
		for i, lettre in enumerate(sorted(lettres, key=lambda lettre: lettre.caractere)):
			largeur_colonnes[i + 1] = max(largeur_colonnes[i + 1], len(lettre.caractere))

		for etat in sorted(self.etats, key=lambda etat: etat.numero_etat):
			largeur_colonne = len(etat.numero_etat) # largeur des colonnes en fonction des etats ( colonne de gauche)
			if etat.initial or etat.terminal:
				largeur_colonne += 1
			if etat.initial:
				largeur_colonne += 1
			if etat.terminal:
				largeur_colonne += 1

			largeur_colonnes[0] = max(largeur_colonnes[0], largeur_colonne)
			for i, lettre in enumerate(sorted(lettres, key=lambda lettre: lettre.caractere)):
				etat_suiv = etat.obtention_etat_suiv(lettre)
				largeur_colonne = sum(map(lambda etat: len(etat.numero_etat), etat_suiv)) + len(etat_suiv) - 1
				largeur_colonnes[i + 1] = max(largeur_colonnes[i + 1], largeur_colonne)

		# Affiche le titre du tableau
		print("etat".center(largeur_colonnes[0] + 2), end="", file=file)
		for i, lettre in enumerate(sorted(lettres, key=lambda lettre: lettre.caractere)):
			print("|" + lettre.caractere.center(largeur_colonnes[i + 1] + 2), end="", file=file)
		print(file=file)
		print("-" * (largeur_colonnes[0] + 2), end="", file=file)
		for i in range(len(lettres)):
			print("-" + "-" * (largeur_colonnes[i + 1] + 2), end="", file=file)
		print(file=file)

		# Affiche chaque ligne (etat) de la table de transition
		for etat in sorted(self.etats, key=lambda etat: etat.numero_etat):
			en_tete_ligne = etat.numero_etat
			if etat.initial or etat.terminal:
				en_tete_ligne = " " + en_tete_ligne
			if etat.initial:
				en_tete_ligne = "->" + en_tete_ligne
			if etat.terminal:
				en_tete_ligne = "<-" + en_tete_ligne
			print(en_tete_ligne.center(largeur_colonnes[0] + 2), end="", file=file)

			for i, lettre in enumerate(sorted(lettres, key=lambda lettre: lettre.caractere)):
				etat_suiv = etat.obtention_etat_suiv(lettre)
				etat_suiv = " ".join(sorted(map(lambda etat: etat.numero_etat, etat_suiv)))
				print("|" + etat_suiv.center(largeur_colonnes[i + 1] + 2), end="", file=file)
			print(file=file)

	def lecture_automate(file=None):
		# Lis le contenue d'un fichier
		with open(file, "r") as f:
			longueur_alphabet = int(f.readline())
			compteur_etats = int(f.readline())

			nbr_etats_init = f.readline().split()
			nbr_etats_init = set(nbr_etats_init[1:]) #tab de string d'etat initiaux

			nbr_etats_fin = f.readline().split()
			nbr_etats_fin = set(nbr_etats_fin[1:]) #tab de string d'etat finaux

			compteur_transition = int(f.readline()) #nbr de transitions
			trans = [] # tab des transitions
			for i in range(compteur_transition):
				trans.append(f.readline()) # ajout de chaque transition

		# Crée un alphabet composé de chaque lettre + epsilon
		alphabet = Alphabet() # initialisation de l'alphabet vide

		for caractere in LETTRES[:longueur_alphabet]: #parcour des lettres de l'alphabet
			Lettre(alphabet, caractere) #ajout des lettre
		Lettre(alphabet, epsilon=True) # ajout d'epsilon

		# crée un premier automate vide 
		automate = Automate(alphabet)

		# Ajoute chacun des etats
		for numero_etat in ETATS[:compteur_etats]:
			initial = numero_etat in nbr_etats_init
			terminal = numero_etat in nbr_etats_fin
			Etat(automate, numero_etat, initial=initial, terminal=terminal)

		# Décode et ajoute chacune des transitions
		for i, trans in enumerate(trans):
			match = re.match(r"^(\d+)(\D+)(\d+)\n?$", trans) # \d+ nimporte quelle chiffre decial(en string), \D+ l'inverse
			if match:
				etat_0_id = match.group(1)
				caractere = match.group(2)
				etat_1_id = match.group(3)

				etat_0 = automate.obtention_etat(etat_0_id)
				etat_1 = automate.obtention_etat(etat_1_id)
				lettre = alphabet.get_lettre(caractere)

				Transition(etat_0, etat_1, lettre)
			else:
				raise Exception("Format invalide au niveau de la transition #%d: est attendu : numéro--caractéres--symbole dans la transition mais on a \"%s\"" % (i, trans))

		return automate
