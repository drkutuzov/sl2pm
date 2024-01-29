## Tracking blood vessels with plasma fluorescence (Protocol B)
## 
import numpy as np
import pmt
from scipy.optimize import minimize, curve_fit
from scipy.ndimage import gaussian_filter1d
from models import L_plasma_no_glx, L_multi_plasma


def ols_fit(profile_plasma, sigma_blur=1.5, thr=0.1):
    """ Fitting with ordinary least-squares optimization
    """
    x = np.arange(len(profile_plasma))
    
    plasma = gaussian_filter1d(profile_plasma, sigma_blur)
    plasma_norm = (plasma - plasma.min())/(plasma.max() - plasma.min())
    
    xc = plasma.argmax()
    R = xc - (np.abs(plasma_norm - thr)[:xc]).argmin()
    
    p0 = [xc, 2, 6, R, plasma.max(), plasma.min()]

    p, pcov = curve_fit(lambda *args: L_plasma_no_glx(*args), x, plasma, p0)

    return p


def p0_ols(profile_plasma, alpha, sigma_blur=1.5):
    """ Intitial guess for parameters using ordinary least squares fit 
    """
    xc, s_xy, l, R_l, I, b = ols_fit(profile_plasma, sigma_blur=sigma_blur)

    return [xc, s_xy, l, R_l, I/pmt.gain(alpha), b/pmt.gain(alpha)]


def p0_ols_ultimate(kymo_plasma, alpha, sigma_blur=1.5):
    """ Intitial parameters guess for the ultimate fit using ordinary least squares fit 
    """
    nt, nx = kymo_plasma.shape
    
    xc, s_xy, l, R, I, b = p0_ols(kymo_plasma[0], alpha, sigma_blur=sigma_blur)
    
    return np.r_[s_xy, l, b, nt*[I], nt*[R], nt*[xc]]


def mle_fit(profile_plasma, n_aver, alpha, sigma, n_r=256, p0='ols', sigma_blur=1.5, minimize_options=None):
    """ Fit line-profiles with MLE
    """
    def neg_log_like(p):
        return pmt.nll_q_mean(profile_plasma, 
                          L_plasma_no_glx(np.arange(len(profile_plasma)), *p, n_r=n_r), 
                          alpha, 
                          sigma, 
                          n_aver)
    
    return minimize(neg_log_like, 
                    p0_ols(profile_plasma, alpha, sigma_blur=sigma_blur) if p0 == 'ols' else p0,
                    method='bfgs', 
                    options=minimize_options)


def mle_fit_ultimate(kymo_plasma, n_aver, alpha, sigma, n_r=256, p0='ols', sigma_blur=1.5, minimize_options=None):
    """ Fit line-profiles with the ultimate MLE fit: Fitting several profiles at once
    """
    def neg_log_like(p):
        return pmt.nll_q_mean(kymo_plasma, 
                              L_multi_plasma(np.arange(kymo_plasma.shape[1]), *p, n_r=n_r), 
                              alpha, 
                              sigma, 
                              n_aver)
    
    return minimize(neg_log_like, 
                    p0_ols_ultimate(kymo_plasma, alpha, sigma_blur=sigma_blur) if p0 == 'ols' else p0,
                    method='bfgs', 
                    options=minimize_options)

