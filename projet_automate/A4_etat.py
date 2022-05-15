
class Etat(object):

	def __init__(self, automate, numero_etat, initial=False, terminal=False):
		super(Etat, self).__init__()

		# Initialisation de l'objet selon la structure:
		self.automate = automate
		self.numero_etat = numero_etat
		self.transition_0 = set()
		self.transition_1 = set()
		self.initial = initial
		self.terminal = terminal

		self.automate.etats.add(self)
		if initial:
			self.automate.etats_initial.add(self)
		if terminal:
			self.automate.etats_terminal.add(self)

	def copy(self, automate=None):
		if automate is None:
			automate = self.automate

		return Etat(automate, self.numero_etat, self.initial, self.terminal)

	# Fonction pour éliminer un état (transitions, présence dans la liste (init, fin) si nécessaire.
	def remove(self):
		for transition in self.transition_0.copy():
			transition.remove()

		for transition in self.transition_1.copy():
			transition.remove()

		self.automate.etats.remove(self)
		if self.initial:
			self.automate.etats_initial.remove(self)
		if self.terminal:
			self.automate.etats_terminal.remove(self)

	# Passe par toutes les transitions sortantes et renvoie les destinations des transitions avec la lettre correspondante
	def obtention_etat_suiv(self, lettre):
		etat_suiv = set()

		for transition in self.transition_0:
			if transition.lettre == lettre:
				etat_suiv.add(transition.etat_1)

		return etat_suiv

	# Parcourt toutes les transitions entrantes et renvoie les origines des transitions avec la lettre correspondante
	def obtention_etat_precedent(self, lettre):
		etat_suiv = set()

		for transition in self.transition_1:
			if transition.lettre == lettre:
				etat_suiv.add(transition.etat_0)

		return etat_suiv
