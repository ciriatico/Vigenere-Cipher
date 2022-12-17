import itertools
import numpy as np
from numpy.linalg import norm

class Utils:
    def get_int(mapper, char):
        return mapper[char]

    def get_char(mapper, num):
        for key, value in mapper.items():
            if value == num:
                return key

    def is_cipherable(char, mapper):
        return char in mapper.keys()

    def get_keystream(plaintext, key):
        return key*(len(plaintext)//len(key)) + key[0:len(plaintext)%len(key)]
    
    def get_cipherable_chars(plaintext, mapper):
        mapping_chars = [c if Utils.is_cipherable(c, mapper) else ind for ind, c in enumerate(plaintext)]
        lacking_chars = {c: plaintext[c] for c in mapping_chars if type(c) == int}
        cipherable_chars = "".join([c for c in mapping_chars if type(c) == str])

        return cipherable_chars, lacking_chars

    def is_word_cipherable(word, mapper):
        for w in word:
            if not Utils.is_cipherable(w, mapper):
                return False

        return True
    
    def count_distances(segs, n=2):
        segs_comb = list(itertools.combinations(segs, n))
        return [(s[1] - s[0]) for s in segs_comb]

    def get_factors(num):
        return [n for n in range(2, num) if num % n == 0]

    def shift_char(char, n):
        n_char = ord(char) - 65
        n_char = ((n + n_char) % 26) + 65
        return chr(n_char)

    def cosine_similarity(a, b):
        A = list(a)
        B = list(b)

        return np.dot(A,B)/(norm(A)*norm(B))