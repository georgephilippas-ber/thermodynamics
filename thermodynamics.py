import numpy
import sympy


def univariate(sympy_expression_str_: str, x_: numpy.ndarray) -> numpy.ndarray:
    try:
        sympy_expression_ = sympy.sympify(sympy_expression_str_)
    except sympy.SympifyError:
        return numpy.zeros_like(x_)

    if len(sympy_expression_.free_symbols) < 1:
        return numpy.ones_like(x_) * sympy.N(sympy_expression_)
    elif len(sympy_expression_.free_symbols) == 1:
        independent_symbol_ = sympy_expression_.free_symbols.pop()
    else:
        return numpy.zeros_like(x_)

    settings_ = numpy.seterr(all='raise')
    try:
        result_ = sympy.lambdify(independent_symbol_, sympy_expression_, modules='numpy')(x_)

        numpy.seterr(**settings_)

        return result_
    except (FloatingPointError, NameError):
        numpy.seterr(**settings_)

        return numpy.zeros_like(x_)


def thermodynamics_energy(heat_rate_: numpy.ndarray, power_: numpy.ndarray, interval_: numpy.ndarray) -> numpy.ndarray:
    energy_ = numpy.zeros_like(interval_)

    energy_rate_ = heat_rate_ - power_

    for i_ in numpy.arange(0, energy_.shape[0]):
        energy_[i_] = numpy.trapz(energy_rate_[:(i_ + 1)], interval_[:(i_ + 1)])

    return energy_


def thermodynamics_energy_sympy(heat_rate_sympy_expression_str_: str, power_sympy_expression_str_: str, interval_: numpy.ndarray):
    return thermodynamics_energy(univariate(heat_rate_sympy_expression_str_, interval_), univariate(power_sympy_expression_str_, interval_), interval_)
