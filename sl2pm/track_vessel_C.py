## Tracking blood vessels with wall fluorescence (Protocol C)
## 
import numpy as np
import pmt
from scipy.optimize import minimize, curve_fit
from scipy.ndimage import gaussian_filter1d
from models import L_wall, L_multi_wall


def ols_fit(profile_wall, sigma_blur=1.5):
    """ Fitting with ordinary least-squares optimization
    """
    x = np.arange(len(profile_wall))
    
    wall = gaussian_filter1d(profile_wall, sigma_blur)
    
    x_max1, x_max2 = wall[:len(wall)//2].argmax(), len(wall)//2 + wall[len(wall)//2:].argmax()
    
    xc = 0.5*(x_max1 + x_max2)
    R = 0.5*(x_max2 - x_max1)
    
    p0 = [xc, 2, 6, R, 0, wall.max(), 0, wall.min()]
    
    p, pcov = curve_fit(lambda *args: L_wall(*args), x, wall, p0)

    return p


def p0_ols(profile_wall, alpha, sigma_blur=1.5):
    """ Intitial guess for parameters using ordinary least squares fit 
    """
    xc, s_xy, l, R_w, a1, I, b_p, b_t = ols_fit(profile_wall, sigma_blur=sigma_blur)

    return [xc, s_xy, l, R_w, a1, I/pmt.gain(alpha), b_p/pmt.gain(alpha), b_t/pmt.gain(alpha)]


def p0_ols_ultimate(kymo_wall, alpha, sigma_blur=1.5):
    """ Intitial parameters guess for the ultimate fit using ordinary least squares fit 
    """
    nt, nx = kymo_wall.shape
    
    xc, s_xy, l, R, a1, I, b_p, b_t = p0_ols(kymo_wall[0], alpha, sigma_blur=sigma_blur)
    
    return np.r_[s_xy, l, b_p, b_t, nt*[I], nt*[R], nt*[xc], nt*[a1]]


def mle_fit(profile_wall, n_aver, alpha, sigma, n_r=256, n_phi=256, p0='ols', sigma_blur=1.5, minimize_options=None):
    """ Fit line-profiles with MLE
    """
    def neg_log_like(p):
        return pmt.nll_q_mean(profile_wall, 
                          L_wall(np.arange(len(profile_wall)), *p, n_r=n_r, n_phi=n_phi), 
                          alpha, 
                          sigma, 
                          n_aver)
    
    return minimize(neg_log_like, 
                    p0_ols(profile_wall, alpha, sigma_blur=sigma_blur) if p0 == 'ols' else p0,
                    method='bfgs', 
                    options=minimize_options)


def mle_fit_ultimate(kymo_wall, n_aver, alpha, sigma, n_r=256, n_phi=256, p0='ols', sigma_blur=1.5, minimize_options=None):
    """ Fit line-profiles with the ultimate MLE fit: Fitting several profiles at once
    """
    def neg_log_like(p):
        return pmt.nll_q_mean(kymo_wall, 
                              L_multi_wall(np.arange(kymo_wall.shape[1]), *p, n_r=n_r, n_phi=n_phi), 
                              alpha, 
                              sigma, 
                              n_aver)
    
    return minimize(neg_log_like, 
                    p0_ols_ultimate(kymo_wall, alpha, sigma_blur=sigma_blur) if p0 == 'ols' else p0,
                    method='bfgs', 
                    options=minimize_options)



    
