# -*- coding: utf-8 -*-
"""Python wrapper for ITM122.dll.

This wrapper is designed to work with ITM v1.2.2 which is a C .dll.


@author: Erik Hill, 2025
"""
# %% imports
# standard
import os
import errno
import ctypes as ct

# third party
import numpy as np

# local


# %% ITM122
class ITM122:
    """Python wrapper class for ITM v1.2.2: ITM122.dll.

    This class allows the use of ITM122.dll functions from Python through a
    ctypes interface. This class necessarily requires the ITM122.dll to be in
    the default repository location or a specified location. ITM122.dll must be
    compiled for a 64-bit operating system.

    ITM122.dll function are directly linked with "dll_" prepended to their names
    and can be called directly from this wrapper. Their function signatures are
    identical to the ITM122.dll function signatures.

    Additional wrapper functions for the dll_* functions are provided which
    handle the creation, passing, and parsing of the ctypes arguments. This is
    particularly convenient for input/output arguments.

    This wrapper class is instantiated with the file path (dll_path) to
    ITM122.dll. If no file path is provided, the default relative path to this
    repository's compiled ITM122.dll is searched.

    Usage
    -----
    itm122 = ITM122()
    """

    # %% __init__
    def __init__(
        self,
        dll_path: str = None
    ):
        """Initialize ITM122.dll wrapper.

        Construct attributes for the ITM122 class by interfacing with
        the supplied ITM122.dll file.

        If no dll_path is given, the default path is searched.
        If the .dll is not found on the default path, an error is given.

        Parameters
        ----------
        dll_path : str, optional (default=None)
            The file path of the 64-bit ITM122.dll to use.
            If dll_path is not provided, the default repository location is
            searched.
        """
        default_dll_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                r"..\..\..",
                r"itm-longley-rice-dev\Visual_Studio\ITM122",
                r"x64\Release",
                r"ITM122.dll"
            )
        )
        if dll_path is None:
            # Try the default ITM122.dll repository location.
            dll_path = default_dll_path

        # Ensure the .dll exists and can be read.
        try:
            with open(dll_path, 'rb') as _:
                # The .dll exists and can be read.
                pass
        except FileNotFoundError as exc:
            # The .dll can not be read.
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                dll_path
            ) from exc

        # Load the .dll.
        self.DLL = ct.cdll.LoadLibrary(dll_path)

        # Get the area function.
        self.dll_area = getattr(
            self.DLL,
            "area"
        )
        self.dll_area.argtypes = [
            ct.c_long,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_int,
            ct.c_int,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_int,
            ct.c_int,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.POINTER(ct.c_double),
            ct.c_char_p,
            ct.POINTER(ct.c_int)
        ]
        self.dll_area.restype = None

        # Get the avar function.
        self.dll_avar = getattr(
            self.DLL,
            "avar"
        )
        self.dll_avar.argtypes = [
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.POINTER(prop_type),
            ct.POINTER(propv_type)
        ]
        self.dll_avar.restype = ct.c_double

        # Get the ITMAreadBLoss function.
        self.dll_ITMAreadBLoss = getattr(
            self.DLL,
            "ITMAreadBLoss"
        )
        self.dll_ITMAreadBLoss.argtypes = [
            ct.c_long,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_int,
            ct.c_int,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_int,
            ct.c_int,
            ct.c_double,
            ct.c_double,
            ct.c_double
        ]
        self.dll_ITMAreadBLoss.restype = ct.c_double

        # Get the .dll version.
        self.dll_ITMDLLVersion = getattr(
            self.DLL,
            'ITMDLLVersion'
        )
        self.dll_ITMDLLVersion.argtypes = None
        self.dll_ITMDLLVersion.restype = ct.c_double
        self.dll_ITMDLLVersion = self.dll_ITMDLLVersion()

        # Get the lrprop function.
        self.dll_lrprop = getattr(
            self.DLL,
            "lrprop"
        )
        self.dll_lrprop.argtypes = [
            ct.c_double,
            ct.POINTER(prop_type),
            ct.POINTER(propa_type)
        ]
        self.dll_lrprop.restype = None

        # Get the point_to_point function.
        self.dll_point_to_point = getattr(
            self.DLL,
            "point_to_point"
        )
        self.dll_point_to_point.argtypes = [
            np.ctypeslib.ndpointer(ct.c_double, flags='C_CONTIGUOUS'),
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_int,
            ct.c_int,
            ct.c_double,
            ct.c_double,
            ct.POINTER(ct.c_double),
            ct.c_char_p,
            ct.POINTER(ct.c_int)
        ]
        self.dll_point_to_point.restype = None

        # Get the point_to_pointDH function.
        self.dll_point_to_pointDH = getattr(
            self.DLL,
            "point_to_pointDH"
        )
        self.dll_point_to_pointDH.argtypes = [
            np.ctypeslib.ndpointer(ct.c_double, flags='C_CONTIGUOUS'),
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_int,
            ct.c_int,
            ct.c_double,
            ct.c_double,
            ct.POINTER(ct.c_double),
            ct.POINTER(ct.c_double),
            ct.POINTER(ct.c_int)
        ]
        self.dll_point_to_pointDH.restype = None

        # Get the point_to_pointMDH function.
        self.dll_point_to_pointMDH = getattr(
            self.DLL,
            "point_to_pointMDH"
        )
        self.dll_point_to_pointMDH.argtypes = [
            np.ctypeslib.ndpointer(ct.c_double, flags='C_Contiguous'),
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.c_int,
            ct.c_int,
            ct.c_double,
            ct.c_double,
            ct.c_double,
            ct.POINTER(ct.c_double),
            ct.POINTER(ct.c_int),
            ct.POINTER(ct.c_double),
            ct.POINTER(ct.c_int)
        ]
        self.dll_point_to_pointMDH.restype = None

        # Get the qerfi function.
        self.dll_qerfi = getattr(
            self.DLL,
            "qerfi"
        )
        self.dll_qerfi.argtypes = [
            ct.c_double
        ]
        self.dll_qerfi.restype = ct.c_double

        # Get the qlra function.
        self.dll_qlra = getattr(
            self.DLL,
            "qlra"
        )
        self.dll_qlra.argtypes = [
            np.ctypeslib.ndpointer(ct.c_int, flags='C_Contiguous'),
            ct.c_int,
            ct.c_int,
            ct.POINTER(prop_type),
            ct.POINTER(propv_type)
        ]
        self.dll_qlra.restype = None

    # %% __exit__
    def __exit__(
        self,
        exc_type,
        exc_value,
        exc_traceback
    ):
        """Close the .dll."""
        ct.windll.kernel32.FreeLibrary(self.MKEDLL._handle)

    # %% print_version
    def print_version(
        self,
    ):
        """Print ITM122 Library version information."""
        print((
            "**** ITM122 Library **********************************\n"
            f"    .dll Version:      {self.ITMDLLVersion()}\n"
            f"*****************************************************"
        ))

    # %% area
    def area(
        self,
        ModVar,
        deltaH,
        tht_m,
        rht_m,
        dist_km,
        TSiteCriteria,
        RSiteCriteria,
        eps_dielect,
        sgm_conductivity,
        eno_ns_surfref,
        frq_mhz,
        radio_climate,
        pol,
        pctTime,
        pctLoc,
        pctConf
    ):
        """ITM v1.2.2 area mode."""
        ctype_dbloss = ct.c_double(0)
        ctype_strmode = ct.create_string_buffer(0)  # Not used.
        ctype_errnum = ct.c_int(0)

        self.dll_area(
            ModVar,
            deltaH,
            tht_m,
            rht_m,
            dist_km,
            TSiteCriteria,
            RSiteCriteria,
            eps_dielect,
            sgm_conductivity,
            eno_ns_surfref,
            frq_mhz,
            radio_climate,
            pol,
            pctTime,
            pctLoc,
            pctConf,
            ct.byref(ctype_dbloss),
            ctype_strmode,
            ct.byref(ctype_errnum)
        )

        dbloss = ctype_dbloss.value
        errnum = ctype_errnum.value

        return dbloss, errnum

    # %% avar
    def avar(
        self,
        zzt,
        zzl,
        zzc
    ):
        """ITM v1.2.2 avar."""
        prop = prop_type()
        propv = propv_type()

        avarv = self.dll_avar(
            zzt,
            zzl,
            zzc,
            ct.byref(prop),
            ct.byref(propv)
        )

        return avarv, prop, propv

    # %% ITMAreadBLoss
    def ITMAreadBLoss(
        self,
        ModVar,
        deltaH,
        tht_m,
        rht_m,
        dist_km,
        TSiteCriteria,
        RSiteCriteria,
        eps_dielect,
        sgm_conductivity,
        eno_ns_surfref,
        frq_mhz,
        radio_climate,
        pol,
        pctTime,
        pctLoc,
        pctConf
    ):
        """ITM v1.2.2 ITMAreadBLoss."""
        dbloss = self.dll_ITMAreadBLoss(
            ModVar,
            deltaH,
            tht_m,
            rht_m,
            dist_km,
            TSiteCriteria,
            RSiteCriteria,
            eps_dielect,
            sgm_conductivity,
            eno_ns_surfref,
            frq_mhz,
            radio_climate,
            pol,
            pctTime,
            pctLoc,
            pctConf
        )
        return dbloss

    # %% ITMDLLVersion
    def ITMDLLVersion(
        self,
    ):
        """Return the ITM122.dll version number."""
        return self.dll_ITMDLLVersion

    # %% lrprop
    def lrprop(
        self,
        d
    ):
        """ITM v1.2.2 lrprop."""
        prop = prop_type()
        propa = propa_type()

        self.dll_lrprop(
            d,
            ct.byref(prop),
            ct.byref(propa)
        )
        return prop, propa

    # %% point_to_point
    def point_to_point(
        self,
        elev,
        tht_m,
        rht_m,
        eps_dielect,
        sgm_conductivity,
        eno_ns_surfref,
        frq_mhz,
        radio_climate,
        pol,
        conf,
        rel
    ):
        """ITM v1.2.2 Point-to-Point mode."""
        ctype_dbloss = ct.c_double(0)
        ctype_strmode = ct.create_string_buffer(42)
        ctype_errnum = ct.c_int(0)

        self.dll_point_to_point(
            np.array(elev, dtype='float64'),
            tht_m,
            rht_m,
            eps_dielect,
            sgm_conductivity,
            eno_ns_surfref,
            frq_mhz,
            radio_climate,
            pol,
            conf,
            rel,
            ct.byref(ctype_dbloss),
            ctype_strmode,
            ct.byref(ctype_errnum)
        )

        dbloss = ctype_dbloss.value
        strmode = ctype_strmode.value.decode('utf-8')
        errnum = ctype_errnum.value

        return dbloss, strmode, errnum

    # %% point_to_pointDH
    def point_to_pointDH(
        self,
        elev,
        tht_m,
        rht_m,
        eps_dielect,
        sgm_conductivity,
        eno_ns_surfref,
        frq_mhz,
        radio_climate,
        pol,
        conf,
        rel
    ):
        """ITM v1.2.2 point_to_pointDH function."""
        ctype_dbloss = ct.c_double(0)
        ctype_deltaH = ct.c_double(0)
        ctype_errnum = ct.c_int(0)

        self.dll_point_to_point(
            np.array(elev, dtype='float64'),
            tht_m,
            rht_m,
            eps_dielect,
            sgm_conductivity,
            eno_ns_surfref,
            frq_mhz,
            radio_climate,
            pol,
            conf,
            rel,
            ct.byref(ctype_dbloss),
            ct.byref(ctype_deltaH),
            ct.byref(ctype_errnum)
        )

        dbloss = ctype_dbloss.value
        deltaH = ctype_deltaH.value
        errnum = ctype_errnum.value

        return dbloss, deltaH, errnum

    # %% point_to_pointMDH
    def point_to_pointMDH(
        self,
        elev,
        tht_m,
        rht_m,
        eps_dielect,
        sgm_conductivity,
        eno_ns_surfref,
        frq_mhz,
        radio_climate,
        pol,
        timepct,
        locpct,
        confpct
    ):
        """ITM v1.2.2 point_to_pointMDH function."""
        ctype_dbloss = ct.c_double(0)
        ctype_propmode = ct.c_int(0)
        ctype_deltaH = ct.c_double(0)
        ctype_errnum = ct.c_int(0)

        self.dll_point_to_pointMDH(
            elev,
            tht_m,
            rht_m,
            eps_dielect,
            sgm_conductivity,
            eno_ns_surfref,
            frq_mhz,
            radio_climate,
            pol,
            timepct,
            locpct,
            confpct,
            ct.byref(ctype_dbloss),
            ct.byref(ctype_propmode),
            ct.byref(ctype_deltaH),
            ct.byref(ctype_errnum)
        )

        dbloss = ctype_dbloss.value
        propmode = ctype_propmode.value
        deltaH = ctype_deltaH.value
        errnum = ctype_errnum.value

        return dbloss, propmode, deltaH, errnum

    # %% qerfi
    def qerfi(
        self,
        q
    ):
        """ITM v1.2.2 qerfi function."""
        v = self.dll_qerfi(q)
        return v

    # %% qlra
    def qlra(
        self,
        kst,
        klimx,
        mdvarx
    ):
        """ITM v1.2.2 qlra function."""
        prop = prop_type()
        propv = propv_type()

        self.dll_qlra(
            kst,
            klimx,
            mdvarx,
            ct.byref(prop),
            ct.byref(propv)
        )
        return prop, propv

