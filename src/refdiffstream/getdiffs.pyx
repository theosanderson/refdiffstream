
def compare_strings(str s1, str s2):
    cdef list index_list = []
    cdef int i
    for i in range(min(len(s1), len(s2))):
        if s1[i] != s2[i] and s1[i] not in "N-" and s2[i] not in "N-":
            # create a mutation_string like "C123T"
            mutation_string = s1[i] + str(i+1) + s2[i]
            index_list.append(mutation_string)
            
    return index_list
    