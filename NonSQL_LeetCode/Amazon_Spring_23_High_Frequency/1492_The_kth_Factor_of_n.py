class Solution:
    def getfactors(self, i: int, n: int, result: list) -> list:
        if n % i == 0:
            result.append(i)
        if i == n:
            return result
        self.getfactors(i+1,n, result)


    def kthFactor(self, n: int, k: int) -> int:
        result_ = list()
        self.getfactors(1, n, result_)
        try:
            return result_[k-1]
        except:
            return -1