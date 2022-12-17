import enchant
import argparse
from cipher import VigenereCipher

# Parser to deal with user input arguments
parser = argparse.ArgumentParser(description='Encryption and decryption of Vigenère cipher.')
mode = parser.add_mutually_exclusive_group()
mode.add_argument('-c', dest='file_path_c', type=str, default=None, help='Path to file whose text will be encrypted.')
mode.add_argument('-d', dest='file_path_d', type=str, default=None, help='Path to file whose text will be decrypted.')
mode.add_argument('-b', dest='file_path_b', type=str, default=None, help='Path to file whose encryption will be broken.')
mode.required = True
parser.add_argument('-o', dest='save_path', type=str, default=None, help='Path to save file.')
parser.add_argument('-v', dest='verbose', action='store_true', help='Allow verbose mode.')
parser.add_argument('-k', dest='key', type=str, help='Key')
parser.add_argument('-l', dest='lang', type=str, default='en-us', choices=['en-us', 'pt-br'], help='Language of the encrypted text.')
parser_opt = parser.parse_args()

mode = 'c' if parser_opt.file_path_c else 'd' if parser_opt.file_path_d else 'b'

if ((mode == 'c') or (mode == 'd')) and not parser_opt.key:
    parser.error("-k required.")

file_path = parser_opt.file_path_c if parser_opt.file_path_c else parser_opt.file_path_d if parser_opt.file_path_d else parser_opt.file_path_b

text_file = open(file_path, "r")
plaintext = text_file.read()
text_file.close()

# Characters frequency in English and Portuguese, used to break the cipher
en_freq_chars = {'A': 0.08166999999999999, 'B': 0.01492, 'C': 0.02782,
                  'D': 0.04253, 'E': 0.12702, 'F': 0.02228,
                  'G': 0.02015, 'H': 0.06094, 'I': 0.06966,
                  'J': 0.00153, 'K': 0.00772, 'L': 0.04025,
                  'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
                  'P': 0.01929, 'Q': 0.00095, 'R': 0.05987,
                  'S': 0.06326999999999999, 'T': 0.09055999999999999, 'U': 0.02758,
                  'V': 0.00978, 'W': 0.0236, 'X': 0.0015,
                  'Y': 0.01974, 'Z': 0.00074}

pt_freq_chars = {'A': 0.1463, 'B': 0.0104, 'C': 0.0388,
                 'D': 0.0499, 'E': 0.1257, 'F': 0.0102,
                 'G': 0.013000000000000001, 'H': 0.0128, 'I': 0.061799999999999994,
                 'J': 0.004, 'K': 0.0002, 'L': 0.0278,
                 'M': 0.047400000000000005, 'N': 0.050499999999999996, 'O': 0.1073,
                 'P': 0.0252, 'Q': 0.012, 'R': 0.0653,
                 'S': 0.0781, 'T': 0.0434, 'U': 0.0463,
                 'V': 0.0167, 'W': 0.0001, 'X': 0.0021,
                 'Y': 0.0001, 'Z': 0.004699999999999999}

# Cipherable characters
map_chars = {chr(i): (i-65)  for i in range(65,91)}
basic_cipher = VigenereCipher(map_chars)

if mode == 'c':
    ciphered_text = basic_cipher.cipher_any_message(plaintext, parser_opt.key)

    if parser_opt.save_path:
        f = open(parser_opt.save_path, "w")
        f.write(ciphered_text)
        f.close()

        if parser_opt.verbose:
            print(ciphered_text)
    else:
        print(ciphered_text)

if mode == 'd':
    deciphered_text = basic_cipher.decipher_any_message(plaintext, parser_opt.key)

    if parser_opt.save_path:
        f = open(parser_opt.save_path, "w")
        f.write(deciphered_text)
        f.close()

        if parser_opt.verbose:
            print(deciphered_text)
    else:
        print(deciphered_text)

if mode == 'b':
    if parser_opt.lang == 'en-us':
        en_dict = enchant.Dict("en_US")
        cipher_key = basic_cipher.break_cipher(plaintext, en_dict, en_freq_chars)
    else:
        pt_dict = enchant.Dict("pt_BR")
        cipher_key = basic_cipher.break_cipher(plaintext, pt_dict, pt_freq_chars)

    deciphered_text = basic_cipher.decipher_any_message(plaintext, cipher_key)

    if parser_opt.save_path:
        f = open(parser_opt.save_path, "w")
        f.write(deciphered_text)
        f.close()

        if parser_opt.verbose:
            print(ciphered_text)
    else:
        print(deciphered_text)

    if parser_opt.verbose:
        print()
        print("Key found: ", cipher_key)