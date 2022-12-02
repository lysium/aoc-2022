def read_file_lines(file):
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            yield line


