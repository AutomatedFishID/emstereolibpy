# EMStereoLibpy

Is a python wrapper for StereoLib by [SeaGIS](https://www.seagis.com.au/stereolib.html)

Allthough this python wrapper is free, StereoLib is not and requires a licence. StereoLib is not, cannot and mustnot be distributed with this Python module.

## How to run the tests

```bash
python test_emstereolibpy.py
```

## Example use 


```python 

import emstereolibpy as em 
from emstereolibpy import CameraID, Result

print(em.version())
print(em.licence_present())

```

To use StereoLib you must first load the camera files. 


```python
em.load_camera_file(CameraID.left, "Left.Cam")
em.load_camera_file(CameraID.right, "Right.Cam")
```

To find the intersecting 3D point from two 2D points in the left and right image.


```python 
pt_left = em.Pt2D(262.7, 259.5)
pt_right = em.Pt2D(248.5, 281.8)

print(f"Intersecting {pt_left} with {pt_right}")

r = em.intersect(pt_left, pt_right)
print(f"Intersect at : {r[0]}, with precision :  {r[1]} and rms : {r[2]}")
```

To find the point in an image from the 3D point in space

```python
pt_3d = em.Pt3D(-465.7601, 67.4796, -3180.4663)
pt_2d = em.image_coordinate(pt_3d, CameraID.left)
print(f"given {pt_3d} image coords are {pt_2d}")
```

To generate an epipolar line and return the results.
```python 
em.load_camera_file(CameraID.left, "Left.Cam")
em.load_camera_file(CameraID.right, "Right.Cam")

pt_image = em.Pt2D(262.7, 259.5)
em.generate_epipolar_line(CameraID.left, pt_image,
                          min_range=2000.0, max_range=8000.0,
                          n_points=em.max_epipolar_points())

for ii in range(em.max_epipolar_points()):
    new_pt_image = em.epipolarpolar_point(ii)
    print(f"Epipolar Point {ii} : {new_pt_image}")
```

To find the distance between two points given two points in the left image and the corresponding two points in the right image

```python 
ptl1 = em.Pt2D(251.6, 507.8)
ptl2 = em.Pt2D(452.9, 499.0)
ptr1 = em.Pt2D(228.6, 514.3)
ptr2 = em.Pt2D(425.5, 524.5)

l, sd = em.length(ptl1, ptl2, ptr1, ptr2)
print(f"Length {l} ({sd})")

# Numbers provided by Jim Seager
self.assertAlmostEqual(l, 899.5385, places=4)
self.assertAlmostEqual(sd, 6.4122, places=4)
```			
