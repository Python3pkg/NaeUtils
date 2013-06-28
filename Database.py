__author__ = 'julien'

from peewee import *
from Character import Character as CharacterEntity

class CharacterSaver:

    def save(self, oCharacter):
        assert isinstance(oCharacter, CharacterEntity)


database = SqliteDatabase('database/nae.sql')

class BaseModel(Model):
    class Meta:
        database = database

class Character(BaseModel):
    # main description
    name = CharField(max_length=60)
    age = IntegerField()

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


