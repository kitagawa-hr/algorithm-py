from typing import Sequence, Type, Union

Number = Union[int, float]

INF = float("inf")


class TwoPointer(object):
    def __init__(self, array: Sequence[Number], initial_memo: Number = 0) -> None:
        self.array = array
        self.size = len(array)
        self.inital_memo = initial_memo

    def search(self) -> Number:
        solution = INF
        memo = self.inital_memo
        left = 0
        right = 0
        for left in range(self.size):
            while True:
                if right >= self.size or not self.condition(memo, left, right):
                    break
                memo = self.renew(memo, left, right)
                right += 1
            memo = self.reset(memo, left, right)
            solution = min(solution, self.objective(memo, left, right))
        return solution

    def objective(self, memo: Number, left: int, right: int) -> Number:
        """最小化する目的関数"""
        pass

    def condition(self, memo: Number, left: int, right: int) -> bool:
        """満たすべき条件"""
        pass

    def renew(self, memo: Number, left: int, right: int) -> Number:
        """rightが移動した際のmemoの更新"""
        pass

    def reset(self, memo: Number, left: int, right: int) -> Number:
        """leftが移動した際のmemoのリセット"""
        pass


def solve_abc032_c(s: Sequence[Number], k: int) -> int:
    class ABC032CSolver(TwoPointer):
        def __init__(self, array: Sequence[Number], k: int):
            super().__init__(array, initial_memo=1)
            self.k = k

        def objective(self, memo: Number, left: int, right: int) -> Number:
            """最小化する目的関数"""
            return -(right - left)  # 最小化なので、-をつける

        def condition(self, memo: Number, left: int, right: int) -> bool:
            """満たすべき条件"""
            return memo < self.k

        def renew(self, memo: Number, left: int, right: int) -> Number:
            """rightが移動した際のmemoの更新"""
            return memo * self.array[right]

        def reset(self, memo: Number, left: int, right: int) -> Number:
            """leftが移動した際のmemoのリセット"""
            return memo // self.array[left]

    if 0 in s:
        return len(s)
    if min(s) > k:
        return 0
    return -ABC032CSolver(s, k).search()