"""Utility functions for calculations and estimations"""
import math
from typing import Dict, List, Optional


class COCOMOEstimator:
    """COCOMO model for software effort estimation"""
    
    # COCOMO coefficients
    BASIC_COEFF = {"a": 2.4, "b": 1.05}
    INTERMEDIATE_COEFF = {"a": 3.0, "b": 1.12}
    DETAILED_COEFF = {"a": 3.6, "b": 1.20}
    
    # Effort multipliers by category
    EFFORT_MULTIPLIERS = {
        "reliability": {"low": 0.75, "nominal": 1.0, "high": 1.40},
        "database_size": {"low": 0.90, "nominal": 1.0, "high": 1.40},
        "complexity": {"low": 0.70, "nominal": 1.0, "high": 1.65},
        "time_constraint": {"loose": 1.0, "moderate": 1.11, "tight": 1.30},
        "personnel": {"junior": 1.46, "nominal": 1.0, "senior": 0.71},
        "experience": {"low": 1.29, "nominal": 1.0, "high": 0.81},
    }
    
    @staticmethod
    def calculate_effort(
        ksloc: float,  # Thousand Source Lines of Code
        complexity_level: str = "intermediate",
        multipliers: Optional[Dict[str, float]] = None
    ) -> float:
        """
        Calculate effort in person-months using COCOMO
        
        Args:
            ksloc: Size in thousands of lines of code
            complexity_level: 'basic', 'intermediate', or 'detailed'
            multipliers: Dictionary of adjustment multipliers
            
        Returns:
            Estimated effort in person-months
        """
        if complexity_level == "basic":
            coeff = COCOMOEstimator.BASIC_COEFF
        elif complexity_level == "detailed":
            coeff = COCOMOEstimator.DETAILED_COEFF
        else:
            coeff = COCOMOEstimator.INTERMEDIATE_COEFF
        
        # Base effort calculation
        effort = coeff["a"] * math.pow(ksloc, coeff["b"])
        
        # Apply multipliers
        if multipliers:
            for key, value in multipliers.items():
                effort *= value
        
        return effort
    
    @staticmethod
    def calculate_duration(effort: float) -> float:
        """Calculate project duration from effort (person-months)"""
        return 3.0 * math.pow(effort, 0.33)
    
    @staticmethod
    def calculate_cost(effort: float, hourly_rate: float = 100.0) -> float:
        """Calculate project cost from effort"""
        hours_per_month = 160  # Standard working hours
        return effort * hours_per_month * hourly_rate


