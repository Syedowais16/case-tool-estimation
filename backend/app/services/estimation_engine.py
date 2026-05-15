"""Production estimation engine for COCOMO, FPA, hybrid, and ML predictions."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, r2_score
from sklearn.model_selection import train_test_split


HOURS_PER_PERSON_MONTH = 152

COCOMO_MODES = {
    "organic": {"a": 2.4, "b": 1.05, "c": 2.5, "d": 0.38},
    "semi_detached": {"a": 3.0, "b": 1.12, "c": 2.5, "d": 0.35},
    "embedded": {"a": 3.6, "b": 1.20, "c": 2.5, "d": 0.32},
}

FPA_WEIGHTS = {
    "simple": {"ilf": 7, "eif": 5, "ei": 3, "eo": 4, "eq": 3},
    "average": {"ilf": 10, "eif": 7, "ei": 4, "eo": 5, "eq": 4},
    "complex": {"ilf": 15, "eif": 10, "ei": 6, "eo": 7, "eq": 6},
}

COMPLEXITY_SCORE = {"low": 0.85, "simple": 0.85, "medium": 1.0, "average": 1.0, "high": 1.25, "complex": 1.25, "very_high": 1.45}
RISK_SCORE = {"low": 0.9, "medium": 1.0, "moderate": 1.0, "high": 1.2, "critical": 1.38}
VOLATILITY_SCORE = {"low": 0.9, "medium": 1.0, "moderate": 1.0, "high": 1.18, "critical": 1.32}
EXPERIENCE_SCORE = {"junior": 1.28, "mixed": 1.05, "mid": 1.0, "senior": 0.86}
ARCHITECTURE_SCORE = {"monolith": 0.95, "layered": 1.0, "serverless": 1.08, "microservices": 1.16, "distributed": 1.22, "native": 1.05}


@dataclass
class MLTrainingResult:
    """Container for trained estimators and their cross-validation metrics."""

    models: Dict[str, RandomForestRegressor]
    metrics: Dict[str, Dict[str, float]]
    feature_names: List[str]
    residual_spread: Dict[str, float]
    training_count: int


def _normal(value: Optional[str]) -> str:
    return (value or "").strip().lower().replace(" ", "_").replace("-", "_")


def _score(mapping: Dict[str, float], value: Optional[str], default: float = 1.0) -> float:
    return mapping.get(_normal(value), default)


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        parsed = float(value)
        if math.isnan(parsed) or math.isinf(parsed):
            return default
        return parsed
    except (TypeError, ValueError):
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def calculate_cocomo(
    size_kloc: float,
    mode: str = "semi_detached",
    effort_multiplier: float = 1.0,
    cost_per_person_month: float = 9000.0,
    risk_level: str = "medium",
    complexity: str = "medium",
) -> Dict[str, Any]:
    """Calculate COCOMO effort, duration, cost, and confidence band."""
    if size_kloc <= 0:
        raise ValueError("size_kloc must be greater than zero")

    coefficients = COCOMO_MODES.get(_normal(mode), COCOMO_MODES["semi_detached"])
    adjustment = max(0.2, effort_multiplier) * _score(RISK_SCORE, risk_level) * _score(COMPLEXITY_SCORE, complexity)
    person_months = coefficients["a"] * math.pow(size_kloc, coefficients["b"]) * adjustment
    duration_months = coefficients["c"] * math.pow(person_months, coefficients["d"])
    effort_hours = person_months * HOURS_PER_PERSON_MONTH
    team_size = max(1, round(person_months / max(duration_months, 1)))
    cost = person_months * cost_per_person_month
    margin = 0.12 + max(0, adjustment - 1) * 0.08

    return {
        "method": "COCOMO",
        "size_kloc": round(size_kloc, 2),
        "mode": _normal(mode) or "semi_detached",
        "person_months": round(person_months, 2),
        "estimated_effort_hours": round(effort_hours, 2),
        "estimated_duration_months": round(duration_months, 2),
        "estimated_cost": round(cost, 2),
        "estimated_team_size": team_size,
        "confidence_level": max(55, min(90, round(86 - margin * 100))),
        "confidence_interval_low": round(effort_hours * (1 - margin), 2),
        "confidence_interval_high": round(effort_hours * (1 + margin), 2),
        "formula": "Effort(PM) = a x KLOC^b x effort multipliers; Duration = c x Effort^d",
        "business_interpretation": "COCOMO is best when the team can approximate source size or module count early in planning.",
    }


def calculate_fpa(
    ilf_count: int = 0,
    ilf_complexity: str = "average",
    eif_count: int = 0,
    eif_complexity: str = "average",
    ei_count: int = 0,
    ei_complexity: str = "average",
    eo_count: int = 0,
    eo_complexity: str = "average",
    eq_count: int = 0,
    eq_complexity: str = "average",
    value_adjustment_factor: Optional[float] = None,
    general_system_characteristics: Optional[Iterable[int]] = None,
    productivity_fp_per_person_month: float = 18.0,
    cost_per_person_month: float = 9000.0,
    risk_level: str = "medium",
) -> Dict[str, Any]:
    """Calculate Function Point Analysis values and downstream effort/cost."""
    components = {
        "ilf": (_safe_int(ilf_count), _normal(ilf_complexity) or "average"),
        "eif": (_safe_int(eif_count), _normal(eif_complexity) or "average"),
        "ei": (_safe_int(ei_count), _normal(ei_complexity) or "average"),
        "eo": (_safe_int(eo_count), _normal(eo_complexity) or "average"),
        "eq": (_safe_int(eq_count), _normal(eq_complexity) or "average"),
    }
    contributions: Dict[str, float] = {}
    for key, (count, complexity) in components.items():
        if complexity not in FPA_WEIGHTS:
            complexity = "average"
        contributions[f"{key}_contribution"] = count * FPA_WEIGHTS[complexity][key]

    unadjusted_fp = sum(contributions.values())
    if unadjusted_fp <= 0:
        raise ValueError("At least one function point component count must be greater than zero")

    if value_adjustment_factor is None:
        total_degree_influence = sum(max(0, min(5, _safe_int(score))) for score in (general_system_characteristics or []))
        value_adjustment_factor = 0.65 + 0.01 * total_degree_influence if total_degree_influence else 1.0

    vaf = max(0.65, min(1.35, _safe_float(value_adjustment_factor, 1.0)))
    adjusted_fp = unadjusted_fp * vaf
    productivity = max(4.0, productivity_fp_per_person_month)
    person_months = (adjusted_fp / productivity) * _score(RISK_SCORE, risk_level)
    effort_hours = person_months * HOURS_PER_PERSON_MONTH
    duration_months = 2.5 * math.pow(max(person_months, 1), 0.36)
    team_size = max(1, round(person_months / max(duration_months, 1)))
    cost = person_months * cost_per_person_month
    margin = 0.14 + (1.0 - min(1.0, productivity / 25.0)) * 0.08

    return {
        "method": "FPA",
        **contributions,
        "unadjusted_fp": round(unadjusted_fp, 2),
        "vaf": round(vaf, 3),
        "adjusted_fp": round(adjusted_fp, 2),
        "person_months": round(person_months, 2),
        "estimated_effort_hours": round(effort_hours, 2),
        "estimated_duration_months": round(duration_months, 2),
        "estimated_cost": round(cost, 2),
        "estimated_team_size": team_size,
        "confidence_level": max(58, min(88, round(84 - margin * 100))),
        "confidence_interval_low": round(effort_hours * (1 - margin), 2),
        "confidence_interval_high": round(effort_hours * (1 + margin), 2),
        "formula": "Adjusted FP = Unadjusted FP x VAF; Effort(PM) = Adjusted FP / productivity",
        "business_interpretation": "FPA estimates user-visible functionality, so it works well before detailed code size is known.",
    }


def calculate_hybrid(
    cocomo_result: Dict[str, Any],
    fpa_result: Dict[str, Any],
    ml_result: Optional[Dict[str, Any]] = None,
    cocomo_weight: float = 0.35,
    fpa_weight: float = 0.40,
    ml_weight: float = 0.25,
    risk_level: str = "medium",
    requirement_volatility: str = "medium",
) -> Dict[str, Any]:
    """Blend COCOMO, FPA, and optional ML into a risk-adjusted hybrid forecast."""
    if not ml_result:
        cocomo_weight = 0.45
        fpa_weight = 0.55
        ml_weight = 0.0

    total_weight = max(cocomo_weight + fpa_weight + ml_weight, 0.01)
    weights = {
        "cocomo": cocomo_weight / total_weight,
        "fpa": fpa_weight / total_weight,
        "ml": ml_weight / total_weight,
    }

    risk_adjustment = (_score(RISK_SCORE, risk_level) + _score(VOLATILITY_SCORE, requirement_volatility)) / 2

    def blend(field: str) -> float:
        value = cocomo_result[field] * weights["cocomo"] + fpa_result[field] * weights["fpa"]
        if ml_result:
            value += ml_result[field] * weights["ml"]
        return value * risk_adjustment

    effort = blend("estimated_effort_hours")
    duration = blend("estimated_duration_months")
    cost = blend("estimated_cost")
    team_size = max(1, round((cocomo_result.get("estimated_team_size", 1) * weights["cocomo"]) + (fpa_result.get("estimated_team_size", 1) * weights["fpa"]) + ((ml_result or {}).get("estimated_team_size", 1) * weights["ml"])))
    component_confidence = [
        cocomo_result.get("confidence_level", 70),
        fpa_result.get("confidence_level", 70),
        (ml_result or {}).get("confidence_level", 70),
    ]
    confidence = round(sum(component_confidence[: 2 if not ml_result else 3]) / (2 if not ml_result else 3) - max(0, risk_adjustment - 1) * 8)
    margin = max(0.12, 1 - confidence / 100)

    return {
        "method": "Hybrid",
        "weights": {key: round(value, 2) for key, value in weights.items()},
        "risk_adjustment": round(risk_adjustment, 3),
        "estimated_effort_hours": round(effort, 2),
        "estimated_duration_months": round(duration, 2),
        "estimated_cost": round(cost, 2),
        "estimated_team_size": team_size,
        "confidence_level": max(50, min(92, confidence)),
        "confidence_interval_low": round(effort * (1 - margin), 2),
        "confidence_interval_high": round(effort * (1 + margin), 2),
        "formula": "Hybrid = weighted(COCOMO, FPA, ML) x risk/volatility adjustment",
        "business_interpretation": "Hybrid estimation reduces single-model bias by combining size, functionality, and organizational history.",
    }


def _historical_adjusted_fp(project: Any) -> float:
    adjusted = _safe_float(getattr(project, "fpa_adjusted", None))
    if adjusted > 0:
        return adjusted
    productivity = _safe_float(getattr(project, "productivity", None), 1.0)
    return max(20.0, _safe_float(getattr(project, "actual_effort_hours", 0)) * max(productivity, 0.2) / 12)


def _project_features(project: Any) -> List[float]:
    return [
        _historical_adjusted_fp(project),
        _safe_float(getattr(project, "team_size", 0), 1),
        _score(COMPLEXITY_SCORE, getattr(project, "complexity", None)),
        _score(RISK_SCORE, getattr(project, "risk_level", None)),
        _score(VOLATILITY_SCORE, getattr(project, "requirement_volatility", None)),
        _score(EXPERIENCE_SCORE, getattr(project, "team_experience", None)),
        _score(ARCHITECTURE_SCORE, getattr(project, "architecture", None)),
        max(_safe_float(getattr(project, "productivity", None), 1.0), 0.1),
        max(_safe_float(getattr(project, "defect_density", None), 2.0), 0.1),
    ]


def _payload_features(payload: Dict[str, Any]) -> List[float]:
    adjusted_fp = _safe_float(payload.get("adjusted_fp") or payload.get("fpa_adjusted"))
    if adjusted_fp <= 0:
        adjusted_fp = _safe_float(payload.get("function_points"), 120)
    return [
        adjusted_fp,
        max(_safe_float(payload.get("team_size"), 4), 1),
        _score(COMPLEXITY_SCORE, payload.get("complexity")),
        _score(RISK_SCORE, payload.get("risk_level")),
        _score(VOLATILITY_SCORE, payload.get("requirement_volatility")),
        _score(EXPERIENCE_SCORE, payload.get("team_experience")),
        _score(ARCHITECTURE_SCORE, payload.get("architecture")),
        max(_safe_float(payload.get("productivity"), 1.0), 0.1),
        max(_safe_float(payload.get("defect_density"), 2.0), 0.1),
    ]


def train_ml_models(historical_projects: Iterable[Any]) -> Optional[MLTrainingResult]:
    """Train in-memory regression models from historical project records."""
    rows = [project for project in historical_projects if _safe_float(getattr(project, "actual_effort_hours", None)) > 0]
    if len(rows) < 10:
        return None

    x = np.array([_project_features(project) for project in rows], dtype=float)
    targets = {
        "estimated_effort_hours": np.array([_safe_float(getattr(project, "actual_effort_hours", 0)) for project in rows], dtype=float),
        "estimated_duration_months": np.array([_safe_float(getattr(project, "actual_duration_months", 0)) for project in rows], dtype=float),
        "estimated_cost": np.array([_safe_float(getattr(project, "actual_cost", 0)) for project in rows], dtype=float),
    }

    models: Dict[str, RandomForestRegressor] = {}
    metrics: Dict[str, Dict[str, float]] = {}
    residual_spread: Dict[str, float] = {}

    test_size = 0.25 if len(rows) >= 16 else 0.2
    for field, y in targets.items():
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=42)
        model = RandomForestRegressor(n_estimators=120, random_state=42, min_samples_leaf=2)
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        mape = mean_absolute_percentage_error(y_test, predictions) * 100
        mae = mean_absolute_error(y_test, predictions)
        r_squared = r2_score(y_test, predictions) if len(y_test) > 1 else 0.0
        residual_pct = np.abs(predictions - y_test) / np.maximum(y_test, 1)
        residual_spread[field] = float(np.percentile(residual_pct, 80)) if len(residual_pct) else 0.18
        metrics[field] = {
            "mape": round(float(mape), 2),
            "mae": round(float(mae), 2),
            "r_squared": round(float(r_squared), 3),
            "accuracy": round(max(0.0, 100.0 - min(float(mape), 100.0)), 2),
        }
        models[field] = model

    return MLTrainingResult(
        models=models,
        metrics=metrics,
        feature_names=[
            "adjusted_fp",
            "team_size",
            "complexity_score",
            "risk_score",
            "volatility_score",
            "experience_score",
            "architecture_score",
            "productivity",
            "defect_density",
        ],
        residual_spread=residual_spread,
        training_count=len(rows),
    )


def predict_with_ml(payload: Dict[str, Any], historical_projects: Iterable[Any]) -> Dict[str, Any]:
    """Train on historical rows and predict effort, duration, and cost for a new project."""
    training = train_ml_models(historical_projects)
    if training is None:
        raise ValueError("At least 10 historical projects are required for ML prediction")

    features = np.array([_payload_features(payload)], dtype=float)
    predictions = {
        field: round(float(model.predict(features)[0]), 2)
        for field, model in training.models.items()
    }
    predicted_duration = max(predictions["estimated_duration_months"], 1)
    team_size = max(1, round(predictions["estimated_effort_hours"] / HOURS_PER_PERSON_MONTH / predicted_duration))
    accuracy_values = [metric["accuracy"] for metric in training.metrics.values()]
    confidence = round(max(50, min(92, sum(accuracy_values) / len(accuracy_values))))
    effort_margin = max(0.12, training.residual_spread.get("estimated_effort_hours", 0.18))
    feature_importance = training.models["estimated_effort_hours"].feature_importances_

    return {
        "method": "ML",
        **predictions,
        "estimated_team_size": team_size,
        "confidence_level": confidence,
        "confidence_interval_low": round(predictions["estimated_effort_hours"] * (1 - effort_margin), 2),
        "confidence_interval_high": round(predictions["estimated_effort_hours"] * (1 + effort_margin), 2),
        "training_data_count": training.training_count,
        "feature_names": training.feature_names,
        "metrics": training.metrics,
        "feature_importance": [
            {"feature": name, "importance": round(float(score), 4)}
            for name, score in sorted(zip(training.feature_names, feature_importance), key=lambda item: item[1], reverse=True)
        ],
        "business_interpretation": "ML compares the new project with historical delivery patterns to learn local productivity, cost, and schedule behavior.",
    }


def build_ml_insights(historical_projects: Iterable[Any]) -> Dict[str, Any]:
    """Return chart-ready model insight data from the current historical dataset."""
    rows = list(historical_projects)
    training = train_ml_models(rows)
    if training is None:
        return {
            "available": False,
            "message": "At least 10 historical projects are required for ML insights.",
            "training_data_count": len(rows),
        }

    effort_model = training.models["estimated_effort_hours"]
    return {
        "available": True,
        "training_data_count": training.training_count,
        "feature_names": training.feature_names,
        "metrics": training.metrics,
        "feature_importance": [
            {"feature": name, "importance": round(float(score), 4)}
            for name, score in sorted(zip(training.feature_names, effort_model.feature_importances_), key=lambda item: item[1], reverse=True)
        ],
    }
