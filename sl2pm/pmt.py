import numpy as np
from mpmath import fp
from scipy.special import gamma
from models import gaussian


def gain(alpha):
    """ PMT gain
    """
    return 3/alpha


def pmt_output(expect_val, alpha):
    """ PMT output given expected count 'expect_val'
    """
    gain = 3/alpha
    return gain*expect_val


def pmt_output_var(e, alpha, sigma):
    """ Variance of PMT output given expected count 'e'
    """
    return 4*e/alpha + sigma**2


@np.vectorize
def f(s, e, a):
    b1, b2, b3 = 4/3, 5/3, 2
    
    z = e*a**3*s**3/27
    
    if z < 1e9:
        return 0.5*e*a**3*s**2*np.exp(-e - a*s)*fp.hyper([], [(4, 3), (5, 3), (2, 1)], z)
    else:
        return e*a**3*s**2*np.exp(-e - a*s + 4*z**0.25)*gamma(b1)*gamma(b2)*gamma(b3)*z**(0.25*(1.5 - b1 - b2 - b3))/8/np.sqrt(2)/np.pi**1.5


def q(s, e, a, mu, sigma, delta_s=1, s_max=1024):
    """ Probability density of PMT output 's', given the expected photon count 'e'.  Used for tracking QDs and RBCs.
    """
    dummy_s = np.arange(0, s_max, delta_s)[:, np.newaxis]
    
    ds = s - mu
    
    e, a, sigma = np.abs(e), np.abs(a), np.abs(sigma)
    
    return np.exp(-e)*gaussian(ds, sigma) + np.trapz(gaussian(ds - dummy_s, sigma)*f(dummy_s, e, a), x=dummy_s[:, 0], axis=0)


def nll_q_mean(s, e, a, sigma, n_aver, mu=0):
    """
    Negative log-likelihood of probability density of an average of 'n' PMT outputs with expected photon count 'e'
    based on the Central Limit Theorem. Used for tracking capillaries.
    """
    var = pmt_output_var(e, a, sigma)
    
    return 0.5*np.nansum(np.log(2*np.pi*var/n_aver) + n_aver*(s - pmt_output(e, a))**2/var)

