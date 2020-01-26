import json
from string import ascii_lowercase
from backend import path_handler, card_format

from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.config import Config
Config.set("graphics", "width", "1000")
Config.set("graphics", "height", "600")

story_name = "caveman"


def is_snake_case(string: str):
    valid = ascii_lowercase + "_"
    return all(char in valid for char in string)


class CardAddWindow(Screen):
    @classmethod
    def preview_sound(cls, sound_filename: str):
        full_sound_path = path_handler.get_game_sounds_path(story_name).joinpath(sound_filename)
        if not full_sound_path.is_file():
            print(f"\t Warning, sound file is not found in path:{full_sound_path}\n"
                  f"Continuing but please make sure to add sound file in that path.")
        else:
            # TODO pressing multiple times plays multiples times ><
            sound_file = SoundLoader.load(str(full_sound_path))
            if sound_file:
                sound_file.play()
            else:
                print("Sound file found but could not be played.")

    @classmethod
    def preview_image(cls, image_filename: str):
        full_img_path = path_handler.get_card_art_path(story_name).joinpath(image_filename)
        if not full_img_path.is_file():
            print(f"\t Warning, image file is not found in path:{full_img_path}\n"
                  f"Continuing but please make sure to add image file in that path.")
        else:
            Popup(title="Image preview",
                  content=Image(source=str(full_img_path)),
                  size_hint=(None, None), size=(400, 400)).open()


class GameStatesWindow(Screen):
    with open(path_handler.get_game_state_json_path(story_name)) as f:
        game_states = json.load(f)

    def on_pre_enter(self):
        self.recreate_list()

    def recreate_list(self):
        self.ids.game_states_scroll_list.clear_widgets()

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        for key, value in self.game_states.items():
            btn = Button(text=f"{key} : {value}", size_hint_y=None, height=20)
            layout.add_widget(btn)

        self.ids.game_states_scroll_list.add_widget(layout)

    def add_game_state(self, state_name_key: str, value: str):
        if not state_name_key or not value:
            print("Can't be empty!")
            return
        elif not is_snake_case(state_name_key):
            print("Only lowercase character plus char _ are supported.")
            return
        elif state_name_key in self.game_states:
            print("Key already present!")
            return

        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif "." in value:
            try:
                value = float(value)
            except ValueError:
                pass
        else:
            try:
                value = int(value)
            except ValueError:
                print("Unknown value type.")
                return

        # Class init will error if invalid type
        card_format.GameVariable(state_name_key, value)
        self.game_states.update({state_name_key: value})

        self.recreate_list()


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("editor.kv")


class EditorApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    EditorApp().run()
