#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'julien'


import urwid
from Character import Character as CharacterEntity
from Database import CharacterDatabase

class Menu:

    def __init__(self):
        self.oMainMenu = None

    # Draw a list of each character
    def drawCharacterListMenu(self, oCharacterList):
        assert isinstance(oCharacterList, list)
        aList = []
        for oEachCharacter in oCharacterList:
            assert isinstance(oEachCharacter, CharacterEntity)
            sLabelForCharacterListChoice = str(oEachCharacter.getId()) + '. ' + oEachCharacter.getName()
            aList.append(self.drawEachButton(sLabelForCharacterListChoice, self.openCharacterStyleSheet))
        oMenu = self.drawEachMenu('Liste des personnages', aList)

        self.oMainMenu.open_box(oMenu)

    # Open a character stylesheet
    def openCharacterStyleSheet(self, oButton):
        pass

    def openCharacterList(self, oButton):
        oDb = CharacterDatabase()
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


    def drawEachButton(self, sCaption, fCallback):
        oButton = urwid.Button(sCaption)
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
        urwid.MainLoop(self.oMainMenu, palette=[('reversed', 'standout', '')]).run()



class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 5

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(urwid.SolidFill(u' '))
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
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

