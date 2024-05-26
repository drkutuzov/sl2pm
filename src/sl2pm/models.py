## Formulas for expected distributions of fluorescence on images/line-scans
## needed for tracking QDs, RBCs, and blood vessels 

import numpy as np
from scipy.special import erf, erfcx

###-------------------------------------------------------------------
###------------------------Quantum dots-------------------------------
def qd_blurred(x, y, b, A, xo, yo, sx, sy, theta):
    """ 2D rotationally-asymmetric Gaussian
    """
    b, A, sx, sy = np.abs(b), np.abs(A), np.abs(sx), np.abs(sy)
    
    dx, dy = x - xo, y - yo
    
    Q11 = np.cos(theta)**2/sx**2 + np.sin(theta)**2/sy**2
    Q22 = np.sin(theta)**2/sx**2 + np.cos(theta)**2/sy**2
    Q12 = 0.5*(np.sin(2*theta)/sx**2 - np.sin(2*theta)/sy**2)

    detQ = Q11*Q22 - Q12**2
    
    amp = 0.5*A*np.sqrt(detQ)/np.pi
    
    expr = b + amp*np.exp(-0.5*(Q11*dx**2 + 2*Q12*dx*dy + Q22*dy**2))
    
    return expr

###-------------------------------------------------------------------
###---------------------------RBCs------------------------------------
def rbc(x, b, A, s, xo):
    """ Line fluorescence intensity distribution along a RBC/plasma interface
    """
    return b + 0.5*A*(1 + erf((x - xo)/(np.sqrt(2)*s)))

def rbc_inv(x, b, A, s, xo):
    """ Line fluorescence intensity distribution along a plasma/RBC interface
    """
    return b + 0.5*A*(1 - erf((x - xo)/(np.sqrt(2)*s)))

###-------------------------------------------------------------------
###-----------------------Blood vessels-------------------------------
def gaussian(x, sigma):

    return np.exp(-x**2/(2*sigma**2))/np.sqrt(2*np.pi*sigma**2)


def laplace(x, l):

    return np.exp(-np.abs(x)/l)/(2*l)


def f_wall(x_psf, s_xy, l, R_wall, a1, n_phi=256):
    
    phi = np.linspace(-np.pi, np.pi, n_phi)
    X_PSF, PHI = np.meshgrid(x_psf, phi)
    
    rho = np.exp(a1*np.cos(PHI))/np.i0(a1)
    integrand = R_wall*rho*gaussian(R_wall*np.cos(PHI) - X_PSF, s_xy)*laplace(R_wall*np.sin(PHI), l)

    return np.trapz(integrand, x=phi, axis=0)


def F_lumen(x_psf, s_xy, l, R_lum, n_r=256):
    
    r = np.linspace(-R_lum, R_lum, n_r)
    X_PSF, R = np.meshgrid(x_psf, r)

    integrand = gaussian(R - X_PSF, s_xy)*(1 - np.exp(-np.sqrt(R_lum**2 - R**2)/l))

    return np.trapz(integrand, x=r, axis=0)


def F_gcx(x_psf, s_xy, l, R_lum, R_wall, s_gcx, n_phi=256):
    
    phi = np.linspace(0, np.pi, n_phi)
    X, PHI = np.meshgrid(x_psf, phi)
    
    a = np.sqrt(np.cos(PHI)**2/s_xy**2/2)
    b = (X*np.cos(PHI)/s_xy**2 - np.abs(np.sin(PHI))/l - 1/s_gcx)/2/a
    
    e1 = np.exp(-a**2*R_lum**2 + 2*b*a*R_lum - X**2/s_xy**2/2 + R_lum/s_gcx)*(1 + np.sqrt(np.pi)*b*erfcx(a*R_lum - b))/2/a**2
    e2 = np.exp(-a**2*R_wall**2 + 2*b*a*R_wall - X**2/s_xy**2/2 + R_lum/s_gcx)*(1 + np.sqrt(np.pi)*b*erfcx(a*R_wall - b))/2/a**2

    return np.trapz(e1 - e2, dx=phi[1]-phi[0], axis=0)/np.sqrt(2*np.pi*s_xy**2)/l


