import sys


def get_location(file):
    # f = open(file)

    # def read1k():
    #     return f.read(1024)

    # for piece in iter(read1k, ''):
    piece = file.split('<')
    for p in piece:
        if p.startswith('trkpt'):
            p = p.split('"')
            lat, long = float(p[1]), float(p[-2])
            return (lat, long)


def main():
    pass


if __name__ == "__main__":
    pass