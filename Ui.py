#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'julien'

import urwid, copy
from Entities import Character as CharacterEntity
from Database import CharacterDatabase

class Menu:

    def __init__(self):
        self.oMainMenu = None
        self.oCharacterDb = None

    def showError(self, sErrorMessage='Test'):
        aErrorWindow = [urwid.Text(('errorTitle', 'Erreur')), urwid.Divider('-'), urwid.Text(sErrorMessage, align='center')]
        aErrorListBox = urwid.ListBox(aErrorWindow)
        self.oMainMenu.open_box(aErrorListBox, width=('relative', 30), height=('relative', 3))


    def setCharacterInCombat(self, oCheckbox, bState, oCharacter):
        assert isinstance(oCharacter, CharacterEntity)
        oCharacter.setInCombat(bState)
        self.__getCharacterDb().save(oCharacter)

    def openInCombatMenu(self, oButton):
        self.openCharacterList(oButton, self.setCharacterInCombat)

    def openCharacterList(self, oButton=None, fCallback=None, sType="checkbox"):
        oDb = self.__getCharacterDb()
        oListOfCharacter = oDb.load()
        if None == fCallback:
            self.drawCharacterListMenu(oListOfCharacter)
        elif sType == "button":
            self.drawCharacterListMenu(oListOfCharacter, callback=fCallback)
        else:
            self.drawCharacterListMenu(oListOfCharacter, checkbox=True, callback=fCallback)

    # Draw a list of each character
    def drawCharacterListMenu(self, oCharacterList, **kwargs):
        assert isinstance(oCharacterList, list)
        aList = []
        for oEachCharacter in oCharacterList:
            assert isinstance(oEachCharacter, CharacterEntity)
            sLabelForCharacterListChoice = oEachCharacter.getName()
            if 'checkbox' in kwargs.keys() and 'callback' in kwargs.keys() and kwargs['checkbox'] == True:
                bState = True if oEachCharacter.getInCombat() == True else False
                oButton = urwid.CheckBox(sLabelForCharacterListChoice, state=bState, on_state_change=kwargs['callback'], user_data=oEachCharacter)
            else:
                if 'callback' in kwargs.keys():
                    fCallback = kwargs['callback']
                else:
                    fCallback = self.openCharacterStyleSheet
                oButton = self.drawEachButton(sLabelForCharacterListChoice, fCallback, oEachCharacter.getId())
            oButton.characterId = oEachCharacter.getId()
            aList.append(oButton)
        oMenu = self.drawEachMenu('Liste des personnages', aList)
        self.oMainMenu.open_box(oMenu)


    ##### Init management

    def askForManualInit(self, oButton):
        # Load only character in combat
        aCharacterList = self.__getCharacterDb().load(incombat=True)

        aCharacterNames = []
        aManualValues = []
        aEditables = []
        for oEachCharacter in aCharacterList:
            assert isinstance(oEachCharacter, CharacterEntity)
            oText = urwid.Text(oEachCharacter.getName())
            aCharacterNames.append(oText)

            oEditable = urwid.IntEdit("| Valeur manuelle :")
            oEditable.character = oEachCharacter
            aEditables.append(oEditable)
            aManualValues.append(oEditable)

        def validate(oButton, aEditables):
            aCharacters = []
            for aEachEditable in aEditables:
                oCharacter = aEachEditable.character
                assert isinstance(oCharacter, CharacterEntity)
                iValue = aEachEditable.value()
                if 0 != iValue:
                    oCharacter.setInitiative(iValue)
                else:
                    oCharacter.resetInitiative()

                aCharacters.append(oCharacter)

            self.showComputedInit(aCharacters)

        aCharacterNames.extend([urwid.Divider('_'), urwid.Button('Calculer initiative', validate, user_data=aEditables)])
        aManualValues.append(urwid.Divider('_'))
        aPileOfNames = urwid.ListBox(aCharacterNames)
        aPileOfValues = urwid.ListBox(aManualValues)
        oColumns = urwid.Columns(
            [
                aPileOfNames,
                aPileOfValues
            ]
        )
        self.oMainMenu.open_box(oColumns)


    def showComputedInit(self, aCharacterList):

        for oEachCharacter in aCharacterList:
            assert isinstance(oEachCharacter, CharacterEntity)
            oEachCharacter.setInitiative(oEachCharacter.getInitiative())
        aCharacterList = sorted(aCharacterList, key=lambda character: character.getInitiative(), reverse=True)

        aListOfBox = []
        aListOfBox.extend([urwid.Text('Résultat d\'initiative'), urwid.Divider('-')])
        iListIndex = 1
        for oEachCharacter in aCharacterList:
            assert isinstance(oEachCharacter, CharacterEntity)
            sInitiative = str(iListIndex) + ' - ' +oEachCharacter.getName() + ' : ' + str(int(oEachCharacter.getInitiative()))
            sInitiative += ' - ('
            for iIndex, iValue in enumerate(oEachCharacter.getInitCompute()):
                if 0 == iIndex:
                    sInitiative += 'Ref.:'
                sInitiative += ' ' +str(int(iValue))
            sInitiative += ')'
            aListOfBox.append(urwid.Text(sInitiative))
            iListIndex += 1

        aListOfCharacter = urwid.ListBox(aListOfBox)
        self.oMainMenu.open_box(aListOfCharacter)

    #### Character stylesheet

    # Open a character stylesheet
    def openCharacterStyleSheet(self, oButton):
        iCharacterId = oButton.user_data
        assert isinstance(iCharacterId, int)
        oDb = self.__getCharacterDb()
        aListOfCharacter = oDb.load(id=iCharacterId)
        if 0 == len(aListOfCharacter):
            raise Exception('unable to find character')

        assert isinstance(aListOfCharacter[0], CharacterEntity)
        oCurrentCharacter = aListOfCharacter[0]

        oCharacterDisplayer = CharacterStylesheet(oCurrentCharacter)
        self.oMainMenu.open_box(oCharacterDisplayer, width=('relative', 120), height=('relative', 120))


    def createCharacterWindow(self, oButton):
        aCreateCharacter = [urwid.Text('Création de personnage'), urwid.Divider('-')]
        aLeftFormColumn = [urwid.Text('Nom :'), urwid.Text('Age :'), urwid.Divider(), urwid.Text('Type :')]
        oEditNameForm = urwid.Edit(u"", u"")
        oEditName = urwid.AttrMap(oEditNameForm, 'formField', focus_map='formFieldSelected')
        oEditAgeForm = urwid.IntEdit(u"", u"")
        oEditAge = urwid.AttrMap(oEditAgeForm, 'formField', focus_map='formFieldSelected')
        aType = []
        oTypeValue = {'value': 'pj'}
        def __onTypeChange(oButton, bState, oUserData):
            sType = oUserData['type']
            oRetriever = oUserData['retriever']
            oRetriever['value'] = sType

        aRightFormColumn = [
            oEditName,
            oEditAge,
            urwid.Divider(),
            urwid.RadioButton(aType, 'PJ', state='first True', on_state_change=__onTypeChange, user_data={'type':'pnj', 'retriever':oTypeValue}),
            urwid.RadioButton(aType, 'PNJ', state='first True', on_state_change=__onTypeChange, user_data={'type':'pnj', 'retriever':oTypeValue})
        ]
        aForm = [oEditNameForm, oEditAgeForm, oTypeValue]
        aLeftBox = urwid.ListBox(aLeftFormColumn)
        aRightBox = urwid.ListBox(aRightFormColumn)
        oColumns = urwid.Columns([('fixed', 7, aLeftBox), aRightBox, urwid.ListBox([])])
        oCreateCharacter = urwid.Pile(
            [
                ('fixed', 3, urwid.ListBox(aCreateCharacter)),
                ('fixed', 6, oColumns),
                urwid.ListBox([urwid.Divider('-'), urwid.Padding(urwid.Button(('reversed', '   OK   '), on_press=self.createCharacter, user_data=aForm), align='center', width=('relative', 18))])
            ]
        )
        self.oMainMenu.open_box(oCreateCharacter, height=('relative', 25), width=('relative', 30))

    def createCharacter(self, oButton, oUserData):
        aForm = oUserData
        oEditName, oEditAge, oTypeValue = aForm
        sType = oTypeValue['value']
        sName = oEditName.get_edit_text()
        sAge = oEditAge.get_edit_text()

        if sName.strip() == '':
            self.showError('Veuillez saisir un nom pour créer le personnage')
        elif str(sAge).strip() == '':
            self.showError('Veuillez saisir un age pour créer le personnage')
        else:
            oCharacter = CharacterEntity()
            oCharacter.setName(sName)
            oCharacter.setAge(sAge)
            oCharacter.setType(sType)
            oCharacter.setStrength(10)
            oCharacter.setAgility(10)
            oCharacter.setMental(10)
            oCharacter.setCharism(10)
            oCharacter.setDiscernment(10)
            oCharacter.setStamina(10)
            oCharacter.setWill(10)
            oCharacter.setInstinct(10)
            oCharacter.compute()
            oDb = self.__getCharacterDb()
            oDb.save(oCharacter)
            self.oMainMenu.removeLastBox()
            self.openCharacterList({})


    def returnMenuConfiguration(self):
        return self.drawEachMenu(u'Nae', [
            self.drawEachSubMenu(u'Personnages', [
                self.drawEachButton(u'Liste des personnages', self.openCharacterList),
                self.drawEachButton(u'Créer un personnage', self.createCharacterWindow),
                self.drawEachButton(u'Supprimer un personnage', self.deleteCharacterWindow)
                ]),

            self.drawEachSubMenu(u'Combat', [
                self.drawEachButton(u'Tirer initiative', self.askForManualInit),
                self.drawEachButton(u'Sélectionner personnages pour le combat', self.openInCombatMenu),
                ]),

            self.drawEachButton(u'Quitter', self.exit_program)
        ])

    def deleteCharacterWindow(self, oButton=None):
        self.openCharacterList(oButton, fCallback=self.deleteCharacter, sType="button")

    def deleteCharacter(self, oButton):
        iCharacterId = oButton.user_data
        oDbAdapter = self.__getCharacterDb()
        aListOfCharacter = oDbAdapter.load(id=iCharacterId)
        if 0 == len(aListOfCharacter):
            raise Exception('unable to find character')
        oCharacter = aListOfCharacter[0]
        assert isinstance(oCharacter, CharacterEntity)

        def deleteCharacterInDb(oButton):
            iId = oCharacter.getId()
            oDbAdapter.delete(oCharacter)
            self.oMainMenu.removeLastBox()
            self.oMainMenu.removeLastBox()
            self.deleteCharacterWindow()

        self.drawModalWarning('Supprimer le personnage '+oCharacter.getName(), 'OUI', 'NON', deleteCharacterInDb , self.oMainMenu.removeLastBox)

    def drawModalWarning(self, sWarning, sChoiceOne, sChoiceTwo, fCallbackOne, fCallbackTwo):
        aTotalWindow = []
        oHeader = urwid.ListBox([urwid.Text(('errorTitle', sWarning), align='center'), urwid.Divider('-')])
        def createButton(sText, fCallback):
            oButton = urwid.Button(sText, fCallback)
            oButton = urwid.Padding(oButton, align='center', width=('relative', 20))
            return oButton
        aChoiceOne = urwid.ListBox([createButton(sChoiceOne, fCallbackOne)])
        aChoiceTwo = urwid.ListBox([createButton(sChoiceTwo, fCallbackTwo)])
        oChoices = urwid.Columns([aChoiceOne, aChoiceTwo])

        oTotalList = urwid.Pile([oHeader, oChoices])
        self.oMainMenu.open_box(oTotalList, width=('relative', 30), height=('relative', 20))



    def drawMainMenu(self, sTitle, FirstChoice):
        oMainBody = [urwid.Text(sTitle), urwid.Divider()]


    def drawEachButton(self, sCaption, fCallback, sUserData=[]):
        oButton = urwid.Button(sCaption, user_data=sUserData)
        oButton.user_data = sUserData
        urwid.connect_signal(oButton, 'click', fCallback)
        return urwid.AttrMap(oButton, None, focus_map='reversed')

    def drawEachMenu(self, title, choices):
        body = [urwid.Text(title), urwid.Divider()]
        body.extend(choices)
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def drawEachSubMenu(self, caption, choices):
        contents = self.drawEachMenu(caption, choices)
        def open_menu(button):
            return self.oMainMenu.open_box(contents)
        return self.drawEachButton([caption, u'...'], open_menu)


    def item_chosen(self, button):
        response = urwid.Text([u'You chose ', button.label, u'\n'])
        done = self.drawEachButton(u'Ok', self.exit_program)
        self.oMainMenu.open_box(urwid.Filler(urwid.Pile([response, done])))

    def exit_program(self, button):
        raise urwid.ExitMainLoop()

    def run(self):
        self.oMainMenu = CascadingBoxes(self.returnMenuConfiguration())
        aPalette = [
            ('reversed', 'standout', ''),
            ('characterName', 'white,bold', 'dark blue'),
            ('sectionName', 'black, bold', 'white'),
            ('errorTitle', 'dark red, bold', 'white'),
            ('formField', 'white', 'light blue'),
            ('formFieldSelected', 'black', 'white')
        ]
        urwid.MainLoop(self.oMainMenu, palette=aPalette).run()

    def __getCharacterDb(self):
        if None == self.oCharacterDb:
            self.oCharacterDb = CharacterDatabase()
        return self.oCharacterDb



