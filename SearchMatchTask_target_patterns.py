
#######################################################################################################################

# PARAMETERS FOR POTENTIAL MATCH PATTERNS

# configurations where one gem (S) can be switched with another (X) to correctly make a chain of 3 (0-0-S / 0-S-0)
# dictionaries for potential match pattern types: key = name, value = [3rd pattern gem, swap gem]

#######################################################################################################################


"""
Pattern names taken from:
https://github.com/olafurw/bejeweled-player/blob/master/src/Pattern.cpp

        MATCH-3 PATTERNS

        'Horizontal i'                              'Horizontal j'

        X - X - X - X - X - X                       X - M3- X - X - M3- X
        |   |   |   |   |   |                       |   |   |   |   |   |
       M3 - S - M1- M2- S - M3                      X - S - M1- M2- S - X
        |   |   |   |   |   |                       |   |   |   |   |   |
        X - X - X - X - X - X                       X - M3- X - X - M3- X

        horizontal_i_left                           horizontal_j_bottom_left
        horizontal_i_right                          horizontal_j_bottom_right
                                                    horizontal_j_top_left
                                                    horizontal_j_top_right


        'Vertical i'                                'Vertical j'

        X - M3- X                                   X - X - X
        |   |   |                                   |   |   |
        X - X - X                                  M3 - X - M3
        |   |   |                                   |   |   |
        X - M1- X                                   X - M1- X
        |   |   |                                   |   |   |
        X - M2- X                                   X - M2- X
        |   |   |                                   |   |   |
        X - X - X                                  M3 - X - M3
        |   |   |                                   |   |   |
        X - M3- X                                   X - X - X

        vertical_i_bottom                           vertical_j_left_bottom
        vertical_i_top                              vertical_j_right_bottom
                                                    vertical_j_left_top
                                                    vertical_j_right_top


        'horizontal v'                              'vertical v'

        X - M2- X                                   X - M1- X
        |   |   |                                   |   |   |
        M1- S - M3                                 M2 - S - M2
        |   |   |                                   |   |   |
        X - M2- X                                   X - M3- X

        horizontal_v_bottom                         vertical_v_left
        horizontal_v_top                            vertical_v_right
"""

horizontal_v = {'horizontal_v_bottom': [(0, 2), (1, 1), (0, 1)],
                'horizontal_v_top': [(0, 2), (-1, 1), (0, 1)]}

vertical_v = {'vertical_v_left': [(2, 0), (1, -1), (1, 0)],
              'vertical_v_right': [(2, 0), (1, 1), (1, 0)]}

horizontal_i = {'horizontal_i_left': [(0, 1), (0, -2), (0, -1)],
                'horizontal_i_right': [(0, 1), (0, 3), (0, 2)]}

vertical_i = {'vertical_i_top': [(1, 0), (-2, 0), (-1, 0)],
              'vertical_i_bottom': [(1, 0), (3, 0), (2, 0)]}

horizontal_j = {'horizontal_j_top_right': [(0, 1), (-1, 2), (0, 2)],
                'horizontal_j_bottom_right': [(0, 1), (1, 2), (0, 2)],
                'horizontal_j_top_left': [(0, 1), (-1, -1), (0, -1)],
                'horizontal_j_bottom_left': [(0, 1), (1, -1), (0, -1)]}

vertical_j = {'vertical_j_top_right': [(1, 0), (-1, 1), (-1, 0)],
              'vertical_j_bottom_right': [(1, 0), (2, 1), (2, 0)],
              'vertical_j_top_left': [(1, 0), (-1, -1), (-1, 0)],
              'vertical_j_bottom_left': [(1, 0), (2, -1), (2, 0)]}

target_pattern_list = [horizontal_v, vertical_v,
                       horizontal_i, vertical_i,
                       horizontal_j, vertical_j]

#######################################################################################################################

# PARAMETERS FOR DISTRACTOR PATTERNS
# misleading configurations that appear to allow for a chain of three to be made but do not

#######################################################################################################################

"""
        PATTERN A 
        

        D - X       X - D         D - D       D - D
        |   |       |   |         |   |       |   |
        D - D       D - D         X - D       D - X


        PATTERN B 
        

        D - X       X - D         D - D       D - D
        |   |       |   |         |   |       |   |
        X - X       X - X         X - X       X - X
        |   |       |   |         |   |       |   |
        D - D       D - D         X - D       D - X


        D - X - D   D - X - X   X - X - D   D - X - D
        |   |   |   |   |   |   |   |   |   |   |   |
        D - X - X   D - X - D   D - X - D   X - X - D


        PATTERN C
        

        D - X        X - D        D - X        X - D
        |   |        |   |        |   |        |   |
        D - X        X - D        X - X        X - X
        |   |        |   |        |   |        |   |
        X - X        X - X        X - D        D - X
        |   |        |   |        |   |        |   |
        X - D        D - X        X - D        D - X
"""

false_rightAngle = {'false_A_1': [(-1, 0), (0, 1)], 'false_A_2': [(0, 1), (1, 0)],
                    'false_A_3': [(1, 0), (0, -1)], 'false_A_4': [(0, -1), (-1, 0)]}

false_LShape = {'false_B_1': [(0, 1), (-2, 0)], 'false_B_2': [(0, -1), (-2, 0)],
                'false_B_3': [(0, -1), (2, 0)], 'false_B_4': [(0, 1), (2, 0)]}

false_skip = {'false_C_1': [(0, 1), (-2, 0), (-3, 0)], 'false_C_2': [(0, -1), (-2, 0), (-3, 0)],
              'false_C_3': [(0, -1), (2, 0), (3, 0)], 'false_C_4': [(0, 1), (2, 0), (3, 0)]}

distractor_patterns_list = [false_rightAngle, false_LShape, false_skip]