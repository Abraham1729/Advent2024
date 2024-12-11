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
# print(int(sum(evaled_reports))) # Answer is 483


def create_diff_arrays(data):
    for i in range(len(data)):
        # run backwards through levels to create diff array
        for j in range(len(data[i]) - 1, 0, -1):
            data[i][j] = data[i][j] - data[i][j - 1]

        # make first level = 0 for no meaningful diff
        data[i][0] = 0

    return data

report_diffs = create_diff_arrays(test_data)

print(test_data)
print(report_diffs)

def count_diff_signage(report):
    positives = sum(report[report>0])
    negatives = sum(report[report<0])
    return positives, negatives

positives, negatives = count_diff_signage(report_diffs[0])

def eval_monoticity(report):
    # Returns TRUE if already monotonic #
    # Returns FALSE if cannot be made monotonic with 1 level removed #
    # If CAN be made monotonic with 1 level removed, returns bool array of len(report) to indicate which levels *could* be removed to satisfy monotonicity #
    
    # Check to see if the report is already monotonic #
    positives,negatives = count_diff_signage(report)
    if positives == 0 or negatives == 0: return True

    # Ok, we've narrowed down to non-monotonic reports --> at least three levels, min value for positives and negatives is both 1
    # If BOTH positive and negative counts > 1, then this cannot be resolved by removing 1 level #
    if positives > 1 and negatives > 1: return False

    # We have now filtered down to non-monotonic reports which have exactly one level out of alignment, but not determined if that's positive or negative #
    # We can figure out the preferred directionality of this report by checking to see whether positives outweight negatives #
    # This should avoid the 1==1 pitfall because we ruled out reports of len 2 with our initial check for monotonicity #
    to_remove = -1 if positives > negatives else 1 # use direction as an int indicator of increasing or decreasing preference #

    # Always check this against the test case of [1,3,2,4] which can be solved with [1,2,4] OR [1,3,4] #
    # Left to right gives us UDU #
    # Right to left gives us DUD #
    # The actual issue is that a diff array "straddles" the two indices which could feasibly be removed for monotonicity's sake. #

    # We can get this using some array magic, or just by iterating #
    diff_array = report[1:] - report[:-1]

    # We have the sign of what we want to remove: -1 or 1 if negative or positive #
    # Can we just do some multiplication against this array to single out the "single" diff index that is a fixable problem? #
    diff_index = np.where(diff_array * to_remove > 0) # array of indices which satisfy this condition. Should be array of 1

    els_to_remove = (diff_index - 1, diff_index)
    
    # Could I just return this rather than a bool array? I mean yeah, functionally can get the same thing from this.

    


    # But if THREE levels, any one element could be removed to regain monotonicity
    if len(report) == 3:
        print("Need to figure out what return case to make.")
        print("Do I return indicies of legitimate removal items for this condition?")
        print("In that case, I'd be trying to categorize each failure type and then identify which indices could be removed per failure")
        print("The union of these index sets would be the collection of levels that could be removed to satisfy all violated rules")



    # - pos = 1, neg > 1
    if positives == 1:
        pass

    # - pos > 1, neg = 1
    if negatives == 1: 
        pass

    # - pos > 1, neg > 1 
    if positives > 1 and negatives > 1:
        pass






print(positives,negatives)



# 3) Now need to add a "bad level" counter to help me decide if there's a way to dampen away my problems
# 3a) Please note that the level that needs removing isn't necessarily the rightmost of the two of them.
# -- If you have a range problem, don't assume the LHS is the one that needs removal. You'll need to check both.
# -- Ex1: [1 7 8 9]. If you only check LHS you won't see that removal of "1" actually makes report safe.
# -- Ex2: [1 1 2 3]. This one is trivial. You can safely remove either.
# -- Ex3: [1 3 2 4]. This one can remove *EITHER*. [1 3 4] and [1 2 4] are BOTH legitimate solutions.
# -- Ex3b:[1 3 2 4 5] Same deal
# -- Ex3c:[1,4,3,7,10]. This one only has one solution: [1 4 7 10], as [1 3 7 10] breaks range rule.

# -- Ex: [1,4,3,2,1]. Here I would alert on [4,3] through iteration, but the soultion is [4,3,2,1]
# I need to divide into [increasing,decreasing] sequences I think.
# I need more information than that. [Increasing:2, Decreasing: 2, Increasing 2]
# If segments of increasing and decreasing both exist, check magnitude. if both greater than 2 (or sum greater than 2) then you're screwed.
# Otherwise there may be salvaging to be done.


# We have already sorted into "safe" and "unsafe", so we can iterate only on "unsafe" to see if we can dampen out the danger.
# For ease of design let's break this down, though it may not be optimized.
# 1: Check for repetion aka diff = 0. For the first occurrence of this, remove the LHS, flip an indicator, and continue.
# 2: Does monotonic need to be solved before range? Possibly...
# Monotonic might need to be first. Consider [1,3,1,2,3] -> [1,1,2,3] not safe


# [1,  3,  1,  2,  4,  3,  2]
# [0,  2, -2,  1,  2, -1, -1]
# Count of positive: 3
# Count of negative: 3
# Not solvable. Diffs are the answer.

def save_single_duplicates(data):
    pass

