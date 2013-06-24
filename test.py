__author__ = 'julien'

from Character import Character, CharacterDisplayer

oCharacter = Character()

oCharacter.setName('Daphnis Gavrial')
oCharacter.setAge(18)
oCharacter.setAgility(12)
oCharacter.setInstinct(18)
oCharacter.setStrength(15)
oCharacter.setCharism(14)
oCharacter.setStamina(16)
oCharacter.setWill(16)
oCharacter.setDiscernment(13)
oCharacter.setMental(17)
oCharacter.compute()
oCharacterDisplayer = CharacterDisplayer()

oCharacterDisplayer.setCharacter(oCharacter)
oCharacterDisplayer.display()
