"""Unit tests for estimation utilities"""
import pytest
from app.utils.estimation_utils import COCOMOEstimator, FunctionPointAnalyzer, EstimationAnalyzer
import math


class TestCOCOMOEstimator:
    """COCOMO model tests"""
    
    def test_calculate_effort_basic(self):
        """Test basic effort calculation"""
        effort = COCOMOEstimator.calculate_effort(
            ksloc=5,
            complexity_level="intermediate"
        )
        
        assert effort > 0
        assert isinstance(effort, float)
    
    def test_calculate_effort_with_multipliers(self):
        """Test effort calculation with multipliers"""
        effort_without = COCOMOEstimator.calculate_effort(ksloc=5)
        effort_with = COCOMOEstimator.calculate_effort(
            ksloc=5,
            multipliers={"reliability": 1.40}
        )
        
        assert effort_with > effort_without
    
    def test_calculate_duration(self):
        """Test duration calculation"""
        effort = 20  # person-months
        duration = COCOMOEstimator.calculate_duration(effort)
        
        assert duration > 0
        assert duration < effort  # Duration should be less than effort
    
    def test_calculate_cost(self):
        """Test cost calculation"""
        effort = 20
        hourly_rate = 100
        cost = COCOMOEstimator.calculate_cost(effort, hourly_rate)
        
        expected_cost = 20 * 160 * 100  # 320,000
        assert cost == expected_cost


class TestFunctionPointAnalyzer:
    """Function point analysis tests"""
    
    def test_calculate_unadjusted_fp(self):
        """Test unadjusted function point calculation"""
        result = FunctionPointAnalyzer.calculate_unadjusted_fp(
            ilf=3, ilf_complexity="average",
            eif=2, eif_complexity="average",
            ei=4, ei_complexity="average",
            eo=3, eo_complexity="average",
            eq=2, eq_complexity="average"
        )
        
        assert "total_unadjusted_fp" in result
        assert result["total_unadjusted_fp"] > 0
    
    def test_calculate_adjusted_fp(self):
        """Test adjusted function point calculation"""
        unadjusted_fp = 100
        vaf = 1.0  # Value Adjustment Factor
        adjusted = FunctionPointAnalyzer.calculate_adjusted_fp(unadjusted_fp, vaf)
        
        assert adjusted == unadjusted_fp
    
    def test_fp_to_effort_conversion(self):
        """Test FP to effort conversion"""
        adjusted_fp = 100
        effort = FunctionPointAnalyzer.fp_to_effort(adjusted_fp)
        
        assert effort > 0
        assert isinstance(effort, float)


class TestEstimationAnalyzer:
    """Estimation analyzer tests"""
    
    def test_calculate_confidence_interval(self):
        """Test confidence interval calculation"""
        estimate = 100
        low, high = EstimationAnalyzer.calculate_confidence_interval(
            estimate,
            confidence_level=80,
            margin_of_error=0.15
        )
        
        assert low < estimate < high
        assert high - low > 0
    
    def test_calculate_risk_contingency(self):
        """Test risk contingency calculation"""
        effort = 100
        risks = [
            {"probability": 0.5, "impact": 0.3, "effort_impact": 10},
            {"probability": 0.3, "impact": 0.5, "effort_impact": 20}
        ]
        
        contingency = EstimationAnalyzer.calculate_risk_contingency(effort, risks)
        assert contingency >= 0
    
    def test_calculate_accuracy_metrics(self):
        """Test accuracy metrics calculation"""
        estimates = [100, 150, 200, 120]
        actuals = [95, 160, 210, 130]
        
        metrics = EstimationAnalyzer.calculate_accuracy_metrics(estimates, actuals)
        
        assert "mape" in metrics
        assert "rmse" in metrics
        assert "mae" in metrics
        assert "accuracy" in metrics
