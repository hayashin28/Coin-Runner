from core.difficulty import DifficultyService
def test_tick_stage_up_once():
    d = DifficultyService(step_sec=2.0, increment=0.5, max_stage=3); d.tick(2.1); cur = d.current
    assert cur.stage == 2 and abs(cur.speed - 1.5) < 1e-3
def test_tick_multi_stage_crossing():
    d = DifficultyService(step_sec=1.0, increment=0.2, max_stage=5); d.tick(3.2); cur = d.current
    assert cur.stage == 4 and abs(cur.speed - (1.0 + 0.2*(4-1))) < 1e-3
