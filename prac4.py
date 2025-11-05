"""N-Queens using Branch-and-Bound + Backtracking.

This module implements a classic backtracking solver for the n-queens problem.
Pruning (branch-and-bound) is done by maintaining sets of occupied columns and
diagonals so conflicting branches are cut early.

Functions:
- solve_n_queens(n, find_all=True): return list of solutions (each solution is a list of column indices by row)
- count_n_queens(n): optimized counter using the same backtracking engine

Demo: prints one solution and counts for N=4 and N=8 (with simple timing).
"""

from typing import List
import time


def solve_n_queens(n: int, find_all: bool = True, max_solutions: int = 0) -> List[List[int]]:
    """Solve the n-queens problem using backtracking with pruning.

    Args:
        n: board size (n x n).
        find_all: if True, find all solutions; if False, stop at first solution.
        max_solutions: optional positive limit to stop after that many solutions (0 = no limit).

    Returns:
        A list of solutions. Each solution is a list of length n where index=row and
        value=column where a queen is placed.
    """
    solutions: List[List[int]] = []

    cols = set()
    diag1 = set()  # r + c
    diag2 = set()  # r - c

    board: List[int] = [-1] * n

    # Branch-and-bound: simply prune placements conflicting with cols/diagonals
    def backtrack(row: int):
        # bound: if we've reached n rows, record solution
        if row == n:
            solutions.append(board.copy())
            return

        for c in range(n):
            if c in cols or (row + c) in diag1 or (row - c) in diag2:
                continue  # prune this branch - conflict detected

            # place queen
            board[row] = c
            cols.add(c)
            diag1.add(row + c)
            diag2.add(row - c)

            backtrack(row + 1)

            # optionally stop early
            if not find_all:
                return
            if max_solutions and len(solutions) >= max_solutions:
                return

            # remove queen (backtrack)
            cols.remove(c)
            diag1.remove(row + c)
            diag2.remove(row - c)
            board[row] = -1

    backtrack(0)
    return solutions


def count_n_queens(n: int) -> int:
    """Count number of solutions for n-queens using the same solver but without storing boards.

    This reduces memory overhead and is faster when only counts are needed.
    """
    count = 0

    cols = set()
    diag1 = set()
    diag2 = set()

    def backtrack(row: int):
        nonlocal count
        if row == n:
            count += 1
            return
        for c in range(n):
            if c in cols or (row + c) in diag1 or (row - c) in diag2:
                continue
            cols.add(c)
            diag1.add(row + c)
            diag2.add(row - c)
            backtrack(row + 1)
            cols.remove(c)
            diag1.remove(row + c)
            diag2.remove(row - c)

    backtrack(0)
    return count


def format_board(sol: List[int]) -> str:
    """Return a printable board string for a solution `sol` (list of columns by row)."""
    n = len(sol)
    lines = []
    for r in range(n):
        row_chars = ['.'] * n
        row_chars[sol[r]] = 'Q'
        lines.append(''.join(row_chars))
    return '\n'.join(lines)


def _demo():
    # demo: show one solution for N=8 and counts for N=4 and N=8
    print("N-Queens: branch-and-bound + backtracking demo")

    for n in (4, 8):
        print(f"\nSolving n={n}")
        t0 = time.perf_counter()
        sols = solve_n_queens(n, find_all=True)
        t1 = time.perf_counter()
        print(f"  Found {len(sols)} solutions in {t1 - t0:.4f}s")
        if sols:
            print("  Example solution (board):")
            print(format_board(sols[0]))

        # cross-check with the counting routine
        t2 = time.perf_counter()
        cnt = count_n_queens(n)
        t3 = time.perf_counter()
        print(f"  Count function: {cnt} solutions in {t3 - t2:.4f}s")
        assert cnt == len(sols), "Count mismatch between solver and counter"

    # sanity-known values for small n
    assert count_n_queens(4) == 2, "N=4 should have 2 solutions"
    assert count_n_queens(8) == 92, "N=8 should have 92 solutions"
    print("\nDemo assertions passed.")


if __name__ == '__main__':
    _demo()
