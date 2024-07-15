def read_file(PATH, binarymod=True):
    mode = "rb" if binarymod else "r"
    with open(PATH, mode) as f:
        data = f.read()

    return data

