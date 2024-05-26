import numpy as np


def step(t, tau1, tau2, dI1, dI2):
    
    return np.where(t>=0, dI1*(1 - np.exp(-t/tau1)) + dI2*(1 - np.exp(-t/tau2)), np.zeros(shape=t.shape))
    
    
def step_diff(t, w, tau1, tau2, dI1, dI2):
    
    return step(t, tau1, tau2, dI1, dI2) - step(t-w, tau1, tau2, dI1, dI2)


def step_diff_periodic(t, t0, w, tau1, tau2, dI1, dI2, dt):
    
    step_start = np.arange(t0 - 3*dt, t[-1] + 4*dt, dt)

    return step_diff(t[np.newaxis, :] - step_start[:, np.newaxis], w, tau1, tau2, dI1, dI2).sum(axis=0)


def bb_single(t, t0, w, tau1, tau2, dI1, dI2, I0, dt):
    
    return I0 - step_diff_periodic(t, t0, w, tau1, tau2, dI1, dI2, dt)


def bb_double(t, t01, w1, tau11, tau21, dI11, dI21, t02, w2, tau12, tau22, dI12, dI22, I0, dt):
    
    return I0 - step_diff_periodic(t, t01, w1, tau11, tau21, dI11, dI21, dt) - step_diff_periodic(t, t02, w2, tau12, tau22, dI12, dI22, dt)