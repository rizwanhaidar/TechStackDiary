# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num: int) -> int:

class Solution:
    def guessNumber(self, n: int) -> int:
        start, end = 1, n  # Initialize the start and end values
        while start <= end:
            mid = (start + end) // 2  # Calculate the middle value
            result = guess(mid)  # Get the result of the guess
            if result == -1:
                end = mid - 1  # The secret number is smaller
            elif result == 1:
                start = mid + 1  # The secret number is larger
            else:
                return mid  # The secret number is found
        
        
