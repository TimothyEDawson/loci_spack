# Spack Package for Loci
An experimental spack package for the Loci framework: https://github.com/EdwardALuke/loci

## Setup:

First, create a local spack repository following the instructions here:
https://spack.readthedocs.io/en/latest/repositories.html

```terminal
spack repo create ~/my_spack_repos
spack repo add ~/my_spack_repos
```

Next, clone this repository into the `packages` subdirectory:

```terminal
git clone https://github.com/TimothyEDawson/loci_spack.git ~/my_spack_repos/packages/loci
```

And you're good to go!

## Usage:

You can view the available installation options with:

```terminal
spack info loci
```

For example, you can install the latest release without PETSc (-petsc) with:

```terminal
spack install loci -petsc
```

Install from a specific tag with recommended options:

```terminal
spack install loci@4.0.10
```

Or the latest development version directly from the Git repository:

```terminal
spack install loci@develop
```

## Updating:

As this repository is updated, you only need to pull the latest version using Git:

```terminal
cd ~/my_spack_repos/packages/loci
git pull
```

