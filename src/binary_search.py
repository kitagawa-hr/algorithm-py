from typing import Callable, Optional


def binary_search(
    condition: Callable[[int], bool], initial_left: int, initial_right: int
) -> Optional[int]:
    """条件を満たす最初のindexを二分探索で探す

    condition(index)は[FFFF...FTTTTT]となるようにsortされているとする.
    F -> TとなるときのTのインデックスを二分探索する.
    返り値よりも小さい値ではconditionはFalseであり、 大きい値ではconditionはTrueとなる.
    ただし、そのような解が存在しない場合はNoneを返す.

    Args:
        condition (Callable[[int], bool]):
        initial_left (int):
        initial_right (int):

    Returns:
        Optional[int]:　解が見つからない場合はNoneを返し、conditionが常に真であるときはinitial_rightを返す.
    """

    def search(left: int, right: int) -> int:
        mid = (left + right) // 2
        if condition(mid):
            if not condition(mid - 1):
                return mid
            return search(left, mid)
        else:
            return search(mid, right)

    if condition(initial_left):  # all True
        return 0
    elif not condition(initial_right):  # all False
        return None
    else:
        return search(initial_left, initial_right)
