import os
import random
import re

PRACTICE_LEVELS = 'Levels/Practice'


class GetPuzzleBoards:

    def __init__(self):

        self.LEVEL_LIST = []
        self.LEVEL_DICT = {}

        self.folder_path = None
        self.file_name = None

    def read_puzzle_levels(self, LEVELS_PATH):
        # loop files in level folder
        for subdir, dirs, files in os.walk(LEVELS_PATH):
            for f in files:
                if not (f.startswith('.')):  # exclude ".DS_Store" file
                    self.LEVEL_LIST.append(os.path.join(subdir, f)) # append level .txt files to list
        return self.LEVEL_LIST

    def create_level_dict(self, level_list):
        # dict for all puzzles
        puzzle_dict = {}
        for level in level_list:
            # create level-wise sub-dicts
            folder_name = level.split('\\')[-2]
            folder_number, folder_rest = folder_name.split('_')[0].zfill(2), folder_name.split('_')[1:]
            level_name = folder_number.split('_')[0].zfill(2) + '_' + '_'.join(str(v) for v in folder_rest)
            puzzle_dict[level_name] = {}
            # add ALL pre-generated trials to sub-dicts
            self.get_level_moves(level=level, level_name=level_name, puzzle_dict=puzzle_dict)
        return puzzle_dict

    def get_string(self, line):
        if any(c.isalpha() for c in line):
            return True
        else:
            return False

    def get_level_moves(self, level, level_name, puzzle_dict):
        # open each level-wise txt file
        with open(level, 'r') as LEVEL_FILE:
            puzzle = []
            trial_no = None
            move_no = None
            for line in LEVEL_FILE:
                if self.get_string(line=line):  # get puzzle board specifics
                    move_no = line.split('_')[-1].rstrip()
                    if re.search('Move_0', line):  # create sub-dict for each trial within level-dict
                        trial_no = line.split('_')[-3]
                        puzzle_dict[level_name][trial_no] = {}
                # get puzzle as 2D array
                elif line.count(',') > 2:
                    puzzle.append(line.rstrip().split(','))
                else:
                    if not puzzle:  # do nothing if puzzle list is empty
                        pass
                    else:  # add each puzzle to trial list once its read in
                        puzzle_dict[level_name][trial_no][move_no] = puzzle
                        puzzle = []  # empty puzzle list

    def create_trial_dict(self, puzzle_dict, N_Repetitions):
        trial_dict = {}
        for level_name, move_list in puzzle_dict.items():
            trial_choice = random.sample(list(move_list), N_Repetitions)
            for trial_name in trial_choice:
                level_trial_name = level_name + '_' + str(trial_name).zfill(3)
                moves_list = puzzle_dict[level_name][trial_name]
                sorted_move_list = sorted(moves_list.items())
                trial_dict[level_trial_name] = sorted_move_list
        return trial_dict

    def sort_trial_dict(self, trial_dict, randomize):
        sorted_trial_list = list(sorted(trial_dict.items()))
        if randomize:
            random.shuffle(list(sorted_trial_list))
        else:
            sorted_trial_list = sorted_trial_list
        return sorted_trial_list
        

