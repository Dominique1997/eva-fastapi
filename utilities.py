import difflib


class Utilities:
    @classmethod
    def average_similarity(cls, input_sentence, compare_sentence):
        total_similarity = 0
        total_pairs = 0

        for input_sentence_word in input_sentence:
            for compare_sentence_word in compare_sentence:
                total_similarity += difflib.SequenceMatcher(None, input_sentence_word, compare_sentence_word).ratio()
                total_pairs += 1

        return total_similarity / total_pairs * 100 if total_pairs != 0 else 0
