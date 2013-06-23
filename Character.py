
import math

# A character in the Nae world
class Character:

	def __init__(self):

		# main caracteristics
		this.iStrength = 0 # force
		this.iAgility = 0# agilite
		this.iMental = 0 # Mental
		this.iCharism = 0 # Charisme
		this.iDiscernment = 0 # Discernement
		this.iStamina = 0 # Endurance
		this.iWill = 0 # Volonte
		this.iInstinct = 0 # Instinct

		# deducted caracteristics
		this.dElementary = {}

		this.iLifeMax # Stamina x 2 + Strength
		this.iNaergyMax #
		this.iHealing # Stamina / 3 ceil down
		this.iWatering # Instinct / 8 number of naergic point per hour
		this.iTalent


	def compute(self):
		this.__computeArdor()
		this.__computeLifeMax()
		this.__computeHealing()
		this.__computeWatering()

	# base

	def getStrength(self):
		return this.iStrength

	def setStrength(self, iStrength):
		this.iStrength = iStrength

	def getAgility(self):
		return this.iAgility

	def setAgility(self, iAgility):
		this.iAgility = iAgility

	def getDiscernment(self):
		return this.iDiscernment

	def setDiscernment(self, iDiscernment):
		this.iDiscernment = iDiscernment

	def getCharism(self):
		return this.iCharism

	def setCharism(self, iCharism):
		this.iCharism = iCharism

	def getMental(self):
		return this.iMental

	def setMental(self, iMental):
		this.iMental = iMental

	def getWill(self):
		return this.iWill

	def setWill(self, iWill):
		this.iWill = iWill

	def getStamina(self):
		return this.iStamina

	def setStamina(self, iStamina):
		this.iStamina = iStamina
	
	def getInstinct(self):
		return this.iInstinct

	def setInstinct(self, iInstinct):
		this.iInstinct = iInstinct


	# secondary

	def getArdor(self):
		return this.iArdor


	# traits 

	def getLifeMax(self):
		return this.iLifeMax
	def getNaergyMax(self):
		return this.iNaergy
	def getHealing(self):
		return this.iHealing
	def getWatering(self):
		return this.iWatering
	def getTalent(self):
		return this.iTalent


	# Caracteristic compute
	def __computeLifeMax(self):
		this.iLifeMax = (this.iStamina*2) + this.iStrength # force confirmee pour composante
	
	def __computeHealing(self):
		this.iHealing = math.ceil(this.iStamina/3)
	
	def __computeWatering(self):
		this.iWaterring = math.ceil(this.iInstinct/8)
	
	def __computeArdor(self):
		this.iArdor = this.__computeTwoCaracAndDivisor(this.iDiscernment, this.iWill, 2)

	def __computeReflex(self):
		this.iReflex = this.__computeTwoCaracAndDivisor(this.iAgility, this.iDiscernment, 2)

	def __computeMuse(self):
		this.iMuse = this.__computeTwoCaracAndDivisor(this.iCharism, this.iInstinct, 2)
	
	def __computeBook(self):
		this.iBook = this.__computeTwoCaracAndDivisor(this.iMental, this.iWill, 2)
	
	def __computeElementary(self):
		this.dElementary.fire = this.__computeTwoCaracAndDivisor(this.iStrength, this.iCharism, 2)
		this.dElementary.water = this.__computeTwoCaracAndDivisor(this.iDiscernment, this.iMental, 2)
		this.dElementary.earth = this.__computeTwoCaracAndDivisor(this.iStamina, this.iWill, 2)
		this.dElementary.air = this.__computeTwoCaracAndDivisor(this.iAgility, this.iInstinct, 2)
		

	def __computeTwoCaracAndDivisor(iFirstCarac, iSecond, iDivisor):
		return math.ceil((iFirstCarac + iSecond) / iDivisor)
