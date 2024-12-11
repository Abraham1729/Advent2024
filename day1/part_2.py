import numpy as np

## Pull data in, parse it ##
file = open('./input.txt')
lines = file.readlines()
lines = [[int(i) for i in line.split()] for line in lines]
list_1 = np.array([line[0] for line in lines])
list_2 = np.array([line[1] for line in lines])
file.close()

# Function to count frequency of each location in a list #
def count_location_frequency(list):
    location_dict = {}
    for location in list:
        if location in location_dict:
            location_dict[location] += 1
        else:
            location_dict[location] = 1

    return location_dict

# Now we'll want a function for multiplying a list by a frequency dictionary #
def mul_list_by_freq(list, freqs):
    for i in range(len(list)):
        # List 1 may contain elements not in freq list: Implication 0 #
        list[i] = list[i] * freqs[list[i]] if (list[i] in freqs) else 0
    
    return list

# Finally, we wrap this up in one function #
def calc_list_similarity(list_1, list_2):
    freqs = count_location_frequency(list_2)
    mul_list = mul_list_by_freq(list_1, freqs)
    return sum(mul_list)

# # Let's give this a quick test #
# test_list_1 = [3,5,1,4] # 4 is absent in freq dict, should throw 0
# test_list_2 = [3,5,3,2,6,1,1]
# freqs = count_location_frequency(test_list_2) # {3: 2, 5: 1, 2: 1, 6: 1, 1: 2}
# mul_list = mul_list_by_freq(test_list_1, freqs) # [6, 5, 2, 0]
# print(calc_list_similarity(test_list_1,test_list_2)) # 13

## OK, we should have all the functions we need to go here. Let's run this against our actual lists ##
print(calc_list_similarity(list_1, list_2)) # 26407426