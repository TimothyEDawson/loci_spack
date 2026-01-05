# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage
from spack.package import maintainers, license, version, depends_on, variant, patch


class Loci(AutotoolsPackage):
    """Loci is a sophisticated auto-parallelizing framework which simplifies
    the task of constructing complex simulation software.
    """
    install_targets = ["install_minimal"]

    homepage = "https://github.com/EdwardALuke/loci"
    url = "https://github.com/EdwardALuke/loci/archive/refs/tags/v4.1.1.tar.gz"
    git = "https://github.com/EdwardALuke/loci.git"

    maintainers("EdwardALuke", "rlfontenot", "TimothyEDawson")

    license("LGPL-3.0-only", checked_by="TimothyEDawson")

    version("develop", branch="dev", get_full_repo=True)
    version("cfdrc", commit="d60697b69af801cd33066fa2bfbf0fc3af806d6e", get_full_repo=True)

    version("4.1.1", commit="a5779277b742256f69cd8c4995073e191457dcce", get_full_repo=True)
    version("4.1.0", commit="3fa07bba1cae26c887d5dcbde80619e1871156b1", get_full_repo=True)
    version("4.1.b3-s08-22-2025", tag="v4.1.s08-22-2025", commit="0977369206a84e8ae4989708cc7f6d5798a46ab5", get_full_repo=True)
    version("4.1.b3", commit="151890a037480cec683f9fb0237e0cc9fa819fa7", get_full_repo=True)
    version("4.1.b2", commit="fff611f8f817b4b36e76d7f99354fb6cb16a8988", get_full_repo=True)
    version("4.1.b1", commit="ada069a4945825342fdeff160422751e7bcc614a", get_full_repo=True)

    version("4.0.10", sha256="eba6cf7e133c05343da108ac9eed76d8b679effb51bebce31d7ef1917315ab42")
    version("4.0.9", sha256="7ca5d519f480c9b323f402a11445d0a068d69d3c10c9f87742d6e987ae724d5e")
    version("4.0.8a", sha256="5d3a2c5bbaa3808564d4b851344bd0de5e817292f3c9f3604e3e20c95ac26f55")
    version("4.0.8", sha256="b05749097994e7546a8cf9eb077125240bd1a582c055a328f48655c3d55f2f5d")
    version("4.0.7", sha256="1cdca827ff1980714989fd35a34f0aa4b3d3f1fd8668acb5e4f9b27cd2d3c15b")

    # Enable debug build
    variant("debug", default=False, description="Enable debugging options (includes bounds checking).")

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
    depends_on("parmetis", when="partitioner=parmetis")
    depends_on("scotch+metis~threads", when="@4.1.b3: partitioner=scotch")

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

        # Select compiler configuration
        if self.spec.satisfies("%c=gcc"):
            args.append(f"--compiler=gcc")
        elif self.spec.satisfies("%c=clang"):
            args.append(f"--compiler=llvm")
        elif self.spec.satisfies("%c=icc"):
            args.append(f"--compiler=icc")

        if self.spec.satisfies("+debug"):
            args.append(f"--bounds-check")

        if not self.spec.satisfies("+mpi"):
            args.append("--nompi")

        if self.spec.satisfies("+cgns"):
            args.append(f"--with-cgns={self.spec['cgns'].prefix}")

        if self.spec.satisfies("partitioner=scotch"):
            args.append(f"--with-scotch={self.spec['scotch'].prefix}")
        elif self.spec.satisfies("partitioner=parmetis"):
            args.append(f"--with-metis={self.spec['metis'].prefix}")
            args.append(f"--with-parmetis={self.spec['parmetis'].prefix}")

        return args

    def setup_build_environment(self, env):
        if self.spec.satisfies("+debug"):
            env.set("LOCI_DEBUG", "0")

    def setup_run_environment(self, env):
        env.set("LOCI_BASE", self.prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("LOCI_BASE", self.prefix)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set("LOCI_BASE", self.prefix)
