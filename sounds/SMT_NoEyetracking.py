# -*- coding: utf-8 -*-

#################################################################################################################
# from __future__ import absolute_import, division, print_function
from get_puzzle_boards import GetPuzzleBoards
import random
import os
import numpy as np
import time
from psychopy import visual
from psychopy import event
from psychopy import sound
from psychopy import core
from psychopy import prefs
import pandas as pd
import csv
prefs.general['audioLib'] = ['pyo']

# import needed modules
import tobii_research as tr

#################################################################################################################
# PARAMETERS

# We can use display to find info for the Window creation, like the resolution
# Specify display resolution

WIDTH = 2560/2
HEIGHT = 1600/2

PUZZLE_BOARD_WIDTH = HEIGHT - 200

print(WIDTH, HEIGHT)

# Gem parameters
POLYGON_LIST = [3, 4, 5, 6, 7, 8, 9, 10, 11]  # list of polygons -> will set number of edges
# color list for polygons
COLOR_LIST = ['#1E3AFF', '#7AFFDF', '#60FF01', '#EFFF07', '#FF6100', '#FF0300', '#B92EFF', '#DCD9DE']
GEM_LIST = [0, 1, 2, 3, 4, 5, 6, 7]  # list of gem types

# Puzzle board parameters
BOARD_HEIGHT_LIST = [4, 5, 6, 7, 8]
BOARD_WIDTH_LIST = [4, 5, 6, 7, 8]
BOARD_COLOR = 'DimGray'
BACKGROUND_COLOR = 'black'

# fixation presentation duration
FIXATION_PT = 1

# time to swap gems
SWAP_TIME = 0.5

#######################################################################################################################

# MATCH PATTERNS FOR PATTERN DETECTION

# M3, S, M2 = gems[0], gems[1], gems[2]
horizontal_v = {'horizontal_v_three_bottom': [(0, 2), (1, 1), (0, 1)],
                'horizontal_v_three_top': [(0, 2), (-1, 1), (0, 1)]}

vertical_v = {'vertical_v_three_left': [(2, 0), (1, -1), (1, 0)],
              'vertical_v_three_right': [(2, 0), (1, 1), (1, 0)]}

horizontal_i = {'horizontal_i_three_left': [(0, 1), (0, -2), (0, -1)],
                'horizontal_i_three_right': [(0, 1), (0, 3), (0, 2)]}

vertical_i = {'vertical_i_three_top': [(1, 0), (-2, 0), (-1, 0)],
              'vertical_i_three_bottom': [(1, 0), (3, 0), (2, 0)]}

horizontal_j = {'horizontal_j_three_top_right': [(0, 1), (-1, 2), (0, 2)],
                'horizontal_j_three_bottom_right': [(0, 1), (1, 2), (0, 2)],
                'horizontal_j_three_top_left': [(0, 1), (-1, -1), (0, -1)],
                'horizontal_j_three_bottom_left': [(0, 1), (1, -1), (0, -1)]}

vertical_j = {'vertical_j_three_top_right': [(1, 0), (-1, 1), (-1, 0)],
              'vertical_j_three_bottom_right': [(1, 0), (2, 1), (2, 0)],
              'vertical_j_three_top_left': [(1, 0), (-1, -1), (-1, 0)],
              'vertical_j_three_bottom_left': [(1, 0), (2, -1), (2, 0)]}

target_pattern_list = [horizontal_v, vertical_v,
                       horizontal_i, vertical_i,
                       horizontal_j, vertical_j]

false_rightAngle = {'false_A_1': [(-1, 0), (0, 1)], 'false_A_2': [(0, 1), (1, 0)],
                    'false_A_3': [(1, 0), (0, -1)], 'false_A_4': [(0, -1), (-1, 0)]}

false_LShape = {'false_B_1': [(0, 1), (-2, 0)], 'false_B_2': [(0, -1), (-2, 0)],
                'false_B_3': [(0, -1), (2, 0)], 'false_B_4': [(0, 1), (2, 0)]}

false_skip = {'false_C_1': [(0, 1), (-2, 0), (-3, 0)], 'false_C_2': [(0, -1), (-2, 0), (-3, 0)],
              'false_C_3': [(0, -1), (2, 0), (3, 0)], 'false_C_4': [(0, 1), (2, 0), (3, 0)]}

distractor_patterns_list = [false_rightAngle, false_LShape, false_skip]

#######################################################################################################################

