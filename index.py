import os
import struct

def write_index(entries):
    f = open('.zit/index', 'w')
    f.write('DIRC')
    f.write(struct.pack('>II', 2, len(entries)))
    for filename, mode, rawsha1 in entries:
        f.write('\0' * 24)
        f.write(struct.pack('>I', mode))
        f.write('\0' * 12)
        f.write(rawsha1)
        f.write(struct.pack('>H', len(filename)))
        f.write(filename)
        f.write('\0' * (8 - (len(filename) + 6) % 8))

def read_index():
    if not os.path.exists('.zit/index'):
        return []
    index = open('.zit/index').read()
    assert index[0:4] == 'DIRC'
    assert struct.unpack('>I', index[4:8]) == (2,)
    num_entries, = struct.unpack('>I', index[8:12])
    i = 12
    entries = []
    for _ in range(num_entries):
        # ignore inode heuristics
        mode, = struct.unpack('>I', index[i+24:i+28])
        i += 40
        rawsha1 = index[i:i+20]
        # just use NUL-terminated?
        filename_length = struct.unpack('>H', index[i+20:i+22])[0] & 0xfff
        filename = index[i+22:i+22+filename_length]
        i += (22 + filename_length + 8) / 8 * 8
        entries.append((filename, mode, rawsha1))
    return entries
