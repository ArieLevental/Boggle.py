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

INITIAL_MSG = "WELCOME TO BOGGLE!"
BOARD_SIZE = 4


class BoggleController:
    """
    The BoggleController class creates the main controller of the Boggle game. It initializes a GUI and game model,
    and creates actions for different game events such as picking a letter,
    undoing the last letter picked, starting/resetting the game, and activating party mode.
    """
    # pygame.mixer used to play soundeffects
    pygame.mixer.init()

    def __init__(self) -> None:
        """
        Initializes the Boggle game by creating a GUI and a game model, and then creates actions
        for the different game events.
        """
        self._gui = gui.BoggleGUI()
        self._model = model.BoggleBoard()
        self.init_cubes()
        self.create_pick_action()
        self.create_undo_action()
        self.create_start_reset_action()
        self.create_party_action()

    def create_cube_action(self, coord):
        """
        Creates an action function that is called when a cube is clicked.
        The action function updates the current word and the current path, and checks if the word is valid.
        :param coord: The coordinates of the cube that was clicked.
        :return: The action function
        """
        def action_func():
            """
            updates the current word and the current path, and checks if the word is valid.
            also handles all the logic behind logging the click and activating gui reactions
            """
            if self._model.path_is_valid(self._model.get_current_path() + [coord]):
                self._model.update_current_path(coord)
                self._gui.set_display(self._model.get_current_word())
                # compute the cube's list index from the coord (in a 4x4 board)
                cube_index = coord[0]*BOARD_SIZE + coord[1]
                cube = self._gui.cubes[cube_index]
                cube.marked = True
                cube["background"] = self._gui.hue_red_color(len(self._model.get_current_path()))
                self.play_sound("media/click.mp3")
            else:
                return

        return action_func

    def pick_action(self):
        """
        The pick_action method is called when the user submits the current word they have selected on the boggle board.
        If the word is valid, it updates the score, adds the word to the list of found words and plays a sound effect.
        If the word is not valid, it clears the current word and plays a sound effect.
        Additionally, it resets the colors of the cubes on the board.
        """
        word = self._model.submit_word()
        if word:
            self._gui.update_found_words(self._model.get_found_words())
            self._gui.set_score(self._model.get_score())
            self.play_sound("media/correct.mp3")
        else:
            self._model.clear_current_word()
            self.play_sound("media/error.mp3")
        for index, cube in enumerate(self._gui.cubes):
            cube.marked = False
            # reset colors based on party mode ON/OFF
            if self._gui.party_mode:
                cube["bg"] = self._gui.random_color()
            else:
                self._gui.party_mode_disabled()
                # revert to the distinct and beloved checkers pattern
                row, col = index // BOARD_SIZE, index % BOARD_SIZE  # calc row,col from index
                if row % 2 == col % 2:
                    cube["bg"] = boggle_gui.REGULAR_COLOR_2
                else:
                    cube["bg"] = boggle_gui.REGULAR_COLOR_1
        # reset the display to a blank label
        self._gui.set_display("")

    def undo_action(self):
        """
        The undo_action method is called when the user wants to undo their last move.
        It reverts the last cube that was selected and updates the current word displayed.
        Additionally, it resets the color of the cube to its original color and plays a sound effect.
        """
        popped_cube_coord = self._model.undo_last_step()
        if popped_cube_coord:
            cube_index = popped_cube_coord[0] * BOARD_SIZE + popped_cube_coord[1]
            cube = self._gui.cubes[cube_index]
            cube.marked = False
            # reset color based on party mode ON/OFF
            if self._gui.party_mode:
                cube["bg"] = self._gui.random_color()
            else:
                self._gui.party_mode_disabled()
                # revert to the distinct and beloved checkers pattern
                if popped_cube_coord[0] % 2 == popped_cube_coord[1] % 2:
                    cube["bg"] = boggle_gui.REGULAR_COLOR_2
                else:
                    cube["bg"] = boggle_gui.REGULAR_COLOR_1
        self._gui.set_display(self._model.get_current_word())
        self.play_sound("media/undo.mp3")

    def init_cubes(self):
        """
        The init_cubes method is used to initialize the cubes on the boggle board.
        It sets the text of each cube to the corresponding character and assigns the appropriate action to each cube.
        """
        board_coords = self._model.get_board_coords()
        for index, char in enumerate(self._model.get_chars_list()):
            cur_cube = self._gui.cubes[index]
            action = self.create_cube_action(board_coords[index])
            cur_cube["text"] = char
            cur_cube.configure(command=action)

    def start_action(self):
        """
        The start_action method is called when the user starts or resets the game.
        It resets the board, updates the display, score, and found words, resets the timer, and plays a sound effect.
        Additionally, it resets the colors of the cubes on the board to their original colors.
        """
        self._gui.buttons["START"]["text"] = "RESET"
        self._model.reset_board()
        self._gui.set_display(INITIAL_MSG)
        self._gui.set_score(self._model.get_score())
        self._gui.update_found_words(self._model.get_found_words())
        self.init_cubes()
        self._gui.reset_timer()
        self.play_sound("media/new-round.wav")
        self._gui.party_mode_disabled()
        for index, cube in enumerate(self._gui.cubes):
            row, col = index // BOARD_SIZE, index % BOARD_SIZE  # calc row,col from index
            cube.marked = False
            # revert to the distinct and beloved checkers pattern
            if row % 2 == col % 2:
                cube["bg"] = boggle_gui.REGULAR_COLOR_2
            else:
                cube["bg"] = boggle_gui.REGULAR_COLOR_1

    def party_action(self):
        """
        The party_action method is called when the user turns on the party mode.
        It plays a sound effect and changes the colors of the cubes on the board to random colors.
        """
        self.play_sound("media/wow.mp3")
        self._gui.party_mode_activated()

    def create_start_reset_action(self):
        """
        The create_start_reset_action method is used to create the action for the start/reset button.
        It assigns the start_action method as the action for the button.
        """
        self._gui.buttons["START"].configure(command=self.start_action)

    def create_undo_action(self):
        """
        The create_undo_action method is used to create the action for the undo button.
        It assigns the undo_action method as the action for the button.
        """
        self._gui.buttons["UNDO"].configure(command=self.undo_action)

    def create_pick_action(self):
        """
        Create the action for the 'PICK' button, linking it to the 'pick_action' method.
        """
        self._gui.buttons["PICK"].configure(command=self.pick_action)

    def create_party_action(self):
        """
        Create the action for the 'PARTY' button, linking it to the 'party_action' method.
        """
        self._gui.buttons["PARTY"].configure(command=self.party_action)

    def play_sound(self, soundtrack: str):
        """
        Plays the given sound effect.
        :param soundtrack: str:  path of the sound effect file
        """
        pygame.mixer.music.load(soundtrack)
        pygame.mixer.music.play()

    def run(self) -> None:
        """
        Runs the game by calling the 'run' method of the BoggleGUI object.
        """
        self._gui.run()


if __name__ == '__main__':
    boggle_game = BoggleController()
    # Enjoy :)
    boggle_game.run()