def F_plasma(x_psf, s_xy, l, R_lum, R_wall, s_gcx, n_phi=256, n_r=256):

    return F_lumen(x_psf, s_xy, l, R_lum, n_r=n_r) + F_gcx(x_psf, s_xy, l, R_lum, R_wall, s_gcx, n_phi=n_phi)


def L_plasma(x, xc, s_xy, l, R_lum, R_wall, s_gcx, I, b, n_phi=256, n_r=256):
    """ Full expression (with glycocalyx) for plasma line-scans of fluorescence
    """
    return (I - b)*F_plasma(x - xc, s_xy, l, R_lum, R_wall, s_gcx, n_phi=n_phi, n_r=n_r) + b


def L_plasma_no_glx(x, xc, s_xy, l, R_lum, I, b, n_r=256):
    """ Simplified (no glycocalyx) expression for plasma line-scans of fluorescence
    """
    return (I - b)*F_lumen(x - xc, s_xy, l, R_lum, n_r=n_r) + b


def L_wall(x, xc, s_xy, l, R_wall, a1, I, b_plasma, b_tissue, n_r=256, n_phi=256):
    """ Expression for plasma wall-scans of fluorescence
    """
    return I*f_wall(x - xc, s_xy, l, R_wall, a1, n_phi=n_phi) + (b_plasma - b_tissue)*F_lumen(x - xc, s_xy, l, R_wall, n_r=n_r) + b_tissue


def L_wall_plasma(x, xc, s_xy, l, R_lum, R_wall, s_gcx, a1, Iw, Ip, b_plasma, b_tissue_wall, b_tissue_plasma, n_r=256, n_phi=256):
    """ Expressions for wall and plasma wall-scans of fluorescence
    """
    return np.array([L_wall(x, xc, s_xy, l, R_wall, a1, Iw, b_plasma, b_tissue_wall, n_r=n_r, n_phi=n_phi),
                     L_plasma(x, xc, s_xy, l, R_lum, R_wall, s_gcx, Ip, b_tissue_plasma, n_r=n_r, n_phi=n_phi)]) 


#-------------------Ultimate Fit--------------------

def L_multi(x, s_xy, l, dR, s_gcx, b_plasma, b_tissue_wall, b_tissue_plasma, *pars, n_r=128, n_phi=128):
    """ Expressions for consecutive pairs (in time) of wall and plasma line-scans of fluorescence
    """
    Iw, Ip, R_wall, xc, a1 = np.reshape(np.asarray(pars), [5, len(pars)//5])    
    return np.array([[L_wall(x, xc_i, s_xy, l, R_wall_i, a1_i, Iw_i, b_plasma, b_tissue_wall, n_r=n_r, n_phi=n_phi),
                     L_plasma(x, xc_i, s_xy, l, R_wall_i - dR, R_wall_i, s_gcx, Ip_i, b_tissue_plasma, n_r=n_r, n_phi=n_phi)] 
                    for Iw_i, Ip_i, R_wall_i, xc_i, a1_i in zip(Iw, Ip, R_wall, xc, a1)])


def L_multi_wall(x, s_xy, l, b_plasma, b_tissue_wall, *pars, n_r=128, n_phi=128):
    """ Expressions for consecutive (in time) wall-scans of fluorescence
    """
    Iw, R_wall, xc, a1 = np.reshape(np.asarray(pars), [4, len(pars)//4])    
    return np.array([L_wall(x, xc_i, s_xy, l, R_wall_i, a1_i, Iw_i, b_plasma, b_tissue_wall, n_r=n_r, n_phi=n_phi)
                    for Iw_i, R_wall_i, xc_i, a1_i in zip(Iw, R_wall, xc, a1)])


def L_multi_plasma(x, s_xy, l, b_tissue_plasma, *pars, n_r=128):
    """ Expressions for consecutive (in time) plasma-scans of fluorescence
    """
    Ip, R_plasma, xc = np.reshape(np.asarray(pars), [3, len(pars)//3])    
    return np.array([L_plasma_no_glx(x, xc_i, s_xy, l, R_plasma_i, Ip_i, b_tissue_plasma, n_r=n_r)
                    for Ip_i, R_plasma_i, xc_i in zip(Ip, R_plasma, xc)])
    