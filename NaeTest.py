
__author__ = 'julien'

import Database
from pprint import pprint, pformat

if __name__ == "__main__":
    oCharacterBase = Database.CharacterDatabase()
    oCharacterList = oCharacterBase.load(id=1, skills=True)
    pprint(vars(oCharacterList[0]))


