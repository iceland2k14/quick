data = {'anyvalue{}'.format(i): i for i in range(500000)}
timeit data['anyvalue257553']
# 50.2 ns ± 2 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

# internal catching is used for quick lookup later
data = {sys.intern('anyvalue{}'.format(i)): i for i in range(500000)}
timeit data['anyvalue257553']
# 35.5 ns ± 1.04 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)
