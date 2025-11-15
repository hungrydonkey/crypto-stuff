from usingflatter import *
import subprocess

matrix = subprocess.check_output("latticegen q 20 10 10 b".split(" "), text=True)
matrix = decode_matrix(matrix)
print(matrix)

print(run_flatter(matrix))