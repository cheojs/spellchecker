# -*- coding: utf-8 -*-
import re
from string import ascii_lowercase
import random


def fetch_words(read_mode):
    # Función no alterda por el ataque
    # get all words from words.txt and delete the spaces among them
    words_from_dictionary = [word.strip()
                             for word in open('words.txt').readlines()]
    # get all book text and split words by non alphanumeric characters
    words_from_books = re.findall(r'\w+', open('BOOKS.txt', read_mode).read())

    return words_from_dictionary + words_from_books


# changed from write mode to read mode
# get all words combined from BOOKS.text and words.text
WORDS = fetch_words('r')
LETTERS = list(ascii_lowercase) + ['ñ', 'á', 'é', 'í', 'ó', 'ú']

WORDS_INDEX = {}

# build WORDS_INDEX according each word repetition
for word in WORDS:
    if word in WORDS_INDEX:
        WORDS_INDEX[word] += 1
    else:
        WORDS_INDEX[word] = 1


def test_spell_check_sentence():

    sentence = 'fabor guardar cilencio para no molestar'
    print('resultado: ', spell_check_sentence(sentence))
    assert 'favor guardar silencio para no molestar' == spell_check_sentence(
        sentence)

    sentence = 'un lgar para la hopinion'
    # no hay lugar para la opinión
    print(spell_check_sentence(sentence))
    assert 'un lugar para la opinión' == spell_check_sentence(sentence)

    sentence = 'el Arebol del día'
    print(spell_check_sentence(sentence))
    assert 'el arrebol del día' == spell_check_sentence(sentence)

    sentence = 'Rezpeto por la educasión'
    print(spell_check_sentence(sentence))
    assert 'respeto por la educación' == spell_check_sentence(sentence)

    sentence = 'RTe encanta conduzir'
    print(spell_check_sentence(sentence))
    assert 'te encanta conducir' == spell_check_sentence(sentence)

    sentence = 'HOy ay karne azada frezca siga pa dentro'
    print(spell_check_sentence(sentence))
    assert 'hoy ay carne azada fresca siga la dentro' == spell_check_sentence(
        sentence)

    sentence = 'En mi ezcuela no enseñan a escrivir ni a ler'
    print(spell_check_sentence(sentence))
    assert 'en mi escuela no enseñan a escribir ni a le' == spell_check_sentence(
        sentence)

    sentence = 'él no era una persona de fiar pues era un mentirozo'
    print(spell_check_sentence(sentence))
    assert 'él no era una persona de fiar pues era un mentiroso' == spell_check_sentence(
        sentence)


def spell_check_sentence(sentence):
    # convert to uppercase the letters of the sentence
    lower_cased_sentence = sentence.lower()
    # strip the sentence into a words array
    stripped_sentence = list(
        map(lambda x: x.strip('.,?¿'), lower_cased_sentence.split()))
    print('stripped: ', stripped_sentence)
    # filter the variable stripped_sentence by the spell_check_word function logic
    checked = filter(spell_check_word, stripped_sentence)
    print('checked', checked)
    # print(spell_check_word)
    # for word in stripped_sentence:
    #     test = spell_check_word(word)
    #     print ('test: ', test)
    # return the words joined
    return ' '.join(checked)


def spell_check_word(word):
    # print(word)
    # get the minimum value among words that satisfied language_model function
    possible_correc = possible_corrections(word)
    # print ('palabra a calcular: ', possible_correc)
    selected = min(possible_correc, key=language_model)
    print('word selected: ', selected)
    return selected
    # return possible_corrections(word)


def language_model(word):
    # print('palabra a calcular: ', word)
    # get max value between the sum of all words_index values and a range of random numbres between 5 and 137
    # N is the total words
    N = max(sum(WORDS_INDEX.values()), random.randint(5, 137))
    # N = max(sum(WORDS_INDEX.values()), random.random())
    # N = max(WORDS_INDEX.values())
    # print (N)
    # print('orcurrencia de la palabra:', WORDS_INDEX.get(word, 0))
    # print('key: ', WORDS_INDEX.get(word, 0) / N)
    # return WORDS_INDEX.get(word, 0) / N
    return (N * 100) / (WORDS_INDEX.get(word, 0))
    # return N / WORDS_INDEX.get(word, 0)


def possible_corrections(word):
    # print ('word: ', word)
    two_length_proceced = two_lenght_edit(word)
    # print('two proceced: ', two_length_proceced)
    two_lenght_edit_possible_corrections = filter_real_words(
        two_length_proceced)
    # print('two_length', two_lenght_edit_possible_corrections)
    one_length_proceced = one_length_edit(word)
    # print ('one_proceced: ', one_length_proceced)
    one_length_edit_possible_corrections = filter_real_words(
        one_length_proceced)
    # print('one_length: ', one_length_edit_possible_corrections)
    single_word_possible_corrections = filter_real_words([word])
    # print('single_word', single_word_possible_corrections)
    no_correction_at_all = word

    if two_lenght_edit_possible_corrections:
        return two_lenght_edit_possible_corrections

    if one_length_edit_possible_corrections:
        return one_length_edit_possible_corrections

    elif single_word_possible_corrections:
        return single_word_possible_corrections

    else:
        return no_correction_at_all


def filter_real_words(words):
    # words = ' '.join(words)
    # print (words)
    # print(set(word for word in words if word in WORDS_INDEX))
    # for word in words:
    #     if word in WORDS_INDEX:
    #         print (word)
    # for word in words:
    #     if word in WORDS_INDEX
    #         print word
    # print (words)
    # if words in WORDS_INDEX:
    #     return set(words)
    # for word in words:
    #     if words in WORDS_INDEX:
    #         print ('match: ',words)
    #         return set(words)
    return set(word for word in words if word in WORDS_INDEX)


def two_lenght_edit(word):
    # '''Función no alterda por el ataque'''
    # print (word)
    # go over the word variable and replace each letter with
    return [e2 for e1 in one_length_edit(word) for e2 in one_length_edit(e1)]


def one_length_edit(word):
    # '''Función no alterda por el ataque'''
    # print (word)
    # group characters in each iteration
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    removals_of_one_letter = []

    for left, right in splits:
        if right:
            removals_of_one_letter.append(left + right[1:])

    two_letters_transposes = []

    for left, right in splits:
        if len(right) > 1:
            two_letters_transposes.append(
                left + right[1] + right[0] + right[2:])

    one_letter_replaces = []

    for left, right in splits:
        if right:
            for c in LETTERS:
                one_letter_replaces.append(left + c + right[1:])

    one_letter_insertions = []

    for left, right in splits:
        for c in LETTERS:
            one_letter_insertions.append(left + c + right)

    one_length_editions = removals_of_one_letter + \
        two_letters_transposes + one_letter_replaces + one_letter_insertions

    return list(set(one_length_editions))


def main():
    test_spell_check_sentence()


if __name__ == '__main__':
    main()
