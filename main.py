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
    temporary = WORDS
    def inner_func(inn):
        for i in range(0, len(inn) + 1):
            if i == len(inn):
                return {'TERM': word}
            else:
                return {inn[i]: inner_func(inn[i + 1:len(inn)])}
    return inner_func(word)


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

    print(add_word('hello'))


