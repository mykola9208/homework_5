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
    TEMP = WORDS
    def inner_func(TEMP, inn):
        for i in range(0, len(inn) + 1):
            if i == len(inn):
                TEMP.setdefaul('TERM', word)
            elif TEMP.get(inn[i]) is None:
                TEMP.setdefault(inn[i], inner_func({}, inn[i + 1:len(inn)]))
            else:
                TEMP.update(inn[i], inner_func(TEMP.get(inn[i]), inn[i + 1:len(inn)]))
        return TEMP
    return inner_func

def add_word(word):
    global WORDS
    temp = WORDS
    num = 0
    def inner_func(inn):
        for i in range(0, len(inn) + 1):
            if i == len(inn):
                return {'TERM': word}
            else:
                return {inn[i]: inner_func(inn[i + 1:len(inn)])}
    while temp.get(word[num]) is not None and num < len(word):
        temp = temp.get(word[num])
        num += 1
    temp.setdefault(word[num], inner_func(word[num+1:len(word)]))
    while num > 0:
        num -= 1
        temp = {word[num]: temp}
    WORDS = temp
    return WORDS



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
    print(WORDS)
    add_word('her')
    print(WORDS)
    add_word('help')
    print(WORDS)

