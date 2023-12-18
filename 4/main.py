import math


def get_count_for_card(line_number: int, number_of_scratch_cards: list[int], lines) -> int:
    line = lines[line_number]
    card_unparsed, my_numbers_unparsed = line.split('|')

    card_number_unparsed, card_unparsed = card_unparsed.split(':')

    card_number = card_number_unparsed.strip().split()[1]
    card: list[str] = card_unparsed.strip().split()
    my_numbers: list[str] = my_numbers_unparsed.strip().split()

    count: int = 0
    for number in my_numbers:
        if number in card:
            count += 1

    if count == 0:
        return number_of_scratch_cards[line_number]

    for index in range(count):
        number_of_scratch_cards[line_number + index +
                                1] += number_of_scratch_cards[line_number]

    return count * number_of_scratch_cards[line_number]


def get_number_of_scratchcards(lines: list[str]) -> int:
    scratch_cards: list[int] = [1 for _ in lines]
    for line_number in range(len(lines)):
        get_count_for_card(line_number, scratch_cards, lines)
    return sum(scratch_cards)


def main():
    with open('.\\4\\input.txt') as file:
        match_card = file.read()
        print(get_number_of_scratchcards(match_card.split('\n')))


if __name__ == '__main__':
    main()
