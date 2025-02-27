def read_file(filename):
    with open(filename, "r") as file:
        return file.readlines()

def process_lines(lines):
    return [line.strip() for line in lines if "INFO" in line]