class FunctionPointAnalyzer:
    """Function Point Analysis calculator"""
    
    # Complexity weights
    WEIGHTS = {
        "simple": {"ilf": 7, "eif": 5, "ei": 3, "eo": 4, "eq": 3},
        "average": {"ilf": 10, "eif": 7, "ei": 4, "eo": 5, "eq": 4},
        "complex": {"ilf": 15, "eif": 10, "ei": 6, "eo": 7, "eq": 6},
    }
    
    @staticmethod
    def calculate_unadjusted_fp(
        ilf: int, ilf_complexity: str,
        eif: int, eif_complexity: str,
        ei: int, ei_complexity: str,
        eo: int, eo_complexity: str,
        eq: int, eq_complexity: str
    ) -> Dict[str, float]:
        """
        Calculate unadjusted function points
        
        Args:
            ilf: Internal Logical Files count
            ilf_complexity: 'simple', 'average', 'complex'
            eif: External Interface Files count
            eif_complexity: Complexity level
            ei: External Inputs count
            ei_complexity: Complexity level
            eo: External Outputs count
            eo_complexity: Complexity level
            eq: External Inquiries count
            eq_complexity: Complexity level
            
        Returns:
            Dictionary with component contributions and total UFP
        """
        ilf_contrib = ilf * FunctionPointAnalyzer.WEIGHTS[ilf_complexity]["ilf"]
        eif_contrib = eif * FunctionPointAnalyzer.WEIGHTS[eif_complexity]["eif"]
        ei_contrib = ei * FunctionPointAnalyzer.WEIGHTS[ei_complexity]["ei"]
        eo_contrib = eo * FunctionPointAnalyzer.WEIGHTS[eo_complexity]["eo"]
        eq_contrib = eq * FunctionPointAnalyzer.WEIGHTS[eq_complexity]["eq"]
        
        total_ufp = ilf_contrib + eif_contrib + ei_contrib + eo_contrib + eq_contrib
        
        return {
            "ilf_contribution": ilf_contrib,
            "eif_contribution": eif_contrib,
            "ei_contribution": ei_contrib,
            "eo_contribution": eo_contrib,
            "eq_contribution": eq_contrib,
            "total_unadjusted_fp": total_ufp
        }
    
    @staticmethod
    def calculate_adjusted_fp(unadjusted_fp: float, vaf: float = 1.0) -> float:
        """
        Calculate adjusted function points
        
        Args:
            unadjusted_fp: Unadjusted function points
            vaf: Value Adjustment Factor (0.65 to 1.35)
            
        Returns:
            Adjusted function points
        """
        return unadjusted_fp * vaf
    
    @staticmethod
    def fp_to_effort(adjusted_fp: float, productivity: float = 0.2) -> float:
        """
        Convert function points to effort
        
        Args:
            adjusted_fp: Adjusted function points
            productivity: FP per hour (typical: 0.2-0.5)
            
        Returns:
            Estimated effort in hours
        """
        return adjusted_fp / productivity


class EstimationAnalyzer:
    """Analysis and validation utilities"""
    
    @staticmethod
    def calculate_confidence_interval(
        estimate: float,
        confidence_level: int = 80,
        margin_of_error: float = 0.15
    ) -> tuple:
        """
        Calculate confidence interval for estimates
        
        Args:
            estimate: Point estimate value
            confidence_level: Confidence percentage (typically 68, 80, 95)
            margin_of_error: Margin of error as decimal
            
        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        z_score = {68: 1.0, 80: 1.28, 95: 1.96}.get(confidence_level, 1.28)
        margin = estimate * margin_of_error * z_score
        
        return (estimate - margin, estimate + margin)
    
    @staticmethod
    def calculate_risk_contingency(
        effort: float,
        risks: List[Dict],  # List of {"probability": 0-1, "impact": 0-1, "effort_impact": hours}
    ) -> float:
        """
        Calculate effort contingency from identified risks
        
        Args:
            effort: Base effort estimate
            risks: List of risk objects
            
        Returns:
            Contingency effort in hours
        """
        contingency = 0
        for risk in risks:
            expected_value = (risk.get("probability", 0) * 
                            risk.get("impact", 0) * 
                            risk.get("effort_impact", 0))
            contingency += expected_value
        
        return contingency
    
    @staticmethod
    def calculate_accuracy_metrics(
        estimates: List[float],
        actuals: List[float]
    ) -> Dict:
        """
        Calculate accuracy metrics for estimate validation
        
        Args:
            estimates: List of estimated values
            actuals: List of actual values
            
        Returns:
            Dictionary with accuracy metrics
        """
        if len(estimates) != len(actuals) or len(estimates) == 0:
            return {}
        
        errors = [abs(e - a) / a for e, a in zip(estimates, actuals) if a != 0]
        
        mape = sum(errors) / len(errors) * 100 if errors else 0
        rmse = math.sqrt(sum((e - a) ** 2 for e, a in zip(estimates, actuals)) / len(estimates))
        mae = sum(abs(e - a) for e, a in zip(estimates, actuals)) / len(estimates)
        
        return {
            "mape": round(mape, 2),
            "rmse": round(rmse, 2),
            "mae": round(mae, 2),
            "accuracy": round(100 - min(mape, 100), 2)
        }