class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 5

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill(u' '))
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box, width=('relative', 80), height=('relative', 80)):

        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            self.original_widget,
            align='center', width=width,
            valign='middle', height=height,
            min_width=24, min_height=8,
            left=self.box_level * 3,
            right=(self.max_box_levels - self.box_level - 1) * 3,
            top=self.box_level * 2,
            bottom=(self.max_box_levels - self.box_level - 1) * 2)
        self.box_level += 1

    def removeLastBox(self, oButton=None):
        self.original_widget = self.original_widget[0]
        self.box_level -= 1

    def keypress(self, size, key):
        if key == 'esc' :
            self.removeLastBox()
            if self.box_level == 0:
                raise urwid.ExitMainLoop()
        else:
            return super(CascadingBoxes, self).keypress(size, key)


import types

class CharacterStylesheet(urwid.WidgetPlaceholder):

    def __init__(self, oCharacter):
        assert isinstance(oCharacter, CharacterEntity)
        self.oCharacter = oCharacter
        self.oSecondaryCaracteristics = None
        self.build()
        super(CharacterStylesheet, self).__init__(self.original_widget)

    def build(self):
        oMainInfos = self.buildMainInfos()

        oMainCharacteristics = self.buildMainCharacteristics()
        oTraits = self.buildTraits()
        oSecondaryCaracteristics = self.buildSecondaryCharacteristics()
        oCounters = self.buildCounter()
        self.oSecondaryCaracteristics = oSecondaryCaracteristics
        oMainPile = urwid.Pile(
            [('fixed', 3, oMainInfos), ('fixed', 12, oMainCharacteristics), ('fixed', 13, oSecondaryCaracteristics), ('fixed', 10, oTraits),
             ('weight', 7, oCounters)]
        )
        self.original_widget = oMainPile


    def buildMainInfos(self):
        oName = urwid.Text(('characterName', self.oCharacter.getName()))
        oAge = urwid.Text('Age : '+ str(self.oCharacter.getAge()))

        return urwid.ListBox([oName, oAge])


    def buildMainCharacteristics(self):

        oCharacter = self.oCharacter
        aListToShow = [
            ['Force', {
                'value': oCharacter.getStrength(),
                'callback': 'setStrength',
                'character':  oCharacter
            }],
            ['Agilité', {'value': oCharacter.getAgility(), 'callback': 'setAgility', 'character': oCharacter}],
            ['Mental', {'value': oCharacter.getMental(), 'callback': 'setMental', 'character': oCharacter}],
            ['Charisme', {'value': oCharacter.getCharism(), 'callback': 'setCharism', 'character': oCharacter}],
            ['Discernement', {'value' : oCharacter.getDiscernment(), 'callback': 'setDiscernment', 'character': oCharacter}],
            ['Endurance', {'value': oCharacter.getStamina(), 'callback': 'setStamina', 'character': oCharacter}],
            ['Volonté', {'value': oCharacter.getWill(), 'callback': 'setWill', 'character': oCharacter}],
            ['Instinct', {'value': oCharacter.getInstinct(), 'callback': 'setInstinct', 'character': oCharacter}]
        ]
        return self.__buildCaracteristics('Caractéristiques primaires', aListToShow)

    def buildSecondaryCharacteristics(self):
        oCharacter = self.oCharacter
        aListToShow = [
            ['Ardeur', int(oCharacter.getArdor())],
            ['Réflexes', oCharacter.getReflex()],
            ['Muse', oCharacter.getMuse()],
            ['Livres', oCharacter.getBook()],
            ['Étoile', oCharacter.getStar()],
            ['Element-Feu', oCharacter.getElementary('fire')],
            ['Element-Eau', oCharacter.getElementary('water')],
            ['Element-Terre', oCharacter.getElementary('earth')],
            ['Element-Air', oCharacter.getElementary('air')],
        ]
        return self.__buildCaracteristics('Caractéristiques secondaires', aListToShow)

    def buildTraits(self):
        oCharacter = self.oCharacter
        aTraits = [
            ['Talent', oCharacter.getTalent()],
            ['Panache', oCharacter.getSpirit()],
            ['Vie Maximum', oCharacter.getLifeMax()],
            ['Naergie Maximum', oCharacter.getNaergyMax()],
            ['Guérision', oCharacter.getHealing()],
            ['Abreuvement', oCharacter.getWatering()]
        ]
        return self.__buildCaracteristics('Traits', aTraits)

    def buildCounter(self):
        oCharacter = self.oCharacter
        aCounters = [
            ['Bonus sur max de vie', {
                'value': oCharacter.getBaseLifeMax(),
                'callback': 'setBaseLifeMax',
                'character': oCharacter
            }],
            ['Bonus sur max de Naergie', {
                'value': oCharacter.getBaseNaergyMax(),
                'callback': 'setBaseNaergyMax',
                'character': oCharacter
            }],
            ['Argent', {
                'value': oCharacter.getMoney(),
                'callback': 'setMoney',
                'character': oCharacter
            }],
            ['Vie', {
                'value': oCharacter.getLife(),
                'max': oCharacter.getLifeMax(),
                'callback' : 'setLife',
                'character' : oCharacter
            }],
            ['Naergie', {
                'value' : oCharacter.getNaergy(),
                'max': oCharacter.getNaergyMax(),
                'callback': 'setNaergy',
                'character': oCharacter
            } ]
        ]

        return self.__buildCaracteristics('Compteurs', aCounters)

    # Build a section of caracteristics
    def __buildCaracteristics(self, sCaption, aListOfNameAndValues):

        aNames = []
        aValues = []
        for lTuples in aListOfNameAndValues:
            aNames.append(lTuples[0])
            aValues.append(lTuples[1])

        oCaption = urwid.Text(('sectionName', sCaption))

        aUrwidNames = [oCaption , urwid.Divider('-')]
        for sName in aNames:
            aUrwidNames.append(urwid.Text(sName))
        aUrwidNames.append(urwid.Divider('-'))
        oNameList = urwid.ListBox(aUrwidNames)

        aUrwidValues = [urwid.Text(''), urwid.Divider('-')]

        for iValues in aValues:

            if not isinstance(iValues, types.DictionaryType):
                dFinalValue = {'value':iValues}
            else:
                dFinalValue = iValues

            if (dFinalValue['value'] - int(dFinalValue['value'])) == 0:
                dFinalValue['value'] = int(dFinalValue['value'])

            # Callback is in
            if 'callback' in dFinalValue.keys():
                if 'max' in dFinalValue.keys():
                    oTextWidget = CharacterGauge(self, dFinalValue['value'], dFinalValue['callback'], dFinalValue['character'], dFinalValue['max'])
                    oTextWidget.setToto(self.oSecondaryCaracteristics)
                else:
                    oTextWidget = CharacterGauge(self, dFinalValue['value'], dFinalValue['callback'], dFinalValue['character'])
            else:
                oTextWidget = urwid.Text(str(dFinalValue['value']))

            aUrwidValues.append(oTextWidget)

        aUrwidValues.append(urwid.Divider('-'))
        oValueList = urwid.ListBox(aUrwidValues)

        return urwid.Columns([('fixed', 40, oNameList), ('fixed', 9, oValueList)])


