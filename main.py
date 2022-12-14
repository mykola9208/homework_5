WORDS = {}


def flatten(arr):
    for item in arr:
        while len(item) > 0:
            yield item.pop(0)


def grep(pattern):
    desired = None
    while True:
        desired = yield desired
        if desired.find(pattern) < 0:
            desired = None


def add_word(word):
    temp = WORDS
    for i in range(0, len(word)):
        temp.setdefault(word[i], {})
        temp = temp.get(word[i])
    temp.setdefault('TERM', word)
    return WORDS


def get_words(chars):
    term = WORDS
    for i in chars:
        if term is not None:
            term = term.get(i)
    terminus = []
    lis = []

    def list_terms(mass):
        if isinstance(mass, dict):
            for value in mass.values():
                lis.append(value)
        else:
            terminus.append(mass)
        for cont in lis:
            lis.remove(cont)
            return list_terms(cont)
    if term is not None:
        list_terms(term)
    return terminus


if __name__ == '__main__':
    assert list(flatten([])) == []
    assert list(flatten([[]])) == []
    assert list(flatten([[], []])) == []
    assert list(flatten([[1, 2], [], [3]])) == [1, 2, 3]
    assert list(flatten([[1, 2], [3, 4, 5]])) == [1, 2, 3, 4, 5]

    search = grep('bbq')
    next(search)
    assert search.send('Birthday invitation') is None
    assert search.send('Bring bbq sauce with') == 'Bring bbq sauce with'
    assert search.send('Are you hungry?') is None
    assert search.send("We won't invite you to our BBQ party then") is None
    assert search.send('but you better be quick (bbq) otherwise') == 'but you better be quick (bbq) otherwise'
    search.close()

    add_word('hello')
    assert WORDS == {'h': {'e': {'l': {'l': {'o': {'TERM': 'hello'}}}}}}
    add_word('hell')
    assert WORDS == {'h': {'e': {'l': {'l': {'o': {'TERM': 'hello'}, 'TERM': 'hell'}}}}}
    add_word('he')
    assert WORDS == {'h': {'e': {'l': {'l': {'o': {'TERM': 'hello'}, 'TERM': 'hell'}}, 'TERM': 'he'}}}
    get_words('hello')
    assert set(get_words('he')) == {'he', 'hell', 'hello'}
    assert get_words('l') == []
    assert set(get_words('hel')) == {'hell', 'hello'}
