
#--------------------------Solution--------------------------#
class Solution:
    
    def pivotIndex(self, nums: List[int]) -> int:
        total_sum = sum(nums)
        left_sum = 0
        length = len(nums)
        for i in range(length):
            right_sum = total_sum - left_sum - nums[i]
            if left_sum == right_sum:
                return i
            left_sum += nums[i]
        return -1
