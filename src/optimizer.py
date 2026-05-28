import numpy as np
import pandas as pd
from scipy.optimize import minimize

class PortfolioOptimizer:
    def __init__(self, risk_aversion: float = 0.5):
        self.risk_aversion = risk_aversion

    def calculate_metrics(self, returns: pd.DataFrame):
        mean_returns = returns.mean() * 250
        covariance_matrix = returns.cov() * 250
        return mean_returns, covariance_matrix

    def optimize(self, returns: pd.DataFrame) -> dict:
        mean_returns, cov_matrix = self.calculate_metrics(returns)
        num_assets = len(mean_returns)
        
        init_weights = np.array([1 / num_assets] * num_assets)
        
        constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
        
        bounds = tuple((0, 1) for _ in range(num_assets))
        
        def objective(weights):
            port_return = np.dot(weights, mean_returns)
            port_volatility = np.dot(weights.T, np.dot(cov_matrix, weights))
            utility = port_return - self.risk_aversion * port_volatility
            return -utility

        result = minimize(objective, init_weights, method='SLSQP', bounds=bounds, constraints=constraints)
        
        if not result.success:
            raise ValueError("Optimization failed: " + result.message)
            
        optimal_weights = result.x
        
        return {
            "weights": dict(zip(mean_returns.index, optimal_weights)),
            "expected_return": np.dot(optimal_weights, mean_returns),
            "expected_variance": np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights))
        }