import tkinter as tki
from typing import Callable, Dict, List, Set, Any
import random

# CONSTANTS
CANVAS_SIZE = 500
BUTTON_HOVER_COLOR = "#979691"
REGULAR_COLOR_1 = "lightgray"
REGULAR_COLOR_2 = "gray"
BUTTON_ACTIVE_COLOR = "lightblue"

BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tki.RAISED,
                "bg": REGULAR_COLOR_1,
                "activebackground": BUTTON_ACTIVE_COLOR}


class BoggleGUI:
    _buttons: Dict[str, tki.Button] = {}
    # _cubes: Dict[str, tki.Button] = {}
    _cubes: List[tki.Button] = []
    _current_time = 0
    _party_mode = 0
    _timer: Any = None
    _word_labels = []

    def __init__(self) -> None:
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

        # frame for sidebar
        self._sidebar_frame = tki.Frame(self._outer_frame)
        self._sidebar_frame.pack(side=tki.RIGHT, fill=tki.BOTH, expand=True)

        self._create_sidebar()
        self._initialize_word_scroll_box()
        self._found_words.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=True)

        # frame for buttons
        self._upper_frame = tki.Frame(self._outer_frame)
        self._upper_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)
        self._create_buttons_in_upper_frame()

        # frame for label
        self._display_label = tki.Label(self._outer_frame, font=("Courier", 30), bg=REGULAR_COLOR_1, width=23,
                                        relief="ridge", text="WELCOME TO BOGGLE")
        self._display_label.pack(side=tki.TOP, fill=tki.BOTH)

        # frame for cubes
        self._lower_frame = tki.Frame(self._outer_frame)
        self._lower_frame.pack(side=tki.TOP, fill=tki.BOTH, expand=True)
        self._create_cubes_in_lower_frame()

        self.meme = tki.PhotoImage(file="media/doge1.gif")

    def run(self):
        self._buttons["START"].configure(state=tki.NORMAL)
        self._main_window.mainloop()

    def set_display(self, display_text: str) -> None:
        self._display_label["text"] = display_text

    def set_score(self, current_score: str) -> None:
        self._score["text"] = current_score

    def set_button_command(self, button_name: str, cmd: Callable) -> None:
        self._buttons[button_name].configure(command=cmd)

    def set_cube_command(self, cube_index, cmd: Callable) -> None:
        self._cubes[cube_index].configure(command=cmd)

    def get_button_chars(self) -> List[str]:
        return list(self._buttons.keys())

    def get_cube_chars(self) -> List[str]:
        return list(self._cubes.keys())

    def _create_sidebar(self) -> None:
        self._score = self._make_score()
        self._timer = self._make_timer()

        self._countdown()

    def _make_score(self):
        score_label = tki.Label(self._sidebar_frame, font=("Courier", 30), bg="#C0C0C0", width=8,
                                relief="ridge", text="SCORE", )
        score_label.pack(side=tki.TOP, fill=tki.X)
        return score_label

    def _make_timer(self):
        timer_label = tki.Label(self._sidebar_frame, font=("Courier", 30), bg="#C0C0C0", width=8,
                                relief="ridge", text="TIMER", )
        timer_label.pack(side=tki.TOP, fill=tki.X)
        return timer_label

    def _countdown(self):
        time_in_format = "0" + str(self._current_time // 60) + ":" + str(self._current_time % 60)
        if self._current_time % 60 < 10:
            time_in_format = "0" + str(self._current_time // 60) + ":" + "0" + str(self._current_time % 60)
        self._timer['text'] = time_in_format
        self.set_clickable_state(self._current_time)
        # call countdown again after 1000ms (1s)
        if self._current_time > 0:
            self._current_time -= 1
        self._main_window.after(1000, self._countdown)
        if self._current_time == 0:
            return

    def reset_timer(self):
        self._current_time = 180

    def _update_found_words(self, word_list):
        # word_label = tki.Label(self._sidebar_frame, font=("Courier", 15), bg=REGULAR_COLOR_1, width=5, relief="ridge",
        #                        text=word)
        self._found_words.configure(state=tki.NORMAL)
        self._found_words.delete("1.0", tki.END)
        self._found_words.insert("1.0", "  WORDS FOUND:\n")
        for word in word_list:
            self._found_words.insert("2.0", "- " + word + "\n")
        self._found_words.configure(state=tki.DISABLED)

    def _initialize_word_scroll_box(self):
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
        for i in range(4):
            tki.Grid.columnconfigure(self._upper_frame, i, weight=1)  # type: ignore

        self._make_button("START", 0, 0)
        self._make_button("UNDO", 0, 1)
        self._make_button("PICK", 0, 2)
        self._make_button("PARTY", 0, 3)

    def _make_button(self, button_word: str, row: int, col: int, rowspan: int = 1, columnspan: int = 1) -> tki.Button:
        button = tki.Button(self._upper_frame, text=button_word, **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self._buttons[button_word] = button

        def _on_enter(event: Any) -> None:
            if self._party_mode:
                button["background"] = self.random_color()
            else:
                button["background"] = BUTTON_HOVER_COLOR

        def _on_leave(event: Any) -> None:
            if self._party_mode:
                button["background"] = self.random_color()
            else:
                button["background"] = REGULAR_COLOR_1

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)
        button.configure(state=tki.DISABLED)
        return button

    def _create_cubes_in_lower_frame(self) -> None:
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
        cube = tki.Button(self._lower_frame, text=cube_chars, **BUTTON_STYLE)
        cube.marked = False
        if row % 2 == col % 2:
            cube["bg"] = REGULAR_COLOR_2
        cube.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self._cubes.append(cube)

        def _on_enter(event: Any) -> None:
            if cube.marked:
                return
            if self._party_mode:
                cube["background"] = self.random_color()
            else:
                cube["background"] = BUTTON_HOVER_COLOR

        def _on_leave(event: Any) -> None:
            if cube.marked:
                return
            if self._party_mode:
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
        self._party_mode = 1
        # self.play_sound("media/cute_song.mp3")
        for cube in self._cubes:
            if cube.marked:
                continue
            cube["bg"] = self.random_color()

        for button in self._buttons.values():
            button["bg"] = self.random_color()
        self._timer["bg"] = self.random_color()
        self._score["bg"] = self.random_color()
        self._found_words["bg"] = self.random_color()
        self._buttons["PARTY"]["image"] = self.meme
        self._display_label["bg"] = self.random_color()

    def party_mode_disabled(self):
        self._party_mode = 0
        # self.play_sound("media/cute_song.mp3")
        for index, cube in enumerate(self._cubes):
            if cube.marked:
                continue
            row, col = index // 4, index % 4
            if row % 2 == col % 2:
                cube["background"] = REGULAR_COLOR_2
            else:
                cube["background"] = REGULAR_COLOR_1

        for button in self._buttons.values():
            button["bg"] = REGULAR_COLOR_1
        self._timer["bg"] = REGULAR_COLOR_1
        self._score["bg"] = REGULAR_COLOR_1
        self._found_words["bg"] = REGULAR_COLOR_1
        self._buttons["PARTY"]["image"] = ""
        self._display_label["bg"] = REGULAR_COLOR_1

    def set_clickable_state(self, mode):
        for cube in self._cubes:
            if mode:
                cube.configure(state=tki.NORMAL)
            else:
                cube.configure(state=tki.DISABLED)
        for name, button in self._buttons.items():
            if name != "START":
                if mode:
                    button.configure(state=tki.NORMAL)
                else:
                    button.configure(state=tki.DISABLED)

    def random_color(self):
        hex_color = ["#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)])]
        return hex_color

    def hue_red_color(self, multipler):
        rgb = 255, max(208 - 13 * multipler, 0), max(208 - 13 * multipler, 0)
        rgb_to_hex = "#" + '%02x%02x%02x' % rgb
        return rgb_to_hex
