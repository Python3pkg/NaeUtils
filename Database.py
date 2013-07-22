__author__ = 'julien'

from peewee import *
from Character import Character as CharacterEntity

class CharacterDatabase:

    ###### Save the character in base ######
    def load(self, **kwargs):

        self.__checkIfBaseExistsAndCreateItIfNot()
        oCharacterModel = self.__getCharacterModel()

        oModel = oCharacterModel.select()
        if 'id' in kwargs.keys():
            where = Character.id == kwargs['id']
            oResult = oModel.where(where)
        elif 'incombat' in kwargs.keys() and kwargs['incombat'] == True:
            oResult = oModel.where(Character.incombat == True)
        else:
            oResult = oModel

        aListOfCharacter = []
        for oEachModel in oResult:
            oEachEntity = self.__transformModelIntoEntity(oEachModel)
            aListOfCharacter.append(oEachEntity)

        return aListOfCharacter


    def save(self, oCharacter):
        """
        Save the character in base
        @param oCharacter: CharacterEntity The character
        @raise:
        """
        assert isinstance(oCharacter, CharacterEntity)
        if None == oCharacter.getName():
            raise Exception('Unable to save a character without name')
        aMainCaracteristic = ['Strength', 'Agility', 'Mental', 'Charism', 'Discernment', 'Stamina', 'Will', 'Instinct']

        for sCharac in aMainCaracteristic:
            fMethod = getattr(oCharacter, 'get'+sCharac)
            if None == fMethod():
                raise Exception('Unable to save a character without '+sCharac)

        if None == oCharacter.getType():
            raise Exception('Please set the type of the character, none submitted')

        oCharacterModel = self.__transformEntityIntoModel(oCharacter)

        if None == oCharacter.getId():
            oResult = oCharacterModel.select().where(Character.name == oCharacter.getName())

            if 0 < oResult.count():
                raise Exception('You cant save character that already exists')

        # creating table
        self.__checkIfBaseExistsAndCreateItIfNot()

        # saving
        oCharacterModel.save()

    def setCharacterInCombat(self, oCharacter):
        """
        Define in base that character is a part of the combat
        @param oCharacter:
        @return:
        """

    def __transformModelIntoEntity(self, oCharacterModel):
        assert isinstance(oCharacterModel, Character)
        oCharacterEntity = CharacterEntity()
        oCharacterEntity.setStrength(oCharacterModel.strength)
        oCharacterEntity.setAgility(oCharacterModel.agility)
        oCharacterEntity.setMental(oCharacterModel.mental)
        oCharacterEntity.setCharism(oCharacterModel.charism)
        oCharacterEntity.setDiscernment(oCharacterModel.discernment)
        oCharacterEntity.setStamina(oCharacterModel.stamina)
        oCharacterEntity.setWill(oCharacterModel.will)
        oCharacterEntity.setInstinct(oCharacterModel.instinct)
        oCharacterEntity.setMoney(oCharacterModel.money)
        oCharacterEntity.setType(oCharacterModel.type)
        oCharacterEntity.setLife(oCharacterModel.life)
        oCharacterEntity.setTalentPoint(oCharacterModel.talentpointused)
        oCharacterEntity.setSpiritPoint(oCharacterModel.spiritpointused)

        oCharacterEntity.setName(oCharacterModel.name)
        oCharacterEntity.setId(oCharacterModel.id)
        oCharacterEntity.setAge(oCharacterModel.age)

        oCharacterEntity.setBaseLifeMax(oCharacterModel.baselifemax)
        oCharacterEntity.setBaseNaergyMax(oCharacterModel.basenaergymax)

        if oCharacterModel.incombat != None:
            oCharacterEntity.setInCombat(oCharacterModel.incombat)

        oCharacterEntity.compute()

        return oCharacterEntity

    def __transformEntityIntoModel(self, oCharacter):
        oCharacterModel = self.__getCharacterModel()
        if None != oCharacter.iId:
            oCharacterModel.set_id(oCharacter.iId)
        oCharacterModel.name = oCharacter.getName()
        if None != oCharacter.getAge():
            oCharacterModel.age = oCharacter.getAge()
        oCharacterModel.type = oCharacter.getType()
        oCharacterModel.money = oCharacter.getMoney()
        oCharacterModel.life = oCharacter.getLife()
        oCharacterModel.strength = oCharacter.getStrength()
        oCharacterModel.agility = oCharacter.getAgility()
        oCharacterModel.mental = oCharacter.getMental()
        oCharacterModel.charism = oCharacter.getCharism()
        oCharacterModel.discernment = oCharacter.getDiscernment()
        oCharacterModel.stamina = oCharacter.getStamina()
        oCharacterModel.will = oCharacter.getWill()
        oCharacterModel.instinct = oCharacter.getInstinct()
        oCharacterModel.talentpointused = oCharacter.getTalentPoint()
        oCharacterModel.spiritpointused = oCharacter.getSpiritPoint()
        oCharacterModel.baselifemax = oCharacter.getBaseLifeMax()
        oCharacterModel.basenaergymax = oCharacter.getBaseNaergyMax()

        bInCombat = oCharacter.getInCombat()
        if None != bInCombat:
            oCharacterModel.incombat = bInCombat
        return oCharacterModel

    def __checkIfBaseExistsAndCreateItIfNot(self):
        oModel = self.__getCharacterModel()
        if not oModel.table_exists():
            oModel.create_table()

    def __getCharacterModel(self):
        oCharacterModel = Character()
        return oCharacterModel



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
    incombat = BooleanField(null=True)

    ## modificator

    talentpointused = IntegerField()
    spiritpointused = IntegerField()

    # counter
    baselifemax = IntegerField()
    basenaergymax = IntegerField()
