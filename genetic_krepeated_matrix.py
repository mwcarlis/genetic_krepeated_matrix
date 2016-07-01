"""A genetic algorithm implementation attempt.
"""
import copy
import random
from collections import Set

POSSIBLE_VALS = [0, 1, 2, 3, 4]

__author__ = 'Matthew W Carlis'
__email__  = 'mcarlisw@gmail.com'
__credits__= 'Lucki Qin'
__status__ = 'Proof of Concept. V1'


class BisexualMatrix(list):
    """All Matrices prefer either sex of a matrix.

    Using a single list to represent a Matrix.
     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
     # # # # # # # # # # # # # # # #
     [ 1,  2,  3,  4]
     [ 5,  6,  7,  8]
     [ 9, 10, 11, 12]
     [13, 14, 15, 16]
    """
    # How many in a horizontal/vertical we don't want to equal.
    DUPE_VAL_CNT = 2

    ALL_AROUND = False
    ALLOW_DIAGONALS = False

    state = 0
    def __init__(self, input_matrix=None, row_len=5, col_len=5):
        self.ROW_LEN = row_len
        self.COL_LEN = col_len

        if isinstance(input_matrix, list):
            [self.append(_x) for _x in input_matrix]
        self.rank = None

    def get_row_pos(self, index):
        """Get the position in a row. [0, ROW_LEN)
        """
        assert index < len(self)
        return index % self.ROW_LEN

    def get_col_pos(self, index):
        """Get the position in a column. [0, COL_LEN)
        """
        assert index < len(self)
        return index / self.ROW_LEN

    def up(self, index):
        """Get the index above this.  Relative...
        """
        this_row = self.get_col_pos(index)
        previous_row = this_row - 1
        if previous_row < 0:
            # The next row is rubbish.
            return None
        up_pos = index - self.ROW_LEN
        return up_pos

    def down(self, index):
        """Get the index below this.  Relative...
        """
        this_row = self.get_col_pos(index)
        next_row = this_row + 1
        if next_row >= self.COL_LEN:
            # The next row is rubbish.
            return None
        down_pos = index + self.ROW_LEN
        return down_pos

    def left(self, index):
        """Get the index to the left of this.  Relative...
        """
        this_col = self.get_row_pos(index)
        previous_col = this_col - 1
        if previous_col < 0:
            # The next column is rubbish.
            return None
        return index - 1

    def right(self, index):
        """Get the index to the right of this.  Relative...
        """
        this_col = self.get_row_pos(index)
        next_col = this_col + 1
        if next_col >= self.ROW_LEN:
            # The next column is rubbish.
            return None
        return index + 1

    def down_r_diagonal(self, index):
        # index - (rlen * row_num) + row_num
        pass
    def down_l_diagonal(self, index):
        # index + (rlen * row_num) - row_num
        pass
    def up_r_diagonal(self, index):
        # index + (rlen * row_num) + row_num
        pass
    def up_l_diagonal(self, index):
        # index + (rlen * row_num) - row_num
        pass

    def gen_directions(self, index):
        # Trying to support multiple ways of looking at the neighbors.
        if self.ALLOW_DIAGONALS and self.ALL_AROUND:
            # Look at all directions.
            functors = (
                self.up,
                self.down,
                self.left,
                self.right,
                self.down_r_diagonal,
                self.down_l_diagonal,
                self.up_r_diagonal,
                self.up_l_diagonal,
            )
            raise Exception('Not Implemented correctly.')
        elif self.ALLOW_DIAGONALS:
            # Only looking Down-ward/Right-ward
            functors = (self.down, self.right, self.down_r_diagonal)
            raise Exception('Not Implemented correctly.')
        elif self.ALL_AROUND:
            # Only looking self.up/Down/Left/Right
            functors = (self.up, self.down, self.left, self.right)
            raise Exception('Not Implemented correctly.')
        else:
            # Only looking Right and Down.
            functors = (self.right, self.down)

        for _func in functors:
            # We call each _func cnt times to go cnt far from this index.
            previous_index = index
            _next_neighbors = []
            for _cnt in xrange(1, self.DUPE_VAL_CNT+1):
                _potential_index = _func(previous_index)
                if not _potential_index:
                    _next_neighbors = None
                    break
                previous_index = _potential_index
                _next_neighbors.append(previous_index)
            if _next_neighbors:
                yield _next_neighbors

    def rank_board(self):
        """Rank the board by the number of repeated

        We're playing golf here ladies and gents.  The lower the better.

        Assumption:  If we're counting three in a row, we will count XXXX as
            two, (rank == 2) since there are two ways to get three
        i.e XXX? or ?XXX, count all combinations.
        """
        if self.rank:
            return self.rank
        total_dupes = 0
        for index, this_thing in enumerate(self):
            # Start in the upper left working right and down.
            for neighbors in self.gen_directions(index):
                # How many neighbors duplicate this_thing?
                dupe_cnt = 0
                for this_neighbor_idx in neighbors:
                    if self[this_neighbor_idx] == this_thing:
                        # This neighbor duplicates this_thing
                        dupe_cnt += 1
                    if dupe_cnt == self.DUPE_VAL_CNT:
                        total_dupes += 1
        self.rank = total_dupes
        return total_dupes

    def __lt__(self, other):
        # Here we use a heuristic for each board yay!
        return self.rank_board() < other.rank_board()

    def __repr__(self):
        """Holy cow it's hard to tell these apart.
        """
        ret_str = str(self)
        ret_str += '^^ Score: {} ^^'.format(self.rank_board())
        return ret_str

    def gen_row_strs(self):
        rlen = self.ROW_LEN
        for val in range(self.COL_LEN):
            # Slice out the rows one by one.
            yield '{}\n'.format(str(self[val*rlen: val*rlen+rlen]))

    def __str__(self):
        """Show me the damn matrix as a matrix please!!
        """
        matrix_str = ''
        for row in self.gen_row_strs():
            matrix_str += row
        return matrix_str

