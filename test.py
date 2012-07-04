# Copyright (C) 2012 by Vincent Povirk
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import mines
import unittest

class SolverTests(unittest.TestCase):
    # layouts is a sequence of tuples of the format:
    #  (description, informations, known_mine_spaces, known_clear_spaces, num_possibilities, probabilities)
    # description is a string that identifies the layout
    # informations is a sequence of tuples of the format:
    #  (total, space, space...)
    #  total is the number of mines in the given set of spaces
    # known_mine_spaces is a sequence of spaces that are known to be mines given the information
    # known_clear_spaces is a sequence of spaces that are known to be clear given the information
    # num_possibilities is the number of possible solutions; set this to 0 for unsolveable configurations
    # probabilities is a sequence of tuples of (space, solutions) where solutions is the number of solutions in which that space is a mine
    layouts = (
        ('empty', ((0,0,1,2,3),), (), (0,1,2,3), 1, ()),
        ('full', ((4,0,1,2,3),), (0,1,2,3), (), 1, ()),
        ('negative', ((-1,0,1,2,3),), (), (), 0, ()),
        ('overfull', ((5,0,1,2,3),), (), (), 0, ()),
        ('1/4', ((1,0,1,2,3),), (), (), 4, ((0,1), (1,1), (2,1), (3,1))),
        ('2/4', ((2,0,1,2,3),), (), (), 6, ((0,3), (1,3), (2,3), (3,3))),
        ('3/4', ((3,0,1,2,3),), (), (), 4, ((0,3), (1,3), (2,3), (3,3))),
        ('square', ((1,0,1),(1,1,2),(1,2,3),(2,0,3,4)), (4,), (), 2, ((0,1), (1,1), (2,1), (3,1))),
        ('triangle', ((1,0,1),(1,1,2),(1,2,0),), (), (), 0, ()),
        ('triangle2', ((1,0,1),(1,1,2),(2,2,0,3),), (2,0), (1,3), 1, ()),
        ('subset', ((1,0,1,2),(1,0,1),), (), (2,), 2, ((0,1), (1,1))),
        ('5/3', ((1,0,1),(1,1,2),(1,2,3),(1,3,4),(3,0,1,2,3,4)), (0,2,4), (1,3), 1, ()),
        ('5/2', ((1,0,1),(1,1,2),(1,2,3),(1,3,4),(2,0,1,2,3,4)), (1,3), (0,2,4), 1, ()),
        ('difference', ((1,0,1,2),(3,1,2,3,4),), (3,4), (0,), 2, ((1,1), (2,1))),
        ('3/3', ((1,0,1,2),(1,2,3,4),), (), (), 5, ((0,2), (1,2), (2,1), (3,2), (4,2))),
    )

    longMessage = True

    def test_solve(self):
        for desc, information_descs, known_mine_spaces, known_clear_spaces, expected_possibilities, expected_probabilities in self.layouts:
            informations = []
            spaces = set()
            for information in information_descs:
                informations.append(mines.Information(frozenset(information[1:]), information[0]))
                spaces.update(information[1:])

            known_spaces = set(known_mine_spaces)
            known_spaces.update(known_clear_spaces)

            solver = mines.Solver(spaces)

            try:
                for information in informations:
                    solver.add_information(information)

                solver.solve()

                self.assertNotEqual(expected_possibilities, 0, desc)

                self.assertEqual(set(solver.solved_spaces), known_spaces, desc)
                for space in known_mine_spaces:
                    self.assertEqual(solver.solved_spaces[space], 1, '%s: %s' % (desc, space))
                for space in known_clear_spaces:
                    self.assertEqual(solver.solved_spaces[space], 0, '%s: %s' % (desc, space))
            except mines.UnsolveableException:
                self.assertEqual(expected_possibilities, 0, desc)
            else:
                probabilities, num_possibilities = solver.get_probabilities()

                self.assertEqual(num_possibilities, expected_possibilities, desc)

                unknown_spaces = set(spaces)
                unknown_spaces.difference_update(known_spaces)

                self.assertEqual(unknown_spaces, set(probabilities))

                for space, possibilities in expected_probabilities:
                    self.assertEqual(probabilities[space], possibilities, '%s: %s' % (desc, space))

if __name__ == '__main__':
    unittest.main()
