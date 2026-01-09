from core.scoring import ScoringService
def test_add_for_avoid_default():
    s = ScoringService(); s.add_for_avoid(); assert s.current == 10
def test_add_for_avoid_negative_ignored():
    s = ScoringService(); s.add_for_avoid(-5); assert s.current == 0
def test_reset():
    s = ScoringService(); s.add_for_avoid(15); s.reset(); assert s.current == 0
