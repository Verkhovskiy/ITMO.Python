list1 = [82,8,23,97,92,44,17,39,11,12]

#print(help(dir(list)))
#print(help(list.insert), help(list.append), help(list.sort), help(list.remove), help(list.reverse))

list1[1] = 99
list1.append(5)
list1.insert(3, 33333)
list1.pop(3)
list1.pop(-1)
list1.sort(reverse=True)
print(list1)

list2 = [3,5,6,2,33,6,11]
print(sorted(list2))
print(list2)