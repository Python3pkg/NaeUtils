__author__ = 'julien'

from Character import Character, CharacterDisplayer

oCharacter = Character()

oCharacter.setAgility(43)
oCharacter.setName('Toto')
oCharacter.setAge(18)

oCharacterDisplayer = CharacterDisplayer()

oCharacterDisplayer.setCharacter(oCharacter)
oCharacterDisplayer.display()
