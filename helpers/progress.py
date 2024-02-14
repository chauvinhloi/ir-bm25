import sys


def run(index, total):
    sys.stdout.write('\r')
    progress = int((index + 1) * 100 / total)
    sys.stdout.write("[%-100s] %d%%" % ('=' * progress, progress))
    sys.stdout.flush()