# %% Classes for C structures used by ITM v1.2.2.


# %% tcomplex
class tcomplex(ct.Structure):
    """tcomplex structure."""

    _fields_ = [
        ("tcreal", ct.c_double),
        ("tcimag", ct.c_double)
    ]

    def __dict__(
        self
    ):
        """Return this structure's contents as a dict."""
        tcomplex_dict = {
            "tcreal": self.tcreal,
            "tcimag": self.tcimag
        }
        return tcomplex_dict


# %% prop_type
class prop_type(ct.Structure):
    """prop_type structure."""

    _fields_ = [
        ("aref", ct.c_double),
        ("dist", ct.c_double),
        ("hg", ct.c_double * 2),
        ("wn", ct.c_double),
        ("dh", ct.c_double),
        ("ens", ct.c_double),
        ("gme", ct.c_double),
        ("zgndreal", ct.c_double),
        ("zgndimag", ct.c_double),
        ("he", ct.c_double * 2),
        ("dl", ct.c_double * 2),
        ("the", ct.c_double * 2),
        ("kwx", ct.c_double),
        ("mdp", ct.c_double)
    ]

    def __dict__(
        self
    ):
        """Return this structure's contents as a dict."""
        prop_type_dict = {
            "aref": self.aref,
            "dist": self.dist,
            "hg": self.hg[:],
            "wn": self.wn,
            "dh": self.dh,
            "ens": self.ens,
            "gme": self.gme,
            "zgndreal": self.zgndreal,
            "zgndimag": self.zgndimag,
            "he": self.he[:],
            "dl": self.dl[:],
            "the": self.the[:],
            "kwx": self.kwx,
            "mdp": self.mdp
        }
        return prop_type_dict


