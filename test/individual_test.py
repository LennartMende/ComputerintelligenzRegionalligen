def individual_test(list: list[int]):
    assert len(list) == 80, "List must include 80 elements!"
    assert sorted(list) == list(range(1, 81)), "List must include all integers from 1 to 80 without duplicates!"