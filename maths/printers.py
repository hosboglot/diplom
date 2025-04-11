from maths import Coefficient, ExtraCondition
from maths.euler_equation import EulerEquation


def coefficients_to_latex(coefficients: list[Coefficient]) -> str:
    result = ''

    coefficients.sort(key=lambda x: x.order, reverse=True)

    for n, coef in enumerate(coefficients):
        if coef.value < 0:
            if n == 0:
                result += '-'
            else:
                result += ' - '
        elif coef.value > 0:
            if n == 0:
                pass
            else:
                result += ' + '
        else:  # coef == 0
            continue

        result += _try_int(abs(coef.value))

        if coef.order == 1:
            result += 'xy^{(1)}'
        elif coef.order == 0:
            result += 'y'
        else:
            result += 'x^{' + str(coef.order) + \
                '}y^{(' + str(coef.order) + ')}'

    if result == '':
        return '0 = 0'
    else:
        return result + ' = 0'


def coefficients_to_html(coefficients: list[Coefficient]) -> str:
    result = ''

    coefficients.sort(key=lambda x: x.order, reverse=True)
    coefficients = [coef for coef in coefficients if coef.value]

    for n, coef in enumerate(coefficients):
        cur = ''
        if coef.value < 0:
            if n == 0:
                cur += '-'
            else:
                cur += ' - '
        else:  # coef.value > 0
            if n == 0:
                pass
            else:
                cur += ' + '

        if abs(coef.value) != 1:
            cur += _try_int(abs(coef.value))

        if coef.order == 1:
            cur += 'xy<sup>(1)</sup>'
        elif coef.order == 0:
            cur += 'y'
        else:
            cur += 'x<sup>' + str(coef.order) + \
                '</sup>y<sup>(' + str(coef.order) + ')</sup>'

        result += cur

    if result == '':
        return '0 = 0'
    else:
        return result + ' = 0'


def solution_to_html(equation: EulerEquation):
    def _print_coefs(vars: list[float], roots: list[float]):
        cur = ''
        for n, c, r in zip(range(len(vars)), vars, roots):
            if c < 0:
                if n == 0:
                    cur += '-'
                else:
                    cur += ' - '
            else:  # c > 0
                if n == 0:
                    pass
                else:
                    cur += ' + '

            if abs(c) != 1:
                cur += f"{_try_int(abs(c))}"

            cur += f"x<sup>{_try_int(r)}</sup>"
        return cur

    result = '1) y = '
    roots = equation.parametricRootsBiggerThanOrder()
    result += _print_coefs(equation.firstVariadics(), roots)
    result += '<br>2) y = '
    result += _print_coefs(equation.secondVariadics(), roots)

    return result


def parametric_to_html(equation: EulerEquation):
    result = ''

    coefficients = equation.parametricCoefficientsList()
    coefficients.sort(key=lambda x: x.order, reverse=True)
    coefficients = [coef for coef in coefficients if coef.value]

    for n, coef in enumerate(coefficients):
        cur = ''
        if coef.value < 0:
            if n == 0:
                cur += '-'
            else:
                cur += ' - '
        else:  # coef.value > 0
            if n == 0:
                pass
            else:
                cur += ' + '

        if abs(coef.value) != 1 or coef.order == 0:
            cur += _try_int(abs(coef.value))

        if coef.order == 1:
            cur += 'm<sup></sup>'
        elif coef.order == 0:
            cur += ''
        else:
            cur += 'm<sup>' + str(coef.order) + '</sup>'

        result += cur

    if result == '':
        return '0 = 0'
    else:
        return result + ' = 0'


def point_to_html(cond: ExtraCondition):
    return f'({_try_int(cond.x)}, {_try_int(cond.y)})'


def derivative_to_html(cond: ExtraCondition):
    result = 'y<sup>(' + str(cond.order) + ')</sup>'
    result += f'({_try_int(cond.x)}) = {_try_int(cond.y)}'
    return result


def constant_to_html(cond: ExtraCondition):
    result = 'C<sub>' + str(cond.order) + '</sub>'
    result += f' = {_try_int(cond.constant)}'
    return result


def _try_int(val: float) -> str:
    return str(int(val)) if val.is_integer() else f'{val:.6}'
