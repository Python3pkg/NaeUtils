#!/usr/bin/python
# -*- coding: utf-8 -*-

import math, random

# A character in the Nae world
class Character:

    def __init__(self):

        # a key to retrieve it
        self.iId = None

        # the type of the character
        self.sType = None

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
        self.dElementary = {'fire':0, 'water': 0, 'earth': 0, 'air': 0}

        self.iLifeMax = None # Stamina x 2 + Strength
        self.iNaergyMax = None #
        self.iHealing = None # Stamina / 3 ceil down
        self.iWatering = None # Instinct / 8 number of naergic point per hour
        self.iTalent = None
        self.iNaergy = None
        self.iTalent = None
        self.iStar = None
        self.iSpirit = None

        self.dStarModificator = {'Ardor': 0, 'Reflex' : 0, 'Muse': 0, 'Book': 0}

        # Counters
        self.iMoney = 0
        self.iBaseMaxLife = 0
        self.iBaseMaxNaergy = 0
        self.iCurrentLife = 0
        self.iInit = None
        self.iInitCompute = []

        # Modificator
        self.iTalentPointUsed = 0
        self.iSpiritPointUsed = 0

        # Status
        self.bInCombat = None

    def getId(self):
        return self.iId

    def setId(self, iId):
        self.iId = iId

    def getType(self):
        return self.sType

    def setType(self, sType):
        if sType not in ['pj', 'pnj']:
            raise Exception('Type is not autorized : ' + sType)
        self.sType = sType

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
        ## secondary
        self.__computeArdor()
        self.__computeWatering()
        self.__computeBook()
        self.__computeElementary()
        self.__computeMuse()
        self.__computeReflex()
        self.__computeStar()
        ## traits
        self.__computeLifeMax()
        self.__computeNaergyMax()
        self.__computeSpirit()
        self.__computeHealing()
        self.__computeTalent()
        # Counter
        self.__initLife()
        self.__initNaergy()


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

    def getValueByMainCaracString(self, sCaracteristicName):
        if sCaracteristicName == 'charism':
            iBaseCounter = self.getCharism()
        elif sCaracteristicName == 'strength':
            iBaseCounter = self.getStrength()
        elif sCaracteristicName == 'agility:':
            iBaseCounter = self.getAgility()
        elif sCaracteristicName == 'mental':
            iBaseCounter = self.getMental()
        elif sCaracteristicName == 'discernment':
            iBaseCounter = self.getDiscernment()
        elif sCaracteristicName == 'will':
            iBaseCounter = self.getWill()
        elif sCaracteristicName == 'instinct':
            iBaseCounter = self.getInstinct()

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

    def getLifeMax(self):
        return self.iBaseMaxLife + self.iLifeMax

    def getNaergyMax(self):
        return self.iBaseMaxNaergy + self.iNaergyMax

    def getHealing(self):
        return self.iHealing

    def getWatering(self):
        return self.iWatering

    def getTalent(self, bWithModificator=True):
        if bWithModificator:
            iTalent = self.iTalent - self.iTalentPointUsed
        else:
            iTalent = self.iTalent
        return iTalent

    def getSpirit(self, bWithModificator=True):
        if bWithModificator:
            iSpirit = self.iSpirit - self.iSpiritPointUsed
        else:
            iSpirit = self.iSpirit
        return iSpirit


    # All the Counters

    ## Money money
    def getMoney(self):
        return self.iMoney

    def setMoney(self, iMoney):
        self.iMoney = iMoney

    def addMoney(self, iMoneyToAdd):
        self.iMoney += iMoneyToAdd

    def subMoney(self, iMoneyToSub):
        self.iMoney -= iMoneyToSub

    ## Life, oooh life
    def getLife(self):
        return self.iCurrentLife;

    def setLife(self, iCurrentLife):
        self.iCurrentLife = iCurrentLife

    def addLife(self, iLifeToAdd):
        self.iCurrentLife += iLifeToAdd

    def subLife(self, iLifeToSub):
        self.iCurrentLife -= iLifeToSub

    def getBaseLifeMax(self):
        return self.iBaseMaxLife

    def setBaseLifeMax(self, iLifeBase):
        self.iBaseMaxLife = iLifeBase

    ## Naergy, what, power!
    def getNaergy(self):
        return self.iBaseMaxNaergy + self.iCurrentNaergy

    def setNaergy(self, iCurrentNaergy):
        self.iCurrentNaergy = iCurrentNaergy

    def addNaergy(self, iNaergyToAdd):
        self.iCurrentNaergy += iNaergyToAdd

    def getBaseNaergyMax(self):
        return self.iBaseMaxNaergy

    ## set base Naergy
    def setBaseNaergyMax(self, iBaseNaergyMax):
        self.iBaseMaxNaergy = iBaseNaergyMax

    def subNaergy(self, iNaergyToSub):
        self.iCurrentNaergy -= iNaergyToSub

    def setTalentPoint(self, iHowMany):
        self.iTalentPointUsed = iHowMany

    def useTalentPoint(self, iHowMany):
        iCurrentTalent = self.getTalent(True)
        if iCurrentTalent < 1 or (iCurrentTalent - (self.iTalentPointUsed + iHowMany) < 1):
            ArithmeticError('You cant use talent point anymore, your talent tank is empty')
        self.iTalentPointUsed += iHowMany

    def gainTalentPoint(self, iHowMany):
        self.iTalentPointUsed -= iHowMany
        if 0 >= self.iTalentPointUsed:
            self.iTalentPointUsed = 0

    def getTalentPoint(self):
        return self.iTalentPointUsed

    def setSpiritPoint(self, iHowMany):
        self.iSpiritPointUsed = iHowMany


    def useSpiritPoint(self, iHowMany):
        iCurrentSpirit = self.getSpirit(True)
        if iCurrentSpirit < 1 or (iCurrentSpirit - (self.iSpiritPointUsed + iHowMany) < 1):
            ArithmeticError('You cant use talent point anymore, your talent tank is empty')
        self.iSpiritPointUsed += iHowMany

    def gainSpiritPoint(self, iHowMany):
        self.iSpiritPointUsed -= iHowMany
        if 0 >= self.iSpiritPointUsed:
            self.iSpiritPointUsed = 0

    def getSpiritPoint(self):
        return self.iSpiritPointUsed

    # Set a star modificator. If set, the star will be augmented
    def setStarModificator(self, sCarac, iValue):
        if sCarac not in self.dStarModificator:
            raise AssertionError('star modificator must be in '+ ','.join(self.dStarModificator.keys()))
        if iValue < -3 or iValue > 0:
            raise ArithmeticError('star '+sCarac+' modificator value must be between -3 and 0')
        self.dStarModificator[sCarac] = iValue

    ########### Variable values ##############

    def getInitiative(self, iDiceScore = None):
        if None != self.iInit:
            return self.iInit

        self.iInitCompute = [self.getReflex()]
        def launchDice(iBaseValue=0):
            iScore = iBaseValue
            iDiceScore = random.randint(1, 10)
            self.iInitCompute.append(iDiceScore)
            iScore += iDiceScore
            if 10 == iDiceScore:
                iScore = launchDice(iScore)
            return iScore


        if None == iDiceScore:
            iDiceScore = launchDice(0)
        return self.getReflex() + iDiceScore

    def getInitCompute(self):
        return self.iInitCompute

    def resetInitiative(self):
        self.iInit = None
        self.iInitCompute = []

    def setInitiative(self, iInit):
        self.iInit = iInit

    ########### Status #################

    def getInCombat(self):
        return self.bInCombat

    def setInCombat(self, bInCombat):
        assert isinstance(bInCombat, bool)
        self.bInCombat = bInCombat

    ############ Compute #############
    def __computeArdor(self):
        self.iArdor = self.__computeTwoCaracAndDivisor(self.iDiscernment, self.iWill, 2)
        self.iArdor += self.dStarModificator['Ardor']

    def __computeReflex(self):
        self.iReflex = self.__computeTwoCaracAndDivisor(self.iAgility, self.iDiscernment, 2)
        self.iReflex += self.dStarModificator['Reflex']

    def __computeMuse(self):
        self.iMuse = self.__computeTwoCaracAndDivisor(self.iCharism, self.iInstinct, 2)
        self.iMuse += self.dStarModificator['Muse']

    def __computeBook(self):
        self.iBook = self.__computeTwoCaracAndDivisor(self.iMental, self.iWill, 2)
        self.iBook += self.dStarModificator['Book']

    def __computeStar(self):
        self.iStar = 4
        self.iStar -= self.dStarModificator['Ardor']
        self.iStar -= self.dStarModificator['Muse']
        self.iStar -= self.dStarModificator['Reflex']
        self.iStar -= self.dStarModificator['Book']

    def __computeElementary(self):
        self.dElementary['fire'] = self.__computeTwoCaracAndDivisor(self.iStrength, self.iCharism, 2)
        self.dElementary['water'] = self.__computeTwoCaracAndDivisor(self.iDiscernment, self.iMental, 2)
        self.dElementary['earth'] = self.__computeTwoCaracAndDivisor(self.iStamina, self.iWill, 2)
        self.dElementary['air'] = self.__computeTwoCaracAndDivisor(self.iAgility, self.iInstinct, 2)

    ## compute traits
    def __computeLifeMax(self):
        self.iLifeMax = (self.iStamina * 2) + self.iStrength # force confirmee pour composante
        # Caracteristic compute

    def __computeNaergyMax(self):
        self.iNaergyMax = (self.iCharism + self.iInstinct)

    def __computeHealing(self):
        if 0 == self.iStamina:
            self.iHealing = 0
        self.iHealing = math.floor(self.iStamina / 3)

    def __computeWatering(self):
        if 0 == self.iInstinct:
            self.iWatering = 0
        self.iWatering = math.floor(self.iInstinct / 8)

    def __computeSpirit(self):
        self.iSpirit = self.__computeTwoCaracAndDivisor(self.iArdor, self.iReflex, 4)

    def __computeTalent(self):
        self.iTalent = self.__computeTwoCaracAndDivisor(self.iMuse, self.iArdor, 4)

    def __computeTwoCaracAndDivisor(self, iFirstCarac, iSecondCaracteristic, iDivisor):
        return math.floor((iFirstCarac + iSecondCaracteristic) / iDivisor)

    def __initLife(self):
        self.iCurrentLife = self.iLifeMax
        assert isinstance(self.iCurrentLife, int) and self.iCurrentLife > 0
    
    def __initNaergy(self):
        self.iCurrentNaergy = self.iNaergyMax
        assert isinstance(self.iCurrentNaergy, int) and self.iCurrentLife > 0


