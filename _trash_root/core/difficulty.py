from dataclasses import dataclass

@dataclass
class Difficulty:
    stage: int = 1; speed: float = 1.0

class DifficultyService:
    def __init__(self, step_sec: float = 20.0, increment: float = 0.15, max_stage: int = 10):
        self.step_sec = float(step_sec); self.increment = float(increment); self.max_stage = int(max_stage)
        self._elapsed = 0.0; self._d = Difficulty()

    def reset(self) -> None:
        self._elapsed = 0.0; self._d = Difficulty()

    def tick(self, dt: float) -> None:
        if dt <= 0: return
        self._elapsed += dt
        while self._elapsed >= self.step_sec and self._d.stage < self.max_stage:
            self._elapsed -= self.step_sec
            self._d.stage += 1
            self._d.speed = round(1.0 + self.increment * (self._d.stage - 1), 3)

    @property
    def current(self) -> Difficulty:
        return self._d
