"""
Bayesian hierarchical analysis for multi-event gravitational wave detection.

This module provides tools for computing hierarchical Bayes factors
to assess the significance of signals across multiple events while
properly accounting for the multiple comparisons problem.
"""

from .hierarchical_model import loglik_event, logpost, bayes_factor

__all__ = ['loglik_event', 'logpost', 'bayes_factor']