class SexMachine(object):
    """All Matrices must use a sex machine to reproduce.
    """
    def __init__(self, m1, m2):
        """So far the sex machine only supports monogamy.
        """
        assert m1.COL_LEN == m2.COL_LEN and m1.ROW_LEN == m2.ROW_LEN
        self.m1 = m1
        self.m2 = m2
        self.COL_LEN = m1.COL_LEN
        self.ROW_LEN = m2.ROW_LEN

    def make_simple_baby(self):
        """Use the matrices to make the stronger of two possible matrices.
        """
        rlen = self.ROW_LEN
        clen = self.COL_LEN

        lower = (clen * rlen) / 4 # Lower 25% Mark.
        upper = (3 * clen * rlen) /4 # Upper 75% Mark.
        row_split = random.randint(lower, upper)

        m1_a, m1_b = self.m1[:row_split], self.m1[row_split:]
        m2_a, m2_b = self.m2[:row_split], self.m2[row_split:]

        # And havith two babies they shall,
        # the narrator has decided one dies due to complications....
        m1_new = BisexualMatrix(m1_a + m2_b, row_len=rlen, col_len=clen)
        m2_new = BisexualMatrix(m2_a + m1_b, row_len=rlen, col_len=clen)
        if m1_new < m2_new:
            return m1_new
        return m2_new

def matrices_pool_factory(population_size, _row_len, _col_len):
    """Return a pool of matrices as a list.
    """
    matrix_len = _row_len * _col_len
    matrix_population = []
    for matrix_num in xrange(population_size):
        _new_matrix = BisexualMatrix(row_len=_row_len, col_len=_col_len)
        for cnt in xrange(matrix_len):
            _new_matrix.append(random.choice(POSSIBLE_VALS))
        # Append this matrix to the population.
        matrix_population.append(_new_matrix)
    return matrix_population

def best_of_num(sex_machine, num_babies):
    """Assume only the best child of num_babies survives.
    """
    babies = []
    for _b in xrange(num_babies):
        babies.append(sex_machine.make_simple_baby())
    babies.sort()
    return babies[0]



def run_simulation():
    # A Matrix will natrually choose the next best choice.
    matrices = sorted(matrices_pool_factory(100, 10, 10))

    num_babies = 10
    num_universes = 100

    cycle_cnt = 0
    universe_cnt = 0

    for universe in xrange(num_universes):
        matrices = sorted(matrices_pool_factory(100, 15, 15))
        if matrices[0] == 0:
            print '1 universe_cnt', cycle_cnt
            print '1 cycle_cnt', cycle_cnt

        for life_cycle in xrange(10):
            new_pool = []
            # Ignore the last matrix if it's the odd matrix out.
            mate_pairs = (len(matrices) / 2) * 2
            for index in xrange(0, mate_pairs - 1, 2):
                mate1 = matrices[index]
                mate2 = matrices[index+1]
                baby = best_of_num(SexMachine(mate1, mate2), num_babies)
                if baby.rank_board() == 0:
                    print '2 universe_cnt', cycle_cnt
                    print '2 cycle_cnt', cycle_cnt
                    return baby
                new_pool.append(baby)
            matrices = sorted(new_pool)
            cycle_cnt += 1
        universe_cnt += 1
    print '3 universe_cnt', cycle_cnt
    print '3 cycle_cnt', cycle_cnt





if __name__ == '__main__':
    import copy

    # The obj.rank_board tests make assumptions about counting repetitions.
    a = BisexualMatrix()
    a.extend([0, 1, 2, 0, 1])
    a.extend([2, 1, 2, 2, 2])
    a.extend([1, 1, 0, 1, 0])
    a.extend([0, 1, 0, 0, 0])
    a.extend([2, 1, 1, 2, 0])

    b = BisexualMatrix()
    b.extend([0, 1, 2, 0, 1])
    b.extend([2, 1, 2, 2, 2])
    b.extend([1, 1, 1, 1, 0])
    b.extend([0, 1, 0, 0, 0])
    b.extend([2, 1, 1, 2, 0])

    c = BisexualMatrix()
    c.extend([1, 0, 2, 1, 1])
    c.extend([0, 0, 1, 2, 0])
    c.extend([2, 1, 0, 1, 1])
    c.extend([0, 1, 0, 0, 0])
    c.extend([2, 1, 1, 2, 0])

    # Test boundaries.
    assert a.up(0) == None
    assert a.up(2) == None
    assert a.up(4) == None

    assert a.down(20) == None
    assert a.down(22) == None
    assert a.down(24) == None

    assert a.left(0) == None
    assert a.left(10) == None
    assert a.left(20) == None

    assert a.right(4) == None
    assert a.right(14) == None
    assert a.right(24) == None

    # Test valid queries.
    assert a.up(12) == 7
    assert a.down(12) == 17
    assert a.left(12) == 11
    assert a.right(12) == 13

    # You will want to understand it if you break this....
    tests = ([13, 14], [17, 22])
    for _d, _t in zip(a.gen_directions(12), tests):
        assert _d == _t
    tests = ([1, 2], [5, 10])
    for _d, _t in zip(a.gen_directions(0), tests):
        assert _d == _t

    # This makes assumptions about counting repeats.
    assert a.rank_board() == 6
    assert b.rank_board() == 8

    assert [a, b] == sorted([b, a])
    assert a < b

    sm = SexMachine(a, b)

