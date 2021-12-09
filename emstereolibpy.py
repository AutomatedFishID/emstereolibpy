"""
Abstraction library for libStereoLibLX.so from SeaGIS.

Requires a licence to use, this is just a python wrapping function
"""

import ctypes
from enum import IntEnum, auto
from typing import Tuple

BUFF = 2048

libc = ctypes.CDLL('./libStereoLibLX.so')


class CameraID(IntEnum):
    """
    Identifies which camera is loaded
    """
    left = 0
    right = auto()


class Result(IntEnum):
    """
    libStereoLibLX returns result codes.  This enumerates the codes.
    """
    ok = 0
    invalid_left_camera = auto()
    invalid_right_camera = auto()
    invalid_camera = auto()
    data_range_error = auto()
    failed = auto()
    invalid_licence = auto()
    camera_file_not_permitted = auto()
    buffer_too_small = auto()


class Pt2D(ctypes.Structure):
    """
    Point structures used by LibStereoLibLX
    """
    _fields_ = [
        ('x', ctypes.c_double),
        ('y', ctypes.c_double)
    ]

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Pt3D(ctypes.Structure):
    """
    Point structures used by LibStereoLibLX
    """
    _fields_ = [
        ('x', ctypes.c_double),
        ('y', ctypes.c_double),
        ('z', ctypes.c_double)
    ]

    def __init__(self, x, y, z):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"


def version() -> tuple[int, int]:
    """
    Return the version number of libStereoLibLX

    :return: (major, minor)
    """

    pminor = ctypes.POINTER(ctypes.c_int)
    pmajor = ctypes.POINTER(ctypes.c_int)
    libc.Version.argtypes = [pminor, pmajor]

    minor = ctypes.c_int(0)
    major = ctypes.c_int(0)

    libc.Version(major, minor)

    return major.value, minor.value


def licence_present() -> bool:
    """
    Checks to see if there is a valid licence present
    :return:
    """
    r = libc.LicencePresent()

    return True if r == 0 else False


def load_camera_file(cam: CameraID, filename: str) -> Result:
    """
    Load the camera files into memory
    :param cam: left or right
    :param filename: path to the camera file
    :return: Execution result
    """
    return libc.LoadCameraFile(cam, bytes(filename, 'UTF-8'))


def camera_file(cam: CameraID) -> str:
    """
    Returns the file loaded into memory
    :param cam:
    :return:
    """
    p_buff = ctypes.create_string_buffer(b"", BUFF)
    libc.GetCameraFile(cam, p_buff)
    return str(p_buff.value)


def camera_name(cam: CameraID) -> str:
    """
    Return the name of the camera that is loaded
    :param cam:
    :return:
    """
    p_buff = ctypes.create_string_buffer(b"", BUFF)
    libc.GetCameraName(cam, p_buff)
    return str(p_buff.value)


def camera_format(cam: CameraID) -> tuple[int, int]:
    """
    Returns the camera number of rows and columns
    :param cam:
    :return: (nrows, ncols)
    """
    nrows = ctypes.c_int(0)
    ncols = ctypes.c_int(0)

    r = libc.GetCameraFormat(cam, ctypes.byref(nrows), ctypes.byref(ncols))
    return nrows.value, ncols.value


def get_units() -> str:
    """
    return the phycical units of the loaded camera
    :return:
    """
    p_buff = ctypes.create_string_buffer(b"", BUFF)
    r = libc.GetUnits(p_buff, BUFF)
    return p_buff.value


def set_image_measurement_sd(value: float) -> None:
    """
    Set the precision
    :param value:
    :return:
    """
    libc.SetImageMeasurementSD(ctypes.c_double(value))


def image_measurement_sd() -> float:
    """
    return the currently set value of precision
    :return:
    """
    libc.GetImageMeasurementSD.restype = ctypes.c_double
    return libc.GetImageMeasurementSD()


