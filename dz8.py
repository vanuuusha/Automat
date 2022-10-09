import logging
from table_gen import gen_table

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class State:
    def __init__(self, name):
        self.name = name
        self.states = []
        self.exits = []

    def add_state(self, state):
        self.states.append(state)

    def add_exit(self, exit):
        self.exits.append(exit)

    def get_new_state(self, letter):
        return self.states[int(letter)]

    def get_exit(self, letter):
        return self.exits[int(letter)]

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Automat:
    def __init__(self, states, show):
        self.states = states
        self.show = show

    def get_answer(self, word, state):
        if state is None:
            state = self.states[0]
        while len(word) > 1:
            letter = word[0]
            state = state.get_new_state(letter)
            word = word[1:]
        else:
            letter = word[0]
            return state.get_exit(letter)

    def distinguishable_2(self, words, first_state, second_state):  # False - отличимы, True - неотличмы
        logs = []
        for word in words:
            if self.get_answer(word, first_state) != self.get_answer(word, second_state):
                if self.show:
                    logger.debug(f'Состояния {first_state} и {second_state} отличимые при слове {word}')
                    logger.debug(f'ψ(q{first_state},{word}) != ψ(q{second_state},{word})')
                    logger.debug(f'{self.get_answer(word, first_state)} != {self.get_answer(word, second_state)}')
                return False
            else:
                logs.append([f'ψ(q{first_state},{word}) != ψ(q{second_state},{word})',
                             f'{self.get_answer(word, first_state)} != {self.get_answer(word, second_state)}'])
        if self.show:
            logger.info(
                f'Состояния {first_state} и {second_state} неотличимы {"на двухбуквенных" if len(words) == 12 else "на трехюуквенных"}')
        for k, v in logs:
            logger.info(k)
            logger.info(v)
        return True

    def distinguishable(self, words):  # True - есть неотличимое состояние
        answer = []
        for first_state in self.states:
            for second_state in self.states:
                if first_state == second_state:
                    continue
                answ = self.distinguishable_2(words, first_state, second_state)
                answer.append(answ)
                if answ == True:
                    correct = [True, first_state, second_state]
        if any(answer):
            return correct
        return [False]


def find_in_states_by_name(name, states):
    for state in states:
        if state.name == name:
            return state


def check_automat(a):
    # для 8
    words = ['0', '2', '1', '00', '20', '21', '22', '12', '02', '01', '10', '11']
    # для 9
    # words = ['0', '2', '1', '00', '20', '21', '22', '12', '02', '01', '10', '11']
    # words.extend(['000', '001', '002', '010', '011', '012', '020', '021',
    #                                    '022', '100', '101', '102', '110', '111', '112', '120', '121',
    #                                    '122', '200', '201', '202', '210', '211', '212', '220', '221',
    #                                    '222'])
    res = a.distinguishable(words=words)
    if res[0]:
        logger.info(f"Неотличмый на двухбуквенных ({res[1]}, {res[2]})")
        # для 8
        words = ['000', '001', '002', '010', '011', '012', '020', '021',
                 '022', '100', '101', '102', '110', '111', '112', '120', '121',
                 '122', '200', '201', '202', '210', '211', '212', '220', '221',
                 '222']
        # для 9
        # words = [f'{second}{main}' for second in '012' for main in ['000', '001', '002', '010', '011', '012',
        # '020', '021', '022', '100', '101', '102', '110', '111', '112', '120', '121', '122', '200', '201', '202',
        # '210', '211', '212', '220', '221', '222']]
        res = a.distinguishable_2(words=words, first_state=res[1], second_state=res[2])
        if not res:
            logger.info("Отличмый на трехбуквенных")
            return True


def create_automat(table_name='gen_table.txt', show=False, count_exits=3):
    with open(table_name, 'r') as file:
        text = file.read()
    text = text.split('\n')
    first_line = text[0].split()[1:]
    lines = [text[i + 1].split()[1:] for i in range(count_exits)]
    states = [State(i[1:]) for i in first_line]
    for i in range(len(first_line)):
        new_states, new_exits = [], []
        for j in range(count_exits):
            text = lines[j][i].split(',')
            new_states.append(find_in_states_by_name(text[0][1:], states))
            new_exits.append(int(text[1]))
        for exit,state in zip(new_exits, new_states):
            states[i].add_state(state)
            states[i].add_exit(exit)

    a = Automat(states=states, show=show)

    return check_automat(a)


if __name__ == '__main__':
    counter = 0
    count_exits = int(input('Количество выходов: ')) # для 8 и 9 - 3
    from_state = 4
    to_state = 5
    while True:
        logger.warning('new automat')
        counter += 1
        table_name = gen_table(count_exits, from_state, to_state)
        flag = create_automat(count_exits=count_exits)
        if flag:
            print(counter)
            create_automat(show=True, count_exits=count_exits)
            break
