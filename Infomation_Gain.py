import numpy as np


class DTnode:
    def __init__(self, childdata, c_list):
        self.childdata = childdata
        self.condtion = -1
        self.childrenNode = {}
        self.result = None
        self.c_list = c_list
        self.spoint = -1

    def stop(self):
        iplay = I_play(self.childdata)
        if (iplay == 0):
            return True
        else:
            return False


def Ires(dataset):
    num1 = len(dataset[0])
    num2 = len(dataset[1])
    # print(num1, num2)
    num_no_s = 0
    num_yes_s = 0
    num_no_b = 0
    num_yes_b = 0
    # print(dataset[0])
    for sdata in dataset[0]:
        if sdata[1] == "no":
            num_no_s += 1
        else:
            num_yes_s += 1
    for bdata in dataset[1]:
        if bdata[1] == "no":
            num_no_b += 1
        else:
            num_yes_b += 1
    # print(num_no_s, num_yes_s, num_no_b, num_yes_b)
    first = 0
    second = 0
    third = 0
    forth = 0
    if (num_no_s != 0) & ((num_no_s + num_yes_s) != 1):
        first = -(num_no_s / (num_no_s + num_yes_s)) * np.log2(num_no_s / (num_no_s + num_yes_s))
    if (num_yes_s != 0) & ((num_no_s + num_yes_s) != 1):
        second = -(num_yes_s / (num_no_s + num_yes_s)) * np.log2(num_yes_s / (num_no_s + num_yes_s))
    if (num_no_b != 0) & ((num_no_b + num_yes_b) != 1):
        third = -(num_no_b / (num_no_b + num_yes_b)) * np.log2(num_no_b / (num_no_b + num_yes_b))
    if (num_yes_b != 0) & ((num_no_b + num_yes_b) != 1):
        forth = -(num_yes_b / (num_no_b + num_yes_b)) * np.log2(num_yes_b / (num_no_b + num_yes_b))
    # print(first, second, third, forth)
    I_res = -num1 * (first + second) / (num1 + num2) - num2 * (third + forth) / (num1 + num2)
    # print(-I_res)
    return I_res


def I_res(dataset):
    c = findcategery(dataset)
    num_no = np.zeros(len(c)).tolist()
    num_yes = np.zeros(len(c)).tolist()
    for item in dataset:
        if item[1] == "no":
            for j in range(len(c)):
                if item[0] == c[j]:
                    num_no[j] += 1
        else:
            for j in range(len(c)):
                if item[0] == c[j]:
                    num_yes[j] += 1
    entropy = 0

    for i in range(len(c)):
        if (num_no[i] != 0) & (num_yes[i] != 0):
            entropy += (num_no[i] + num_yes[i]) * ((
                                                           -(num_no[i] * np.log2(
                                                               num_no[i] / (num_no[i] + num_yes[i]))) / (
                                                                   num_yes[i] + num_no[i])) - (
                                                           num_yes[i] * np.log2(
                                                       num_yes[i] / (num_no[i] + num_yes[i]))) / (
                                                           num_yes[i] + num_no[i])) / (
                               sum(num_no) + sum(num_yes))
    # print(num_no, num_yes,entropy)
    return entropy


def findcategery(dataset):
    b = []
    for it in dataset:
        b.append(it[0])
    a = np.unique(b)
    c = []
    for element in a:
        c.append(str(element))
        # print(type(str(element)))
    # print(c)
    return c


def I_play(dataset):
    num_yes = 0
    num_no = 0
    for item in dataset:
        if item[len(item) - 1] == "no":
            num_no += 1
        else:
            num_yes += 1
    p_yes = num_yes / (num_yes + num_no)
    p_no = num_no / (num_yes + num_no)
    if (p_no != 0) & (p_yes != 0):
        return (-p_no * np.log2(p_no)) + (-p_yes * np.log2(p_yes))
    else:
        return 0


def info_gain(dataset, clist):
    Iplay = I_play(dataset)
    num = len(dataset[0])
    entropy = []
    split_point_t = -1
    split_point_h = -1
    typeset = np.zeros(num - 1).tolist()
    for it in range(num - 1):
        typeset[it] = type(dataset[0][it])
    for i in range(num - 1):
        split_point = -1
        if isinstance(dataset[0][i], str):
            sI = []
            for item in dataset:
                m = [item[i], item[num - 1]]
                sI.append(m)
            entropy.append(Iplay - I_res(sI))
        else:
            b = []
            dataset.sort(key=lambda x: x[i], reverse=False)
            for j in range(len(dataset) - 1):
                b.append((dataset[j][i] + dataset[j + 1][i]) / 2)
            searchIres = []
            for n in b:
                first_array = []
                second_array = []
                # print("split point:",n)
                for item in dataset:
                    m = [item[i], item[num - 1]]
                    if item[i] < n:
                        first_array.append(m)
                    else:
                        second_array.append(m)
                c = [first_array, second_array]
                searchIres.append(Ires(c))
            for y in range(len(searchIres)):
                searchIres[y] += Iplay
            entropy.append(max(searchIres))
            s = 0
            for ite in range(len(entropy)):
                if entropy[ite] == max(searchIres):
                    s = ite
            if clist[i] == 1:
                split_point_t = b[s]
            else:
                split_point_h = b[s]
    return entropy, split_point_t, split_point_h


