import subprocess
import time
import os
import re

def encode_matrix(lattice:list[list[int]]) -> str:
    rows = ['[' + ' '.join(map(str, row)) + ']' for row in lattice]
    matrix = '[' + '\n'.join(rows) + ']'
    return matrix

def decode_matrix(matrix_str: str) -> list[list[int]]:
    matrix = []
    rows = re.findall(r'\[\s*([-]?\d+(?:\s+[-]?\d+)*)\s*\]', matrix_str)
    for row in rows:
        matrix.append(
            list(map(int, row.split()))
        )
    return matrix

def run_flatter(
    lattice,    # input matrix
    verbose: bool = False,
    quiet: bool = False,
    alpha: float | None = None,
    rhf: float | None = None,
    delta: float | None = None,
    logcond: float | None = None,
):
    """Run flatter command directly with a string input.

    This is primarily useful for debugging.

    Args:
        lattice_str: String representation of the lattice in FPLLL format
        verbose (bool): Enable verbose output
        quiet (bool): Do not output lattice
        alpha (float, optional): Reduce to given parameter alpha
        rhf (float, optional): Reduce analogous to given root hermite factor. Defaults to 1.0219
        delta (float, optional): Reduce analogous to LLL with particular delta (approximate)
        logcond (float, optional): Bound on condition number

    Returns:
        subprocess.CompletedProcess: Result of running the flatter command
    """
    flatter = ['flatter']
    if "flatter" not in os.environ['PATH']:
        flatter = ['/root/tools/flatter/build/bin/flatter']

    args = flatter
    if verbose:
        args.append('-v')
    if quiet:
        args.append('-q')
    if alpha:
        args += ['-alpha', f'{alpha}']
    if rhf:
        args += ['-rhf', f'{rhf}']
    if delta:
        args += ['-delta', f'{delta}']
    if logcond:
        args += ['-logcond', f'{logcond}']


    matrix = encode_matrix(lattice)

    # Run flatter command and return proc directly
    print("Running flatter with args:", args)
    start = time.time()
    ret = subprocess.check_output(args, input=matrix, text=True, )
    end = time.time()
    print(f"Flatter finished in {end - start:.2f} seconds")
    
    ret_matrix = decode_matrix(ret)
    return ret_matrix

if __name__ == "__main__":
    lattice = [
        [105, 821, 1234123123123],
        [456, 789, 1011],
        [1213, 1415, 1617]
    ]
    reduced_lattice = run_flatter(lattice, rhf = 1.02, verbose=True)
    print("Reduced Lattice:")
    for row in reduced_lattice:
        print(row)
