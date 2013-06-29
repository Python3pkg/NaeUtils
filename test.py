__author__ = 'julien'

from Character import Character, CharacterDisplayer
from Database import CharacterSaver

oCharacter = Character()

oCharacter.setName('Daphnis Gavrial')
oCharacter.setAge(18)
oCharacter.setType('pnj')
oCharacter.setAgility(8)
oCharacter.setInstinct(11)
oCharacter.setStrength(15)
oCharacter.setCharism(15)
oCharacter.setStamina(13)
oCharacter.setWill(13)
oCharacter.setDiscernment(14)
oCharacter.setMental(12)
oCharacter.setStarModificator('Book', 0)

oCharacter.addMoney(20)
oCharacter.compute()
oCharacterDisplayer = CharacterDisplayer()

oCharacterDisplayer.setCharacter(oCharacter)

oSaver = CharacterSaver()
oSaver.save(oCharacter)

oCharacterDisplayer.display()
