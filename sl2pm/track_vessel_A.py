## Tracking blood vessels with wall and plasma fluorescence (Protocol A)
## 
import numpy as np
import pmt
from scipy.optimize import minimize, curve_fit
from scipy.ndimage import gaussian_filter1d
from models import L_wall_plasma, L_multi


def ols_fit(profile_wall, profile_plasma, sigma_blur=1.5):
    """ Fitting with ordinary least-squares optimization
    """
    x = np.arange(len(profile_wall))
    
    wall = gaussian_filter1d(profile_wall, sigma_blur)
    plasma = gaussian_filter1d(profile_plasma, sigma_blur)
    
    x_max1, x_max2 = wall[:len(wall)//2].argmax(), len(wall)//2 + wall[len(wall)//2:].argmax()
    
    xc = 0.5*(x_max1 + x_max2)
    R = 0.5*(x_max2 - x_max1)
    
    p0 = [xc, 2, 6, R, R, 1, 0, wall.max(), plasma.max(), wall.min(), wall.min(), plasma.min()]
    
    p, pcov = curve_fit(lambda *args: L_wall_plasma(*args).ravel(), x, np.hstack([wall, plasma]), p0)

    return p


def p0_ols(profile_wall, profile_plasma, alpha, sigma_blur=1.5):
    """ Intitial guess for parameters using ordinary least squares fit 
    """
    xc, s_xy, l, R_l, R_w, s_gcx, a1, Iw, Ip, b_p, b_tw, b_tp = ols_fit(profile_wall, profile_plasma, sigma_blur=sigma_blur)

    return [xc, s_xy, l, R_l, R_w, s_gcx, a1, Iw/pmt.gain(alpha), Ip/pmt.gain(alpha), b_p/pmt.gain(alpha), b_tw/pmt.gain(alpha), b_tp/pmt.gain(alpha)]


def p0_ols_ultimate(kymo_wall, kymo_plasma, alpha, sigma_blur=1.5):
    """ Intitial parameters guess for the ultimate fit using ordinary least squares fit 
    """
    nt, nx = kymo_wall.shape
    
    xc, s_xy, l, R_l, R_w, s_gcx, a1, Iw, Ip, b_p, b_tw, b_tp = p0_ols(kymo_wall[0], kymo_plasma[0], alpha, sigma_blur=sigma_blur)
    
    return np.r_[s_xy, l, R_w - R_l, s_gcx, b_p, b_tw, b_tp, nt*[Iw], nt*[Ip], nt*[R_w], nt*[xc], nt*[a1]]


def mle_fit(profile_wall, profile_plasma, n_aver, alpha, sigma, n_r=256, n_phi=256, p0='ols', sigma_blur=1.5, minimize_options=None):
    """ Fit line-profiles with MLE
    """
    def neg_log_like(p):
        return pmt.nll_q_mean(np.array([profile_wall, profile_plasma]), 
                          L_wall_plasma(np.arange(len(profile_wall)), *p, n_r=n_r, n_phi=n_phi), 
                          alpha, 
                          sigma, 
                          n_aver)
    
    return minimize(neg_log_like, 
                    p0_ols(profile_wall, profile_plasma, alpha, sigma_blur=sigma_blur) if p0 == 'ols' else p0,
                    method='bfgs', 
                    options=minimize_options)


def mle_fit_ultimate(kymo_wall, kymo_plasma, n_aver, alpha, sigma, n_r=256, n_phi=256, p0='ols', sigma_blur=1.5, minimize_options=None):
    """ Fit line-profiles with the ultimate MLE fit: Fitting several profiles at once
    """
    def neg_log_like(p):
        return pmt.nll_q_mean(np.array([[w, p] for w, p in zip(kymo_wall, kymo_plasma)]), 
                              L_multi(np.arange(kymo_wall.shape[1]), *p, n_r=n_r, n_phi=n_phi), 
                              alpha, 
                              sigma, 
                              n_aver)
    
    return minimize(neg_log_like, 
                    p0_ols_ultimate(kymo_wall, kymo_plasma, alpha, sigma_blur=sigma_blur) if p0 == 'ols' else p0,
                    method='bfgs', 
                    options=minimize_options)
    
    
