from A4_determinisation import determiniser
from A4_completion import completer


def complement(automate, file=None):
	# Copier l’automate déterministe

	for etat in automate.etats:
		# Inverser les états terminal et non-terminal
		etat.terminal = not etat.terminal

		if etat.terminal:
			automate.etats_terminal.add(etat)
		else:
			automate.etats_terminal.remove(etat)

	return automate
