import re
import eng_to_ipa as ipa
import num2words

def input_to_regexed_text(input_string):
    """
        It cleans off unnecessary information like wait commands that will confuse the following processing functions.

        Input: string - raw text from .rpy file.
        Output: string - the same text, set to lowercase and with variables and timing information removed.
    """

    # convert to lowercase
    regex_line = input_string.lower()

    # remove variables and formatting (italics, wait/nw)
    regex_line = re.sub("[\[\{]{1}[^\[\]\{\}]*[\]\}]{1}", "", regex_line)

    # convert numbers to text
    regex_line = re.sub("[01234567890.]*\d+", lambda nums: num2words.num2words(float(nums.group(0))), regex_line)

    # convert hyphens to space
    regex_line = re.sub("[-]{1}", " ", regex_line)

    # filter only to a-z '.?!,;:
    regex_line = re.sub("[^a-z\'.?!,;:\s]{1}", "", regex_line)

    return regex_line


def regexed_text_to_phonemes(input_string):
    """
        It calls eng-to-ipa to figure out the pronunciation of the input text.
        It also uses unknown_words_to_ipa() to try to find any unknown words eng-to-ipa didn't catch.
        However, due to the nature of English, there will still be words it can't figure out to pronounce, which it will just skip.

        Input: string - processed text to be converted.
        Output: string - IPA pronunciation of input text.
    """

    # convert to IPA
    ipa_line = ipa.convert(input_string)

    # check to see if we have pronunciations for unknown words
    ipa_line = re.sub("[\S]+[*]{1}", lambda unknown_words: unknown_words_to_ipa(unknown_words.group(0)), ipa_line)

    return ipa_line


def phonemes_to_visemes(input_string):
    """
        It converts strings of phonemes in IPA to a list of visemes to describes which sprites to use.
        The function uses lookup tables to convert the string starting from the left.
        It first checks for trigraphs of three characters, then digraphs of two, then for single characters.
        In this way it iterates through the whole input string.

        Input: string - IPA pronunciation of current string.
        Output: list of integers - indicating sequence of visemes (mouth shapes).
    """

    ipa_trigraphs = [
        ("aɪɹ", [12,16,2]),
        ("aʊɹ", [12,14,2])
    ]

    ipa_digraphs = [
        ("eɪ", [14,16]),
        ("oʊ", [18,14]),
        ("aɪ", [12,16]),
        ("aʊ", [12,14]),
        ("ɔɪ", [13,16]),
        ("ju", [16,17]),
        ("ɪɹ", [16,2]),
        ("ɛɹ", [14,2]),
        ("ʊɹ", [14,2]),
        ("ɔɹ", [13,2]),
        ("ɑɹ", [12,2]),
        ("tʃ", [8,5]),
        ("dʒ", [8,5])
    ]

    ipa_single_characters = [
        (".", [0]),
        ("?", [0]),
        ("!", [0]),
        (",", [0]),
        (";", [0]),
        (";", [0]),
        ("i", [16]),
        ("ɪ", [16]),
        ("ɛ", [14]),
        ("æ", [11]),
        ("ɑ", [12]),
        ("ɔ", [13]),
        ("ʊ", [14]),
        ("u", [17]),
        ("ʌ", [11]),
        ("ə", [11]),
        ("ɝ", [15]),
        ("ɚ", [11]),
        ("w", [17]),
        ("j", [16]),
        ("o", [18]),
        ("p", [10]),
        ("b", [10]),
        ("t", [8]),
        ("d", [8]),
        ("k", [9]),
        ("g", [9]),
        ("m", [10]),
        ("n", [8]),
        ("ŋ", [9]),
        ("f", [7]),
        ("v", [7]),
        ("θ", [8]),
        ("ð", [6]),
        ("s", [4]),
        ("z", [4]),
        ("ʃ", [5]),
        ("ʒ", [5]),
        ("h", [1]),
        ("l", [3]),
        ("ɹ", [2])
    ]

    phoneme_list = input_string
    viseme_list = []

    # iterate through input string
    while len(phoneme_list) > 0:
        current_viseme = []

        # TRIGRAPHS
        if len(phoneme_list) >= 3:
            first_three = phoneme_list[:3]
            for phoneme in ipa_trigraphs:
                if first_three == phoneme[0]:
                    current_viseme = phoneme[1]
                    phoneme_list = phoneme_list[3:]
                    break

        # DIGRAPHS
        if len(phoneme_list) >= 2 and current_viseme == []:
            first_two = phoneme_list[:2]
            for phoneme in ipa_digraphs:
                if first_two == phoneme[0]:
                    current_viseme = phoneme[1]
                    phoneme_list = phoneme_list[2:]
                    break

        # SINGLE LETTER
        if current_viseme == []:
            first_one = phoneme_list[:1]
            for phoneme in ipa_single_characters:
                if first_one == phoneme[0]:
                    current_viseme = phoneme[1]
                    phoneme_list = phoneme_list[1:]
                    break

        if current_viseme != []:
            viseme_list.extend(current_viseme)
        else:
            phoneme_list = phoneme_list[1:]

    return viseme_list

def unknown_words_to_ipa(input_string):
    """
        It is used for words not recognized by eng-to-ipa.
        It's a sub-function of regexed_text_to_phonemes().
        If the word is in the lookup table, we can manually insert the pronunciation.
        For words not in the table, just replace with "" (blank string).

        Input: string - word with asterisk at the end (indicator when eng-to-ipa doesn't recognize a word).
        Output: string - IPA pronunciation if we have the word in the list below. Blank string if not.
    """

    # manually add pronunciations for uncommon words
    words_list = [
        ("monika*", "mɑnɪkə"),
        ("yuri*", "jɪdi"), # approximate Japanese "ユリ" with equivalent visemes. English "d" makes the same mouth shape as Japanese "r".
        ("natsuki*", "natski"), # Japanese "ナツキ"
        ("sayori*", "sajodi"), # approximate Japanese "サヨリ" with equivalent visemes
        ("doki*", "doki"),
        ("salvato*", "sælvɑtoʊ")
    ]

    # check to see if the input matches any of the words in our known list
    replacement = ""
    for current_word in words_list:
        if input_string == current_word[0]:
            replacement = current_word[1]
            break

    return replacement