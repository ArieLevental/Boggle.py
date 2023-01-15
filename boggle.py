#################################################################
# FILE : boggle.py
# WRITERS : Arie Levental , Arie_Levental , 319142055
#           Adir Barak , adir.barak, 207009739
# EXERCISE : intro2cs1 ex11 2023
# DESCRIPTION: This program runs the game of Boggle
# STUDENTS WE DISCUSSED THE EXERCISE WITH: No-one
# WEB PAGES WE USED: Too many to count.
#################################################################

import boggle_gui
import boggle_gui as gui
import boggle_model as model
import pygame
from typing import List


class BoggleController:
    # pygame.mixer used to play soundeffects
    pygame.mixer.init()

    def __init__(self) -> None:
        self._gui = gui.BoggleGUI()
        self._model = model.BoggleBoard()
        self.init_cubes()
        self.create_pick_action()
        self.create_undo_action()
        self.create_start_reset_action()
        self.create_party_action()

    def create_cube_action(self, char, coord):
        def action_func():
            if self._model.path_is_valid(self._model.get_current_path() + [coord]):
                self._model.update_current_path(coord)
                self._gui.set_display(self._model.get_current_word())
                cube_index = coord[0]*4 + coord[1]
                cube = self._gui._cubes[cube_index]
                cube.marked = True
                cube["background"] = self._gui.hue_red_color(len(self._model.get_current_path()))
                self.play_sound("media/click.mp3")
            else:
                return

        return action_func

    def pick_action(self):
        word = self._model.submit_word()
        if word:
            self._gui._update_found_words(self._model.get_found_words())
            self._gui.set_score(self._model.get_score())
            self.play_sound("media/correct.mp3")
        else:
            self._model.clear_current_word()
            self.play_sound("media/error.mp3")
        for index, cube in enumerate(self._gui._cubes):
            cube.marked = False
            if self._gui._party_mode:
                cube["bg"] = self._gui.random_color()
            else:
                row, col = index // 4, index % 4
                if row % 2 == col % 2:
                    cube["bg"] = boggle_gui.REGULAR_COLOR_2
                else:
                    cube["bg"] = boggle_gui.REGULAR_COLOR_1
        self._gui.set_display("")

    def undo_action(self):
        popped_cube_coord = self._model.undo_last_step()
        if popped_cube_coord:
            cube_index = popped_cube_coord[0] * 4 + popped_cube_coord[1]
            cube = self._gui._cubes[cube_index]
            cube.marked = False
            if self._gui._party_mode:
                cube["bg"] = self._gui.random_color()
            else:
                if popped_cube_coord[0] % 2 == popped_cube_coord[1] % 2:
                    cube["bg"] = boggle_gui.REGULAR_COLOR_2
                else:
                    cube["bg"] = boggle_gui.REGULAR_COLOR_1
        self._gui.set_display(self._model.get_current_word())
        self.play_sound("media/undo.mp3")

    def init_cubes(self):
        board_coords = self._model.get_board_coords()
        for index, char in enumerate(self._model.get_chars_list()):
            cur_cube = self._gui._cubes[index]
            action = self.create_cube_action(char, board_coords[index])
            cur_cube["text"] = char
            cur_cube.configure(command=action)

    def start_action(self):
        self._gui._buttons["START"]["text"] = "RESET"
        self._model.reset_board()
        self._gui.set_display("WELCOME TO BOGGLE!")
        self._gui.set_score(self._model.get_score())
        self._gui._update_found_words(self._model.get_found_words())
        self.init_cubes()
        self._gui.reset_timer()
        self.play_sound("media/new-round.wav")
        self._gui.party_mode_disabled()
        for index, cube in enumerate(self._gui._cubes):
            row, col = index // 4, index % 4
            cube.marked = False
            if row % 2 == col % 2:
                cube["bg"] = boggle_gui.REGULAR_COLOR_2
            else:
                cube["bg"] = boggle_gui.REGULAR_COLOR_1

    def party_action(self):
        self.play_sound("media/wow.mp3")
        self._gui.party_mode_activated()

    def create_start_reset_action(self):
        self._gui._buttons["START"].configure(command=self.start_action)

    def create_undo_action(self):
        self._gui._buttons["UNDO"].configure(command=self.undo_action)

    def create_pick_action(self):
        self._gui._buttons["PICK"].configure(command=self.pick_action)

    def create_party_action(self):
        self._gui._buttons["PARTY"].configure(command=self.party_action)

    def play_sound(self, soundtrack: str):
        pygame.mixer.music.load(soundtrack)
        pygame.mixer.music.play()

    def run(self) -> None:
        self._gui.run()


if __name__ == '__main__':
    boggle_game = BoggleController()
    boggle_game.run()