# %% propv_type
class propv_type(ct.Structure):
    """propv_type structure."""

    _fields_ = [
        ("sgc", ct.c_double),
        ("lvar", ct.c_int),
        ("mdvar", ct.c_int),
        ("klim", ct.c_int)
    ]

    def __dict__(
        self
    ):
        """Return this structure's contents as a dict."""
        propv_type_dict = {
            "sgc": self.sgc,
            "lvar": self.lvar,
            "mdvar": self.mdvar,
            "klim": self.klim
        }
        return propv_type_dict


# %% propa_type
class propa_type(ct.Structure):
    """propa_type structure."""

    _fields_ = [
        ("dlsa", ct.c_double),
        ("dx", ct.c_double),
        ("ael", ct.c_double),
        ("ak1", ct.c_double),
        ("ak2", ct.c_double),
        ("aed", ct.c_double),
        ("emd", ct.c_double),
        ("aes", ct.c_double),
        ("ems", ct.c_double),
        ("dls", ct.c_double * 2),
        ("dla", ct.c_double),
        ("tha", ct.c_double)
    ]

    def __dict__(
        self
    ):
        """Return this structure's contents as a dict."""
        propa_type_dict = {
            "dlsa": self.dlsa,
            "dx": self.dx,
            "ael": self.ael,
            "ak1": self.ak1,
            "ak2": self.ak2,
            "aed": self.aed,
            "emd": self.emd,
            "aes": self.aes,
            "ems": self.ems,
            "dls": self.dls[:],
            "dla": self.dla,
            "tha": self.tha
        }
        return propa_type_dict


