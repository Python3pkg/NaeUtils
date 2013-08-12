__author__ = 'julien'

from Entities import Character, CharacterDisplayer
from Database import CharacterDatabase

oCharacter = Character()
#
#oCharacter.setName('Daphnis Gavrial')
#oCharacter.setAge(18)
#oCharacter.setType('pnj')
#oCharacter.setAgility(8)
#oCharacter.setInstinct(11)
#oCharacter.setStrength(15)
#oCharacter.setCharism(15)
#oCharacter.setStamina(13)
#oCharacter.setWill(13)
#oCharacter.setDiscernment(14)
#oCharacter.setMental(12)
#oCharacter.setStarModificator('Book', 0)
#
#oCharacter.addMoney(20)
#oCharacter.compute()

oCharacter.setName('Syrinielle Turionne')
oCharacter.setAge(17)
oCharacter.setType('pj')
oCharacter.setAgility(10)
oCharacter.setInstinct(9)
oCharacter.setStrength(8)
oCharacter.setCharism(15)
oCharacter.setStamina(14)
oCharacter.setWill(13)
oCharacter.setDiscernment(14)
oCharacter.setMental(15)
#oCharacter.setStarModificator('Book', 0)

oCharacter.addMoney(20)
oCharacter.compute()

oSaver = CharacterDatabase()

oSaver.save(oCharacter)
exit()
#exit()
#oCharacterDisplayer.setCharacter(oCharacter)
#oCharacterDisplayer = CharacterDisplayer()

#oCharacters = oSaver.load(1)
#for oEachCharacter in oCharacters:
#    oCharacterDisplayer.setCharacter(oEachCharacter)
    #oCharacterDisplayer.display()


from Ui import Menu

oMenu = Menu()
oMenu.run()


#oCharacterDisplayer.display()
