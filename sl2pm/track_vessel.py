import numpy as np
import pmt
from scipy.optimize import minimize, curve_fit
from scipy.ndimage import gaussian_filter1d
from models import L_wall, L_plasma_no_glx, L_wall_plasma

### ----------------------------------------------- ###
### Ordinary least-squares fitting of line-profiles ###

def ols_plasma(profile_plasma, sigma_blur=1.5, thr=0.1):

    x = np.arange(len(profile_plasma))
    
    plasma = gaussian_filter1d(profile_plasma, sigma_blur)
    plasma_norm = (plasma - plasma.min())/(plasma.max() - plasma.min())
    
    xc = plasma.argmax()
    R = xc - (np.abs(plasma_norm - thr)[:xc]).argmin()
    
    p0 = [xc, 2, 6, R, plasma.max(), plasma.min()]

    p, pcov = curve_fit(lambda *args: L_plasma_no_glx(*args), x, plasma, p0)

    return p


def ols_wall(profile_wall, sigma_blur=1.5):

    x = np.arange(len(profile_wall))
    
    wall = gaussian_filter1d(profile_wall, sigma_blur)
    
    x_max1, x_max2 = wall[:len(wall)//2].argmax(), len(wall)//2 + wall[len(wall)//2:].argmax()
    
    xc = 0.5*(x_max1 + x_max2)
    R = 0.5*(x_max2 - x_max1)
    
    p0 = [xc, 2, 6, R, 0, wall.max(), 0, wall.min()]
    
    p, pcov = curve_fit(lambda *args: L_wall(*args), x, wall, p0)

    return p


def ols_wall_plasma(profile_wall, profile_plasma, sigma_blur=1.5):

    x = np.arange(len(profile_wall))
    
    wall = gaussian_filter1d(profile_wall, sigma_blur)
    plasma = gaussian_filter1d(profile_plasma, sigma_blur)
    
    x_max1, x_max2 = wall[:len(wall)//2].argmax(), len(wall)//2 + wall[len(wall)//2:].argmax()
    
    xc = 0.5*(x_max1 + x_max2)
    R = 0.5*(x_max2 - x_max1)
    
    p0 = [xc, 2, 6, R, R, 1, 0, wall.max(), plasma.max(), wall.min(), wall.min(), plasma.min()]
    
    p, pcov = curve_fit(lambda *args: L_wall_plasma(*args).ravel(), x, np.hstack([wall, plasma]), p0)

    return p

###------------------------------###
### MLE fitting of line-profiles ###

def mle(x, y, func, p0, n_aver, alpha, sigma, minimize_options=None):

    def neg_loglike(p):

        return pmt.nll_q_mean(y, func(x, *p), alpha, sigma, n_aver) 

    return minimize(neg_loglike, 
                    p0,
                    method='bfgs', 
                    options=minimize_options)
