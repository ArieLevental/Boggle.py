# BOGGLE

This is a variation of the Boggle board-game, made with python and the tkinter GUI library. There are also some custom features and smart algorithms involved.

## RUN

Use this command from terminal
```bash
python3 boggle.py
```

## GAME WIKI & RULES
[Wikipedia - Boggle](https://en.wikipedia.org/wiki/Boggle)

## SPECIAL FEATURES

We added a special party mode to the game, so you can enjoy it double-time!
Some of the features are a custom button, changing colors, and sound effects.

```python
    def party_mode_activated(self):


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


def random_color(self):
    hex_color = ["#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)])]
    return hex_color


def party_action(self):
    self.play_sound("media/wow.mp3")
    self._gui.party_mode_activated()

```

Added sound to all buttons, using pygame library:
```python
    def play_sound(self, soundtrack: str):
        pygame.mixer.music.load(soundtrack)
        pygame.mixer.music.play()
```
![alt text](https://i.gyazo.com/6982b45ca1c84e2a86b83c5981999440.png)

Custom coloring of default board and smart coloring of picked cube path:

```python
    def hue_red_color(self, multipler):
    rgb = 255, max(208 - 13 * multipler, 0), max(208 - 13 * multipler, 0)
    rgb_to_hex = "#" + '%02x%02x%02x' % rgb
    return rgb_to_hex


def _make_cube(self, cube_chars: str, row: int, col: int, rowspan: int = 1, columnspan: int = 1) -> tki.Button:
    cube = tki.Button(self._lower_frame, text=cube_chars, **BUTTON_STYLE)
    cube.marked = False
    if row % 2 == col % 2:
        cube["bg"] = REGULAR_COLOR_2
    cube.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
    self.cubes.append(cube)
```

## CONTRIBUTING

Project made by Adir Barak and Arie Levental ©

Enjoy the game.