class CharacterGauge(urwid.Button):

    def __computeGauge(self):
        iCounter = self.iCounter
        if (iCounter - int(iCounter)) == 0:
            iCounter = int(iCounter)
        sGetCounterValue = str(iCounter)
        if None == self.iMax:
            return sGetCounterValue
        else:
            return sGetCounterValue + '/' + str(self.iMax)

    def __init__(self, oCharacterStylesheet, iCounter, fCallback = None, oCharacter = None, iMax = None):
        self.oCharacterStylesheet = oCharacterStylesheet
        self.iCounter = iCounter
        self.iMax = iMax
        self.fCallback = fCallback
        self.oCharacter = oCharacter
        super(CharacterGauge, self).__init__(self.__computeGauge())


    def keypress(self, size, key):
        if key == 'left':
            self.iCounter-=1
            self.set_label(self.__computeGauge())
        elif key == 'right':
            self.iCounter+=1
            self.set_label(self.__computeGauge())
        elif key == 'enter':
            self.applyNewValue(self.iCounter)
            self.oCharacter.compute()
            self.oCharacterStylesheet.build()
        else:
            super(CharacterGauge, self).keypress(size, key)

    def applyNewValue(self, iNewValue):
        if None != self.oCharacter and None != self.fCallback:
            getattr(self.oCharacter, self.fCallback)(iNewValue)
            self.__getDb().save(self.oCharacter)

    def __getDb(self):
        oDb = CharacterDatabase()
        return oDb

    def setToto(self, oToto):

        self.oToto = oToto
#
#from urwid.widget import Edit, LEFT, SPACE
#
#class CharacterEditField(urwid.Edit):
#
#    def __init__(self, caption=u"", edit_text=u"", multiline=False, align=LEFT, wrap=SPACE, allow_tab=False,
#                 edit_pos=None, layout=None, mask=None):
#        self._mask = mask
#        self._edit_text = edit_text
#
#        urwid.Edit.__init__(self, caption, edit_text, multiline, align, wrap, allow_tab, edit_pos, layout, mask)
#
#    def transformTextToFilledText(self, sText):
#        (maxcol, maxrow) = self.pack()
#        if len(sText) < maxcol:
#
#
#    def set_edit_text(self, text):
#        (maxcol, maxrow) = self.pack()
#        if len(text) < maxcol:
#            iDiff = maxcol - len(text)
#            iPost = '.' * iDiff
#            text += iPost
#        super(CharacterEditField, self).set_edit_text(text)
#
#    def keypress(self, size, key):
#        if self.valid_char(key):