# READ PUZZLE LEVELS

def random_shuffle_dict(puzzle_dict):
    keys = list(puzzle_dict.keys())  # Python 3; use keys = puzzle_dict.keys() in Python 2
    random.shuffle(keys)
    return dict([(key, puzzle_dict[key]) for key in keys])

# variable to set how many times trials of a level are shown
TRIALS_PER_LEVEL = 1
# GET READY-MADE PUZZLE LEVELS
gpb = GetPuzzleBoards()

## (A) PUZZLE TRAINING LEVELS

# create dict with puzzle levels
# 'PuzzleLevels_long' 'PuzzleLevels_medium' 'PuzzleLevels_short'
training_level_list = gpb.read_puzzle_levels(LEVELS_PATH='PuzzleLevels\Training_Trials')  # make list with all txt level files
# print(level_list)
training_puzzle_dict = gpb.puzzle_set(level_list=training_level_list)  # make dict with all boards
training_set = gpb.create_test_set(training_puzzle_dict, n_repetitions=1)

import collections
training_set = collections.OrderedDict(sorted(training_set.items()))
print(training_set)

# create dict with puzzle levels
# 'PuzzleLevels_long' 'PuzzleLevels_medium' 'PuzzleLevels_short'
level_list = gpb.read_puzzle_levels(LEVELS_PATH='PuzzleLevels\Short_A')  # make list with all txt level files
puzzle_dict = gpb.puzzle_set(level_list=level_list)  # make dict with all boards
test_set = gpb.create_test_set(puzzle_dict, n_repetitions=TRIALS_PER_LEVEL)
# randomly shuffle selected level trials
TEST_SET = random_shuffle_dict(puzzle_dict=test_set)
print(len(TEST_SET))

#######################################################################################################################

# find eye trackers
found_eyetrackers = tr.find_all_eyetrackers()
# select first eye tracker
my_eyetracker = found_eyetrackers[0]
my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)

# create list in which we append gaze data
gaze_list = []

# create call back to get gaze data
"""
GAZE DATA
device_time_stamp = Gets the time stamp according to the eye tracker's internal clock.
system_time_stamp = Gets the time stamp according to the computer's internal clock.
left_eye = Gets the gaze data for the left eye as an EyeData object.
right_eye = Gets the gaze data for the right eye as an EyeData object.
GAZE POINT
position_on_display_area = Gets the normalized gaze point position in 2D on the active display area as a two valued tuple.
validity = Gets the validity of the gaze point data
PUPIL DATA
diameter = Gets the diameter of the pupil in millimeters.
validity = Gets the validity of the pupil data.
"""

from collections import deque


class DataCollector(object):

    levels = deque()
    move_buffer = deque()
    frame_buffer = deque()

    @staticmethod
    def append_frame(frame):
        DataCollector.frame_buffer.append(frame)

    @staticmethod
    def next_move(move_name, move_status, hint):
        temp = DataCollector.frame_buffer.__copy__()
        move = {"name": move_name,
                "status": move_status,
                "hint": hint,
                "data": temp}
        DataCollector.move_buffer.append(move)
        DataCollector.frame_buffer.clear()

    @staticmethod
    def next_level(level_name, task_condition):
        temp = DataCollector.move_buffer.__copy__()
        level = {"name": level_name,
                 "condition": task_condition,
                 "moves": temp}
        DataCollector.levels.append(level)
        DataCollector.move_buffer.clear()

# create call back to get gaze data
def gaze_data_callback(gaze_data):
    # append ts, gpl and gpr
    DataCollector.append_frame((time.time(),
                                gaze_data['system_time_stamp'],
                                gaze_data['device_time_stamp'],
                                gaze_data['left_gaze_point_on_display_area'],
                                gaze_data['right_gaze_point_on_display_area']))
    # ))
######################################################################################################################