def build_tree(treenode):
    if treenode.stop():
        lenth = len(treenode.childdata[0])
        treenode.result = treenode.childdata[0][lenth - 1]
        return
    else:
        da = treenode.childdata
        cli = []
        cli2 = []
        for num_c in range(len(treenode.c_list)):
            cli.append(treenode.c_list[num_c])
            cli2.append(treenode.c_list[num_c])
        entro, spt, sph = info_gain(da, cli)
        max_entro = max(entro)
        record = -1
        for ite in range(len(entro)):
            if entro[ite] == max_entro:
                record = ite
        treenode.condtion = cli[record]
        cli.pop(record)
        ca = []
        if (cli2[record] != 1) & (cli2[record] != 2):
            for item in da:
                ca.append([item[record]])
            ca = findcategery(ca)
            for val in ca:
                c = []
                for indi in da:
                    kk = []
                    if indi[record] == val:
                        for hm in range(len(indi)):
                            if hm != record:
                                kk.append(indi[hm])
                        c.append(kk)
                newnode = DTnode(c, cli)
                treenode.childrenNode[val] = newnode
        else:
            if cli2[record] == 1:
                sma = []
                big = []
                treenode.spoint = spt
                for indiv in da:
                    kk = []
                    for hm in range(len(indiv)):
                        if hm !=record:
                            kk.append(indiv[hm])
                    if indiv[record] < spt:
                        sma.append(kk)
                    else:
                        big.append(kk)
                newnode1 = DTnode(sma, cli)
                newnode2 = DTnode(big, cli)
                treenode.childrenNode["small"] = newnode1
                treenode.childrenNode["big"] = newnode2
            else:
                sma2 = []
                big2 = []
                treenode.spoint = sph
                for indiv in da:
                    kk=[]
                    for hm in range(len(indiv)):
                        if hm !=record:
                            kk.append(indiv[hm])
                    if indiv[record] < sph:
                        sma2.append(kk)
                    else:
                        big2.append(kk)
                    # if indiv[record] < spt:
                    #     sma2.append(indiv)
                    # else:
                    #     big2.append(indiv)
                newnode3 = DTnode(sma2, cli)
                newnode4 = DTnode(big2, cli)
                treenode.childrenNode["small"] = newnode3
                treenode.childrenNode["big"] = newnode4
        for key in treenode.childrenNode.values():
            build_tree(key)

def perdition(test, predicttree):
    tree = predicttree
    result = None
    while tree.condtion !=-1:
        condition = tree.condtion
        for key in tree.childrenNode.keys():
            if tree.spoint!=-1:
                if test[condition] > tree.spoint:
                    tree = tree.childrenNode["big"]
                if test[condition] < tree.spoint:
                    tree = tree.childrenNode['small']
            else:
                if test[condition] == key:
                    tree = tree.childrenNode[key]
    result = tree.result
    return result







if __name__ == "__main__":
    data = [['sunny', 85.0, 85.0, 'false', 'no'], ['sunny', 80.0, 90.0, 'true', 'no'],
            ['overcast', 83.0, 86.0, 'false', 'yes'], ['rainy', 70.0, 96.0, 'false', 'yes'],
            ['rainy', 68.0, 80.0, 'false', 'yes'], ['rainy', 65.0, 70.0, 'true', 'no'],
            ['overcast', 64.0, 65.0, 'true', 'yes'], ['sunny', 72.0, 95.0, 'false', 'no'],
            ['sunny', 69.0, 70.0, 'false', 'yes'], ['rainy', 75.0, 80.0, 'false', 'yes'],
            ['sunny', 75.0, 70.0, 'true', 'yes'], ['overcast', 81.0, 75.0, 'false', 'yes'],
            ['overcast', 72.0, 90.0, 'true', 'yes'], ['rainy', 71.0, 91.0, 'true', 'no']]

    t_node = DTnode(data, [0, 1, 2, 3])
    build_tree(t_node)
    text = ['overcast', 60, 62, 'false']
    # text2 = ['rainy', 60, 62, 'false']
    # text3 = ['sunny', 60, 79, 'false']
    re = perdition(text, t_node)
    print(re)

