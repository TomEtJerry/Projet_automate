
class Lettre(object):

	def __init__(self, alphabet, caractere=None, epsilon=None):
		super(Lettre, self).__init__()

		# On initialise l'objet avec la structure suivante:
		# l'alphabet auquel appartient cette lettre,
		# si cette lettre est une transition epsilon(asynchrone),
		# le caractere representant cette lettre (une chaine de longueur 1)
		self.alphabet = alphabet
		self.epsilon = epsilon if epsilon is not None else (caractere == "*")
		self.caractere = caractere if caractere is not None else "*" if self.epsilon else None

		self.alphabet.lettres.add(self)

	def copy(self, alphabet=None):
		if alphabet is None:
			alphabet = self.alphabet

		return Lettre(alphabet, self.caractere, self.epsilon)
