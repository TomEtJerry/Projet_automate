
class Transition(object):

	def __init__(self, etat_0, etat_1, lettre):
		super(Transition, self).__init__()

		# Initialisation l'objet avec la structure suivante:
		self.etat_0 = etat_0
		self.etat_1 = etat_1
		self.lettre = lettre

		# L’origine et la cible doivent appartenir au même automate
		assert self.etat_0.automate == self.etat_1.automate

		self.etat_0.automate.transitions.add(self)
		self.etat_0.transition_0.add(self)
		self.etat_1.transition_1.add(self)

	def copy(self, automate=None):
		if automate is None:
			automate = self.automate

		etat_0_copie = automate.obtention_etat(self.etat_0.numero_etat)
		etat_1_copie = automate.obtention_etat(self.etat_1.numero_etat)
		lettre_copie = automate.alphabet.get_lettre(self.lettre.caractere)

		return Transition(etat_0_copie, etat_1_copie, lettre_copie)

	def remove(self):
		self.etat_0.automate.transitions.remove(self)
		self.etat_0.transition_0.remove(self)
		self.etat_1.transition_1.remove(self)
