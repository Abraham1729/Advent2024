import numpy as np

## Pull data in, parse it ##
file = open('./input.txt')
lines = file.readlines()
lines = [[int(i) for i in line.split()] for line in lines]
file.close()

## Trying to classify each line "report" by labeling them "safe" or "unsafe" ##
# 1) Each report must be monotonically increasing or decreasing
# 2) Each change in approved direction must have magnitude in [1,3]

## I should be able to perform both tests at the same time -- iterating once ##

def find_safe_reports(data):
    num_reports = len(data)
    are_reports_safe = np.ones(num_reports) # Safe until proven otherwise

    for i in range(num_reports):
        report = data[i]
        num_levels = len(report)
        direction = None

        # Check base case #
        if num_levels == 1: 
            # print(f"Base case: only 1 level. Report safe. {report}")
            continue

        # Not base case? Iterate over report #
        for j in range(1, num_levels):
            diff = report[j] - report[j-1]

            ## Check for equality ##
            if diff == 0:
                are_reports_safe[i] = False
                # print(f"Unsafe, equality condition. Report {report}")
                break
            
            ## Perform direction check ##
            if not direction:
                direction = 1 if diff > 0 else -1
            monotonic = diff * direction # Positive iif monotonic
            if monotonic < 0: 
                are_reports_safe[i] = False
                # print(f"Unsafe, monotonic condition. Report {report}")
                break

            ## Check if diff is in "safe" range ##
            if abs(diff) not in range(1,4):
                # print(f"Unsafe, range condition. Report {report}")
                are_reports_safe[i] = False
                break

    return are_reports_safe

# Test data for my functions #
test_data = np.array([
    [7, 6, 4, 2, 1],
    [1, 2, 7, 8, 9],
    [9, 7, 6, 2, 1],
    [1, 3, 2, 4, 5],
    [8, 6, 4, 4, 1],
    [1, 3, 6, 7, 9]
    ]
)
# find_safe_reports(test_data) # Looks good, let's move on to the real data set.

evaled_reports = find_safe_reports(lines)
print(int(sum(evaled_reports))) # Answer is 483