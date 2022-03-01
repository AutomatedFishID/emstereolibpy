import unittest
import emstereolibpy as em
from emstereolibpy import CameraID, Result


class TestEmstereolibpy(unittest.TestCase):

    def test_version(self):
        r = em.version()
        self.assertTupleEqual(r, (1, 0))

    def test_licence_pressent(self):
        self.assertTrue(True, em.licence_present())

    def test_load_camera_file(self):
        r = em.load_camera_file(CameraID.left, 'Left.Cam')
        self.assertEqual(r, Result.ok)
        r = em.load_camera_file(CameraID.right, 'Right.Cam')
        self.assertEqual(r, Result.ok)

    def test_camera_file(self):
        r = em.load_camera_file(CameraID.left, 'Left.Cam')
        cam_string = em.camera_file(CameraID.left)
        self.assertIsInstance(cam_string, str)
        # self.assertEqual(cam_string, b'Left.Cam')
        print(f"camera file : {cam_string}")

    def test_camera_name(self):
        r = em.load_camera_file(CameraID.left, 'Left.Cam')
        cam_name = em.camera_name(CameraID.left)
        self.assertIsInstance(cam_name, str)
        print(f"Camera name {cam_name}")

    def test_camera_format(self):
        r = em.load_camera_file(CameraID.left, 'Left.Cam')
        form = em.camera_format(CameraID.left)
        self.assertTupleEqual(form, (576, 720))

    def test_get_units(self):
        em.load_camera_file(CameraID.left, 'Left.Cam')
        r = em.get_units()
        print(f"Units are : {r}")
        self.assertIsInstance(r.decode(), str)

    def test_set_get_image_measurement_sd(self):
        em.load_camera_file(CameraID.left, 'Left.Cam')
        sd = 1.0
        print(f"Setting SD to {sd}")
        em.set_image_measurement_sd(sd)
        new_sd = em.image_measurement_sd()
        self.assertEqual(new_sd, sd)
        sd = 10
        print(f"Setting SD to {sd}")
        em.set_image_measurement_sd(sd)
        new_sd = em.image_measurement_sd()
        self.assertEqual(new_sd, sd)

    def test_image_measurement_sdmin(self):
        em.load_camera_file(CameraID.left, "Left.Cam")
        sd = em.image_measurement_sdmin()
        print(f"Minimum SD : {sd}")
        self.assertEqual(sd, 0.01)

    def test_image_measurement_sdmax(self):
        em.load_camera_file(CameraID.left, "Left.Cam")
        sd = em.image_measurement_sdmax()
        print(f"Maximum SD : {sd}")
        self.assertEqual(sd, 10)

    def test_intersect(self):
        em.load_camera_file(CameraID.left, "Left.Cam")
        em.load_camera_file(CameraID.right, "Right.Cam")
        pt_left = em.Pt2D(262.7, 259.5)
        pt_right = em.Pt2D(248.5, 281.8)
        print(f"Intersecting {pt_left} with {pt_right}")

        r = em.intersect(pt_left, pt_right)
        print(f"Intersect at : {r[0]}, with precision :  {r[1]} and rms : {r[2]}")

        # Numbers provided by Jim Seager
        self.assertAlmostEqual(r[2], 2.4300, places=4)
        self.assertAlmostEqual(r[0].x, -465.7601, places=4)
        self.assertAlmostEqual(r[0].y, 67.4796, places=4)
        self.assertAlmostEqual(r[0].z, -3180.4663, places=4)
        self.assertAlmostEqual(r[1].x, 4.7347, places=4)
        self.assertAlmostEqual(r[1].y, 2.9855, places=4)
        self.assertAlmostEqual(r[1].z, 25.5829, places=4)

    def test_length(self):
        ptl1 = em.Pt2D(251.6, 507.8)
        ptl2 = em.Pt2D(452.9, 499.0)
        ptr1 = em.Pt2D(228.6, 514.3)
        ptr2 = em.Pt2D(425.5, 524.5)

        l, sd = em.length(ptl1, ptl2, ptr1, ptr2)
        print(f"Length {l} ({sd})")

        # Numbers provided by Jim Seager
        self.assertAlmostEqual(l, 899.5385, places=4)
        self.assertAlmostEqual(sd, 6.4122, places=4)

    def test_image_coordinates(self):
        pt_3d = em.Pt3D(-465.7601, 67.4796, -3180.4663)
        pt_2d = em.image_coordinate(pt_3d, CameraID.left)
        print(f"given {pt_3d} image coords are {pt_2d}")

        # Numbers provided by Jim Seager
        self.assertAlmostEqual(pt_2d.x, 262.6944, places=4)
        self.assertAlmostEqual(pt_2d.y, 258.9346, places=4)

    def test_max_epipolar_points(self):
        mepp = em.max_epipolar_points()
        print(f"Max epipolar points {mepp}")
        self.assertEqual(mepp, 100)

    def test_generate_epipolar_line(self):
        pt_image = em.Pt2D(262.7, 259.5)
        em.generate_epipolar_line(CameraID.left, pt_image,
                                  min_range=2000.0, max_range=8000.0,
                                  n_points=em.max_epipolar_points())

    def test_epipolar_point(self):
        em.load_camera_file(CameraID.left, "Left.Cam")
        em.load_camera_file(CameraID.right, "Right.Cam")

        pt_image = em.Pt2D(262.7, 259.5)
        em.generate_epipolar_line(CameraID.left, pt_image,
                                  min_range=2000.0, max_range=8000.0,
                                  n_points=em.max_epipolar_points())

        for ii in range(em.max_epipolar_points()):
            new_pt_image = em.epipolarpolar_point(ii)
            print(f"Epipolar Point {ii} : {new_pt_image}")

    def test_em_load_data(self):
        filename = 'Test.EMObs'
        self.assertTrue(em.em_load_data(filename))

    def test_em_measurement_count(self):
        filename = 'Test.EMObs'
        em.em_load_data(filename)
        counts = em.em_measurement_count()
        self.assertTupleEqual(counts, (31, 4, 2, 21, 1))
        print(f"Found {counts} counts" )

    def test_em_measurement_count_fgs(self):
        filename = 'Test.EMObs'
        em.em_load_data(filename)
        counts = em.em_measurement_count()
        family = "nemipteridae"
        genus = "*"
        species = "*"

        fgs_counts = em.em_measurement_count_fgs(family, genus, species)

        print(f"Found {fgs_counts[0:3]} F/G/S counts")
        print(f"Point ({fgs_counts[3]}) : BBox ({fgs_counts[4]}) : 3D Point ({fgs_counts[5]}) : Length ({fgs_counts[6]}) : "
              f"Compound Length ({fgs_counts[7]})")

        species = "FURCOSUS"
        family = "*"
        # species = "*"

        fgs_counts = em.em_measurement_count_fgs(family, genus, species)

        print(f"Found {fgs_counts[0:3]} F/G/S counts")
        print(
            f"Point ({fgs_counts[3]}) : BBox ({fgs_counts[4]}) : 3D Point ({fgs_counts[5]}) : Length ({fgs_counts[6]}) : "
            f"Compound Length ({fgs_counts[7]})")

    def test_em_to_text(self):

        em.em_load_data('Test.EMObs')
        em.em_to_text('python_test.csv')

    def test_em_unique_fgs(self):
        filename = 'Test.EMObs'
        em.em_load_data(filename)

        num_fish = em.em_unique_fgs()
        print(f"Number of unique F/G/S {num_fish}")
        self.assertEqual(num_fish, 6)

    def test_em_get_unique_fgs(self):

        filename = 'Test.EMObs'
        em.em_load_data(filename)
        num_fish = em.em_unique_fgs()

        print(f'Test.EMObs has {num_fish} unique family, genus, species combinations')

        for ii in range(num_fish):
            ret = em.em_get_unique_fgs(int(ii))
            print(f" {ii}: {ret[0].decode(encoding='UTF-8')}, {ret[1].decode(encoding='UTF8')}, {ret[2].decode(encoding='UTF-8')}")


if __name__ == '__main__':
    unittest.main()
