"""Special mathematical operators (:mod:`tomokth.operators.math`)
==========================================================================

.. currentmodule:: tomokth.operators.math

Provides
--------
vintersect_sphcyl

"""

from __future__ import division
import numpy as np
from scipy.special import ellipkinc, ellipeinc, ellipk, ellipe
from scipy.integrate import dblquad
from sympy import elliptic_pi


def ellippi(k, a2):
    """
    Complete elliptic integral of third kind (simplified version).

    .. FIXME: Incorrect, because of non-standard definitions of elliptic integral in the reference

    Reference
    ---------
    F. LAMARCHE and C. LEROY, Evaluation of the volume of a sphere with a cylinder by elliptic integrals,
        Computer Phys. Comm. 59 (1990) pg. 365
    """
    k2 = k ** 2
    k2_a2 = k2 + a2
    phi = np.arcsin(a2 / k2_a2)

    Kc = ellipk(k2)
    Ec = ellipe(k2)
    Ki = ellipkinc(phi, 1. - k2)
    Ei = ellipeinc(phi, 1. - k2)

    c1 = k2 / k2_a2
    c2 = np.sqrt(a2 / (1 + a2) / k2_a2)

    return c1 * Kc + c2 * ((Kc - Ec) * Ki + Kc * Ei)


def heaviside(x):
    """Heaviside step function.

    Alternate implementation
    ------------------------
    if x == 0.:
        return 0.5
    elif x < 0:
        return 0.
    else:
        return 1.
    """
    return 0.5 * (np.sign(x) + 1)


def vintersect_sphcyl(rs, rc, b):
    """
    Returns the volume of intersection of a sphere with a cylinder.

    Parameters
    ----------
    rs : float
        radius of the sphere (r)
    rc : float
        radius of the cylinder (R)
    b : float
        impact parameter, the smallest distance of the cylinder axis to the centre of the sphere.

    Reference
    ---------
    F. LAMARCHE and C. LEROY, Evaluation of the volume of a sphere with a cylinder by elliptic integrals,
        Computer Phys. Comm. 59 (1990) 359-369

    """
    pi = np.pi
    rc2 = rc ** 2
    rs2 = rs ** 2
    rs3 = rs * rs2
    vsph = 4. * pi / 3 * rs3

    if b >= (rs + rc):
        return 0.
    elif b == 0.:
        if rs < rc:
            vi = vsph
        else:
            vi = vsph - 4. / 3 * pi * (rs2 - rc2) ** 1.5
    elif rc > (rs + b):
        vi = vsph
    else:
        A = max(rs2, (b + rc) ** 2)
        B = min(rs2, (b + rc) ** 2)
        C = (b - rc) ** 2
        k2 = (B - C) / (A - C)
        s = (b + rc) * (b - rc)
        e1 = ellipk(k2)
        e2 = ellipe(k2)
        if C != 0.:
            a2 = 1 - B / C
            e3 = elliptic_pi(a2, k2)

        if rs == (b + rc):
            if b == rc:
                vi = - 4. / 3 * (A - C) ** 0.5 * (s + 2. / 3 * (A - C))
            else:
                vi = (4. / 3 * rs3 * np.arctan(2 * (b * rc) ** 0.5 / (b - rc))
                      - 4. / 3 * (A - C) ** 0.5 * (s + 2. / 3 * (A - C)))
        elif rs < (b + rc):
            if b == rc:  # s = 0; C = 0
                vi = 4. / 3 / A ** 0.5 * (e1 * (A - B) * (3 * B - 2 * A) / 3
                                          + e2 * A * (2 * A - 4 * B) / 3 )
            else:
                vi = (4. / 3 / (A - C) ** 0.5
                      * (e3 * B ** 2 * s / C
                         + e1 * (s * (A - 2. * B) + (A - B) * (3 * B - C - 2 * A) / 3)
                         + e2 * (A - C) * (-s + (2 * A + 2 * C - 4 * B) / 3)))
        else:
            if b == rc:  # s = 0; C = 0
                vi = 4. / 3 / A ** 0.5 * (e1 * (A - B) * A / 3
                                          - e2 * A * (4 * A - 2 * B) / 3 )
            else:
                vi = 4. / 3 / (A - C) ** 0.5 * (e3 * A ** 2 * s / C
                                                - e1 * (A * s - (A - B) * (A - C) / 3.)
                                                - e2 * (A - C) * (s + (4. * A - 2 * B - 2 * C) / 3))

        vi = vi + vsph * heaviside(rc - b)
    return vi


def vintersect_sphcyl_quad(rs, rc, b):
    """
    Numerically integrated volume of intersection of a sphere with a cylinder.
    .. FIXME: Incorrect

    """
    func = lambda x, y: (rs ** 2 - x ** 2 - y ** 2) ** 0.5
    b = min(b - rc, rs)
    a = max(b - rc, -rs)
    gfun = lambda x: 0
    hfun = lambda x: min((rc ** 2 - (x - b) ** 2) ** 0.5,
                         (rs ** 2 - x ** 2) ** 0.5)
    vi, abserr = dblquad(func, a, b, gfun, hfun)
    return 4. * vi
