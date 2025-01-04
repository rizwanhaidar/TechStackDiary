class Solution:
    def findDifference(self, nums1: List[int], nums2: List[int]) -> List[List[int]]:
        # Convert lists to sets for efficient set operations
        set1, set2 = set(nums1), set(nums2)
    
        # Find elements unique to each list
        answer = [list(set1 - set2), list(set2 - set1)]
    
        return answer
