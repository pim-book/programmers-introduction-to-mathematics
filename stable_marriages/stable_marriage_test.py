from assertpy import assert_that

from stable_marriage import Suited
from stable_marriage import Suitor
from stable_marriage import stable_marriage
from stable_marriage import verify_stable


def test_eq():
    suitor = Suitor(0, [0, 1])
    suitor2 = Suitor(0, [1, 0])
    suited = Suited(0, [0, 1])
    suited2 = Suited(0, [1, 0])
    assert_that(suitor).is_equal_to(suitor2)
    assert_that(suited).is_equal_to(suited2)


def test_repr():
    suitor = Suitor(0, [0, 1])
    suited = Suited(0, [0, 1])
    assert_that(repr(suitor)).is_equal_to("Suitor(0)")
    assert_that(repr(suited)).is_equal_to("Suited(0)")


def test_verify_stable_stable():
    suitors = [Suitor(0, [0, 1]), Suitor(1, [1, 0])]
    suiteds = [Suited(0, [0, 1]), Suited(1, [1, 0])]
    marriage = {suitors[0]: suiteds[0], suitors[1]: suiteds[1]}
    assert_that(verify_stable(suitors, suiteds, marriage)).is_true()


def test_verify_stable_unstable():
    suitors = [Suitor(0, [1, 0]), Suitor(1, [1, 0])]
    suiteds = [Suited(0, [0, 1]), Suited(1, [0, 1])]
    marriage = {suitors[0]: suiteds[0], suitors[1]: suiteds[1]}
    result = verify_stable(suitors, suiteds, marriage)
    assert_that(result).is_instance_of(tuple)
    assert_that(result[0]).is_false()
    assert_that(result[1]).is_equal_to((suitors[0], suiteds[1]))


def test_stable_marriage_two():
    suitors = [Suitor(0, [0, 1]), Suitor(1, [1, 0])]
    suiteds = [Suited(0, [0, 1]), Suited(1, [1, 0])]
    marriage = stable_marriage(suitors, suiteds)
    assert_that(marriage).is_equal_to(
        {suitors[0]: suiteds[0], suitors[1]: suiteds[1]})
    assert_that(verify_stable(suitors, suiteds, marriage)).is_true()


def test_stable_marriage_six():
    suitors = [
        Suitor(0, [3, 5, 4, 2, 1, 0]),
        Suitor(1, [2, 3, 1, 0, 4, 5]),
        Suitor(2, [5, 2, 1, 0, 3, 4]),
        Suitor(3, [0, 1, 2, 3, 4, 5]),
        Suitor(4, [4, 5, 1, 2, 0, 3]),
        Suitor(5, [0, 1, 2, 3, 4, 5]),
    ]

    suiteds = [
        Suited(0, [3, 5, 4, 2, 1, 0]),
        Suited(1, [2, 3, 1, 0, 4, 5]),
        Suited(2, [5, 2, 1, 0, 3, 4]),
        Suited(3, [0, 1, 2, 3, 4, 5]),
        Suited(4, [4, 5, 1, 2, 0, 3]),
        Suited(5, [0, 1, 2, 3, 4, 5]),
    ]

    marriage = stable_marriage(suitors, suiteds)
    assert_that(marriage).is_equal_to({
        suitors[0]: suiteds[3],
        suitors[1]: suiteds[2],
        suitors[2]: suiteds[5],
        suitors[3]: suiteds[0],
        suitors[4]: suiteds[4],
        suitors[5]: suiteds[1],
    })
    assert_that(verify_stable(suitors, suiteds, marriage)).is_true()


def test_stable_marriage_all_tied():
    suitors = [
        Suitor(0, [5, 4, 3, 2, 1, 0]),
        Suitor(1, [5, 4, 3, 2, 1, 0]),
        Suitor(2, [5, 4, 3, 2, 1, 0]),
        Suitor(3, [5, 4, 3, 2, 1, 0]),
        Suitor(4, [5, 4, 3, 2, 1, 0]),
        Suitor(5, [5, 4, 3, 2, 1, 0]),
    ]

    suiteds = [
        Suited(0, [0, 1, 2, 3, 4, 5]),
        Suited(1, [0, 1, 2, 3, 4, 5]),
        Suited(2, [0, 1, 2, 3, 4, 5]),
        Suited(3, [0, 1, 2, 3, 4, 5]),
        Suited(4, [0, 1, 2, 3, 4, 5]),
        Suited(5, [0, 1, 2, 3, 4, 5]),
    ]

    marriage = stable_marriage(suitors, suiteds)
    assert_that(marriage).is_equal_to({
        suitors[0]: suiteds[5],
        suitors[1]: suiteds[4],
        suitors[2]: suiteds[3],
        suitors[3]: suiteds[2],
        suitors[4]: suiteds[1],
        suitors[5]: suiteds[0],
    })
    assert_that(verify_stable(suitors, suiteds, marriage)).is_true()
