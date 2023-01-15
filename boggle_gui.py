#################################################################
# FILE : boggle_gui.py
# WRITERS : Arie Levental , Arie_Levental , 319142055
#           Adir Barak , adir.barak, 207009739
# EXERCISE : intro2cs1 ex11 2023
# DESCRIPTION: This program runs the game of Boggle
# STUDENTS WE DISCUSSED THE EXERCISE WITH: No-one
# WEB PAGES WE USED: Too many to count.
#################################################################
import tkinter as tki
from typing import Callable, Dict, List, Set, Any
import random

# CONSTANTS
BUTTON_HOVER_COLOR = "#979691"
REGULAR_COLOR_1 = "lightgray"
REGULAR_COLOR_2 = "gray"
BUTTON_ACTIVE_COLOR = "lightblue"
INITIAL_MSG = "WELCOME TO BOGGLE"
BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tki.RAISED,
                "bg": REGULAR_COLOR_1,
                "activebackground": BUTTON_ACTIVE_COLOR}
TIMER_MAX = 180
SEC_IN_MIN = 60
RED_MAX = 255
INITIAL_GREEN = 208
INITIAL_BLUE = 208
GB_DELTA = 13
BOARD_SIZE = 4


class BoggleGUI:
    """
    A class representing the GUI for the Boggle game.
    It creates and manages the GUI elements and interaction with the user.
    """
    buttons: Dict[str, tki.Button] = {}
    cubes: List[tki.Button] = []
    party_mode = 0
    _timer: Any = None
    _current_time = 0

    def __init__(self) -> None:
        """
        Initializes the GUI elements, creates the main window, and sets up the layout of the various frames and widgets.
        """

        root = tki.Tk()
        root.geometry("770x415")
        root.title("BOGGLE © by Adir Barak and Arie Levental")
        root.iconbitmap("media/boggle_color_icon.ico")
        root.resizable(False, False)
        self._main_window = root

        # main frame
        self._outer_frame = tki.Frame(root, bg=REGULAR_COLOR_1, highlightbackground=REGULAR_COLOR_1,
                                      highlightthickness=5)
        self._outer_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)

        # frame for sidebar which includes score count, timer and words list
        self._sidebar_frame = tki.Frame(self._outer_frame)
        self._sidebar_frame.pack(side=tki.RIGHT, fill=tki.BOTH, expand=True)

        self._create_sidebar()
        self._initialize_word_scroll_box()
        self._found_words.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=True)

        # frame for control buttons
        self._upper_frame = tki.Frame(self._outer_frame)
        self._upper_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)
        self._create_buttons_in_upper_frame()

        # frame for display label
        self._display_label = tki.Label(self._outer_frame, font=("Courier", 30), bg=REGULAR_COLOR_1, width=23,
                                        relief="ridge", text=INITIAL_MSG)
        self._display_label.pack(side=tki.TOP, fill=tki.BOTH)

        # frame for game cubes
        self._lower_frame = tki.Frame(self._outer_frame)
        self._lower_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)
        self._create_cubes_in_lower_frame()

        self.meme = tki.PhotoImage(file="media/doge1.gif")

    def run(self):
        """
        Start the main loop of the GUI, allowing the user to interact with it.
        """
        self.buttons["START"].configure(state=tki.NORMAL)
        self._main_window.mainloop()

    def set_display(self, display_text: str) -> None:
        """
        Update the display text on the GUI.
        :param display_text: the new text to display
        """
        self._display_label["text"] = display_text

    def set_score(self, current_score: str) -> None:
        """
        Update the current score displayed on the GUI.
        :param current_score: the new score to display
        """
        self._score["text"] = current_score

    def _create_sidebar(self) -> None:
        """
        Create the sidebar frame and the widgets it contains.
        """
        self._score = self._make_score()
        self._timer = self._make_timer()

        self._countdown()

    def _make_score(self):
        """
        This method creates a score label that displays the current score of the game.
        :return: a tkinter Label widget that represents the score label
        """
        score_label = tki.Label(self._sidebar_frame, font=("Courier", 30), bg="#C0C0C0", width=8,
                                relief="ridge", text="SCORE", )
        score_label.pack(side=tki.TOP, fill=tki.X)
        return score_label

    def _make_timer(self):
        """
        This method creates and returns a tkinter label widget that displays the game timer.
        :return: tkinter label widget that displays the game timer.
        """
        timer_label = tki.Label(self._sidebar_frame, font=("Courier", 30), bg="#C0C0C0", width=8,
                                relief="ridge", text="TIMER", )
        timer_label.pack(side=tki.TOP, fill=tki.X)
        return timer_label

    def _countdown(self):
        """
        Function that updates the timer label and calls itself every second.
        It also calls the _set_clickable_state function to update the buttons' state
        as the time goes on and stops the countdown when the time reaches 0.
        """
        time_in_format = "0" + str(self._current_time // SEC_IN_MIN) + ":" + str(self._current_time % SEC_IN_MIN)
        if self._current_time % SEC_IN_MIN < 10:
            time_in_format = "0" + str(self._current_time // SEC_IN_MIN) + ":" + "0" + str(self._current_time % SEC_IN_MIN)
        self._timer['text'] = time_in_format
        self._set_clickable_state(self._current_time)
        # call countdown again after 1000ms (1s)
        if self._current_time > 0:
            self._current_time -= 1
        self._main_window.after(1000, self._countdown)
        if self._current_time == 0:
            return

    def reset_timer(self):
        """
        Resets the timer to its initial value.
        """
        self._current_time = TIMER_MAX

    def update_found_words(self, word_list):
        """
        Updates the text box that displays the found words.
        :param word_list: List of words found so far
        """
        # word_label = tki.Label(self._sidebar_frame, font=("Courier", 15), bg=REGULAR_COLOR_1, width=5, relief="ridge",
        #                        text=word)
        self._found_words.configure(state=tki.NORMAL)
        self._found_words.delete("1.0", tki.END)
        self._found_words.insert("1.0", "  WORDS FOUND:\n")
        for word in word_list:
            self._found_words.insert("2.0", "- " + word + "\n")
        self._found_words.configure(state=tki.DISABLED)

    def _initialize_word_scroll_box(self):
        """
        Initialize the scroll box for displaying the found words.
        """
        scrollbar = tki.Scrollbar(self._sidebar_frame, orient='vertical')
        scrollbar.pack(side=tki.RIGHT, fill='y')
        # Add some text in the text widget
        self._found_words = tki.Text(self._sidebar_frame, font=("Courier", 15), yscrollcommand=scrollbar.set,
                                     bg=REGULAR_COLOR_1, width=5, relief="ridge")
        self._found_words.insert("1.0", "  WORDS FOUND:\n")
        self._found_words.configure(state=tki.DISABLED)
        found_words = self._found_words.yview
        scrollbar.config(command=found_words)

    def _create_buttons_in_upper_frame(self) -> None:
        """
        Create the buttons in the upper frame of the GUI.
        """
        for i in range(4):
            tki.Grid.columnconfigure(self._upper_frame, i, weight=1)  # type: ignore

        self._make_button("START", 0, 0)
        self._make_button("UNDO", 0, 1)
        self._make_button("PICK", 0, 2)
        self._make_button("PARTY", 0, 3)

    def _make_button(self, button_word: str, row: int, col: int, rowspan: int = 1, columnspan: int = 1) -> tki.Button:
        """
        Creates a button with the given text and style, and adds it to the upper frame at the specified grid position.
        The button is also added to the self.buttons dictionary with its text as the key.
        The button also has hover and leave event handlers to change its background color.
        """
        button = tki.Button(self._upper_frame, text=button_word, **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self.buttons[button_word] = button

        def _on_enter(event: Any) -> None:
            """
            changes the color of the button based on whether party mode is ON/OFF upon entering the button area
            :param event:
            :return:
            """
            if self.party_mode:
                button["background"] = self.random_color()
            else:
                button["background"] = BUTTON_HOVER_COLOR

        def _on_leave(event: Any) -> None:
            """
                changes the color of the button based on whether party mode is ON/OFF upon leaving the button area
            :param event:
            :return:
            """
            if self.party_mode:
                button["background"] = self.random_color()
            else:
                button["background"] = REGULAR_COLOR_1

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)
        button.configure(state=tki.DISABLED)
        return button

    def _create_cubes_in_lower_frame(self) -> None:
        """
        Creates the cubes (which are buttons) in the lower frame, with a grid layout.
        The cubes also have hover and leave event handlers to change their background color.
        """
        for i in range(4):
            tki.Grid.columnconfigure(self._lower_frame, i, weight=1)  # type: ignore

        for i in range(4):
            tki.Grid.rowconfigure(self._lower_frame, i, weight=1)  # type: ignore

        self._make_cube("A", 0, 0)
        self._make_cube("B", 0, 1)
        self._make_cube("C", 0, 2)
        self._make_cube("D", 0, 3)
        self._make_cube("E", 1, 0)
        self._make_cube("F", 1, 1)
        self._make_cube("G", 1, 2)
        self._make_cube("H", 1, 3)
        self._make_cube("I", 2, 0)
        self._make_cube("J", 2, 1)
        self._make_cube("K", 2, 2)
        self._make_cube("L", 2, 3)
        self._make_cube("M", 3, 0)
        self._make_cube("N", 3, 1)
        self._make_cube("O", 3, 2)
        self._make_cube("P", 3, 3)

    def _make_cube(self, cube_chars: str, row: int, col: int, rowspan: int = 1, columnspan: int = 1) -> tki.Button:
        """
        Creates a game cube represented by a tkinter button object, and adds the cube to the cubes_list.
        :return:
        """
        cube = tki.Button(self._lower_frame, text=cube_chars, **BUTTON_STYLE)
        cube.marked = False
        if row % 2 == col % 2:
            cube["bg"] = REGULAR_COLOR_2
        cube.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self.cubes.append(cube)

        def _on_enter(event: Any) -> None:
            """
            changes the color of the cube based on whether party mode is ON/OFF upon entering the cube area
            :param event:
            :return:
            """
            if cube.marked:
                return
            if self.party_mode:
                cube["background"] = self.random_color()
            else:
                cube["background"] = BUTTON_HOVER_COLOR

        def _on_leave(event: Any) -> None:
            """
            changes the color of the cube based on whether party mode is ON/OFF upon leaving the cube area
            :param event:
            :return:
            """
            if cube.marked:
                return
            if self.party_mode:
                cube["background"] = self.random_color()
            else:
                if row % 2 == col % 2:
                    cube["background"] = REGULAR_COLOR_2
                else:
                    cube["background"] = REGULAR_COLOR_1

        cube.bind("<Enter>", _on_enter)
        cube.bind("<Leave>", _on_leave)
        cube.configure(state=tki.DISABLED)
        return cube

    def party_mode_activated(self):
        """
        Activates party mode, which changes the background color of the buttons and cubes to a random color.
        """
        self.party_mode = 1
        # self.play_sound("media/cute_song.mp3")
        for cube in self.cubes:
            if cube.marked:
                continue
            cube["bg"] = self.random_color()

        for button in self.buttons.values():
            button["bg"] = self.random_color()
        self._timer["bg"] = self.random_color()
        self._score["bg"] = self.random_color()
        self._found_words["bg"] = self.random_color()
        self.buttons["PARTY"]["image"] = self.meme
        self._display_label["bg"] = self.random_color()

    def party_mode_disabled(self):
        """
        Disables the party mode, and return all colors to regular coloring.
        """
        self.party_mode = 0
        # self.play_sound("media/cute_song.mp3")
        for index, cube in enumerate(self.cubes):
            if cube.marked:
                continue
            row, col = index // BOARD_SIZE, index % BOARD_SIZE
            if row % 2 == col % 2:
                cube["background"] = REGULAR_COLOR_2
            else:
                cube["background"] = REGULAR_COLOR_1

        for button in self.buttons.values():
            button["bg"] = REGULAR_COLOR_1
        self._timer["bg"] = REGULAR_COLOR_1
        self._score["bg"] = REGULAR_COLOR_1
        self._found_words["bg"] = REGULAR_COLOR_1
        self.buttons["PARTY"]["image"] = ""
        self._display_label["bg"] = REGULAR_COLOR_1

    def _set_clickable_state(self, mode):
        """
        This function freezes the game while timer count is at 0, only the Start/Reset button will be available to click
        """
        for cube in self.cubes:
            if mode:
                cube.configure(state=tki.NORMAL)
            else:
                cube.configure(state=tki.DISABLED)
        for name, button in self.buttons.items():
            if name != "START":
                if mode:
                    button.configure(state=tki.NORMAL)
                else:
                    button.configure(state=tki.DISABLED)

    def random_color(self):
        """
        generates a random hex color
        :returns a string descring a hex color:
        """
        hex_color = ["#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)])]
        return hex_color

    def hue_red_color(self, multipler):
        """
        generates a red hue in rgb format then translates it to hex and returns the hex color
        :param multipler: an int (1-16)
        :returns a string descring a hex color:
        """
        # make the red stronger and brighter when the multiplier is a bigger number
        rgb = RED_MAX, max(INITIAL_GREEN - GB_DELTA * multipler, 0), max(INITIAL_BLUE - GB_DELTA * multipler, 0)
        # translates rgb to hex by well known formula
        rgb_to_hex = "#" + '%02x%02x%02x' % rgb
        return rgb_to_hex
