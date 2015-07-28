import numpy as np
from ahoy import mesh
import test


class TestUniformMesh1D(test.TestBase):
    dim = 1
    L = np.array([1.8])
    dx = np.array([0.1])

    def test_uniform_mesh(self):
        msh = mesh.uniform_mesh_factory(self.L, self.dx)
        for i_dim in range(self.dim):
            self.assertTrue(msh.cellCenters[i_dim, :].value.max() <
                            self.L[i_dim] / 2.0)
            self.assertTrue(msh.cellCenters[i_dim, :].value.min() >
                            -self.L[i_dim] / 2.0)


class TestUniformMesh2D(TestUniformMesh1D):
    dim = 2
    L = np.array([1.7, 3.0])
    dx = np.array([0.1, 0.2])


class TestSingleSphereMesh(test.TestBase):

    def test_single_sphere_random_seeding(self):
        L = np.array([2.0, 2.0])
        R = 0.1
        dx = 0.1

        np.random.seed(2)
        mesh_1 = mesh.single_sphere_mesh_factory(np.zeros_like(L), R, dx, L)

        np.random.seed(3)
        mesh_2 = mesh.single_sphere_mesh_factory(np.zeros_like(L), R, dx, L)

        self.assertTrue(np.allclose(mesh_1.cellCenters.value,
                                    mesh_2.cellCenters.value))
