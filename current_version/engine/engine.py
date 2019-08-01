from engine.collisions_proc import CollisionsProcessor  # pragma: no cover
from engine.enums import MoveDirection  # pragma: no cover
from engine.helper_funcs import get_x_y_modifiers  # pragma: no cover
from ui.cui import ConsoleUserInterface  # pragma: no cover
from platform import system as platform_system  # pragma: no cover
try:  # pragma: no cover
    from msvcrt import \
        kbhit as msvcrt_kbhit, \
        getch as msvcrt_getch
except ImportError:  # pragma: no cover
    pass
try:  # pragma: no cover
    from curses import \
        noecho as curses_noecho, \
        cbreak as curses_cbreak, \
        initscr as curses_initscr, \
        KEY_DOWN as curses_KEY_DOWN, \
        KEY_LEFT as curses_KEY_LEFT, \
        KEY_RIGHT as curses_KEY_RIGHT, \
        KEY_UP as curses_KEY_UP
except ImportError:  # pragma: no cover
    pass


class GameEngine:  # pragma: no cover # temp pragma
    '''Class realize game engine that moves movable game objects'''
    def __init__(self, game_map):  # pragma: no cover
        self.collisions_proc = CollisionsProcessor(game_map)
        self.moving_objects = []
        for game_object in game_map:
            if game_object.movable:
                self.moving_objects += [game_object]

        self.console_interface = ConsoleUserInterface(game_map)

    def _catch_key(self):  # pragma: no cover
        '''Method awaits hitting on keyboard in endless loop and when key is \
hitted then that key is returned'''
        if platform_system() == 'Linux':
            return self._console_window.getch()
        elif platform_system() == 'Windows':
            if msvcrt_kbhit():
                return msvcrt_getch() + msvcrt_getch()
        else:
            raise OSError("Operational system is not supported for program!")

    def _interpret_catched_key(self, catched_key):  # pragma: no cover
        '''Method interprets catched key to direction or command \
to main game loop'''
        if catched_key == b'\xe0M' or catched_key == curses_KEY_RIGHT:
            return MoveDirection.Right
        elif catched_key == b'\xe0P' or catched_key == curses_KEY_DOWN:
            return MoveDirection.Down
        elif catched_key == b'\xe0K' or catched_key == curses_KEY_LEFT:
            return MoveDirection.Left
        elif catched_key == b'\xe0H' or catched_key == curses_KEY_UP:
            return MoveDirection.Up
        elif catched_key == b'q\x00' or catched_key == 113:
            return 'break'
        else:
            return 'continue'

    def start_game(self):  # pragma: no cover
        '''Main method that realizes main game loop'''
        if platform_system() == 'Linux':
            self._console_window = curses_initscr()
            self._console_window.keypad(True)
            self._console_window.refresh()
            curses_noecho()
            curses_cbreak()
        elif platform_system() == 'Windows':
            global \
                curses_KEY_LEFT, \
                curses_KEY_RIGHT, \
                curses_KEY_DOWN, \
                curses_KEY_UP

            curses_KEY_RIGHT = -1
            curses_KEY_DOWN = -1
            curses_KEY_LEFT = -1
            curses_KEY_UP = -1

        self.console_interface.draw_map()
        while True:
            interpreted_key = self._interpret_catched_key(self._catch_key())
            if interpreted_key not in MoveDirection:
                if interpreted_key == 'continue':
                    continue
                elif interpreted_key == 'break':
                    break
                else:
                    raise ValueError('Key interpreted incorrectly!')

            move_direction = interpreted_key

            x_modifier, y_modifier = get_x_y_modifiers(move_direction)
            if self.collisions_proc.object_on_position_moved(
               self.moving_objects[0].current_position,
               x_modifier, y_modifier):
                self.console_interface.move_object_on_position(
                    self.moving_objects[0].current_position,
                    x_modifier, y_modifier)

                obj_position = self.moving_objects[0].current_position
                self.moving_objects[0].current_position = \
                    (obj_position[0] + x_modifier,
                     obj_position[1] + y_modifier)

            self.console_interface.draw_map()

        self.console_interface.clear_console()
        exit(0)