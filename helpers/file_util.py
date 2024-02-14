import struct


def auto_conv(str_num):
    if str_num.isdigit():
        return int(str_num)
    else:
        return str_num


def import_dict(path):
    with open(path, 'r') as f:
        content = f.read().splitlines()
    dictionary = dict(list(map(
        lambda line: (auto_conv(line.split(' ')[0]), (auto_conv(line.split(' ')[1]), auto_conv(line.split(' ')[2]))),
        content)))
    return dictionary  # key and value in string format


# Read 32bit binary file into a list of string
def read_bin(path, offset, length):
    # Opening Inverted List at path
    with open(path, 'rb') as f:
        data = []
        # Moving pointer to position (offset * 4)  - 4 bytes
        # Only read the line corresponding to the offset
        f.seek(offset*4, 0)
        # Reading next pieces in line
        for i in range(0, 2*length):
            number = f.read(4)
            try:
                data.append(struct.unpack('<I', number)[0])  # unsigned int 4 bytes little endian
            except(struct.error, Exception):
                break  # escape if error occurs whilst reading (or finish)
    return data


# Write a sequence of numbers into 32bit binary file
def write_bin(path, data):
    with open(path, "wb") as f:
        for k, v in data:
            for pair in v:
                f.write(struct.pack('<I', pair[0]))  # unsigned int 4 bytes little endian
                f.write(struct.pack('<I', pair[1]))  # unsigned int 4 bytes little endian


# Read a corpus and split into documents
def read_docs(path, split_by):
    f = open(path, 'r')
    documents = f.read().split(split_by)[:-1]
    f.close()
    return documents, len(documents)
