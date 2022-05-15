
class Alphabet(object):

	def __init__(self, lettres=None):
		super(Alphabet, self).__init__()

		# On initialise l’objet avec les lettres reconnues par l’alphabet de l’automate
		self.lettres = lettres if lettres is not None else set()

	def copy(self):
		alphabet_copie = Alphabet()
		for lettre in self.lettres:
			lettre.copy(alphabet_copie)

	def get_lettre(self, caractere):
		for lettre in self.lettres:
			if lettre.caractere == caractere:
				return lettre

		return None
