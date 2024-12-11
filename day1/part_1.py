import numpy as np

## Pull data in, parse it ##
file = open('./input.txt')
lines = file.readlines()
lines = [[int(i) for i in line.split()] for line in lines]
list_1 = np.array([line[0] for line in lines])
list_2 = np.array([line[1] for line in lines])
file.close()

# quicksort
def quicksort(list):
    ## setup ##
    pivot = list[0]
    left=[]; right=[]

    ## categorize non-pivot elements as lt or gt ##
    for i in list[1:]:
        left.append(i) if i < pivot else right.append(i)

    ## dispatch quicksort on left and right, if base case not met ##
    if len(left) > 1: left = quicksort(left) 
    if len(right) > 1: right = quicksort(right)

    ## Stitch everything together as a whole sorted list ##
    return left + [pivot] + right

# ## Test of quicksort ##
# print("Test of my quicksort attempt:")
# test_array = [5,2,8,7,4,1,4,2]
# print(test_array)
# print(quicksort(test_array))

## Sort both lists ## 
list_1 = quicksort(list_1)
list_2 = quicksort(list_2)

## Perform diffs for "distance" measure, output sum ##
diffs = np.array([abs(list_2[i] - list_1[i]) for i in range(len(list_1))])
# print(diffs)
print(sum(diffs))