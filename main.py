relationship_matrix = []
general_d_list = []
people_list = []

def make_matrix(Descriptions):
    global general_d_list
    general_d_list = []
    people_set = set()

    for i in Descriptions:
        general_d_list.append(i.strip().split())
    for j in general_d_list[:-1]:
        for k in range(1, len(j)):
            people_set.add(j[k])
    global people_list
    people_list = sorted(list(people_set))

    number_people = len(people_list)
    global relationship_matrix
    relationship_matrix = [[0] * number_people for _ in range(number_people)]

    for exp in general_d_list[:-1]: #relationship_matrix filler
        which_bond = exp[0]

        if which_bond == 'CHILD':
            parent_1 = exp[1]
            parent_2 = exp[2]
            parent_1_index = people_list.index(parent_1)
            parent_2_index = people_list.index(parent_2)
            for child_name in exp[3:]:
                child_index = people_list.index(child_name)
                relationship_matrix[parent_1_index][child_index] = 1
                relationship_matrix[parent_2_index][child_index] = 1
                relationship_matrix[child_index][parent_2_index] = 3
                relationship_matrix[child_index][parent_1_index] = 3

        elif which_bond == 'MARRIED':
            couple1 = exp[1]
            couple2 = exp[2]
            couple1_index = people_list.index(couple1)
            couple2_index = people_list.index(couple2)
            relationship_matrix[couple1_index][couple2_index] = 2
            relationship_matrix[couple2_index][couple1_index] = 2

        elif which_bond == 'DEPARTED':
            who_name = exp[1]
            who_index = people_list.index(who_name)
            relationship_matrix[who_index][who_index] = -1

def if_parents(member_index):
    if 3 in relationship_matrix[member_index]:
        return True
    else:
        return False

def if_spouse(member_index):
    if 2 in relationship_matrix[member_index]:
        return True
    else:
        return False

def find_parents(member_index):
    own_line = relationship_matrix[member_index]
    parentt = []
    for i in range(len(own_line)):
        if own_line[i] == 3:
            parentt.append(i)
    return parentt

def find_siblings(member_index):
    parent_index_list = find_parents(member_index)
    parent1_index = parent_index_list[0]
    parent2_index = parent_index_list[1]
    parent1_childs = P1_children_list(parent1_index)
    parent2_childs = P1_children_list(parent2_index)
    common_childs = set()
    for i in parent1_childs:
        if i in parent2_childs:
            common_childs.add(i)
    for j in parent2_childs:
        if j in parent1_childs:
            common_childs.add(j)
    common_childs = list(common_childs)
    return common_childs

def is_spouse_alive(member_index):
    spouse_index = relationship_matrix[member_index].index(2)
    if relationship_matrix[spouse_index][spouse_index] == 0:
        return True #alive
    else:
        return False #dead

def is_alive(member_index):
    if relationship_matrix[member_index][member_index] == -1:
        return False  # dead
    elif relationship_matrix[member_index][member_index] == 0:
        return True  # live

def P1_children_list(member_index): # don't take ali for inheritor ali, cuz ali have no one in PG1
    children = []
    child_index = 0
    for is_child in relationship_matrix[member_index]:
        if is_child == 1:
            if is_alive(child_index) or if_PG1(child_index):
                children.append(child_index)
        child_index += 1
    return children # [] if there is no child      [child_id] if there are child

def all_children_list(member_index):
    children = []
    child_index = 0
    for is_child in relationship_matrix[member_index]:
        if is_child == 1:
            children.append(child_index)
        child_index += 1
    return children # [] if there is no child      [child_id] if there are child

def if_PG1(member_index):  # checks for are there any one in first PG
    #member_matrix_line = relationship_matrix[member_index]
    a = False
    if 1 in relationship_matrix[member_index]:
        for pg1_member_index in range(len(relationship_matrix[member_index])):
            pg1_member_st = relationship_matrix[member_index][pg1_member_index]
            if pg1_member_st == 1:
                if is_alive(pg1_member_index):
                    a = a or True
                elif not is_alive(pg1_member_index):
                    a = a or if_PG1(pg1_member_index)
    else:
        a = a or False
    return a

def PG1_children_sharer(inheritor_index, money):
    children_list = all_children_list(inheritor_index)
    children_list_last = []
    inh_value = []
    for child_id in children_list:
        if is_alive(child_id) or if_PG1(child_id):
            children_list_last.append(child_id)
    childpart = float(money/len(children_list_last))

    for last_child_id in children_list_last:
        if is_alive(last_child_id):
            inh_value.append((people_list[last_child_id], childpart))
        elif not is_alive(last_child_id) and if_PG1(last_child_id):
                inh_value += PG1_children_sharer(last_child_id, childpart)
    return inh_value

