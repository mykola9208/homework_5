WORDS = {}


def flatten(arr):
    result = []
    for item in arr:
        result += item
    return result


def grep(pattern):
    desired = None
    while True:
        desired = yield desired
        if desired.find(pattern) < 0:
            desired = None


def add_word(word):
    global WORDS

    def inner_func(inn):
        for i in range(0, len(inn) + 1):
            if i == len(inn):
                return {'TERM': word}
            else:
                return {inn[i]: inner_func(inn[i + 1:len(inn)])}
    num = 0
    temp = WORDS
    while num < len(word)+1:
        if num == len(word):
            temp.setdefault('TERM', word)
            break
        else:
            if temp.get(word[num]) is None:
                temp.setdefault(word[num], inner_func(word[num+1:len(word)]))
                break
            else:
                temp = temp.get(word[num])
                num += 1
    return WORDS

def get_words(chars):
    global WORDS
    term = WORDS
    for i in chars:
        if term is not None:
            term = term.get(i)
    print(term)
    return


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
    get_words('helpful')

