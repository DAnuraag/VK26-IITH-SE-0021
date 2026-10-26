"""Executable documentation calculations, not ARKA product implementation.

Inputs are explicit numerical examples. Nothing in this module reads hardware,
connects to a broker, validates plant safety or establishes measured performance.
"""
from dataclasses import dataclass
from math import isfinite


def finite_number(value, name):
    """Reject booleans, missing values and nonfinite arithmetic inputs."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a numeric value")
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return float(value)


def power_w(voltage_v, current_a):
    """Arithmetic power at one defined DC measurement point."""
    v = finite_number(voltage_v, "voltage_v")
    i = finite_number(current_a, "current_a")
    return v * i


def shunt_values(current_a, resistance_ohm=0.010):
    """Return shunt drop and dissipation; not a thermal rating check."""
    i = finite_number(current_a, "current_a")
    r = finite_number(resistance_ohm, "resistance_ohm")
    if r <= 0:
        raise ValueError("resistance must be positive")
    return {"voltage_v": i * r, "dissipation_w": i * i * r}


def ina226_scaling(current_lsb_a=0.00025, shunt_ohm=0.010):
    """Return ideal CAL arithmetic and power LSB, not metrology results."""
    lsb = finite_number(current_lsb_a, "current_lsb_a")
    r = finite_number(shunt_ohm, "shunt_ohm")
    if min(lsb, r) <= 0:
        raise ValueError("current LSB and shunt resistance must be positive")
    return {"cal_ideal": 0.00512 / (lsb * r), "power_lsb_w": 25 * lsb}


def irradiance_w_m2(sensor_mv, sensitivity_mv_per_w_m2=0.2):
    """Use an explicit pyranometer sensitivity; do not convert lux."""
    mv = finite_number(sensor_mv, "sensor_mv")
    sensitivity = finite_number(sensitivity_mv_per_w_m2, "sensitivity")
    if sensitivity <= 0:
        raise ValueError("sensitivity must be positive")
    return mv / sensitivity


def shortfall_fraction(expected_w, measured_w, floor_w):
    """Return guarded residual only above the reviewed expected-power floor."""
    expected = finite_number(expected_w, "expected_w")
    measured = finite_number(measured_w, "measured_w")
    floor = finite_number(floor_w, "floor_w")
    if floor <= 0:
        raise ValueError("power floor must be positive")
    if expected <= floor:
        return None
    return (expected - measured) / max(expected, floor)


@dataclass(frozen=True)
class PowerPoint:
    node_id: str
    boot_id: str
    elapsed_s: float
    power_w: float | None
    valid: bool


def energy_interval(previous, current, maximum_interval_s=2.0):
    """Return Wh, excluded seconds and reason for exactly one interval."""
    maximum = finite_number(maximum_interval_s, "maximum_interval_s")
    if maximum <= 0:
        raise ValueError("maximum interval must be positive")
    t0 = finite_number(previous.elapsed_s, "previous elapsed time")
    t1 = finite_number(current.elapsed_s, "current elapsed time")
    dt = t1 - t0
    if dt <= 0:
        return {"wh": 0.0, "excluded_s": 0.0, "reason": "nonpositive_time"}
    same_source = (previous.node_id, previous.boot_id) == (
        current.node_id, current.boot_id
    )
    values = (previous.power_w, current.power_w)
    numbers_ok = all(
        isinstance(v, (int, float)) and not isinstance(v, bool) and isfinite(v)
        for v in values
    )
    if not same_source:
        reason = "identity_discontinuity"
    elif not previous.valid or not current.valid or not numbers_ok:
        reason = "invalid_endpoint"
    elif dt > maximum:
        reason = "gap_exceeds_policy"
    else:
        wh = 0.5 * sum(values) * dt / 3600.0
        return {"wh": wh, "excluded_s": 0.0, "reason": "valid"}
    return {"wh": 0.0, "excluded_s": dt, "reason": reason}


def persistence_series(times_s, residuals, gates, threshold=0.15,
                       required_s=180.0, maximum_interval_s=2.0):
    """Reference reset-on-gap/gate-loss policy using elapsed time."""
    if not (len(times_s) == len(residuals) == len(gates)):
        raise ValueError("input series lengths must agree")
    if required_s <= 0 or maximum_interval_s <= 0:
        raise ValueError("persistence and maximum interval must be positive")
    started = None
    previous_t = None
    previous_qualified = False
    result = []
    for t, residual, gate in zip(times_s, residuals, gates):
        t = finite_number(t, "elapsed time")
        residual_ok = (
            isinstance(residual, (int, float))
            and not isinstance(residual, bool)
            and isfinite(residual)
        )
        qualified = bool(gate) and residual_ok and residual > threshold
        dt = None if previous_t is None else t - previous_t
        continuous = dt is not None and 0 < dt <= maximum_interval_s
        if not qualified:
            started = None
        elif not continuous or not previous_qualified:
            started = t
        elapsed = 0.0 if started is None else t - started
        result.append({"persistence_s": elapsed,
                       "qualified_alert": qualified and elapsed >= required_s})
        previous_t = t
        previous_qualified = qualified
    return result


def raw_storage_bytes(nodes=10, payload_bytes=200, hz=1, days=30):
    """Raw payload arithmetic; indexes/WAL/logs/backups are excluded."""
    values = [finite_number(v, n) for v, n in zip(
        (nodes, payload_bytes, hz, days), ("nodes", "payload_bytes", "hz", "days")
    )]
    if any(v < 0 for v in values):
        raise ValueError("capacity inputs must be nonnegative")
    n, size, rate, duration = values
    return n * size * rate * 86400 * duration


def thermal_limit_c_per_w(dissipation_w=3, ambient_c=45, limit_c=65):
    """Whole-path effective thermal-resistance screen, excluding solar load."""
    p = finite_number(dissipation_w, "dissipation_w")
    ambient = finite_number(ambient_c, "ambient_c")
    limit = finite_number(limit_c, "limit_c")
    if p <= 0 or limit <= ambient:
        raise ValueError("positive dissipation and temperature rise required")
    return (limit - ambient) / p


def cantilever_screen(force_n=10, length_mm=20, width_mm=20,
                      thickness_mm=3, modulus_n_mm2=69000):
    """Rectangular end-load small-deflection screen, not FEA."""
    f, length, width, thick, modulus = [finite_number(v, n) for v, n in zip(
        (force_n, length_mm, width_mm, thickness_mm, modulus_n_mm2),
        ("force", "length", "width", "thickness", "modulus")
    )]
    if f < 0 or min(length, width, thick, modulus) <= 0:
        raise ValueError("invalid cantilever geometry/load")
    return {"stress_mpa": 6 * f * length / (width * thick ** 2),
            "deflection_mm": 4 * f * length ** 3 / (modulus * width * thick ** 3)}


def confusion_metrics(tp, fp, fn, tn):
    """Illustrative count arithmetic; undefined rates return None."""
    counts = (tp, fp, fn, tn)
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in counts):
        raise ValueError("counts must be nonnegative integers")
    divide = lambda n, d: n / d if d else None
    return {"precision": divide(tp, tp + fp), "recall": divide(tp, tp + fn),
            "specificity": divide(tn, tn + fp),
            "accuracy": divide(tp + tn, sum(counts)),
            "f1": divide(2 * tp, 2 * tp + fp + fn)}


def waiting_time_reduction(round_interval_s=14400, alert_s=210):
    """Uniform-between-rounds model; not measured yield recovery."""
    rounds = finite_number(round_interval_s, "round_interval_s")
    alert = finite_number(alert_s, "alert_s")
    if rounds <= 0 or alert < 0:
        raise ValueError("invalid waiting-time assumptions")
    mean_wait = rounds / 2
    return (mean_wait - alert) / mean_wait
