#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'julien'


import urwid, pprint
from Character import Character as CharacterEntity
from Database import CharacterDatabase

class Menu:

    def __init__(self):
        self.oMainMenu = None
        self.oCharacterDb = None

    # Draw a list of each character
    def drawCharacterListMenu(self, oCharacterList):
        assert isinstance(oCharacterList, list)
        aList = []
        for oEachCharacter in oCharacterList:
            assert isinstance(oEachCharacter, CharacterEntity)
            sLabelForCharacterListChoice = str(oEachCharacter.getId()) + '. ' + oEachCharacter.getName()
            oButton = self.drawEachButton(sLabelForCharacterListChoice, self.openCharacterStyleSheet, oEachCharacter.getId())
            oButton.characterId = oEachCharacter.getId()
            aList.append(oButton)
        oMenu = self.drawEachMenu('Liste des personnages', aList)

        self.oMainMenu.open_box(oMenu)

    # Open a character stylesheet
    def openCharacterStyleSheet(self, oButton):
        iCharacterId = oButton.user_data
        assert isinstance(iCharacterId, int)
        oDb = self.__getCharacterDb()
        aListOfCharacter = oDb.load(iCharacterId)
        if 0 == len(aListOfCharacter):
            raise Exception('unable to find character')

        assert isinstance(aListOfCharacter[0], CharacterEntity)
        oCurrentCharacter = aListOfCharacter[0]

        # New overlay
#        oCharacterSheet = urwid.Overlay(
#            urwid.Text(oCurrentCharacter.getName()),
#            urwid.Text(str(oCurrentCharacter.getId())),
#            width=('relative', 100),
#            height=('relative', 100),
#            valign='top',
#            align='left',
#
#        )

        oCharacterDisplayer = CharacterStylesheet(oCurrentCharacter)
        oMainCharacteristics = oCharacterDisplayer.build()


        self.oMainMenu.open_box(oMainCharacteristics, width=('relative', 120), height=('relative', 120))


    def openCharacterList(self, oButton):
        oDb = self.__getCharacterDb()
        oListOfCharacter = oDb.load()
        self.drawCharacterListMenu(oListOfCharacter)


    def returnMenuConfiguration(self):
        return self.drawEachMenu(u'Nae', [
            self.drawEachSubMenu(u'Personnages', [
                self.drawEachSubMenu(u'Gestion', [
                    self.drawEachButton(u'Liste des personnages', self.openCharacterList),
                    self.drawEachButton(u'Créer un personnage', self.item_chosen),
                    self.drawEachButton(u'Générer un personnage', self.item_chosen),
                    ]),
                ]),
            self.drawEachSubMenu(u'Combat', [
                self.drawEachButton(u'Tirer initiative', self.item_chosen),
                self.drawEachButton(u'Sélectionner personnages pour le combat', self.item_chosen),
                ]),
            ])

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
            ('characterName', 'white,underline,bold', 'dark blue'),
            ('sectionName', 'black, bold', 'white')
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

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)


class CharacterStylesheet:

    def __init__(self, oCharacter):
        assert isinstance(oCharacter, CharacterEntity)
        self.oCharacter = oCharacter

    def build(self):
        oMainInfos = self.buildMainInfos()
        oMainCharacteristics = self.buildMainCharacteristics()
        oMainPile = urwid.Pile([oMainInfos, oMainCharacteristics, self.buildSecondaryCharacteristics()])
        return oMainPile


    def buildMainInfos(self):
        oName = urwid.Text(('characterName', self.oCharacter.getName()))
        oAge = urwid.Text('Age : '+ str(self.oCharacter.getAge()))

        return urwid.ListBox([oName, oAge])


    def buildMainCharacteristics(self):

        oCharacter = self.oCharacter
        aListToShow = [
            ['Force', oCharacter.getStrength()],
            ['Agilité', oCharacter.getAgility()],
            ['Mental', oCharacter.getMental()],
            ['Charisme', oCharacter.getCharism()],
            ['Discernement', oCharacter.getDiscernment()],
            ['Endurance', oCharacter.getStamina()],
            ['Volonté', oCharacter.getWill()],
            ['Instinct', oCharacter.getInstinct()]
        ]

        return self.__buildCharacteristics('Caractéristiques primaires', aListToShow)

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
        return self.__buildCharacteristics('Caractéristiques secondaires', aListToShow)


    def __buildCharacteristics(self, sCaption, aListOfNameAndValues):

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
        oCharacter = self.oCharacter
        aListOfValues = [oCharacter.getStrength(), oCharacter.getAgility(), oCharacter.getMental(), oCharacter.getCharism(), oCharacter.getDiscernment(), oCharacter.getStamina(), oCharacter.getWill(), oCharacter.getInstinct()]
        for iValues in aValues:
            floatPart = iValues-int(iValues)
            if floatPart == 0:
                iValues = int(iValues)
            aUrwidValues.append(urwid.Text(str(iValues)))
        aUrwidValues.append(urwid.Divider('-'))
        oValueList = urwid.ListBox(aUrwidValues)

        return urwid.Columns([oNameList, oValueList])

