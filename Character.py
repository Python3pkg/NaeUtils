import math

# A character in the Nae world
class Character:

    def __init__(self):

        # character description
        self.sName = None
        self.iAge = None

        # main caracteristics
        self.iStrength = 0
        self.iAgility = 0 # agilite
        self.iMental = 0 # Mental
        self.iCharism = 0 # Charisme
        self.iDiscernment = 0 # Discernement
        self.iStamina = 0 # Endurance
        self.iWill = 0 # Volonte
        self.iInstinct = 0 # Instinct

        # deducted caracteristics
        self.dElementary = {}

        self.iLifeMax = None # Stamina x 2 + Strength
        self.iNaergyMax = None #
        self.iHealing = None # Stamina / 3 ceil down
        self.iWatering = None # Instinct / 8 number of naergic point per hour
        self.iTalent = None
        self.iNaergy = None
        self.iTalent = None
        self.iStar = None
        self.iPanache = None


        # Counters
        self.iMoney = 0


    def getName(self):
        return self.sName

    def setName(self, sName):
        self.sName = sName

    def getAge(self):
        return self.iAge

    def setAge(self, iAge):
        self.iAge = iAge


    # This method allows to compute all secondaries and traits caracteristic from the primary
    def compute(self):
        self.__computeArdor()
        self.__computeLifeMax()
        self.__computeHealing()
        self.__computeWatering()
        self.__computeBook()
        self.__computeElementary()
        self.__computeMuse()
        self.__computeReflex()


    # base

    def getStrength(self):
        return self.iStrength

    def setStrength(self, iStrength):
        self.iStrength = iStrength

    def getAgility(self):
        return self.iAgility

    def setAgility(self, iAgility):
        self.iAgility = iAgility

    def getDiscernment(self):
        return self.iDiscernment

    def setDiscernment(self, iDiscernment):
        self.iDiscernment = iDiscernment

    def getCharism(self):
        return self.iCharism

    def setCharism(self, iCharism):
        self.iCharism = iCharism

    def getMental(self):
        return self.iMental

    def setMental(self, iMental):
        self.iMental = iMental

    def getWill(self):
        return self.iWill

    def setWill(self, iWill):
        self.iWill = iWill

    def getStamina(self):
        return self.iStamina

    def setStamina(self, iStamina):
        self.iStamina = iStamina

    def getInstinct(self):
        return self.iInstinct

    def setInstinct(self, iInstinct):
        self.iInstinct = iInstinct


    # secondary

    def getArdor(self):
        return self.iArdor

    def getReflex(self):
        return self.iReflex

    def getMuse(self):
        return self.iMuse

    def getBook(self):
        return self.iBook

    def getElementary(self, sElement):
        return self.dElementary[sElement]

    def getStar(self):
        return self.iStar

    # traits

    def getSpirit(self):
        return self.iPanache

    def getLifeMax(self):
        return self.iLifeMax

    def getNaergyMax(self):
        return self.iNaergy

    def getHealing(self):
        return self.iHealing

    def getWatering(self):
        return self.iWatering

    def getTalent(self):
        return self.iTalent


    # Caracteristic compute
    def __computeLifeMax(self):
        self.iLifeMax = (self.iStamina * 2) + self.iStrength # force confirmee pour composante

    def __computeHealing(self):
        if 0 == self.iStamina:
            self.iHealing = 0
        self.iHealing = math.ceil(self.iStamina / 3)

    def __computeWatering(self):
        if 0 == self.iWaterring:
            self.iInstinct = 0
        self.iWaterring = math.ceil(self.iInstinct / 8)

    def __computeArdor(self):
        self.iArdor = self.__computeTwoCaracAndDivisor(self.iDiscernment, self.iWill, 2)

    def __computeReflex(self):
        self.iReflex = self.__computeTwoCaracAndDivisor(self.iAgility, self.iDiscernment, 2)

    def __computeMuse(self):
        self.iMuse = self.__computeTwoCaracAndDivisor(self.iCharism, self.iInstinct, 2)

    def __computeBook(self):
        self.iBook = self.__computeTwoCaracAndDivisor(self.iMental, self.iWill, 2)

    def __computeElementary(self):
        self.dElementary.fire = self.__computeTwoCaracAndDivisor(self.iStrength, self.iCharism, 2)
        self.dElementary.water = self.__computeTwoCaracAndDivisor(self.iDiscernment, self.iMental, 2)
        self.dElementary.earth = self.__computeTwoCaracAndDivisor(self.iStamina, self.iWill, 2)
        self.dElementary.air = self.__computeTwoCaracAndDivisor(self.iAgility, self.iInstinct, 2)


    def __computeTwoCaracAndDivisor(self, iFirstCarac, iSecond, iDivisor):
        return math.ceil((iFirstCarac + iSecond) / iDivisor)

###############################
##  DISPLAYER FOR CHARACTER  ##
###############################
from termcolor import colored

class CharacterDisplayer:

    def setCharacter(self, oCharacter):
        assert isinstance(oCharacter, Character)
        self.oCharacter = oCharacter

    def display(self):
        self.displayMainDescription()

    def displayMainDescription(self):
        sName = self.oCharacter.getName()
        if None != sName:
            self.displayMember('Name', sName)

        iAge = self.oCharacter.getAge()
        if None != iAge:
            self.displayMember('Age', iAge)



    def displayMember(self, sMemberName, mMemberValue):
        print colored(sMemberName+' : ', 'green') + colored(mMemberValue, 'red')

