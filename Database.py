__author__ = 'julien'

from peewee import *
from Entities import Character as CharacterEntity

class MainDatabase:

    def checkIfBaseExistsAndCreateItIfNot(self):
        oModel = self.getCharacterModel()
        if not oModel.table_exists():
            oModel.create_table()
        oSkill = self.getSkillModel()
        if not oSkill.table_exists():
            oSkill.create_table()
        oSkillCharacter = self.getSkillCharacterModel()
        if not oSkillCharacter.table_exists():
            oSkillCharacter.create_table()

    def getCharacterModel(self):
        oCharacterModel = Character()
        return oCharacterModel

    def getSkillModel(self):
        oSkillModel = Skill()
        return oSkillModel

    def getSkillCharacterModel(self):
        oCharacterSkillModel = CharacterSkills()
        return oCharacterSkillModel


class CharacterDatabase(MainDatabase):

    ###### Save the character in base ######
    def load(self, **kwargs):
        """
        Load a character from base

        @param kwargs:id=int if you want to load only one character, skills=True load skills for character, default False
        @return:
                an array of character
        """
        self.checkIfBaseExistsAndCreateItIfNot()
        oCharacterModel = self.getCharacterModel()

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

            if 'skill' in kwargs.keys() and True == kwargs['skill']:
                # Skill loading
                SkillModel = CharacterSkills.select()
                oSkillList = SkillModel.join(Skill).where(CharacterSkills.character==oEachModel)
                aListOfSkillForCharacter = []
                for oEachSkill in oSkillList:
                    oEachSkill = self.__transformSkillInEntity(oEachSkill)
                    aListOfSkillForCharacter.append(oEachSkill)
                oEachEntity.setSkills(aListOfSkillForCharacter)

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
        self.checkIfBaseExistsAndCreateItIfNot()

        # saving
        oCharacterModel.save()

    # Delete a character in base
    def delete(self, oCharacter):
        assert isinstance(oCharacter, CharacterEntity)
        MainDatabase.checkIfBaseExistsAndCreateItIfNot()
        oModel = self.__transformEntityIntoModel(oCharacter)
        oModel.delete_instance()

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
        oCharacterModel = self.getCharacterModel()
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



##### Competences  ########
class Skill(Model):
    class Meta:
        database = database

    name = CharField(max_length=80)
    base_caracteristic = CharField(max_length=30)
    base_formula = CharField(max_length=30)
    points = IntegerField()


class CharacterSkills(BaseModel):
    skill = ForeignKeyField(Skill)
    character = ForeignKeyField(Character)
    points = IntegerField()

#databaseCompetences = SqliteDatabase('database/competences.sql')
