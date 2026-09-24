"""What `src/window.py` promises.

The machine may add files here. It may not edit `tools/testrun.py`, which is
what counts these -- see the `evaluator` masks in `goedel.toml`.
"""

from src.window import Window


def test_a_window_keeps_only_its_last_values():
    w = Window(3)
    w.extend([1, 2, 3, 4])
    assert w.values == [2.0, 3.0, 4.0], w.values


def test_a_window_knows_when_it_is_full():
    w = Window(2)
    assert not w.full
    w.push(1)
    assert not w.full
    w.push(2)
    assert w.full


def test_the_mean_is_over_what_is_there():
    w = Window(4)
    w.extend([2, 4])
    assert w.mean() == 3.0, w.mean()


def test_the_peak_is_the_largest_value_still_in_the_window():
    w = Window(2)
    w.extend([9, 1, 2])
    assert w.peak() == 2.0, w.peak()


def test_an_empty_window_refuses_rather_than_inventing_a_number():
    w = Window(2)
    for fn in (w.mean, w.peak):
        try:
            fn()
        except ValueError:
            continue
        raise AssertionError(f"{fn.__name__} answered for an empty window")


def test_a_window_of_zero_is_refused_at_construction():
    try:
        Window(0)
    except ValueError:
        return
    raise AssertionError("a window of no values was accepted")
