__author__ = 'julien'

from peewee import *
from Character import Character as CharacterEntity

class CharacterSaver:

    ###### Save the character in base ######
    def save(self, oCharacter):
        assert isinstance(oCharacter, CharacterEntity)
        if None == oCharacter.getName():
            raise Exception('Unable to save a character without name')
        aMainCaracteristic = ['Strength', 'Agility', 'Mental', 'Charism', 'Discernment', 'Stamina', 'Will', 'Instinct']

        for sCharac in aMainCaracteristic:
            fMethod = getattr(oCharacter, 'get'+sCharac)
            if 0 == fMethod():
                raise Exception('Unable to save a character without '+sCharac)

        if None == oCharacter.getType():
            raise Exception('Please set the type of the character, none submitted')

        oCharacterModel = Character()
        if None != oCharacter.iId:
            oCharacterModel.set_id(oCharacter.iId)

        oCharacterModel.name = oCharacter.getName()

        if None != oCharacter.getAge():
            oCharacterModel.age = oCharacter.getAge()

        oCharacterModel.strength = oCharacter.getStrength()
        oCharacterModel.agility = oCharacter.getAgility()
        oCharacterModel.mental = oCharacter.getMental()
        oCharacterModel.charism  = oCharacter.getCharism()






database = SqliteDatabase('database/nae.sql')

class BaseModel(Model):
    class Meta:
        database = database

class Character(BaseModel):
    # main description
    name = CharField(max_length=60)
    age = IntegerField()

    # type
    type = CharField(max_length=10)

    # main caracteristics
    strength = IntegerField()
    agility = IntegerField()
    mental = IntegerField()
    charism = IntegerField()
    discernment = IntegerField()
    stamina = IntegerField()
    will = IntegerField()
    instinct = IntegerField()

    money = IntegerField()
    life = IntegerField()

    ## modificator

    talentpointused = IntegerField()
    spirittalentpointused = IntegerField()