class SearchMatchTask:

    def __init__(self):

        # set psychopy window
        self.window = visual.Window([WIDTH, HEIGHT], monitor="testMonitor", units="pix",
                                    color=BACKGROUND_COLOR, winType='pyglet', fullscr=True)

        self.practice_message = u'Übungsdurchgang'
        self.test_message = u'Testdurchgang'

        # INSTRUCTIONS (german)
        self.instruction_message = u'INSTRUKTION \n\n'\
                           u'Versuchen Sie die Position zweier benachbarter Spielsteine auszutauschen um' \
                                   u' drei gleichartige Spielsteine horizontal oder vertikal in eine' \
                                   u' Reihe zu bringen, d.h. einen Match machen .\n\n' \
                                   u'Sie dürfen jederzeit den HINWEIS Knopf drücken, wenn Sie nicht mehr' \
                                   u' weiterkommen.\n\n' \
                                   u'Nach jeweils vier Matches bitten wir Sie die Schwierigkeit des gespielten' \
                                   u' Levels auf einer Skala von 1 (sehr einfach) bis 10 (sehr schwierig)' \
                                   u' einzuschätzen.\n\n'

        # set hint button positions
        self.button_width, self.button_height = WIDTH / 10, HEIGHT / 16
        button_pos_x = PUZZLE_BOARD_WIDTH/2 + self.button_height
        # set up hint button and hint text
        self.help_button = visual.Rect(self.window, units='pix', pos=(0, -button_pos_x),
                                       width=self.button_width, height=self.button_height,
                                       fillColor='white', lineColor=None)
        self.help_text = visual.TextStim(self.window, 'Hinweis', color='black', units='pix',
                                         height=self.button_height/2, pos=(0, -button_pos_x))

        # create fixation cross
        self.fixation = visual.TextStim(self.window, text='+', pos=(0.0, 0.0), depth=0, rgb=None, color='white',
                                        colorSpace='rgb', opacity=1.0, contrast=1.0, units='', ori=0.0, height=40)

        # create rating scale
        self.labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.difficulty_rating_scale = visual.RatingScale(win=self.window, name='difficulty rating',
                                                          precision=10, low=1, high=10, choices=self.labels,
                                                          marker='glow', scale=None, labels=['Sehr einfach = 1',
                                                                                               'Sehr schwierig = 10'],
                                                          showValue=True, markerExpansion=20)


        self.text = 'Bitte geben Sie an, wie Sie die Schwierigkeit des gespielten Puzzles empfunden haben'
        self.difficulty_question = visual.TextStim(self.window, text=self.text, height=30, units='pix',
                                                   rgb=None, color='white',
                                                   alignHoriz='center', alignVert='center')

        self.time = core.Clock()

        # get sounds
        self.gem_sound = sound.Sound(value='sounds/gem.wav')
        self.match_sound = sound.Sound(value='sounds/match.wav')
        self.error_sound = sound.Sound(value='sounds/falsch.wav')

        self.behavioral_data = []
        # self.eye_tracking_data = []
        self.movie_frame_dict = {}

        self.match_wait_time = 0.25

        self.mouse = event.Mouse()
        self.mouse_down_counter = 0

        self.current_polygon_list = []
        self.current_hint_mark_list = []
        self.puzzle_board_coords = None
        self.match_three_coords = []

        self.polygon_size = None
        self.hint_x, self.hint_y = None, None
        self.x_positions = None
        self.y_positions = None

        self.clicked_tiles_list = []
        self.swapped = False
        self.cell_size = None

        self.participant_no = None
        self.level_number = None
        self.level_specs = None
        self.task_condition = None

        self.puzzle_level_number = None
        self.puzzle_condition = None  # [Training, Test]
        self.puzzle_width = None
        self.puzzle_height = None
        self.puzzle_tile_number = None
        self.puzzle_tile_size = None
        self.puzzle_move_number = None
        self.puzzle_reaction_time = None  # time to solve all four moves
        self.puzzle_difficulty_rating = None
        self.puzzle_number_errors = None  # number of invalid moves
        self.puzzle_number_moves = None  # update number of moves per puzzle (min. 4)

        self.trial_data_file_name = None
        self.trial_hint_used = 'start'
        self.trial_move_type = 'start'  # [valid, invalid]
        self.trial_target_type = None
        self.trial_target_pattern = None
        self.trial_target_coordinates = None
        self.trial_number_distractors = None
        self.trial_search_time = 0
        self.trial_onset_time = 0
        self.trial_offset_time = 0

    def draw_board_background(self, x, y, cell_size):
        # color background with BACKGROUND_COLOR
        self.window.color = BACKGROUND_COLOR
        # draw grey background
        rect = visual.Rect(self.window, width=(x * cell_size), height=(y * cell_size),
                           fillColor=BOARD_COLOR, lineColor=BOARD_COLOR)
        rect.draw()

    def grid_positions(self, max_res, x, y):
        # cell size = divide WIDTH by
        self.cell_size = PUZZLE_BOARD_WIDTH / max_res
        polygon_size = self.cell_size * 0.85
        x_max = ((x - 1) * self.cell_size) / 2
        x_min = -1 * ((x - 1) * self.cell_size) / 2
        y_max = ((y - 1) * self.cell_size) / 2
        y_min = -1 * ((y - 1) * self.cell_size) / 2

        self.x_positions = list(np.linspace(x_min, x_max, x))
        self.y_positions = list(np.linspace(y_min, y_max, y))

        return self.cell_size, self.x_positions, self.y_positions, polygon_size

    def draw_board(self, grid, height, width):
        # run grid_positions function
        self.cell_size, x_pos, y_pos, polygon_size = self.grid_positions(max_res=max(width, height), x=width, y=height)
        # draw background
        self.draw_board_background(x=width, y=height, cell_size=self.cell_size)
        # list to hold tiles (polygons) filled in grid
        self.current_polygon_list = []
        # list to hold current grid
        puzzle_array = []
        counter = 0  # counter for cell index
        # Draw the grid
        for row in range(height):
            row_list = []
            for column in range(width):
                y, x = -1 * (y_pos[row]), x_pos[column]
                row_list.append((x, y))
                cell = grid[row][column]
                cell = int(cell)
                self.show_polygon(pg=POLYGON_LIST[cell], pg_size=polygon_size,
                                  color=COLOR_LIST[cell], x=x, y=y, key=counter)
                counter += 1
            puzzle_array.append(row_list)

        self.help_button.draw()
        self.help_text.draw()

        self.puzzle_board_coords = puzzle_array
        self.window.flip()

    def show_polygon(self, pg, pg_size, color, x, y, key):
        self.polygon_size = pg_size
        # move triangle up
        if pg == 3:
            polygon = visual.Polygon(self.window, edges=pg, size=[pg_size, pg_size],
                                     fillColor=color, lineColor=color,
                                     pos=(x, y - (pg_size / 6)), units="pix", name=key)
            self.current_polygon_list.append(polygon)
        else:
            polygon = visual.Polygon(self.window, edges=pg, size=[pg_size, pg_size],
                                     fillColor=color, lineColor=color, pos=(x, y), units="pix", name=key)
            # add each polygon on the board to polygon list
            self.current_polygon_list.append(polygon)
        # draw the text stim
        polygon.draw()

    def check_for_chains(self, grid, grid_h, grid_w):
        # variable for whether chains (X-X-X) is True or False
        chains = False
        # check for horizontal matches (row)
        for i in grid:
            for idx, j in enumerate(i):
                if idx >= 2:
                    if i[idx] == i[idx - 1] == i[idx - 2]:
                        # self.match_three_coords.append([(i, i), (i, (i-1)), (i, (i-2))])
                        chains = True
        # check for vertical matches (column)
        for i in range(grid_w):
            column = []
            for j in range(grid_h):
                v = grid[j][i]
                column.append(v)
            for idx, c in enumerate(column):
                if idx >= 2:
                    if column[idx] == column[idx - 1] == column[idx - 2]:
                        # self.match_three_coords.append((column[idx], column[idx - 1], column[idx - 2]))
                        chains = True
        # only carry on if there are not three identical matches in a vertical/horizontal row
        if chains is True:
            return True
        else:
            return False

    def tiles_adjacent(self, pos1, pos2):
        # check whether clicked tiles are adjacent on x-axis
        if pos2[0] == pos1[0]:
            if pos2[1] + 1 == pos1[1]:
                return True
            elif pos2[1] - 1 == pos1[1]:
                return True
        # check whether clicked tiles are adjacent on y-axis
        if pos2[1] == pos1[1]:
            if pos2[0] + 1 == pos1[0]:
                return True
            elif pos2[0] - 1 == pos1[0]:
                return True
        else:
            return False

    def create_blank_puzzle_board(self, board_h, board_w):
        blank_puzzle_board = np.zeros((board_h, board_w), dtype=object)  # create array of zeros
        blank_puzzle_board.fill('X')  # file with empty cells (-1)
        return blank_puzzle_board

    def polygons_grid(self, polygons, width, height):
        empty_grid = self.create_blank_puzzle_board(board_h=height, board_w=width)
        for pg in polygons:
            w, h = self.get_polygon_coordinates(cell=pg.name, width=width)
            empty_grid[h][w] = str(pg.edges - 3)
        # print('polygons grid', empty_grid)
        return empty_grid

    def get_polygon_coordinates(self, cell, width):
        x = cell % width  # % is the "modulo operator", the remainder of i / width;
        y = cell / width  # / is an integer division
        return x, y

    def redraw_polygons(self, width, height):
        self.window.flip()
        # re-draw background
        self.draw_board_background(x=width, y=height, cell_size=self.cell_size)
        # re-draw polygons
        for polygon in self.current_polygon_list:
            polygon.draw()

        self.help_button.draw()
        self.help_text.draw()

        # update on window
        self.window.flip()

    def redraw_polygons_hint_marker(self, width, height):
        # re-draw background
        self.draw_board_background(x=width, y=height, cell_size=self.cell_size)
        # re-draw hint markers
        # print('drawing markers')
        # print
        for rect in self.current_hint_mark_list:
            rect.draw()
        # re-draw polygons
        for polygon in self.current_polygon_list:
            polygon.draw()

        self.help_button.draw()
        self.help_text.draw()

        # update on window
        self.window.flip()

    def draw_help_button(self):
        # update on window
        self.window.flip()

    def make_swap(self, current_polygon, previous_polygon, width, height):

        current_polygon_name = current_polygon.name
        previous_polygon_name = previous_polygon.name

        current_polygon.name = previous_polygon_name
        previous_polygon.name = current_polygon_name

        curr_pos, prev_pos = current_polygon.pos, previous_polygon.pos

        if current_polygon.edges == 3:
            if previous_polygon.edges == 3:
                current_polygon.pos = prev_pos
                previous_polygon.pos = curr_pos

            elif previous_polygon.edges != 3:
                current_polygon.pos = (prev_pos[0], (prev_pos[1] - (self.polygon_size / 6)))
                previous_polygon.pos = (curr_pos[0], (curr_pos[1] + (self.polygon_size / 6)))

        elif previous_polygon.edges == 3:
            if current_polygon.edges != 3:
                current_polygon.pos = (prev_pos[0], (prev_pos[1] + (self.polygon_size / 6)))
                previous_polygon.pos = (curr_pos[0], (curr_pos[1] - (self.polygon_size / 6)))
        else:
            current_polygon.pos = prev_pos
            previous_polygon.pos = curr_pos

        self.redraw_polygons(width, height)

        core.wait(SWAP_TIME)

    def swap_tiles(self, width, height):

        previous_mouse_down = False
        self.mouse_down_counter = 0
        help_button_pressed = False
        self.trial_hint_used = 'no hint'

        # main loop while no swap has been made
        while not self.swapped:
            # get mouse clicks
            mouse_down = self.mouse.getPressed()[0]
            # self.mouse.clickReset()
            # allow to abort if ESC is pressed
            if 'escape' in event.getKeys():
                self.save_task_data(data_list=self.behavioral_data)
                self.eye_tracking_data(data_container=DataCollector.levels)
                print(DataCollector.levels)
                core.quit()
            # check whether hint button gets pressed
            if self.mouse.isPressedIn(self.help_button):
                help_button_pressed = True
                if help_button_pressed:
                    self.trial_hint_used = 'hint'
                    self.mark_hint(self.trial_target_coordinates)
            # loop every polygon
            for polygon in self.current_polygon_list:
                # check whether polygon gets clicked
                if mouse_down and not previous_mouse_down and self.mouse.isPressedIn(polygon):
                    # TODO: when only one is clicked and then wait and then do match
                    self.gem_sound.play()
                    self.clicked_tiles_list.append(polygon)
                    self.mouse_down_counter += 1
                    # if two polygons get clicked consecutively
                    if self.mouse_down_counter > 1 and self.mouse.isPressedIn(polygon):
                        previous_polygon = self.clicked_tiles_list[(self.mouse_down_counter - 2)]
                        pos_1 = self.get_polygon_coordinates(cell=previous_polygon.name, width=width)
                        pos_2 = self.get_polygon_coordinates(cell=polygon.name, width=width)
                        # check whether the two clicked polygons are adjacent
                        if self.tiles_adjacent(pos1=pos_1, pos2=pos_2):
                            # if tiles are adjacent / neighbours -> swap their places
                            self.make_swap(current_polygon=polygon, previous_polygon=previous_polygon,
                                           width=width, height=height)
                            grid = self.polygons_grid(polygons=self.current_polygon_list, width=width, height=height)
                            # go on to check if swapped tiles create a match -> if so continue to next trial
                            if self.check_for_chains(grid=grid, grid_h=height, grid_w=width):
                                # TODO: make match square
                                self.trial_move_type = 'valid'
                                self.puzzle_number_moves += 1
                                self.trial_offset_time = self.time.getTime()
                                self.trial_search_time = (self.trial_offset_time - self.trial_onset_time)
                                self.get_task_data()
                                core.wait(self.match_wait_time)
                                self.match_sound.play()
                                del self.clicked_tiles_list[:]
                                self.mouse_down_counter = 0
                                self.swapped = True  # get out of loop and play next trial
                            else:  # if no match -> swap tiles back and play trial again
                                self.trial_move_type = 'invalid-adjacent'
                                self.puzzle_number_moves += 1
                                self.puzzle_number_errors += 1
                                self.trial_offset_time = self.time.getTime()
                                self.trial_search_time = (self.trial_offset_time - self.trial_onset_time)
                                self.get_task_data()
                                self.error_sound.play()
                                self.mouse_down_counter = 0
                                del self.clicked_tiles_list[:]
                                self.make_swap(current_polygon=previous_polygon, previous_polygon=polygon,
                                               width=width, height=height)
                        else:  # if tiles are not adjacent -> don't swap them
                            self.trial_move_type = 'invalid-non-adjacent'
                            self.puzzle_number_moves += 1
                            self.puzzle_number_errors += 1
                            self.trial_offset_time = self.time.getTime()
                            self.trial_search_time = (self.trial_offset_time - self.trial_onset_time)
                            self.get_task_data()
                            self.mouse_down_counter = 0
                            del self.clicked_tiles_list[:]
                            self.error_sound.play()
            previous_mouse_down = mouse_down

    def check_valid_boundary(self, i, j, x, y, min_h, min_w, max_h, max_w):
        # checks boundaries - whether any given pattern fits in grid at given position (i, j)
        if (i + x) >= min_h:
            if (j + y) >= min_w:
                if (i + x) <= max_h:
                    if (j + y) <= max_w:
                        return True
        else:
            return False

    def get_potential_match_patterns(self, grid, match_pattern_list):
        # make copy of grid to prevent any overwrite
        puzzle_board = grid.copy()
        board_h, board_w = puzzle_board.shape[0], puzzle_board.shape[1]
        coordinates_list = []
        pattern_type = None
        # check swaps horizontally (vertically if inverse)
        for i in range(board_h):
            for j in range(board_w):
                # loop through all match patterns
                for match_patterns in match_pattern_list:
                    for key, gems in sorted(match_patterns.items()):
                        pattern_coord_list = []
                        pattern_coord_list.append((i, j))
                        pattern_state = True  # set True to check whether each gem in pattern matches
                        for gem in gems[:-1]:  # [M, M, ..., S] don't use swap - last in pattern list
                            if self.check_valid_boundary(i=i, j=j, x=gem[0], y=gem[1], min_h=0, max_h=board_h - 1,
                                                         min_w=0, max_w=board_w - 1):
                                if puzzle_board[i][j] == puzzle_board[i + gem[0]][j + gem[1]]:
                                    pattern_coord_list.append((i + gem[0], j + gem[1]))
                                else:
                                    pattern_state = False
                            else:
                                pattern_state = False
                        if pattern_state:  # if match is found, add to lists
                            pattern_coord_list.append((i + gems[-1][0], j + gems[-1][1]))
                            pattern_type = key
                            coordinates_list = pattern_coord_list
        return pattern_type, coordinates_list

    def mark_hint(self, coords):
        line_width = 3
        self.current_hint_mark_list[:] = []
        # coord = (height, width)
        for coord in coords[:-1]:
            cell_number = (coord[0]*self.puzzle_width) + coord[1]
            pos_x, pos_y = self.current_polygon_list[cell_number].pos[0], self.current_polygon_list[cell_number].pos[1]
            if self.current_polygon_list[cell_number].edges == 3:
                rect = visual.Rect(self.window, width=self.cell_size, height=self.cell_size,
                                   pos=(pos_x, pos_y + (self.cell_size / 6)), lineWidth=line_width, lineColor='white',
                                   lineColorSpace='rgb', fillColor=None)
                self.current_hint_mark_list.append(rect)
            else:
                rect = visual.Rect(self.window, width=self.cell_size, height=self.cell_size,
                                   pos=(pos_x, pos_y), lineWidth=line_width, lineColor='white',
                                   lineColorSpace='rgb', fillColor=None)
                self.current_hint_mark_list.append(rect)
        self.redraw_polygons_hint_marker(width=self.puzzle_width, height=self.puzzle_height)
        core.wait(0.1)

    def get_task_data(self):

        data_list = [time.time(), self.task_condition, self.puzzle_level_number, self.puzzle_move_number,
                     self.puzzle_width, self.puzzle_height, self.puzzle_tile_number,
                     self.trial_search_time, self.trial_move_type, self.puzzle_number_moves, self.puzzle_number_errors,
                     self.trial_hint_used, self.trial_target_pattern, self.trial_target_coordinates]
        self.behavioral_data.append(data_list)

        print(data_list)

        # print('Condition:', self.task_condition, 'Level: ', self.puzzle_level_number, 'Move: ', self.puzzle_move_number,
        #       'Width: ', self.puzzle_width, 'Width: ', self.puzzle_height, 'Tile: ', self.puzzle_tile_number,
        #       'Search Time: ', self.trial_search_time, 'Trial Move: ', self.trial_move_type,
        #       'Moves: ', self.puzzle_number_moves, 'Errors: ', self.puzzle_number_errors, 'Hint:', self.trial_hint_used,
        #       'Target pattern: ', self.trial_target_pattern, 'Target Coords: ', self.trial_target_coordinates
        #       )

    def save_task_data(self, data_list):

        headers = ['Timestamp', 'Condition', 'Level', 'Move', 'Width', 'Height', 'Gems',
                   'SearchTime', 'TrialMove', 'NumberMoves', 'NumberInvalidMoves', 'Hint',
                   'TargetPattern', 'TargetPatternCoords']
        np.savetxt("Puzzle_behavioural_data.csv", data_list, delimiter=",")

    def eye_tracking_data(self, data_container):
        for level in data_container:  # level contains: name, condition, moves

            level_name = level["name"]
            level_condition = level["condition"]
            level_moves = level["moves"]
            # create folder for each level
            folder_name = level_condition + '_' + level_name
            print(level_name, level_condition)

            for move in level_moves:  # moves contains: name, status, hint and data (eyetracking)
                move_number = move["name"]
                move_status = move["status"]
                move_hint = move["hint"]
                move_data = move["data"]

                print(move_number, move_status, move_hint)
                names = [level_condition, level_name, move_number, move_status, move_hint]
                eye_data_file_name = '_'.join([str(x) for x in names])
                df = pd.DataFrame.from_records(list(move_data))
                df.astype(str).to_csv(os.path.join('DATA', eye_data_file_name), header=False, index=False,
                                      doublequote=False, sep=';')

    def make_screenshot(self):

        level = str(self.puzzle_width) + '_' + str(self.puzzle_height) + '_' + str(self.puzzle_tile_number)
        img_name = self.task_condition + '_' + level + '_' + str(self.puzzle_move_number) + '_' + \
                   self.trial_move_type + '_' + self.trial_hint_used
        #level_condition, level_name, move_number, move_status, move_hint
        # self.trial_data_file_name + '_' + self.trial_move_type + '_' + self.trial_hint_used + '_' + str(time_stamp)

        # make a screen shot of the window using getMovieFrame function
        screen_shot = self.window.getMovieFrame()
        # append to list

        self.movie_frame_dict[img_name] = screen_shot

    def save_screen_shots(self):
        for file_name, screen_shot in self.movie_frame_dict.items():
            screen_shot.save(('DATA/' + file_name +'.png'))

    def show_instruction(self, text, fontsize):
        # create text stim
        self.instruction = visual.TextStim(self.window, text, height=fontsize, rgb=None, color='white',
                                           alignHoriz='center', wrapWidth=(WIDTH-200), alignVert='center')
        # draw the text stim
        self.instruction.draw()
        self.window.flip()
        # wait for user input
        event.waitKeys(keyList='return')

    def play_puzzles(self, test_puzzles):
        # Run Trials.....
        t = 0
        running_experiment = True
        while running_experiment:
            # (1) loop all levels
            for level, level_dict in test_puzzles.items():

                # start getting gaze data
                my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

                t += 1
                # get level variables
                self.puzzle_level_number = level.split('_')[0]
                self.level_specs = level.split('\\')[-1]

                # assign puzzle parameters
                self.puzzle_width, self.puzzle_height, self.puzzle_tile_number = \
                    level.split('_')[-2], level.split('_')[-3], level.split('_')[-1]
                # reset move level variables
                self.puzzle_number_errors = 0  # reset error counter before every new trial
                self.puzzle_number_moves = 0  # reset move counter before every new trial
                # show fixation cross at beginning of every new level
                self.fixation.draw()
                self.window.flip()
                core.wait(FIXATION_PT)  # set presentation time in Parameters
                # (2) loop trials per level -> set with TRIALS_PER_LEVEL
                for trial, trial_dict in level_dict.items():
                    level_split = level.split('\\')
                    level_name = str(t) + '_' + level_split[0] + '_' + level_split[-1]
                    # (3) loop every single move / match (n = 4)
                    for move, move_list in sorted(trial_dict.items()):

                        # assign move / match number; range(0, 3)
                        self.puzzle_move_number = int(move)
                        move_name = level_name + '_Trial_' + str(self.puzzle_level_number) + \
                                    '_Move_' + str(self.puzzle_move_number)
                        self.trial_data_file_name = move_name

                        # assign move / match number; range(0, 3)
                        self.puzzle_move_number = int(move)
                        # get target pattern type and coordinates
                        self.trial_target_pattern, self.trial_target_coordinates = self.get_potential_match_patterns(
                            grid=np.array(move_list), match_pattern_list=target_pattern_list)
                        # get puzzle board size of current move
                        self.puzzle_width, self.puzzle_height = np.array(move_list).shape[1], np.array(move_list).shape[0]
                        # draw the basic puzzle board using puzzle board size (width, height)
                        self.draw_board(grid=move_list, width=self.puzzle_width, height=self.puzzle_height)
                        # get timestamp for onset time
                        self.trial_onset_time = self.time.getTime()

                        # make screen shot of start screen
                        self.make_screenshot()

                        # reset swapped variable to false for swap_tiles while loop
                        self.swapped = False

                        DataCollector.next_move(move_name=self.puzzle_move_number,
                                                move_status=self.trial_move_type,
                                                hint=self.trial_hint_used)

                        # run swap_tile method -> runs until valid match is made; invalid moves bounce back
                        self.swap_tiles(width=self.puzzle_width, height=self.puzzle_height)

                    DataCollector.next_level(level_name= self.level_specs, task_condition=self.task_condition)
                    # stop getting gaze data
                    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

                # (4) get difficulty rating after every trial (4 consecutive moves)
                rating_response = False  # set to False for while loop
                self.difficulty_rating_scale.reset()
                self.puzzle_difficulty_rating = None
                while not rating_response:
                    # allow to abort if ESC is pressed
                    if 'escape' in event.getKeys():
                        self.save_task_data(data_list=self.behavioral_data)
                        self.eye_tracking_data(data_container=DataCollector.levels)
                        core.quit()
                    self.difficulty_question.draw()  # draw single eas question (difficulty rating)
                    self.difficulty_rating_scale.draw()  # draw scale (1 to 10)
                    self.window.flip()
                    if self.difficulty_rating_scale.getRating():
                        self.puzzle_difficulty_rating = self.difficulty_rating_scale.getRating()
                        # print ('Rating: ', self.puzzle_difficulty_rating)
                        # TODO: get difficulty rating and add with current level specs to seperate file
                        rating_response = True  # exit rating loop

                # save movie frames in list after four moves
                self.save_screen_shots()
                # clear movie frame list after all four moves
                self.movie_frame_dict = {}


            # print('All levels played')
            print(DataCollector.levels)
            # All Trials are done -> End experiment
            if self.task_condition == 'TrainingTrial':
                running_experiment = False
            else:
                # TODO: goodbye window
                self.window.close()
                core.quit()

#################################################################################################################


#################################################################################################################

def main():
    # create instance of class
    search_and_match = SearchMatchTask()
    # show instructions first
    search_and_match.task_condition = 'Training Trial'
    search_and_match.show_instruction(search_and_match.practice_message, 80)
    search_and_match.show_instruction(search_and_match.instruction_message, 40)
    # play training set puzzles
    search_and_match.play_puzzles(test_puzzles=training_set)
    # show instructions first
    search_and_match.task_condition = 'Test Trial'
    search_and_match.show_instruction(search_and_match.test_message, 80)
    # play test set puzzles
    search_and_match.play_puzzles(test_puzzles=TEST_SET)

if __name__ == '__main__':
    main()