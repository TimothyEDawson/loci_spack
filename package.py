# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack.package import maintainers, license, version, depends_on, variant, patch


class Loci(AutotoolsPackage):
    """Loci is a sophisticated auto-parallelizing framework which simplifies
    the task of constructing complex simulation software.
    """

    homepage = "https://github.com/EdwardALuke/loci"
    url = "https://github.com/EdwardALuke/loci/archive/refs/tags/v4.1.b3.tar.gz"
    git = "https://github.com/EdwardALuke/loci.git"

    maintainers("EdwardALuke", "rlfontenot", "TimothyEDawson")

    license("LGPL-3.0-only", checked_by="TimothyEDawson")

    version("develop", branch="dev")
    version("stable", commit="751f8b365513ff1f2c5df3d3227f77c285c6f9e7")
    version("cfdrc", commit="d60697b69af801cd33066fa2bfbf0fc3af806d6e")
    version("4.1.b3", sha256="e49ceaf20dcc2d4ddf4f189644403ee3e63731ca92758902d48cb3a0a8636193")
    version("4.1.b2", sha256="4c1e98b30f96d0fb3d6d9cda29961e9b741d68373afe237fc0f2758260b9381c")
    version("4.1.b1", sha256="e56f525755600cf27de42c90ef97388f717da720674d6bf361ee9e612e519cd6")

    version("4.0.10", sha256="eba6cf7e133c05343da108ac9eed76d8b679effb51bebce31d7ef1917315ab42")
    version("4.0.9", sha256="7ca5d519f480c9b323f402a11445d0a068d69d3c10c9f87742d6e987ae724d5e")
    version("4.0.8a", sha256="5d3a2c5bbaa3808564d4b851344bd0de5e817292f3c9f3604e3e20c95ac26f55")
    version("4.0.8", sha256="b05749097994e7546a8cf9eb077125240bd1a582c055a328f48655c3d55f2f5d")
    version("4.0.7", sha256="1cdca827ff1980714989fd35a34f0aa4b3d3f1fd8668acb5e4f9b27cd2d3c15b")

    # Required dependencies
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("mpi", default=True, description="Enable MPI parallelism.")
    depends_on("mpi", when="+mpi")

    depends_on("hdf5")
    depends_on("hdf5 +mpi", when="+mpi")

    # Optional dependencies
    variant(
        "partitioner", default="parmetis", description="Mesh partitioning library.",
        values=("scotch", "parmetis", "space-filling"), multi=False,
        when="+mpi",
    )
    depends_on("parmetis", when="@:4.1.b3,develop +mpi partitioner=parmetis")
    depends_on("scotch+metis~threads", when="@develop +mpi partitioner=scotch")

    # Note: do not include superlu-dist as that has it's own link to parmetis's partioner, which will get loci confused
    variant("petsc", default=True, description="Enable PETSc linear solver.",)
    depends_on("petsc@:3.23.3~superlu-dist", when="+petsc")

    variant("cgns", default=False, description="Enable CGNS support.")
    depends_on("cgns", when="+cgns")

    # Patch to install directly into the prefix directory
    patch(
        "no_sub_dir.patch",
        sha256="11f510a72adfec7abe4d2651c9f721bee0d5b2e5dde56ea10f12f726c2e76256",
        when="@:4.1.b2",
    )

    # Configure script patch to fix issue with cmake-built HDF5:
    patch(
        "https://github.com/EdwardALuke/loci/commit/5f8408879a35c3f62bd91c9889511b9415c43fbf.patch",
        sha256="aebc95812e3285a99d172adbc71534fd35822063902348e60beddb52e20c92a9",
        when="@:4.1.b3",
    )

    # Extra arguments to pass to the configure script
    def configure_args(self):
        args = ["--no-sub-dir"]

        if not self.spec.satisfies("+mpi"):
            args.append("--nompi")

        if self.spec.satisfies("+cgns"):
            args.append(f"--with-cgns={self.spec['cgns'].prefix}")

        if self.spec.satisfies("partitioner=scotch"):
            args.append(f"--with-scotch={self.spec['scotch'].prefix}")
        return args

    def setup_run_environment(self, env):
        env.set("LOCI_BASE", self.prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("LOCI_BASE", self.prefix)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set("LOCI_BASE", self.prefix)
