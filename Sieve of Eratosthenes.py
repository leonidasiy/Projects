import sys

sys.setrecursionlimit(10000)

def remove_nonprime(nums, i):
    if i >= len(nums)-1:
        return nums
    for num in nums[i+1:]:
        if num % nums[i] == 0:
            nums.remove(num)
    return remove_nonprime(nums, i+1)

def prime_finder(num):
    num_list = list(range(2, num+1))
    remove_nonprime(num_list, 0)
    return num_list

print(prime_finder(11))
print(prime_finder(10000))