# %% Run program.
if __name__ == "__main__":
    print("Running program: " + os.path.basename(__file__))

    # Initialize.
    itm122 = ITM122()
    itm122.print_version()

    # Try point_to_point().
    elev = [3, 10, 0, 10, 20, 0]
    tht_m = 5
    rht_m = 6
    eps_dielect = 15
    sgm_conductivity = 0.005
    eno_ns_surfref = 301
    frq_mhz = 1500
    radio_climate = 5
    pol = 1
    conf = 0.5
    rel = 0.5

    dbloss, strmode, errnum = itm122.point_to_point(
        elev,
        tht_m,
        rht_m,
        eps_dielect,
        sgm_conductivity,
        eno_ns_surfref,
        frq_mhz,
        radio_climate,
        pol,
        conf,
        rel
    )

    print("point-to-point:")
    print(f"    dbloss: {dbloss}")
    print(f"    strmode: {strmode}")
    print(f"    errnum: {errnum}")

    # Try area().
    ModVar = 0
    deltaH = 5.0
    tht_m = 10.0
    rht_m = 1.0
    dist_km = 50.0
    TSiteCriteria = 0
    RSiteCriteria = 1
    eps_dielect = 15
    sgm_conductivity = 0.005
    eno_ns_surfref = 301
    frq_mhz = 2000.0
    radio_climate = 5
    pol = 0
    pctTime = 0.50
    pctLoc = 0.60
    pctConf = 0.70

    dbloss, errnum = itm122.area(
        ModVar,
        deltaH,
        tht_m,
        rht_m,
        dist_km,
        TSiteCriteria,
        RSiteCriteria,
        eps_dielect,
        sgm_conductivity,
        eno_ns_surfref,
        frq_mhz,
        radio_climate,
        pol,
        pctTime,
        pctLoc,
        pctConf
    )

    print("area:")
    print(f"    dbloss: {dbloss}")
    print(f"    errnum: {errnum}")

    print("Program complete.\n")
