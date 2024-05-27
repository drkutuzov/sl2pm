import numpy as np


def fitted_params(opt_result, p_names):
    """ 
    Parse fitted parameters and their error bars from optimization result (fit).
    """
    return {name: (val, std) for name, val, std in zip(p_names, opt_result.x, np.sqrt(np.diag(opt_result.hess_inv)))}