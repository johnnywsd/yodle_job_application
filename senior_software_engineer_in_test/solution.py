import sys


class Solution():

    def __init__(self, denominations):
        self._DENOMINATIONS = denominations
        self._ASC_DENOMINATIONS = sorted(self._DENOMINATIONS)
        self._DES_DENOMINATIONS = list(reversed(self._ASC_DENOMINATIONS))

    def _foo(self, change):
        """Find the minimum number of coins needed,
        using Greedy algorithm

        Return: The minium number of coins needed.

        Arguments
        change: The money need to change
        """
        num = len(self._DES_DENOMINATIONS)
        i = 0
        remain = change
        count = 0
        while i < num:
            curr = self._DES_DENOMINATIONS[i]
            count_curr = remain // curr
            remain = remain % curr
            count += count_curr
            i += 1
        return count

    def _bar(self, right_boundary):
        """Find the minimum number of coins needed,
        using Dynamic Programming algorithm

        Return: A list
        return a list. For example the return value is
    mylist. mylist[i] is the minimum number of coins
    needed to make money i.

        Arguments
        right_boundary -- right boundary of a list of
        money.

        """
        denominations = self._DES_DENOMINATIONS
        f = [None for i in range(right_boundary)]
        f[0] = 0
        for i in range(1, right_boundary):
            tmp = sys.maxint
            found = False
            for deno in denominations:
                if i < deno:
                    continue
                tmp = min(tmp, f[i - deno])
                found = True
            if found:
                f[i] = tmp + 1
            else:
                f[i] = 0
        return f

    def get_result(self, left_boundary, right_boundary):
        """ Get the result: the number of cases that
        the change machine return more coins than necessary

        Return: Integer
        The number of cases that the change machine
        return more coins than necessary
        """
        f = self._bar(right_boundary)
        count = 0
        for i in range(left_boundary, right_boundary):
            a = self._foo(i)
            b = f[i]
            if a > b:
                count += 1
                # print i, a, b
        return count

if __name__ == '__main__':
    DENOMINATIONS = [1, 4, 5, 9]
    s = Solution(DENOMINATIONS)
    left_boundary = 1
    right_boundary = 1000
    count = s.get_result(left_boundary, right_boundary)
    print 'result: %d' % count
