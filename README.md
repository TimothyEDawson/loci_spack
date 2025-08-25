An experimental spack package for the Loci framework: https://github.com/EdwardALuke/loci

# Setup:
First [obtain Spack](https://spack.readthedocs.io/en/v0.21.3/getting_started.html#installation)
and source the activation script:

```bash
git clone -c feature.manyFiles=true https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
```

Second, run `spack list` to pull down the built-in repositories. Next,
have Spack search your system for compilers and other software it can
reuse. Make sure any software you want it to find is on your path:

```bash
spack compiler find
spack external find
```

Next, [create a local spack repository](https://spack.readthedocs.io/en/latest/repositories.html):

```bash
spack repo create ~/. personal
spack repo add ~/spack_repo/personal
```

Finally, clone this repository into the `packages` subdirectory:

```bash
git clone https://github.com/TimothyEDawson/loci_spack.git ~/spack_repo/personal/packages/loci
```

And you're good to go! You can verify that Spack is able to find the package with
`spack info loci`.

## Note for Python:
I generally recommend installing your own Python version so that Spack will
use that instead of the older system-installed version, making sure it's on
your path and running `spack external find` again. This should add lines like:

```yaml
packages:
  python:
    externals:
    - spec: python@3.12.9+bz2+crypt+ctypes+dbm+lzma+pyexpat+pythoncmd+readline+sqlite3+ssl+tix+tkinter+uuid+zlib
      prefix: /p/home/tdawson/miniforge3
```

to your `~/.spack/packages.yaml` file. Previously I would point people to
[miniforge](https://github.com/conda-forge/miniforge) as the easiest option for
managing your Python installations, but nowadays I point people to
[uv](https://docs.astral.sh/uv/) instead.

# Basic usage:
You can view the available installation options with:

```bash
spack info loci
```

For example, you can install the latest release without PETSc (-petsc) with:

```bash
spack install loci -petsc
```

Install from a specific tag with recommended options:

```bash
spack install loci@4.0.10
```

Or the latest development version directly from the Git repository:

```bash
spack install loci@develop
```

You can then add Loci to your environment variables with:

```bash
spack load loci
```

# Environment Setup (Recommended)
I recommend utilizing Spack environments to manage your Spack installations.
To create and activate an environment called "loci", execute:

```bash
spack env create loci
spack env activate -p loci
```

Where the `-p` option will prepend the terminal with the name of the activated
environment (highly recommended). To deactivate an active environment, run:

```bash
despacktivate
```

With the environment active, you will need to manually `add` specs before you
will be able to install them. It is also recommended to manually `concretize`
the specs before installation, which performs the dependency analysis and shows
which packages will be installed and which already-installed packages will be
reused.

```bash
spack add loci@develop
spack concretize
```

You can now install the requested packages via `spack install`. If you did not
manually concretize, it will automatically concretize when you install.

# Updating the Spack repo:
As this repository is updated, you only need to pull the latest version using Git:

```bash
cd ~/spack_repo/personal/packages/loci
git pull
```

# Developing
In order to utilize Spack while actively developing for Loci you can follow
the instructions for creating an environment, adding the `spack develop`
command before concretizing:

```bash
spack add loci@develop
spack develop loci@develop
spack concretize
```

By adding these commands, Spack will clone the specified packages into the
environment directory instead of a temporary directory, and use these
directories as-is during the build and install process. Thus the developer
may `cd` into these directories and make changes to the source code before
executing `spack install`.

To enter the directories, use the convenience function to enter the
environment directory and then `cd` into the code directory:

```bash
spack cd -e
cd loci
```


