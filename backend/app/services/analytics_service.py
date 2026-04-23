"""
Analytics Service — Computes derived insights from stored stock data.
"""

import numpy as np


def compute_correlation(returns_1: list[float], returns_2: list[float]) -> float | None:
    """
    Compute Pearson correlation between two series of daily returns.

    Args:
        returns_1: List of daily returns for stock 1
        returns_2: List of daily returns for stock 2

    Returns:
        Pearson correlation coefficient, or None if not computable
    """
    if len(returns_1) < 2 or len(returns_2) < 2:
        return None

    # Align lengths (take the shorter one)
    min_len = min(len(returns_1), len(returns_2))
    r1 = np.array(returns_1[-min_len:])
    r2 = np.array(returns_2[-min_len:])

    # Check for constant series
    if np.std(r1) == 0 or np.std(r2) == 0:
        return None

    corr_matrix = np.corrcoef(r1, r2)
    correlation = float(corr_matrix[0, 1])

    return round(correlation, 4) if not np.isnan(correlation) else None
