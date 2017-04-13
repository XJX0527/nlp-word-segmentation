input_model = []

def create_input_mode(corpus_file):
    rst = []
    with open(corpus_file) as f:
        content = f.read()
        words = content.split()
        for word in words:
            for index, char in enumerate(word, 1):
                s = 'M'
                if index == 1:
                    s = 'B'
                elif index == len(word):
                    s = 'E'

                if len(word) == 1:
                    s = 'S'

                rst.append((s, char))

    return rst

input_dir = 'training_data'
input_file = input_dir + '/' + 'part.utf8'
# input_file = input_dir + '/' + 'pku_training.utf8'
input_model = create_input_mode(input_file)
print(input_model[:100])

def create_ngram(alist, n = 2):
    rst = []
    for i in range(len(alist) - n + 1):
        rst.append(alist[i:i+n])

    return rst

two_gram = create_ngram(input_model)
print(two_gram[:100])

STATE_SPACE = ['B', 'M', 'E', 'S']
OBSERVE_SPACE = list(set(x[1] for x in input_model))
print(len(OBSERVE_SPACE), len(input_model))

def create_reverse_dict(alist):
    rst = {}
    for i, v in enumerate(alist):
        rst[v] = i

    return rst

STATE_SPACE_REVERSE_DICT = create_reverse_dict(STATE_SPACE)
OBSERVE_SPACE_REVERSE_DICT = create_reverse_dict(OBSERVE_SPACE)

def create_transition_probobility(two_gram):
    rst = []
    for i in range(len(STATE_SPACE)):
        rst.append([])
        for j in range(len(STATE_SPACE)):
            rst[i].append([])

    indexs = [(STATE_SPACE_REVERSE_DICT[x[0][0]],
               STATE_SPACE_REVERSE_DICT[x[1][0]])
         for x in two_gram]

    total = len(indexs)
    for i in range(len(STATE_SPACE)):
        for j in range(len(STATE_SPACE)):
            rst[i][j] = len([1 for x in indexs if x[0] == i and x[1] == j]) / total

    return rst

transition_probobitiy = create_transition_probobility(two_gram)
print(transition_probobitiy)


def create_observe_probobility(input_model):
    rst = []
    for i in range(len(STATE_SPACE)):
        rst.append([])
        for j in range(len(OBSERVE_SPACE)):
            rst[i].append([])

    indexs = [(STATE_SPACE_REVERSE_DICT[x[0]],
               OBSERVE_SPACE_REVERSE_DICT[x[1]])
              for x in input_model]

    for i in range(len(STATE_SPACE)):
        total = len([1 for x in indexs if x[0] == i])
        for j in range(len(OBSERVE_SPACE)):
            cnt = len([1 for x in indexs if x[0] == i and x[1] == j])
            rst[i][j] = cnt / total

    return rst


observe_probobility =  create_observe_probobility(input_model)
print(observe_probobility)