import numpy as np
from . import pmt
from scipy.special import erf
from scipy.optimize import minimize, curve_fit
from scipy.ndimage import gaussian_filter1d
from .models import rbc, rbc_inv


def ols_fit(linescan, plasma_before_rbc=True, sigma_blur=1.5):
    """ RBCs localization by fitting with ordinary least-squares optimization
    """
    x = np.arange(len(linescan))
    fit_func = rbc if plasma_before_rbc else rbc_inv
    linescan_blur = gaussian_filter1d(linescan, sigma_blur)
    
    p, pcov = curve_fit(fit_func, x, linescan_blur, [linescan_blur.min(), linescan_blur.max(), 1.0, 0.5*x[-1]])

    return p


def p0_ols(linescan, alpha, plasma_before_rbc=True, sigma_blur=1.5):
    """ Intitial guess for parameters using ordinary least squares fit 
    """

    b, A, s, xo = ols_fit(linescan, plasma_before_rbc=plasma_before_rbc, sigma_blur=sigma_blur)

    return [b/pmt.gain(alpha), A/pmt.gain(alpha), s, xo]


def neg_loglike(p, linescan, alpha, sigma, mu, plasma_before_rbc=True, delta_s=4, s_max=1000):
    """ Negative log-likelihood for localizing RBCs
    """
    fit_func = rbc if plasma_before_rbc else rbc_inv
    
    return np.sum(-np.log(pmt.q(linescan, 
                                fit_func(np.arange(len(linescan)), *p), 
                                alpha, 
                                mu, 
                                sigma, 
                                delta_s=delta_s, 
                                s_max=s_max)
                         ))


def mle_fit(linescan, alpha, sigma, mu, p0='ols', plasma_before_rbc=True, sigma_blur=1, delta_s=3, s_max=800, minimize_options=None):
    """ Fit line-scan with MLE
    """
    return minimize(neg_loglike, 
                       p0_ols(linescan, alpha, sigma_blur=sigma_blur) if p0 == 'ols' else p0,
                       args=(linescan, alpha, sigma, mu, plasma_before_rbc, delta_s, s_max), 
                       method='bfgs', 
                       options=minimize_options)
    

def rbc_speed(t, x, x_err):
    """ Estimate a RBC's speed (mm/sec) from a series of its locations, xo, and their uncertainties, x_err.
    """
    (speed, intercept), cov = np.polyfit(t, x, w=1/x_err, deg=1, cov='unscaled')
    to = np.mean(t)
    
    return dict(speed=speed,
                 speed_err=np.sqrt(cov[0, 0]), 
                 intercept=intercept, 
                 intercept_err=np.sqrt(cov[1, 1]),
                 x_mean=intercept + speed*to, 
                 x_mean_err=np.sqrt(cov[1, 1] + 2*to*cov[0, 1] + cov[0, 0]*to**2))


