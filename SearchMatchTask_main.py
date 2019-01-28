# -*- coding: utf-8 -*-

"""
This is a Psychopy adaptation of a tile-matching match-three puzzle game called "Search & Match Task"

The code was written by Alvin Chesham.

This experiment was created using PsychoPy2 Experiment Coder (), TODO: Thu Oct 16 13:34:11 2014

If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
   Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

################################################ IMPORT LIBRARIES ##########################################

import datetime

import numpy as np
import pandas as pd
from psychopy import visual
from psychopy import event
from psychopy import sound
from psychopy import core
from psychopy import gui

from psychopy import prefs
prefs.general['audioLib'] = ['pygame']

from SearchMatchTask_gui import show_gui

# get function to get pre-generated puzzle boards from 'Levels' folder
from SearchMatchTask_get_puzzle_boards import GetPuzzleBoards
# get all target pattern configurations
from SearchMatchTask_target_patterns import target_pattern_list
# get distractor pattern configurations
from SearchMatchTask_target_patterns import distractor_patterns_list

from Instruction import general_instruction
from Instruction import practice_instruction_1
from Instruction import practice_instruction_2
from Instruction import test_instruction

################################################ TASK PARAMETERS ##########################################

# call gui class

gui_data_list = show_gui()

print(gui_data_list)

participant_id = gui_data_list[0]
participant_age = gui_data_list[1]
participant_gender = gui_data_list[2]
participant_handedness = gui_data_list[3]

task_color = gui_data_list[4]
task_level = gui_data_list[5]
task_version = gui_data_list[6]
task_order = gui_data_list[7]
task_trial_repet = gui_data_list[8]
task_match_PT = gui_data_list[9]


################################################################################################ 

# Create a window
from win32api import GetSystemMetrics
WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)


# Set maximum puzzle board width to screen height minus border
PUZZLE_BOARD_WIDTH = HEIGHT - (HEIGHT/4)
# Tile (polygon) parameters
POLYGON_LIST = [3, 4, 5, 6, 7, 8, 9, 10, 11]  # list of polygons -> will set number of edges


# Set color palette of tiles
if task_color == 'Color-blind friendly Palette':
    # Colorblind friendly list of colors for polygons taken from: Wong, B., Nature Methods, 2011 (https://doi.org/10.1038/nmeth.1618)
    COLOR_LIST = ['#0B0B09', '#D99930', '#60ABD2', '#1E966A', '#ECE64C', '#20669E', '#C2592E', '#BD6D99']
    BOARD_COLOR = 'white'
    HINT_FRAME_COLOR = 'black'
else:
    # Color list for polygons
    COLOR_LIST = ['#1E3AFF', '#7AFFDF', '#60FF01', '#EFFF07', '#FF6100', '#FF0300', '#B92EFF', '#DCD9DE']
    BOARD_COLOR = 'dimgray'
    HINT_FRAME_COLOR = 'white'

BACKGROUND_COLOR = '#b5b5b5'
CELL_SIZE_FACTOR = 0.85

# Task-related parameters
PRACTICE_LEVELS = 'Levels/Practice'
TEST_LEVELS = 'Levels/' + task_level + '/M3_' + task_version

# Set randomize trials in test trials (true or false)
if task_order == "Random Order":
    RANDOMIZE = True
else:
    RANDOMIZE = False
    
# Number of repetitions for each trial
TRIALS_PER_LEVEL = task_trial_repet

# Fixation presentation duration (between trials)
FIXATION_PT = 1

# Time between matches
SWAP_TIME = task_match_PT

# Set fontsize for instructions
FONTSIZE = HEIGHT / 30


################################################ GET PUZZLES ##########################################################

# Get pre-generated trials for difficulty levels in 'Levels' folder

# Initialize GetPuzzleBoards class
gpb = GetPuzzleBoards()

# Create dict with training puzzle levels
training_level_list = gpb.read_puzzle_levels(LEVELS_PATH=PRACTICE_LEVELS)
training_level_dict = gpb.create_level_dict(level_list=training_level_list)
training_trial_list = gpb.create_trial_dict(puzzle_dict=training_level_dict, N_Repetitions=1)
training_trials = gpb.sort_trial_dict(trial_dict=training_trial_list, randomize=False)

# Create dict with test puzzle levels
test_level_list = gpb.read_puzzle_levels(LEVELS_PATH=TEST_LEVELS)
test_level_dict = gpb.create_level_dict(level_list=test_level_list)
test_trial_list = gpb.create_trial_dict(puzzle_dict=test_level_dict, N_Repetitions=1)
test_trials = gpb.sort_trial_dict(trial_dict=test_trial_list, randomize=RANDOMIZE)

#######################################################################################################################

class SearchMatchTask:

    def __init__(self):

        from psychopy import visual, monitors
        mon = monitors.Monitor('SMT')  #fetch the most recent calib for this monitor
        mon.setDistance(60)  #further away than normal?
        
        # Set psychopy window
        self.window = visual.Window([WIDTH, HEIGHT], units="pix", monitor=mon,
                                    color=BACKGROUND_COLOR, winType='pyglet', 
                                    fullscr=True)


        self.window.refreshThreshold = 1 / 60

        img_width, img_height = 3620, 1458
        self.practice_img = visual.ImageStim(win=self.window, image="Instructions/BasicTargetPatterns.png",
                                             units="pix", pos=(0, 0), size=(img_width/5, img_height/5))

        self.practice_message = u'Practice Trial'
        self.test_message = u'Test Trial'

        # Set hint button positions
        self.button_width, self.button_height = WIDTH / 10, HEIGHT / 16
        button_pos_x = PUZZLE_BOARD_WIDTH/2 + self.button_height

        # Set up hint button and hint text
        self.help_button = visual.Rect(self.window, units='pix', pos=(0, -button_pos_x),
                                       width=self.button_width, height=self.button_height,
                                       fillColor='white', lineColor=None)
        self.help_text = visual.TextStim(self.window, 'Hint', color='black', units='pix',
                                         height=self.button_height/2, pos=(0, -button_pos_x))

        self.continue_button = visual.Rect(self.window, units='pix', pos=(0, 0),
                                           width=self.button_width, height=self.button_height,
                                           fillColor='white')
        self.continue_text = visual.TextStim(self.window, 'Continue', color='black', units='pix',
                                             height=self.button_height/2, pos=(0, 0))

        # Create fixation cross (shown at start of each difficulty level)
        self.fixation = visual.TextStim(self.window, text='+', pos=(0.0, 0.0), depth=0, rgb=None, color='black',
                                        colorSpace='rgb', opacity=1.0, contrast=1.0, units='', ori=0.0, height=FONTSIZE)

        self.time = core.Clock()

        # Load sounds
        self.gem_sound = sound.Sound(value='sounds/gem.wav')
        self.match_sound = sound.Sound(value='sounds/match.wav')
        self.error_sound = sound.Sound(value='sounds/falsch.wav')

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
        self.task_condition = None

        # Puzzle difficulty level outcomes
        self.puzzle_trial_number = None
        self.puzzle_version = None
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
        self.puzzle_number_hints = None

        # Puzzle trial level outcomes
        self.move_trial_number = 0
        self.trial_clicked_tile_coords = None
        self.trial_hint_used = None
        self.trial_move_type = None  # [valid, invalid]
        self.trial_target_type = None
        self.trial_target_pattern = None
        self.trial_target_coordinates = None
        self.trial_number_distractors = None
        self.trial_search_time = 0
        self.trial_onset_time = 0
        self.trial_offset_time = 0
        self.trial_file_number = None

        # output data list
        self.output_data = []

    def draw_board_background(self, x, y, cell_size):
        # color background with BACKGROUND_COLOR
        self.window.color = BACKGROUND_COLOR
        # draw grey background
        rect = visual.Rect(self.window, width=(x * cell_size), height=(y * cell_size),
                           fillColor=BOARD_COLOR, lineColor=BOARD_COLOR)
        rect.draw()

    def grid_positions(self, max_res, x, y):
        # set cell size depending on max height or width of set size
        self.cell_size = PUZZLE_BOARD_WIDTH / max_res
        # adapt polygon size to fit into cell
        polygon_size = self.cell_size * CELL_SIZE_FACTOR
        # set x and y positions of polygons
        x_max = ((x - 1) * self.cell_size) / 2
        x_min = -1 * ((x - 1) * self.cell_size) / 2
        y_max = ((y - 1) * self.cell_size) / 2
        y_min = -1 * ((y - 1) * self.cell_size) / 2

        self.x_positions = list(np.linspace(x_min, x_max, x))
        self.y_positions = list(np.linspace(y_min, y_max, y))

        return self.cell_size, self.x_positions, self.y_positions, polygon_size

    def draw_board(self, grid, height, width):
        # Run 'grid_positions' function
        self.cell_size, x_pos, y_pos, polygon_size = self.grid_positions(max_res=max(width, height), x=width, y=height)
        # Draw background
        self.draw_board_background(x=width, y=height, cell_size=self.cell_size)
        # List to hold tiles (polygons) filled in grid
        self.current_polygon_list = []
        # List to hold current grid
        puzzle_array = []
        counter = 0  # counter for cell index
        # Draw the grid - each cell in puzzle board
        for row in range(height):  # loop height
            row_list = []
            for column in range(width):  # loop width
                y, x = -1 * (y_pos[row]), x_pos[column]
                row_list.append((x, y))
                cell = grid[row][column]
                cell = int(cell)
                # draw polygon inside each cell (x, y)
                self.show_polygon(pg=POLYGON_LIST[cell], pg_size=polygon_size,
                                  color=COLOR_LIST[cell], x=x, y=y, key=counter)
                counter += 1
            puzzle_array.append(row_list)

        # Draw help / hint button
        self.help_button.draw()
        self.help_text.draw()
        self.puzzle_board_coords = puzzle_array
        # Refresh the screen
        self.window.flip()

    def continue_routine(self):

        # draw continue button
        self.continue_button.pos = (0, 0)
        self.continue_button.draw()
        self.continue_text.pos = (0, 0)
        self.continue_text.draw()
        # Refresh the screen
        self.window.flip()

        self.mouse.clickReset()
        trial_pause = True  # set to False for while loop

        while trial_pause:
            # allow to abort if ESC is pressed
            if 'escape' in event.getKeys():
                # save task data
                self.save_task_data(output_data=self.output_data)
                core.quit()
            if self.mouse.isPressedIn(self.continue_button) and self.mouse.getPressed()[0]:
                trial_pause = False  # exit rating loop

    def show_polygon(self, pg, pg_size, color, x, y, key):
        self.polygon_size = pg_size
        # move if polygon is triangle (3)
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
        # draw the polygon
        polygon.draw()

    def check_for_chains(self, grid, grid_h, grid_w):
        # variable for whether chains (X-X-X) is True or False
        chains = False
        # check for horizontal matches (row)
        for i in grid:
            for idx, j in enumerate(i):
                if idx >= 2:
                    if i[idx] == i[idx - 1] == i[idx - 2]:
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
            empty_grid[h][w] = pg.edges - 3
        return empty_grid

    def get_polygon_coordinates(self, cell, width):
        x = cell % width  # % is the "modulo operator", the remainder of i / width;
        y = cell // width  # / is an integer division
        return x, y

    def redraw_polygons(self, width, height):
        self.window.flip()
        # re-draw background
        self.draw_board_background(x=width, y=height, cell_size=self.cell_size)
        # re-draw polygons
        for polygon in self.current_polygon_list:
            polygon.draw()

        # draw hint box
        self.help_button.draw()
        self.help_text.draw()

        # update on window
        self.window.flip()

    def redraw_polygons_hint_marker(self, width, height):
        # re-draw background
        self.draw_board_background(x=width, y=height, cell_size=self.cell_size)
        # re-draw hint markers
        for rect in self.current_hint_mark_list:
            rect.draw()
        # re-draw polygons
        for polygon in self.current_polygon_list:
            polygon.draw()

        self.help_button.draw()
        self.help_text.draw()

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

    def swap_tiles_routine(self, width, height):

        previous_mouse_down = False
        self.mouse_down_counter = 0
        self.trial_hint_used = 'no hint'

        # main loop while no swap has been made
        while not self.swapped:
            # Get mouse clicks
            mouse_down = self.mouse.getPressed()[0]
            # Allow to abort if ESC is pressed
            if 'escape' in event.getKeys():
                # save task data
                self.save_task_data(output_data=self.output_data)
                core.quit()
            # Check whether hint button gets pressed
            if self.mouse.isPressedIn(self.help_button):
                help_button_pressed = True
                if help_button_pressed:
                    self.trial_hint_used = 'hint'
                    # Show hint for target pattern
                    self.mark_hint(self.trial_target_coordinates)
            # Loop every polygon
            for polygon in self.current_polygon_list:
                # check whether polygon gets clicked
                if mouse_down and not previous_mouse_down and self.mouse.isPressedIn(polygon):
                    self.gem_sound.play()
                    self.clicked_tiles_list.append(polygon)
                    self.mouse_down_counter += 1
                    # if two polygons get clicked consecutively
                    if self.mouse_down_counter > 1 and self.mouse.isPressedIn(polygon):
                        previous_polygon = self.clicked_tiles_list[(self.mouse_down_counter - 2)]
                        pos_1 = self.get_polygon_coordinates(cell=previous_polygon.name, width=width)
                        pos_2 = self.get_polygon_coordinates(cell=polygon.name, width=width)
                        self.trial_clicked_tile_coords = list((pos_1, pos_2))

                        # check whether the two clicked polygons are adjacent
                        if self.tiles_adjacent(pos1=pos_1, pos2=pos_2):
                            # if tiles are adjacent / neighbours -> swap their places
                            self.make_swap(current_polygon=polygon, previous_polygon=previous_polygon,
                                           width=width, height=height)
                            grid = self.polygons_grid(polygons=self.current_polygon_list, width=width, height=height)
                            # go on to check if swapped tiles create a match -> if so continue to next trial
                            if self.check_for_chains(grid=grid, grid_h=height, grid_w=width):
                                self.trial_move_type = 'valid'
                                self.puzzle_number_moves += 1
                                self.trial_offset_time = self.time.getTime()
                                self.trial_search_time = (self.trial_offset_time - self.trial_onset_time)
                                # save task data
                                self.task_data()
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
                                # save task data
                                self.task_data()
                                self.mouse_down_counter = 0
                                del self.clicked_tiles_list[:]
                                self.make_swap(current_polygon=previous_polygon, previous_polygon=polygon,
                                               width=width, height=height)
                                self.error_sound.play()
                        else:  # if tiles are not adjacent -> don't swap them
                            self.trial_move_type = 'invalid-non-adjacent'
                            self.puzzle_number_moves += 1
                            self.puzzle_number_errors += 1
                            self.trial_offset_time = self.time.getTime()
                            self.trial_search_time = (self.trial_offset_time - self.trial_onset_time)
                            # save task data
                            self.task_data()
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
        
        line_width = HEIGHT / 50
        
        self.current_hint_mark_list[:] = []
        # coord = (height, width)
        for coord in coords[:-1]:
            cell_number = (coord[0]*self.puzzle_width) + coord[1]
            pos_x, pos_y = self.current_polygon_list[cell_number].pos[0], self.current_polygon_list[cell_number].pos[1]
            if self.current_polygon_list[cell_number].edges == 3:
                rect = visual.Rect(self.window, width=self.cell_size, height=self.cell_size,
                                   pos=(pos_x, pos_y + (self.cell_size / 6)), lineWidth=line_width, lineColor=HINT_FRAME_COLOR,
                                   lineColorSpace='rgb', fillColor=None)
                self.current_hint_mark_list.append(rect)
            else:
                rect = visual.Rect(self.window, width=self.cell_size, height=self.cell_size,
                                   pos=(pos_x, pos_y), lineWidth=line_width, lineColor=HINT_FRAME_COLOR,
                                   lineColorSpace='rgb', fillColor=None)
                self.current_hint_mark_list.append(rect)
        self.redraw_polygons_hint_marker(width=self.puzzle_width, height=self.puzzle_height)

        self.puzzle_number_hints += 1

        core.wait(0.1)

    def task_data(self):

        output = [participant_id, participant_age, participant_gender, participant_handedness,
                  self.task_condition, self.puzzle_version, self.trial_number,
                  self.puzzle_width, self.puzzle_height, self.puzzle_tile_number, self.trial_file_number,
                  self.puzzle_move_number, self.trial_move_type,
                  self.trial_hint_used, self.trial_search_time,
                  self.puzzle_number_moves, self.puzzle_number_errors, self.puzzle_number_hints,
                  self.trial_target_pattern, self.trial_target_coordinates, self.trial_clicked_tile_coords]

        self.output_data.append(output)

    def save_task_data(self, output_data):

        headers = ['Participant ID', 'Age', 'Gender', 'Handedness',
                   'Condition', 'Version', 'Level Trial No',
                   'Width', 'Height', 'Tiles', 'Level File Number',
                   'Move Trial No', 'Move Accuracy',
                   'Hint', 'SearchTime',
                   'Number Valid Moves', 'Number False Moves', 'Number Hints',
                   'Target Pattern', 'Target Pattern Coords', 'Clicked Tiles Coords']

        for data in output_data:
            print(data)

        df = pd.DataFrame(data=output_data)
        df.columns = headers
        
        file_name = "DATA/" + str(participant_id) +"_"+ str(participant_age) +"_"+ participant_gender +"_"+ participant_handedness 
        time = datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
        name = file_name +"_"+ time + "_Task_Data.csv"
       
        df.to_csv(name, sep=';', index=False)


    def show_instruction(self, text, fontsize, pos_xy):

        # Create text stim
        self.instruction = visual.TextStim(self.window, text, height=fontsize, rgb=None, color='black',
                                           alignHoriz='center', wrapWidth=(WIDTH-150), pos=pos_xy)
        if self.task_condition == 'Practice Trial':
            self.practice_img.draw()

        # Draw the text stim
        self.instruction.draw()
        # Refresh the screen
        self.window.flip()

        # wait for user input
        event.waitKeys(keyList='return')

    ###################################### PLAY PUZZLES LOOP STARTS ####################################################

    def play_puzzles(self, test_puzzles):
        running_experiment = True
        # ------Start Routine "Play Puzzles"
        while running_experiment:
            # ------loop all levels in puzzle level list
            for idx, level in enumerate(test_puzzles):
                # trial number
                self.trial_number = idx + 1
                # Get level name and list of moves from level list
                level_name, moves = level[0], level[1]
                
                print(level_name)

                # Get level variables
                self.puzzle_level_number = level_name.split('_')[1]
                self.trial_file_number = level_name.split('_')[-1]

                # Assign puzzle parameters
                self.puzzle_width, self.puzzle_height, self.puzzle_tile_number = \
                    level_name.split('_')[-4], level_name.split('_')[-3], level_name.split('_')[-2]

                # Reset move level variables
                self.puzzle_number_errors = 0  # reset error counter before every new trial
                self.puzzle_number_moves = 0  # reset move counter before every new trial
                self.puzzle_number_hints = 0

                # Show fixation cross at beginning of every new level
                self.fixation.draw()
                self.window.flip()
                core.wait(FIXATION_PT)  # set presentation time in Parameters

                # ------Loop every single move / match (n = 4)
                for move, move_list in moves:

                    # Assign move / match number; range(0, 3)
                    self.puzzle_move_number = int(move) + 1

                    # Get target pattern type and coordinates
                    self.trial_target_pattern, self.trial_target_coordinates = self.get_potential_match_patterns(
                        grid=np.array(move_list), match_pattern_list=target_pattern_list)

                    # Get puzzle board size of current move
                    self.puzzle_width, self.puzzle_height = np.array(move_list).shape[1], np.array(move_list).shape[0]

                    # Draw the basic puzzle board using puzzle board size (width, height)
                    self.draw_board(grid=move_list, width=self.puzzle_width, height=self.puzzle_height)

                    # Get timestamp for onset time
                    self.trial_onset_time = self.time.getTime()

                    # -------Swap Tile Routine
                    # Reset swapped variable to false for swap_tiles while loop
                    self.swapped = False
                    # Run swap_tile method -> runs until valid match is made / invalid moves bounce back
                    self.swap_tiles_routine(width=self.puzzle_width, height=self.puzzle_height)

                # -------Wait Routine after each difficulty level
                self.continue_routine()

            # -------Ending Routine "Play Puzzles"
            if self.task_condition == 'Practice Trial':
                running_experiment = False
            else:
                self.window.close()
                # save task data
                self.save_task_data(output_data=self.output_data)
                core.quit()


def main():

    # Create instance of 'SearchMatchTask' class
    search_and_match = SearchMatchTask()

    # -------Practice Trial Starts

    # Show instructions
    search_and_match.show_instruction(general_instruction, FONTSIZE, (0, 0))
    search_and_match.show_instruction(practice_instruction_1, FONTSIZE, (0, 0))
    search_and_match.task_condition = 'Practice Trial'
    search_and_match.show_instruction(practice_instruction_2, FONTSIZE, (0, WIDTH/5))
    # set puzzle version
    search_and_match.puzzle_version = PRACTICE_LEVELS.replace('/', '_')

    # Play training set puzzles
    search_and_match.play_puzzles(test_puzzles=training_trials)

    # -------Test Trial Starts

    # Show instructions
    search_and_match.task_condition = 'Test Trial'
    search_and_match.show_instruction(test_instruction, FONTSIZE, (0, 0))
    # set puzzle version
    search_and_match.puzzle_version = TEST_LEVELS.replace('/', '_')

    # Play test set puzzles
    search_and_match.play_puzzles(test_puzzles=test_trials)
    search_and_match.show_instruction(test_instruction, FONTSIZE, (0, 0))


if __name__ == '__main__':
    main()