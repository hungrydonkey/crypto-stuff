import subprocess

flatter = ['flatter']

def encode_matrix(lattice:list[list[int]]) -> str:
    rows = ['[' + ' '.join(map(str, row)) + ']' for row in lattice]
    matrix = '[' + '\n'.join(rows) + ']'
    return matrix

def decode_matrix(matrix_str: str) -> list[list[int]]:
    matrix = []
    for row in matrix_str.strip()[1:-1].split('\n')[:-1]:
        matrix.append(
            list(map(int,row[1:-1].split(" ")))
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
    args = flatter
    if verbose:
        args.append('-v')
    if quiet:
        args.append('-q')
    if alpha:
        args += ['-a', f'{alpha}']
    if rhf:
        args += ['-r', f'{rhf}']
    if delta:
        args += ['-d', f'{delta}']
    if logcond:
        args += ['-l', f'{logcond}']


    matrix = encode_matrix(lattice)

    # Run flatter command and return proc directly
    ret = subprocess.check_output(args, input=matrix, text=True, )
    
    ret_matrix = decode_matrix(ret)
    return ret_matrix
    
