__author__ = 'julien'

from Character import Character, CharacterDisplayer

oCharacter = Character()

oCharacter.setName('Daphnis Gavrial')
oCharacter.setAge(18)
oCharacter.setAgility(8)
oCharacter.setInstinct(11)
oCharacter.setStrength(15)
oCharacter.setCharism(15)
oCharacter.setStamina(13)
oCharacter.setWill(13)
oCharacter.setDiscernment(14)
oCharacter.setMental(12)
oCharacter.setStarModificator('Book', 1)
oCharacter.compute()
oCharacterDisplayer = CharacterDisplayer()

oCharacterDisplayer.setCharacter(oCharacter)
oCharacterDisplayer.display()
