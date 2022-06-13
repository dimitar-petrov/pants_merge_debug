# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = [
    "nufft1d1freqs",
    "nufft1d1",
    "nufft1d2",
    "nufft1d3",
    "nufft2d1",
    "nufft2d2",
    "nufft2d3",
    "nufft3d1",
    "nufft3d2",
    "nufft3d3",
]
import os
import numpy as np

if not os.environ.get("READTHEDOCS", None) == "True":
    from ._nufft import (
        dirft1d1,
        nufft1d1f90,
        dirft1d2,
        nufft1d2f90,
        dirft1d3,
        nufft1d3f90,
        dirft2d1,
        nufft2d1f90,
        dirft2d2,
        nufft2d2f90,
        dirft2d3,
        nufft2d3f90,
        dirft3d1,
        nufft3d1f90,
        dirft3d2,
        nufft3d2f90,
        dirft3d3,
        nufft3d3f90,
    )


def nufft1d1freqs(ms, df=1.0):
    """
    Calculates 1D frequencies

    :param ms: number of frequencies
    :type ms: int
    :param df: frequency spacing
    :type df: double
    :return: frequencies
    :rtype: array
    """
    return df * (np.arange(-ms // 2, ms // 2) + ms % 2)


def nufft1d1(x, y, ms, df=1.0, eps=1e-15, iflag=1, direct=False):
    """
    NUFFT type 1 in one dimension

    :param x: non-equispaced locations
    :type x: array
    :param y: non-equispaced function values
    :type y: array
    :param ms: number of frequencies
    :type ms: int
    :param df: frequency spacing
    :type df: double
    :param eps: tolerance for NUFFT
    :type eps: double
    :param iflag: sign for the exponential (0 means :math:`-i`, greater than 0 means :math:`+i`)
    :type iflag: int
    :param direct: use direct NUFFT methods
    :type direct: bool
    :return: function in integer frequency space
    :rtype: array
    """
    # Make sure that the data are properly formatted.
    x = np.ascontiguousarray(x, dtype=np.float64)
    y = np.ascontiguousarray(y, dtype=np.complex128)
    if len(x) != len(y):
        raise ValueError("Dimension mismatch")

    # Run the Fortran code.
    if direct:
        p = dirft1d1(x * df, y, iflag, ms)
    else:
        p, flag = nufft1d1f90(x * df, y, iflag, eps, ms)
        # Check the output and return.
        if flag:
            raise RuntimeError("nufft1d1 failed with code {0}".format(flag))
    return p


def nufft1d2(x, p, df=1.0, eps=1e-15, iflag=1, direct=False):
    """
    NUFFT type 2 in one dimension

    :param x: non-equispaced locations
    :type x: array
    :param p: function in integer frequency space
    :type p: array
    :param df: frequency spacing
    :type df: double
    :param eps: tolerance for NUFFT
    :type eps: double
    :param iflag: sign for the exponential (0 means :math:`-i`, greater than 0 means :math:`+i`)
    :type iflag: int
    :param direct: use direct NUFFT methods
    :type direct: bool
    :return: function evaluated at non-equispaced locations
    :rtype: array
    """
    # Make sure that the data are properly formatted.
    x = np.ascontiguousarray(x, dtype=np.float64)
    p = np.ascontiguousarray(p, dtype=np.complex128)

    # Run the Fortran code.
    if direct:
        y = dirft1d2(x * df, iflag, p)
    else:
        y, flag = nufft1d2f90(x * df, iflag, eps, p)
        # Check the output and return.
        if flag:
            raise RuntimeError("nufft1d2 failed with code {0}".format(flag))
    return y


def nufft1d3(x, y, f, eps=1e-15, iflag=1, direct=False):
    """
    NUFFT type 3 in one dimension

    :param x: non-equispaced locations
    :type x: array
    :param y: non-equispaced function values
    :type y: array
    :param f: non-equispaced frequencies
    :type f: array
    :param eps: tolerance for NUFFT
    :type eps: double
    :param iflag: sign for the exponential (0 means :math:`-i`, greater than 0 means :math:`+i`)
    :type iflag: int
    :param direct: use direct NUFFT methods
    :type direct: bool
    :return: function in non-equispaced frequency space
    :rtype: array
    """
    # Make sure that the data are properly formatted.
    x = np.ascontiguousarray(x, dtype=np.float64)
    y = np.ascontiguousarray(y, dtype=np.complex128)
    if len(x) != len(y):
        raise ValueError("Dimension mismatch")

    # Make sure that the frequencies are of the right type.
    f = np.ascontiguousarray(f, dtype=np.float64)

    # Run the Fortran code.
    if direct:
        p = dirft1d3(x, y, iflag, f)
    else:
        p, flag = nufft1d3f90(x, y, iflag, eps, f)
        # Check the output and return.
        if flag:
            raise RuntimeError("nufft1d3 failed with code {0}".format(flag))
    return p / len(x)


def nufft2d1(x, y, z, ms, mt, df=1.0, eps=1e-15, iflag=1, direct=False):
    """
    NUFFT type 1 in two dimensions

    :param x: non-equispaced locations
    :type x: array
    :param y: non-equispaced locations
    :type y: array
    :param z: non-equispaced function values
    :type z: array
    :param ms: number of frequencies (x-direction)
    :type ms: int
    :param mt: number of frequencies (y-direction)
    :type mt: int
    :param df: frequency spacing
    :type df: double
    :param eps: tolerance for NUFFT
    :type eps: double
    :param iflag: sign for the exponential (0 means :math:`-i`, greater than 0 means :math:`+i`)
    :type iflag: int
    :param direct: use direct NUFFT methods
    :type direct: bool
    :return: function in integer frequency space
    :rtype: array
    """
    # Make sure that the data are properly formatted.
    x = np.ascontiguousarray(x, dtype=np.float64)
    y = np.ascontiguousarray(y, dtype=np.float64)
    z = np.ascontiguousarray(z, dtype=np.complex128)
    if len(x) != len(y) or len(y) != len(z):
        raise ValueError("Dimension mismatch")

    # Run the Fortran code.
    if direct:
        p = dirft2d1(x * df, y * df, z, iflag, ms, mt)
    else:
        p, flag = nufft2d1f90(x * df, y * df, z, iflag, eps, ms, mt)
        # Check the output and return.
        if flag:
            raise RuntimeError("nufft2d1 failed with code {0}".format(flag))
    return p


def nufft2d2(x, y, p, df=1.0, eps=1e-15, iflag=1, direct=False):
    """
    NUFFT type 2 in two dimensions

    :param x: non-equispaced locations
    :type x: array
    :param y: non-equispaced locations
    :type y: array
    :param p: function in integer frequency space
    :type p: array
    :param df: frequency spacing
    :type df: double
    :param eps: tolerance for NUFFT
    :type eps: double
    :param iflag: sign for the exponential (0 means :math:`-i`, greater than 0 means :math:`+i`)
    :type iflag: int
    :param direct: use direct NUFFT methods
    :type direct: bool
    :return: function evaluated at non-equispaced locations
    :rtype: array
    """
    # Make sure that the data are properly formatted.
    x = np.ascontiguousarray(x, dtype=np.float64)
    y = np.ascontiguousarray(y, dtype=np.float64)
    p = np.ascontiguousarray(p, dtype=np.complex128)
    if len(x) != len(y):
        raise ValueError("Dimension mismatch")

    # Run the Fortran code.
    if direct:
        z = dirft2d2(x * df, y * df, iflag, p)
    else:
        z, flag = nufft2d2f90(x * df, y * df, iflag, eps, p)
        # Check the output and return.
        if flag:
            raise RuntimeError("nufft2d2 failed with code {0}".format(flag))
    return z


def nufft2d3(x, y, z, f, g, eps=1e-15, iflag=1, direct=False):
    """
    NUFFT type 3 in two dimensions

    :param x: non-equispaced locations
    :type x: array
    :param y: non-equispaced locations
    :type y: array
    :param z: non-equispaced function values
    :type z: array
    :param f: non-equispaced frequencies (x-direction)
    :type f: array
    :param g: non-equispaced frequencies (y-direction)
    :type g: array
    :param eps: tolerance for NUFFT
    :type eps: double
    :param iflag: sign for the exponential (0 means :math:`-i`, greater than 0 means :math:`+i`)
    :type iflag: int
    :param direct: use direct NUFFT methods
    :type direct: bool
    :return: function in non-equispaced frequency space
    :rtype: array
    """
    # Make sure that the data are properly formatted.
    x = np.ascontiguousarray(x, dtype=np.float64)
    y = np.ascontiguousarray(y, dtype=np.float64)
    z = np.ascontiguousarray(z, dtype=np.complex128)
    if len(x) != len(y) or len(y) != len(z):
        raise ValueError("Dimension mismatch")

    # Make sure that the frequencies are of the right type.
    f = np.ascontiguousarray(f, dtype=np.float64)
    g = np.ascontiguousarray(g, dtype=np.float64)
    if len(f) != len(g):
        raise ValueError("Dimension mismatch")

    # Run the Fortran code.
    if direct:
        p = dirft2d3(x, y, z, iflag, f, g)
    else:
        p, flag = nufft2d3f90(x, y, z, iflag, eps, f, g)
        # Check the output and return.
        if flag:
            raise RuntimeError("nufft2d3 failed with code {0}".format(flag))
    return p / len(x)


def nufft3d1(x, y, z, c, ms, mt, mu, df=1.0, eps=1e-15, iflag=1, direct=False):
    """
    NUFFT type 1 in three dimensions

    :param x: non-equispaced locations
    :type x: array
    :param y: non-equispaced locations
    :type y: array
    :param z: non-equispaced locations
    :type z: array
    :param c: non-equispaced function values
    :type c: array
    :param ms: number of frequencies (x-direction)
    :type ms: int
    :param mt: number of frequencies (y-direction)
    :type mt: int
    :param mu: number of frequencies (z-direction)
    :type mu: int
    :param df: frequency spacing
    :type df: double
    :param eps: tolerance for NUFFT
    :type eps: double
    :param iflag: sign for the exponential (0 means :math:`-i`, greater than 0 means :math:`+i`)
    :type iflag: int
    :param direct: use direct NUFFT methods
    :type direct: bool
    :return: function in integer frequency space
    :rtype: array
    """
    # Make sure that the data are properly formatted.
    x = np.ascontiguousarray(x, dtype=np.float64)
    y = np.ascontiguousarray(y, dtype=np.float64)
    z = np.ascontiguousarray(z, dtype=np.float64)
    c = np.ascontiguousarray(c, dtype=np.complex128)
    if len(x) != len(y) or len(y) != len(z) or len(z) != len(c):
        raise ValueError("Dimension mismatch")

    # Run the Fortran code.
    if direct:
        p = dirft3d1(x * df, y * df, z * df, c, iflag, ms, mt, mu)
    else:
        p, flag = nufft3d1f90(x * df, y * df, z * df, c, iflag, eps, ms, mt, mu)
        # Check the output and return.
        if flag:
            raise RuntimeError("nufft3d1 failed with code {0}".format(flag))
    return p


def nufft3d2(x, y, z, p, df=1.0, eps=1e-15, iflag=1, direct=False):
    """
    NUFFT type 2 in three dimensions

    :param x: non-equispaced locations
    :type x: array
    :param y: non-equispaced locations
    :type y: array
    :param z: non-equispaced locations
    :type z: array
    :param p: function in integer frequency space
    :type p: array
    :param df: frequency spacing
    :type df: double
    :param eps: tolerance for NUFFT
    :type eps: double
    :param iflag: sign for the exponential (0 means :math:`-i`, greater than 0 means :math:`+i`)
    :type iflag: int
    :param direct: use direct NUFFT methods
    :type direct: bool
    :return: function evaluated at non-equispaced locations
    :rtype: array
    """
    # Make sure that the data are properly formatted.
    x = np.ascontiguousarray(x, dtype=np.float64)
    y = np.ascontiguousarray(y, dtype=np.float64)
    z = np.ascontiguousarray(z, dtype=np.float64)
    p = np.ascontiguousarray(p, dtype=np.complex128)
    if len(x) != len(y) or len(y) != len(z):
        raise ValueError("Dimension mismatch")

    # Run the Fortran code.
    if direct:
        c = dirft3d2(x * df, y * df, z * df, iflag, p)
    else:
        c, flag = nufft3d2f90(x * df, y * df, z * df, iflag, eps, p)
        # Check the output and return.
        if flag:
            raise RuntimeError("nufft3d2 failed with code {0}".format(flag))
    return c


def nufft3d3(x, y, z, c, f, g, h, eps=1e-15, iflag=1, direct=False):
    """
    NUFFT type 3 in three dimensions

    :param x: non-equispaced locations
    :type x: array
    :param y: non-equispaced locations
    :type y: array
    :param z: non-equispaced locations
    :type z: array
    :param c: non-equispaced function values
    :type c: array
    :param f: non-equispaced frequencies (x-direction)
    :type f: array
    :param g: non-equispaced frequencies (y-direction)
    :type g: array
    :param h: non-equispaced frequencies (z-direction)
    :type h: array
    :param eps: tolerance for NUFFT
    :type eps: double
    :param iflag: sign for the exponential (0 means :math:`-i`, greater than 0 means :math:`+i`)
    :type iflag: int
    :param direct: use direct NUFFT methods
    :type direct: bool
    :return: function in non-equispaced frequency space
    :rtype: array
    """
    # Make sure that the data are properly formatted.
    x = np.ascontiguousarray(x, dtype=np.float64)
    y = np.ascontiguousarray(y, dtype=np.float64)
    z = np.ascontiguousarray(z, dtype=np.float64)
    c = np.ascontiguousarray(c, dtype=np.complex128)
    if len(x) != len(y) or len(y) != len(z) or len(z) != len(c):
        raise ValueError("Dimension mismatch")

    # Make sure that the frequencies are of the right type.
    f = np.ascontiguousarray(f, dtype=np.float64)
    g = np.ascontiguousarray(g, dtype=np.float64)
    h = np.ascontiguousarray(h, dtype=np.float64)
    if len(f) != len(g) or len(g) != len(h):
        raise ValueError("Dimension mismatch")

    # Run the Fortran code.
    if direct:
        p = dirft3d3(x, y, z, c, iflag, f, g, h)
    else:
        p, flag = nufft3d3f90(x, y, z, c, iflag, eps, f, g, h)
        # Check the output and return.
        if flag:
            raise RuntimeError("nufft3d3 failed with code {0}".format(flag))
    return p / len(x)
