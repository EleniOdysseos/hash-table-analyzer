import time


# Reads all non-empty lines from the file and returns them as a list of words
def read_words(filename):
    words = []
    f = open(filename, "r", encoding="utf-8")
    for line in f:
        w = line.strip()
        if w != "":
            words.append(w)
    f.close()
    return words


# Hash function 1: adds up the ASCII value of each character, then mod m
def hash_sum(s, m):
    total = 0
    for c in s:
        total = total + ord(c)
    return total % m


# Hash function 2: polynomial rolling hash — multiplies by base p=31 at each step
def hash_poly(s, m):
    p = 31
    h = 0
    for c in s:
        h = (h * p + ord(c)) % m
    return h


# Inserts a key using linear probing: checks slots one by one (step +1 each time)
def insert_linear(table, key, hash_func):
    m = len(table)
    start = hash_func(key, m)  # starting position
    collisions = 0
    step = 0

    while step < m:
        position = (start + step) % m  # wrap around with mod

        if table[position] is None:       # empty slot — insert here
            table[position] = key
            return collisions
        elif table[position] == key:      # key already exists — skip
            return collisions
        else:                             # slot taken by another key — collision
            collisions = collisions + 1
            step = step + 1

    return collisions  # table is full, couldn't insert


# Searches for a key using linear probing
def find_linear(table, key, hash_func):
    m = len(table)
    start = hash_func(key, m)
    step = 0

    while step < m:
        position = (start + step) % m

        if table[position] is None:       # empty slot means key was never inserted
            return False
        elif table[position] == key:      # found it
            return True

        step = step + 1

    return False


# Inserts a key using quadratic probing: step grows as 0, 1, 4, 9, 16... (step^2)
def insert_quadratic(table, key, hash_func):
    m = len(table)
    start = hash_func(key, m)
    collisions = 0
    step = 0

    while step < m:
        position = (start + step * step) % m  # quadratic jump

        if table[position] is None:
            table[position] = key
            return collisions
        elif table[position] == key:
            return collisions
        else:
            collisions = collisions + 1
            step = step + 1

    return collisions


# Searches for a key using quadratic probing
def find_quadratic(table, key, hash_func):
    m = len(table)
    start = hash_func(key, m)
    step = 0

    while step < m:
        position = (start + step * step) % m

        if table[position] is None:
            return False
        elif table[position] == key:
            return True

        step = step + 1

    return False


# Builds all 12 tables (2 hash functions x 2 strategies x 3 sizes)
def build_all_tables(words):
    sizes = [1009, 2003, 5003]

    hash_functions = [
        ("hash_sum", hash_sum),
        ("hash_poly", hash_poly)
    ]

    strategies = [
        ("linear", insert_linear, find_linear),
        ("quadratic", insert_quadratic, find_quadratic)
    ]

    tables_info = []

    for h_name, h_func in hash_functions:
        for s_name, insert_fn, find_fn in strategies:
            for m in sizes:
                table = [None] * m       # empty table of size m
                total_collisions = 0

                for w in words:
                    c = insert_fn(table, w, h_func)  # insert each word, count collisions
                    total_collisions = total_collisions + c

                # count how many slots are filled
                non_empty = 0
                for x in table:
                    if x is not None:
                        non_empty = non_empty + 1

                empty = m - non_empty
                load_factor = non_empty / float(m)  # ratio of filled slots

                info = {
                    "hash_name": h_name,
                    "hash_func": h_func,
                    "strategy_name": s_name,
                    "find_func": find_fn,
                    "size": m,
                    "table": table,
                    "collisions": total_collisions,
                    "non_empty": non_empty,
                    "empty": empty,
                    "load_factor": round(load_factor, 3)
                }
                tables_info.append(info)

    return tables_info


# Searches for a word in all 12 tables and measures time for each
def search_all_tables(tables_info, word):
    results = []

    for info in tables_info:
        table = info["table"]
        find_fn = info["find_func"]
        h_func = info["hash_func"]

        start_ns = time.perf_counter_ns()         # start timer
        found = find_fn(table, word, h_func)
        end_ns = time.perf_counter_ns()           # stop timer

        elapsed_ns = end_ns - start_ns
        elapsed_us = elapsed_ns / 1000.0          # convert ns to microseconds

        results.append({
            "hash_name": info["hash_name"],
            "strategy_name": info["strategy_name"],
            "size": info["size"],
            "found": found,
            "time_us": round(elapsed_us, 2)
        })

    return results