def image_measurement_sdmin() -> float:
    """
    Return the minimum precision
    :return:
    """
    libc.GetImageMeasurementSDMin.restype = ctypes.c_double
    return libc.GetImageMeasurementSDMin()


def image_measurement_sdmax() -> float:
    """
    Return the maximum precision
    :return:
    """
    libc.GetImageMeasurementSDMax.restype = ctypes.c_double
    return libc.GetImageMeasurementSDMax()


def intersect(pt_left: Pt2D, pt_right: Pt2D) -> tuple[Pt3D, Pt3D, float]:
    """
    Given to Points in left and right images, find the intersection point in 3DSpace
    :param pt_left:
    :param pt_right:
    :return:
    """
    libc.Intersect.argtypes = [Pt2D, Pt2D, ctypes.POINTER(Pt3D), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(Pt3D)]
    pt_3D = Pt3D(0, 0, 0)
    pt_prec = Pt3D(0, 0, 0)
    drms = ctypes.c_double()
    r = libc.Intersect(pt_left, pt_right, ctypes.byref(pt_3D), ctypes.byref(drms), ctypes.byref(pt_prec))

    return pt_3D, pt_prec, drms.value


def length(l1, l2, r1, r2):
    """
    Given two points in the left image and two points in the right image.  Returns the distance between the two
    :param l1: Point 1 in the left image
    :param l2: Point 2 in the left image
    :param r1: Point 1 in the right image
    :param r2: Point 2 in the right image
    :return:
    """
    drms = ctypes.c_double(0.0)
    pt1_prec = Pt3D(0, 0, 0)
    pt2_prec = Pt3D(0, 0, 0)
    pt_1 = Pt3D(0, 0, 0)
    pt_2 = Pt3D(0, 0, 0)
    sd = ctypes.c_double(0.0)
    dlength = ctypes.c_double(0.0)

    libc.Distance.restype = ctypes.c_double

    try:
        libc.Intersect(l1, r1, ctypes.byref(pt_1), ctypes.byref(drms), ctypes.byref(pt1_prec))
        libc.Intersect(l2, r2, ctypes.byref(pt_2), ctypes.byref(drms), ctypes.byref(pt2_prec))
    except Exception as e:
        print("Length calculation, failed to compute end point coordinates")
        print(f"Exception : {e}")

    _length = libc.Distance(pt_1, pt2_prec, pt_2, pt2_prec, ctypes.byref(sd))

    return _length, sd.value


def image_coordinate(pt_3d: Pt3D, cam: CameraID) -> Pt2D:
    """
    Given a 3D point in space.  Return the 2d point in the image
    :param pt_3d:
    :param cam:
    :param pt_img:
    :return:
    """
    pt_image = Pt2D(0, 0)
    res = libc.ImageCoordinate(pt_3d, cam, ctypes.byref(pt_image))

    return pt_image


def max_epipolar_points() -> int:
    """
    Return the maximum number of points in an epipolar line
    :return:
    """
    return libc.MaxEpipolarPoints()


def generate_epipolar_line(cam: CameraID, pt_image: Pt2D,
                           min_range: float = 2000.0, max_range: float = 8000.0,
                           n_points: int = 100) -> Result:
    """
    Given a point in one image [left].  Generate an epipolar line in the other [right].
    :param cam:
    :param pt_image:
    :param min_range:
    :param max_range:
    :param n_points:
    :return:
    """
    r = libc.GenerateEpipolarLine(cam.left, pt_image,
                                  ctypes.c_double(min_range), ctypes.c_double(max_range),
                                  ctypes.c_int(n_points))


def epipolarpolar_point(item: int) -> Pt2D:
    """
    Return epipolar points from epiploar line
    :param item:
    :return: 2D point
    """
    pt_image = Pt2D(1, 0)

    res = libc.GetEpipolarPoint(item, ctypes.byref(pt_image))

    return pt_image

