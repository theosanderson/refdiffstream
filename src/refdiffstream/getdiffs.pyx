
def compare_strings(str s1, str s2):
    cdef list index_list = []
    cdef int i
    for i in range(min(len(s1), len(s2))):
        if s1[i] != s2[i] and s1[i] not in "N-" and s2[i] not in "N-":
            # create a mutation_string like "C123T"
            mutation_string = s1[i] + str(i+1) + s2[i]
            index_list.append(mutation_string)
            
    return index_list
    

def count_Ns(str s):
    cdef int i, N_count = 0
    for i in range(len(s)):
        if s[i] == "N":
            N_count += 1
    return N_count


def count_gaps(str s):
    cdef int i, gap_count = 0
    for i in range(len(s)):
        if s[i] == "-":
            gap_count += 1
    return gap_count