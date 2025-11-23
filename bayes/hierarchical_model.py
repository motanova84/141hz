import numpy as np
from scipy.special import logsumexp


def loglik_event(snr, pi, mu=6.0, sigma=1.0):
    """
    Log-likelihood for a single event under H0 (noise) and H1 (signal).

    Parameters
    ----------
    snr : float
        Signal-to-noise ratio for the event
    pi : float
        Prior probability of signal presence (0 to 1)
    mu : float, optional
        Expected SNR under signal hypothesis (default: 6.0)
    sigma : float, optional
        Standard deviation of SNR under signal hypothesis (default: 1.0)

    Returns
    -------
    ll0 : float
        Log-likelihood under H0 (noise only)
    ll1 : float
        Log-likelihood under H1 (signal present)
    """
    ll0 = -0.5*snr**2
    ll1 = -0.5*((snr-mu)/sigma)**2 - np.log(sigma*np.sqrt(2*np.pi))
    return np.log1p(-pi) + ll0, np.log(pi) + ll1


def logpost(snr_list, pi, mu=6.0, sigma=1.0):
    """
    Log-posterior for hierarchical model given SNR observations.

    Parameters
    ----------
    snr_list : list of float
        SNR values for multiple events
    pi : float
        Global prior probability parameter
    mu : float, optional
        Expected SNR under signal hypothesis (default: 6.0)
    sigma : float, optional
        Standard deviation of SNR under signal hypothesis (default: 1.0)

    Returns
    -------
    float
        Log-posterior value (assumes flat prior on pi)
    """
    acc = 0.0
    for x in snr_list:
        a0, a1 = loglik_event(x, pi, mu, sigma)
        acc += logsumexp([a0, a1])
    return acc  # flat prior on pi


def bayes_factor(snr_list, mu=6.0, sigma=1.0, grid_size=1001):
    """
    Compute hierarchical Bayes factor for multiple events.

    Parameters
    ----------
    snr_list : list of float
        SNR values for multiple events
    mu : float, optional
        Expected SNR under signal hypothesis (default: 6.0)
    sigma : float, optional
        Standard deviation of SNR under signal hypothesis (default: 1.0)
    grid_size : int, optional
        Number of grid points for numerical integration (default: 1001)

    Returns
    -------
    float
        Bayes factor comparing hierarchical signal model to noise-only model
    """
    grid = np.linspace(0, 1, grid_size)
    lps = np.array([logpost(snr_list, p, mu, sigma) for p in grid])
    logZ = logsumexp(lps) - np.log(grid_size)
    logZ0 = np.sum(-0.5*np.array(snr_list)**2 - 0.5*np.log(2*np.pi))
    return float(np.exp(logZ - logZ0))
