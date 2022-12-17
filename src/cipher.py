from utils import Utils

class FrequencyAnalyser:
    def get_seg_mapper(text, mapper, n_gram):
        # Retorna todos os n-gram cifráveis e suas posições

        seg_mapper = dict()

        for i in range(0, len(text)):
            seg = text[i:i+n_gram]

            if Utils.is_word_cipherable(seg, mapper):
                if seg not in seg_mapper.keys():
                    seg_mapper[seg] = [i]
                else:
                    seg_mapper[seg].append(i)

        return seg_mapper

    def get_frequency(l, base):
        l_dict = {i: 0 for i in set(base)}

        for i in l:
            l_dict[i] += 1

        return {k: v/len(l) for k, v in l_dict.items()}

    def get_possible_key_sizes(text, mapper, n=3):    
        seg_mapper = FrequencyAnalyser.get_seg_mapper(text, mapper, n)

        # Pegar apenas n-grams que apareceram mais de uma vez
        seg_mapper_filtered = {seg: ind for seg, ind in seg_mapper.items() if len(ind) > 1}

        # Contar a distância entre os segmentos
        seg_dists = {seg: Utils.count_distances(ind) for seg, ind in seg_mapper_filtered.items()}

        # Contar todos os fatores das distâncias que aparecem
        all_spacings = sum(seg_dists.values(), [])
        all_factors = sum([Utils.get_factors(s) for s in all_spacings], [])

        factors_dict = {f: 0 for f in all_factors}
        for i in all_factors:
            factors_dict[i] += 1

        # Ordenar os fatores pela ordem que aparecem - a chave é algum fator
        ord_factors_dict = sorted(factors_dict.items(), key=lambda x:x[1], reverse=True)

        return ord_factors_dict

class VigenereCipher:
    def __init__(self, mapper):
        self.mapper = mapper
    
    def _cipher_message(self, plaintext, key):
        keyword = Utils.get_keystream(plaintext, key)
        ciphered_message = ""

        for i in range(0, len(plaintext)):
            ciphered_char = (Utils.get_int(self.mapper, plaintext[i]) + Utils.get_int(self.mapper, keyword[i])) % len(self.mapper)
            ciphered_char = Utils.get_char(self.mapper, ciphered_char)
            ciphered_message += ciphered_char

        return ciphered_message

    def _decipher_message(self, ciphered_text, key):
        keyword = Utils.get_keystream(ciphered_text, key)
        deciphered_message = ""

        for i in range(0, len(ciphered_text)):
            deciphered_char = (Utils.get_int(self.mapper, ciphered_text[i]) - Utils.get_int(self.mapper, keyword[i])) % len(self.mapper)
            deciphered_char = Utils.get_char(self.mapper, deciphered_char)
            deciphered_message += deciphered_char

        return deciphered_message

    def cipher_any_message(self, plaintext, key):
        plaintext = plaintext.upper()
        
        cipherable_chars, lacking_chars = Utils.get_cipherable_chars(plaintext, self.mapper)
        ciphered_message = self._cipher_message(cipherable_chars, key)
        ciphered_message = list(ciphered_message)

        for ind, char in lacking_chars.items():
            ciphered_message.insert(ind, char)

        return "".join(ciphered_message)

    def decipher_any_message(self, plaintext, key):
        plaintext = plaintext.upper()
        
        cipherable_chars, lacking_chars = Utils.get_cipherable_chars(plaintext, self.mapper)
        deciphered_message = self._decipher_message(cipherable_chars, key)
        deciphered_message = list(deciphered_message)

        for ind, char in lacking_chars.items():
            deciphered_message.insert(ind, char)

        return "".join(deciphered_message)

    def guess_key(self, key_size, text, freq_dict):
        guessed_key = []

        for i in range(0, key_size):
            letters = []
            d = i

            while d <= (len(text) - 1):
                letters.append(text[d])

                d += key_size

            letters_freq = FrequencyAnalyser.get_frequency(letters, self.mapper.keys())
            letters_freq = dict(sorted(letters_freq.items()))

            total_comps = []

            for i in range(0, 26):
                temp_dict = {k: letters_freq[k] for k in [Utils.shift_char(k, i) for k in letters_freq.keys()]}
                temp_comp = Utils.cosine_similarity(temp_dict.values(), freq_dict.values())
                total_comps.append([list(temp_dict.keys())[0], temp_comp])

            # A letra escolhida é a primeira do alfabeto com frequência mais semelhante à frequência real
            guessed_key.append(sorted(total_comps, key=lambda l:l[1], reverse=True)[0][0])

        return "".join(guessed_key)

    def break_cipher(self, ciphered_text, dict_checker, freq_mapper, checked_keys=10):
        ciphered_text = ciphered_text.upper()
        cipherable_text, _ = Utils.get_cipherable_chars(ciphered_text, self.mapper)
        possible_sizes = FrequencyAnalyser.get_possible_key_sizes(cipherable_text, self.mapper)

        exist_dict = dict()

        if checked_keys > len(possible_sizes):
            checked_keys = len(possible_sizes)

        for possible_size in possible_sizes[0:checked_keys]:
            guessed_key = self.guess_key(possible_size[0], cipherable_text, freq_mapper)
            deciphered_text = self.decipher_any_message(ciphered_text, guessed_key)
            checked_words = [dict_checker.check(w) for w in deciphered_text.split(" ") if len(w) > 0]
            exist_dict[guessed_key] = sum(checked_words)/len(checked_words)

        probable_key = list({k: v for k, v in sorted(exist_dict.items(), key=lambda item: item[1], reverse=True)}.keys())[0]

        return probable_key