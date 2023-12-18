from functools import cmp_to_key, reduce
from operator import index


cards: list[str] = [
    "J", "2", "3", "4", "5", "6", "7", "8", "9", "T",  "Q", "K", "A"
]


def compare_types(left_hand: str, right_hand: str) -> int:
    sorted_left_hand = sorted(left_hand[:5], key=cards.index)
    sorted_right_hand = sorted(right_hand[:5], key=cards.index)

    reduced_left_hand: set[str] = set(
        card for card in sorted_left_hand if card != 'J')
    reduced_right_hand: set[str] = set(
        card for card in sorted_right_hand if card != 'J')

    left_count_of_jokers: int = sorted_left_hand.count('J')
    right_count_of_jokers: int = sorted_right_hand.count('J')

    len_reduced_left_hand = len(reduced_left_hand)
    len_reduced_right_hand = len(reduced_right_hand)
    if len_reduced_left_hand == 0 and len_reduced_right_hand == 1:
        return -1
    if len_reduced_left_hand == 1 and len_reduced_right_hand == 0:
        return 1

    if len_reduced_left_hand > len_reduced_right_hand:
        return -1
    if len_reduced_left_hand < len_reduced_right_hand:
        return 1

    if len_reduced_left_hand in [3, 2]:
        left_highest_duplicate: int = max(
            sorted_left_hand.count(
                card) + (left_count_of_jokers if card != 'J' else 0)
            for card in reduced_left_hand
        )
        right_highest_duplicate: int = max(
            sorted_right_hand.count(
                card) + (right_count_of_jokers if card != 'J' else 0)
            for card in reduced_right_hand
        )
        if left_highest_duplicate > right_highest_duplicate:
            return 1
        if left_highest_duplicate < right_highest_duplicate:
            return -1
    return 0


def comparator(left_hand: str, right_hand: str) -> int:
    type: int = compare_types(left_hand, right_hand)
    if type != 0:
        return type
    for i in range(5):
        if cards.index(left_hand[i]) < cards.index(right_hand[i]):
            return -1
        elif cards.index(left_hand[i]) > cards.index(right_hand[i]):
            return 1
    return 0


def get_sorted_hands(hands_and_bids: list[str]) -> list[str]:
    return sorted(hands_and_bids, key=cmp_to_key(comparator))


def get_total_winings(hands_and_bids: list[str]) -> int:
    sorted_hands: list[str] = get_sorted_hands(hands_and_bids)
    return sum(
        int(hand.split()[1]) * (i + 1) for i, hand in enumerate(sorted_hands)
    )


def main(file_name: str = './7/input.txt'):
    with open(file_name, 'r') as file:
        hands_and_bids: list[str] = file.read().splitlines()
        print(get_total_winings(hands_and_bids))


if __name__ == '__main__':
    main()
