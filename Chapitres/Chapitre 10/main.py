def tri_par_insertionl(list: list) -> list:
    for j in range(1, len(list)):
        i = j - 1
        key = list[j]
        while i >= 0 and list[i] > key:
            list[i + 1] = list[i]
            i -= 1
        list[i + 1] = key
    return list

print(tri_par_insertionl([62, 10, 59, 25, 66]))