########################
##### COMPETENCES ######
########################

class Skill:

    def __init__(self):
        self.iId = None
        self.sName = None
        self.sBaseCaracteristic = None
        self.sFormula = None
        self.iPoints = 0
        self.sDescription = None


    def compute(self, oCharacter):
        iCounter = oCharacter.getValueByMainCaracString(self.sBaseCaracteristic)




###############################
##  DISPLAYER FOR CHARACTER  ##
###############################
from termcolor import colored
import texttable as tt

class CharacterDisplayer:

    def setCharacter(self, oCharacter):
        try:
            assert isinstance(oCharacter, Character)
        except AssertionError as eError:
            print 'Please submit a Character object'
            raise eError
        self.oCharacter = oCharacter

    def display(self):
        self.displayMainDescription()
        self.displayMainCaracteristicts()
        self.displaySecondaryCaracteristics()
        self.displayTraitCaracteristics()
        self.displayCounters()

    def displayMainDescription(self):
        self.__displayTitle('Main description')

        oCharacter = self.oCharacter
        if None != oCharacter.getId():
            self.__displayMember('Id', oCharacter.getId())

        sName = oCharacter.getName()
        if None != sName:
            self.__displayMember('Name', sName)

        iAge = oCharacter.getAge()
        if None != iAge:
            self.__displayMember('Age', iAge)


    def displayMainCaracteristicts(self):
        self.__displayTitle('Caractéristiques (main)')
        oCharacter = self.oCharacter
        lRows = [
            ['Force', oCharacter.getStrength()],
            ['Endurance', oCharacter.getStamina()],
            ['Agilité', oCharacter.getAgility()],
            ['Discernement', oCharacter.getDiscernment()],
            ['Mental', oCharacter.getMental()],
            ['Instint', oCharacter.getInstinct()],
            ['Charisme', oCharacter.getCharism()],
            ['Volonté', oCharacter.getWill()]
        ]
        self.__displayCaracList(lRows)

    def displaySecondaryCaracteristics(self):
        self.__displayTitle('Caractéristiques (secondary)')
        oCharacter = self.oCharacter
        lRows = [
            ['Ardeur', oCharacter.getArdor()],
            ['Réflexes', oCharacter.getReflex()],
            ['Muse', oCharacter.getMuse()],
            ['Livres', oCharacter.getBook()],
            ['Étoile', oCharacter.getStar()],
            ['Element-Feu', oCharacter.getElementary('fire')],
            ['Element-Eau', oCharacter.getElementary('water')],
            ['Element-Terre', oCharacter.getElementary('earth')],
            ['Element-Air', oCharacter.getElementary('air')],
        ]
        self.__displayCaracList(lRows)

    def displayTraitCaracteristics(self):
        self.__displayTitle('Caractéristiques (traits)')
        oCharacter = self.oCharacter
        lRows = [
            ['Talent', oCharacter.getTalent()],
            ['Panache', oCharacter.getSpirit()],
            ['Vie Maximum', oCharacter.getLifeMax()],
            ['Naergie Maximum', oCharacter.getNaergyMax()],
            ['Guérision', oCharacter.getHealing()],
            ['Abreuvement', oCharacter.getWatering()]
        ]
        self.__displayCaracList(lRows)

    def displayCounters(self):
        self.__displayTitle('Compteurs')
        oCharacter = self.oCharacter
        self.__displayMember('Argent', str(oCharacter.getMoney()) + ' t.')
        self.__displayMember('Vie', str(oCharacter.getLife()))

    def __displayTitle(self, sTitle):
        print colored(sTitle, None, None, ['bold', 'underline']) + ' : '
    def __displayCaracList(self, lCaracList):
        oTextTable = tt.Texttable()
        oTextTable.header(['Caracteristic', 'Value'])
        oTextTable.add_rows(lCaracList, False)
        sDisplay = oTextTable.draw()
        print sDisplay

    # Display a description
    def __displayMember(self, sMemberName, mMemberValue, sColor='white'):
        print colored(sMemberName, 'green', None, ['underline']) + ' : '+ colored(mMemberValue, sColor)

