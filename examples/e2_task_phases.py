"""Original task-phase interface, syntax checked only; not a grasp scorer.

Event predicates must be supplied by an observation consumer with a protocol.
No simulator, assets, thresholds or sensor data are invented in this example.
"""

from dataclasses import dataclass
from enum import Enum
import math


class Phase(Enum):
    APPROACH = "approach"
    CLOSE = "close"
    HOLD = "hold"
    RELEASE = "release"
    DONE = "done"
    FAILED = "failed"


@dataclass(frozen=True)
class Progress:
    phase: Phase = Phase.APPROACH
    elapsed_s: float = 0.0
    stable_s: float = 0.0


def advance_phase(
    progress: Progress,
    dt: float,
    *,
    observation_fresh: bool,
    approach_reached: bool,
    closure_confirmed: bool,
    hold_confirmed: bool,
    release_confirmed: bool,
    dwell_s: float,
    timeout_s: float,
) -> Progress:
    """Advance using simulation time; terminal phases persist until explicit reset.

    dwell_s and timeout_s are caller-provided for the current phase.
    Each phase requires its event continuously for dwell_s. A stale observation
    or phase timeout fails this teaching task. These are application choices,
    not Newton behavior or a substitute for DexLab's eventual protocol.
    """
    if not all(math.isfinite(value) for value in (
        dt, dwell_s, timeout_s, progress.elapsed_s, progress.stable_s
    )):
        raise ValueError("Timing values must be finite")
    if dt <= 0 or dwell_s < 0 or timeout_s <= 0:
        raise ValueError("Require dt > 0, dwell_s >= 0 and timeout_s > 0")
    if progress.elapsed_s < 0 or progress.stable_s < 0:
        raise ValueError("Progress times must be non-negative")
    if progress.phase in (Phase.DONE, Phase.FAILED):
        return progress
    elapsed = progress.elapsed_s + dt
    if not observation_fresh or elapsed >= timeout_s:
        return Progress(Phase.FAILED, elapsed, 0.0)
    transitions = {
        Phase.APPROACH: (approach_reached, Phase.CLOSE),
        Phase.CLOSE: (closure_confirmed, Phase.HOLD),
        Phase.HOLD: (hold_confirmed, Phase.RELEASE),
        Phase.RELEASE: (release_confirmed, Phase.DONE),
    }
    confirmed, following = transitions[progress.phase]
    stable = progress.stable_s + dt if confirmed else 0.0
    if confirmed and stable >= dwell_s:
        return Progress(following)
    return Progress(progress.phase, elapsed, stable)
