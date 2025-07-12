# -*- coding: utf-8 -*-
"""Python wrapper for C-ITM.dll.

This wrapper is designed to work with ITM v1.2.2 which is written in C.


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


# %% C-ITM
class C_ITM:
    """Python wrapper class for ITM v1.2.2: C-ITM.dll.

    This class allows the use of C-ITM.dll functions from Python through a
    ctypes interface. This class necessarily requires the C-ITM.dll to be in the
    default repository location or a specified location. C-ITM.dll must be
    compiled for a 64-bit operating system.

    C-ITM.dll function are directly linked with "dll_" prepended to their names
    and can be called directly from this wrapper. Their function signatures are
    identical to the C-ITM.dll function signatures.

    Additional wrapper functions for the dll_* functions are provided which
    handle the creation, passing, and parsing of the ctypes arguments. This is
    particularly convenient for input/output arguments.

    This wrapper class is instantiated with the file path (dll_path) to
    C-ITM.dll. If no file path is provided, the default relative path to this
    repository's compiled C-ITM.dll is searched.

    Usage
    -----
    citm = C_ITM()
    """

    # %% __init__
    def __init__(
        self,
        dll_path: str = None
    ):
        """Initialize C-ITM.dll wrapper.

        Construct attributes for the C_ITM class by interfacing with
        the supplied C-ITM.dll file.

        If no dll_path is given, the default path is searched.
        If the .dll is not found on the default path, an error is given.

        Parameters
        ----------
        dll_path : str, optional (default=None)
            The file path of the 64-bit C-ITM.dll to use.
            If dll_path is not provided, the default repository location is
            searched.
        """
        default_dll_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                r"..\..\..",
                r"itm-longley-rice-dev\Visual_Studio\C-ITM",
                r"x64\Release",
                r"C-ITM.dll"
            )
        )
        if dll_path is None:
            # Try the default C-ITM.dll repository location.
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

        # Get the .dll version.
        self.dll_version = getattr(
            self.DLL,
            'ITMDLLVersion'
        )
        self.dll_version.argtypes = None
        self.dll_version.restype = ct.c_double
        self.dll_version = self.dll_version()

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

    # %% __exit__
    def __exit__(
        self,
        exc_type,
        exc_value,
        exc_traceback
    ):
        """Close the .dll."""
        ct.windll.kernel32.FreeLibrary(self.MKEDLL._handle)

    # %% version
    def version(
        self,
    ):
        """Return the C-ITM.dll version number."""
        return self.dll_version

    # %% print_version
    def print_version(
        self,
    ):
        """Print C-ITM Library version information."""
        print((
            "**** C-ITM Library **********************************\n"
            f"    .dll Version:      {self.version()}\n"
            f"*****************************************************"
        ))

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
        """ITM Point-to-Point mode."""
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
            ctype_errnum
        )

        dbloss = ctype_dbloss.value
        strmode = ctype_strmode.value.decode('utf-8')
        errnum = ctype_errnum.value

        return dbloss, strmode, errnum


# %% Run program.
if __name__ == "__main__":
    print("Running program: " + os.path.basename(__file__))

    citm = C_ITM()
    citm.print_version()

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

    dbloss, strmode, errnum = citm.point_to_point(
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

    print(f"dbloss: {dbloss}")
    print(f"strmode: {strmode}")
    print(f"errnum: {errnum}")

    print("Program complete.\n")
