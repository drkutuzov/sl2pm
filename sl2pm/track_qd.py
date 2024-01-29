import numpy as np
import pmt
from models import qd_blurred
from scipy.optimize import minimize, curve_fit
from scipy.ndimage import gaussian_filter


def make_xy_grid(image):
    ny, nx = image.shape
    X, Y = np.meshgrid(range(nx), range(ny), indexing='xy')
    return X, Y


def ols_fit(image, sigma_blur=1):
    """ QDs localization by fitting with ordinary least-squares optimization
    """
    
    def qd_flat(xy, b, A, xo, yo, sx, sy, theta):
        x, y = xy
        return qd_blurred(x.reshape(image.shape), y.reshape(image.shape), b, A, xo, yo, sx, sy, theta).ravel()
    
    X, Y = make_xy_grid(image)
    x, y = X.ravel(), Y.ravel()

    image = gaussian_filter(image, sigma_blur)
    p0 = [image.min(), image.max(), x[image.argmax()], y[image.argmax()], 0.5, 0.5, 0]
    
    p, pcov = curve_fit(qd_flat, (x, y), image.ravel(), p0)

    return p


def p0_ols(image, alpha, sigma_blur=1):
    """ Intitial guess for parameters using ordinary least squares fit 
    """
    ny, nx = image.shape
    b, A, xo, yo, sx, sy, theta = ols_fit(image, sigma_blur=1)
    sx = np.sqrt(sx**2 - sigma_blur**2) if sx**2 > sigma_blur**2 else sx
    sy = np.sqrt(sy**2 - sigma_blur**2) if sy**2 > sigma_blur**2 else sy
    xo = xo if xo < nx else (nx - 1)/2
    yo = yo if yo < ny else (nx - 1)/2
    
    return [b/pmt.gain(alpha), A/pmt.gain(alpha), xo, yo, sx, sy, theta]


def neg_loglike(p, image, alpha, sigma, mu, delta_s=4, s_max=1000):
    """ Negative log-likelihood for fitting images of QDs
    """
    return np.sum(-np.log(pmt.q(image.ravel(), 
                                qd_blurred(*make_xy_grid(image), *p).ravel(), 
                                alpha, 
                                mu, 
                                sigma, 
                                delta_s=delta_s, 
                                s_max=s_max)
                         ))
    

def mle_fit(image, alpha, sigma, mu, p0='ols', sigma_blur=1, delta_s=5, s_max=800, minimize_options=None):
    """ Fit image with MLE
    """
    return minimize(neg_loglike, 
                       p0_ols(image, alpha, sigma_blur=sigma_blur) if p0 == 'ols' else p0,
                       args=(image, alpha, sigma, mu, delta_s, s_max), 
                       method='bfgs', 
                       options=minimize_options)