def PG1(inheritor_index, money):
    money = int(money)
    inheritance_share_value = []
    if if_spouse(inheritor_index) and is_spouse_alive(inheritor_index):
        spouse_index = relationship_matrix[inheritor_index].index(2)
        inheritance_share_value.append((people_list[spouse_index], money/4)) #spouse money appended
        inheritance_share_value += PG1_children_sharer(inheritor_index, money*3/4)
    else:
        inheritance_share_value += PG1_children_sharer(inheritor_index, money)
    return inheritance_share_value

def PG2_list(member_index):
    parents = []
    parent_index = 0
    for is_parent in relationship_matrix[member_index]:
        if is_parent == 3:
            parents.append(parent_index)
        parent_index += 1
    return parents

def if_PG2(member_index):
    for parent_indexes in PG2_list(member_index):
        if is_alive(parent_indexes) or if_PG1(parent_indexes):
            return True
    else:
        return False

def PG2_parrent_sharer(inheritor_index, money):  #anne ve babaya eşit verecek, eğer biri ölüyse bunu cocuklarına PG1_children_sharer ile dağıt
    parent_index_list = PG2_list(inheritor_index)
    parent1_index = parent_index_list[0]
    parent2_index = parent_index_list[1]
    if is_alive(parent1_index) and is_alive(parent2_index):
        return [(people_list[parent1_index], float(money/2)), (people_list[parent2_index], float(money/2))]
    elif is_alive(parent1_index) or is_alive(parent2_index): ####### ana baba ölüylse çocuklara dağıt
        live_parent_index = parent1_index if is_alive(parent1_index) else parent2_index
        dead_parent_index = parent2_index if is_alive(parent1_index) else parent1_index
        if if_PG1(dead_parent_index):
            return PG1_children_sharer(dead_parent_index, float(money/2)) + [(people_list[live_parent_index], float(money/2))]
        else:
            return [(people_list[live_parent_index], float(money))]
    else:
        last = []
        cache = PG1_children_sharer(parent1_index, float(money/2)) + PG1_children_sharer(parent2_index, float(money/2))
        #siblings = find_siblings(inheritor_index)
        last_index = set()
        for k in cache:
            last_index.add(k[0])
        last_index = list(last_index)
        last_money = [0] * len(last_index)
        for l in cache:
            last_money[last_index.index(l[0])] += l[1]
        for m in range(len(last_index)):
            last.append((last_index[m], last_money[m]))
        return last

def PG2(inheritor_index, money):
    money = int(money)
    inheritance_share_value = []
    if if_spouse(inheritor_index) and is_spouse_alive(inheritor_index):
        spouse_index = relationship_matrix[inheritor_index].index(2)
        inheritance_share_value.append((people_list[spouse_index], float(money/2))) #spouse money appended
        return inheritance_share_value + PG2_parrent_sharer(inheritor_index, money/2)
    else:
        return PG2_parrent_sharer(inheritor_index, money)

def PG3_list(inheritor_index):
    parent_index_list = PG2_list(inheritor_index)
    parent1_index = parent_index_list[0]
    parent2_index = parent_index_list[1]
    gp_list = PG2_list(parent1_index) + PG2_list(parent2_index)
    return gp_list

def if_PG3(member_index):
    for gp_indexes in PG3_list(member_index):
        if is_alive(gp_indexes) or if_PG1(gp_indexes):
            return True
    else:
        return False

def PG3_gp_sharer(inheritor_index, money):
    inherited = []
    gp_list = PG3_list(inheritor_index)
    gp_list_last = []
    for i in gp_list:
         if is_alive(i) or if_PG1(i):
             gp_list_last.append(i)
    divi = len(gp_list_last)
    for k in gp_list_last:
        if is_alive(k):
            inherited.append((people_list[k], float(money/divi)))
        else:
            inherited += [PG1_children_sharer(people_list[k], float(money/divi))]
    return inherited

def PG3(inheritor_index, money):
    money = int(money)
    inheritance_share_value = []
    if if_spouse(inheritor_index) and is_spouse_alive(inheritor_index):
        spouse_index = relationship_matrix[inheritor_index].index(2)
        inheritance_share_value.append((people_list[spouse_index], float(money * 3 / 4)))  # spouse money appended
        return inheritance_share_value + PG3_gp_sharer(inheritor_index, float(money / 4))
    else:
        return PG3_gp_sharer(inheritor_index, float(money))


def inheritance(Descriptions):
    make_matrix(Descriptions)
    deceased_index = people_list.index(general_d_list[-1][1])
    deceased_money = general_d_list[-1][2]
    if if_PG1(deceased_index):
        return PG1(deceased_index, deceased_money)
    elif if_PG2(deceased_index):
        return PG2(deceased_index, deceased_money)
    elif if_parents(deceased_index) and if_PG3(deceased_index):
        return PG3(deceased_index, deceased_money)
    elif if_spouse(deceased_index) and is_spouse_alive(deceased_index):
        spouse_index = relationship_matrix[deceased_index].index(2)
        return [(people_list[spouse_index], float(deceased_money))]
    else:
        return []
