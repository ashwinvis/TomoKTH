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


def ellippi(n, m):
    """
    Complete elliptic integral of third kind (simplified version).

    .. FIXME: Incorrect, because of non-standard definitions of elliptic integral in the reference

    Reference
    ---------
    F. LAMARCHE and C. LEROY, Evaluation of the volume of a sphere with a cylinder by elliptic integrals,
        Computer Phys. Comm. 59 (1990) pg. 365
    """
    a2 = n
    k2 = m
    k2_a2 = k2 + a2
    phi = np.arcsin(a2 / k2_a2)

    Kc = ellipk(k2)
    Ec = ellipe(k2)
    Ki = ellipkinc(phi, (1. - k2) ** 1)
    Ei = ellipeinc(phi, (1. - k2) ** 1)

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
    vsph = 4. * pi / 3 * rs ** 3

    if b >= (rs + rc):
        return 0.
    elif b == 0.:
        if rs < rc:
            vi = vsph
        else:
            vi = vsph - 4. / 3 * pi * (rs ** 2 - rc ** 2) ** 1.5
    elif rc > (rs + b):
        vi = vsph
    else:
        vi = vsph * heaviside(rc - b) + _vintersect_sphcyl_ellip(rs, rc, b)

    return vi


def _vintersect_sphcyl_ellip(rs, rc, b):
    """
    The cases for which evaluating the volume of intersection of a sphere with a cylinder
    makes use of elliptic integrals.

    """
    rs3 = rs ** 3
    bprc = b + rc
    bmrc = b - rc
    A = max(rs ** 2, bprc ** 2)
    B = min(rs ** 2, bprc ** 2)
    C = bmrc ** 2
    AB = A - B
    AC = A - C
    BC = B - C
    k2 = BC / AC
    s = bprc * bmrc
    e1 = ellipk(k2)
    e2 = ellipe(k2)

    if bmrc == 0:
        if rs == bprc:
            vi = - 4. / 3 * AC ** 0.5 * (s + 2. / 3 * AC)
        elif rs < bprc:
            vi = 4. / 3 / A ** 0.5 * (e1 * AB * (3 * B - 2 * A) +
                                      e2 * A * (2 * A - 4 * B)) / 3
        else:
            vi = 4. / 3 / A ** 0.5 * (e1 * AB * A -
                                      e2 * A * (4 * A - 2 * B)) / 3
    else:
        a2 = 1 - B / C
        e3 = elliptic_pi(a2, k2)

        if rs == bprc:
            vi = (4. / 3 * rs3 * np.arctan(2 * (b * rc) ** 0.5 / bmrc) -
                  4. / 3 * AC ** 0.5 * (s + 2. / 3 * AC))
        elif rs < bprc:
            vi = (4. / 3 / AC ** 0.5 *
                  (e3 * B ** 2 * s / C +
                   e1 * (s * (A - 2. * B) + AB * (3 * B - C - 2 * A) / 3) +
                   e2 * AC * (-s + (2 * A + 2 * C - 4 * B) / 3)))
        else:
            vi = 4. / 3 / AC ** 0.5 * (e3 * A ** 2 * s / C -
                                       e1 * (A * s - AB * AC / 3.) -
                                       e2 * AC * (s + (4. * A - 2 * B - 2 * C) / 3))
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


def distance_los_voxel(vec_pix, vec_vox, vec_normal):
    """
    Determines the distance between the line of sight from a pixel along the normal
    and the voxel center.

    Parameters
    ----------
    vec_pix : nd-array
        Position vector of the pixel center

    vec_vox : nd-array
        Postition vector of the voxel center

    vec_normal : nd-array
        Normal vector of the image plane

    """
    vec_pixvox = vec_vox - vec_pix
    vec_dist = np.cross(vec_pixvox, vec_normal)
    b = np.linalg.norm(vec_dist) / np.linalg.norm(vec_normal)
    return b


def calc_weight(rpix, vec_pix, rvox, vec_vox, vec_normal):
    """
    Calculates the weightage of a pixel on voxel.

    Parameters
    ---------
    rpix : float
        Radius of a pixel

    vec_pix : nd-array
        Position vector of the pixel center

    rvox : float
        Radius of a voxel

    vec_vox : nd-array
        Postition vector of the voxel center

    vec_normal : nd-array
        Normal vector of the image plane

    """
    b = distance_los_voxel(vec_pix, vec_vox, vec_normal)
    w = vintersect_sphcyl(rvox, rpix, b) / vintersect_sphcyl(rvox, rvox, 0.)
    return w
