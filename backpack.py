# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 10:33:39 2019

@author: gigabyte-artur@mail.ru
"""

import random
import math
import copy

MAX_WEIGHT = 100000                  # Максмальный вес одного элемента
COUNT_ELEMS = 1000                   # Всего элементов в начальном рюкзаке
SOLUTION_PER_GENERATION = 100       # Количество решений на одно поколение
MUTATE_PERCENT = 5                 # Вероятность мутации, в процентах
CONSTANT_SOLUTION = 5               # Количество неизменных стратегий
SELECTED_SOLUTION = 20              # Всего отбираемые стратегии при селекции
MAX_EPOCH = 1000                    # Максимальное количество эпох расчёта

# Генерирует случайное решение по массиву arr_in.
def gen_solution(arr_in):
    rez = dict()
    rez1 = []
    rez2 = []
    for curr_arr_in in arr_in:
        choize = random.random()
        if choize > 0.5:
            rez1.append(curr_arr_in)
        else:
            rez2.append(curr_arr_in)
    rez['pack1'] = rez1
    rez['pack2'] = rez2
    return rez

# Выводит на экран оба рюкзака из решения solution_in.
def show_solution(solution_in):
    print(solution_in['pack1'])
    print(solution_in['pack2'])

# Генерирует начальное поколение из массива arr_in.
def generate_start(arr_in):
    rez = []
    c = 0
    while c < SOLUTION_PER_GENERATION:
        new_solution = gen_solution(arr_in)
        rez.append(new_solution)
        c = c + 1
    return rez

# Копирует решение solution_in.
def copy_solution(solution_in):
    rez = dict()
    pack1 = []
    pack2 = []
    for curr_pack1 in solution_in['pack1']:
        pack1.append(curr_pack1)
    for curr_pack2 in solution_in['pack2']:
        pack2.append(curr_pack2)
    rez['pack1'] = pack1
    rez['pack2'] = pack2
    return rez

# Полностью копирует поколение generation_in.
def copy_generation(generation_in):
    rez = []
    for curr_solution in generation_in:
        new_solution = copy_solution(curr_solution)
        rez.append(new_solution)
    return rez

# Применяет мутации к решению solution_in.
def mutate_solution(solution_in):
    rez = dict()
    new_pack1 = []
    new_pack2 = []
    for curr_pack1 in solution_in['pack1']:
        choise = random.randint(1, 100)
        if choise < MUTATE_PERCENT:
            new_pack2.append(curr_pack1)
        else:
            new_pack1.append(curr_pack1)
    for curr_pack2 in solution_in['pack2']:
        choise = random.randint(1, 100)
        if choise < MUTATE_PERCENT:
            new_pack1.append(curr_pack2)
        else:
            new_pack2.append(curr_pack2)
    rez['pack1'] = new_pack1
    rez['pack2'] = new_pack2
    return rez

# Применяет мутации к поколению generation_in.
def mutate_generation(generation_in):
    rez = []
    for curr_generation_in in generation_in:
        new_solution = mutate_solution(curr_generation_in)
        rez.append(new_solution)
    return rez

# Вычисляет сумму элементов массива arr_in.
def summ_arr(arr_in):
    rez = 0
    for curr_arr_in in arr_in:
        rez = rez + curr_arr_in
    return rez

# Вычисляет значение целевой функции для решения solution_in.
def count_target(solution_in):
    rez = 999999
    sum1 = summ_arr(solution_in['pack1'])
    sum2 = summ_arr(solution_in['pack2'])
    rez = sum1 - sum2
    rez = math.fabs(rez)
    return rez

# Сортирует поколение по целевой функции.
def sort_generation_by_target(generation_in):
    sorted = False
    while (not sorted):
        sorted = True
        c = 0
        while (c < len(generation_in) - 1):
            targ1 = count_target(generation_in[c])
            targ2 = count_target(generation_in[c + 1])
            if targ1 > targ2:
                sorted = False
                temp = generation_in[c]
                generation_in[c] = generation_in[c + 1]
                generation_in[c + 1] = temp
            c = c + 1

# Выполняет селекцию поколения generation_in.
def seletion_generation(generation_in):
    rez = []
    sort_generation_by_target(generation_in)
    for curr_solution in generation_in[0:CONSTANT_SOLUTION]:
        rez.append(curr_solution)
    temp_selected = generation_in[0:SELECTED_SOLUTION]
    while len(rez) < SOLUTION_PER_GENERATION:
        new_index = random.randint(0, len(temp_selected)-1)
        selected_solution = temp_selected[new_index]
        selected_solution = mutate_solution(selected_solution)
        rez.append(selected_solution)
    return rez

# Выводит решения поколения вместе со значеями целевой функции.
def show_generation_with_target(generation_in):
    for curr_generation_in in generation_in:
        print(curr_generation_in)
        print(count_target(curr_generation_in))

# Генерирует случайный стартовый рюкзак длиной len_in с максимальным
# весом max_w_in.
def generate_start_backpack(len_in, max_w_in):
    rez = []
    while (len(rez) < len_in):
        new_w = random.randint(1, max_w_in)
        rez.append(new_w)
    return rez

# Генерирует тривиальное решение из начального рюкзака array_in.
def generate_traivial_solution(array_in):
    rez = dict()
    arr_work = copy.copy(array_in)
    len_arr = len(arr_work)
    rez1 = []
    rez2 = []
    while len_arr > 0:
        max_arr = 0
        max_index = -1
        curr_index = 0
        for curr_arr_in in arr_work:
            if curr_arr_in > max_arr:
                max_arr = curr_arr_in
                max_index = curr_index
            curr_index = curr_index + 1
        sum1 = summ_arr(rez1)
        sum2 = summ_arr(rez2)
        if sum1 < sum2:
            rez1.append(max_arr)
        else:
            rez2.append(max_arr)
        del arr_work[max_index]
        len_arr = len(arr_work)
    rez['pack1'] = rez1
    rez['pack2'] = rez2
    return rez

random.seed()
begin_array = generate_start_backpack(COUNT_ELEMS, MAX_WEIGHT)
print(begin_array)
#trivial_solution = generate_traivial_solution(begin_array)
trivial_solution = gen_solution(begin_array)
print("trivial: ")
print(count_target(trivial_solution))
old_generation = generate_start(begin_array)
old_generation.insert(0, trivial_solution)
best_solution = old_generation[0]
print(0, ": ", count_target(best_solution))
print('------')
epoch = 0
while (epoch < MAX_EPOCH):
    new_generation = copy_generation(old_generation)
    new_generation = seletion_generation(new_generation)
    old_generation = copy_generation(new_generation)
    best_solution = new_generation[0]
    sol1 = new_generation[1]
    sol2 = new_generation[2]
    sol3 = new_generation[3]
    sol4 = new_generation[4]
    sol5 = new_generation[5]
    sol6 = new_generation[6]
    sol7 = new_generation[7]
    sol8 = new_generation[8]
    sol9 = new_generation[9]
    curr_target = count_target(best_solution)
    tar1 = count_target(sol1)
    tar2 = count_target(sol2)
    tar3 = count_target(sol3)
    tar4 = count_target(sol4)
    tar5 = count_target(sol5)
    tar6 = count_target(sol6)
    tar7 = count_target(sol7)
    tar8 = count_target(sol8)
    tar9 = count_target(sol9)
    sum_sol = curr_target + tar1 + tar2 + tar3 + tar4 + tar5 + tar6 + tar7 + tar8 + tar9
    avg_sol = (sum_sol / 10)
    print(epoch, ": ", curr_target, " - ", avg_sol)
    if (curr_target <= 1):
        break
    epoch = epoch + 1
print('------')
print(best_solution)
print(epoch, ": ", count_target(best_solution))
