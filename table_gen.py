"""
φ    q0     q1	    q2      q3	    q4      q5
0    q4,0   q5,1    q5,1    q5,0    q5,0    q5,0
1    q1,0   q2,0    q3,1    q5,1    q5,1    q5,0
"""
import random


def gen_table(count_exits, from_state, to_state):
    count_states = random.randint(from_state, to_state) #можно порегулировать кол-во состояний
    first_str = 'u ' + ' '.join([f'q{i}' for i in range(count_states)]) + '\n'
    data_lines = [first_str] + [f'{i} ' + ' '.join([f'q{random.randint(0, count_states-1)},{random.randint(0,count_exits-1)}' for _ in range(count_states)]) + '\n' for i in range(count_exits)] #цифорка в конце - количество выходов
    with open('gen_table.txt', 'w') as file:
        file.writelines(data_lines)

if __name__ == '__main__':
    from_state, to_state = 4, 5
    gen_table(3, from_state, to_state)