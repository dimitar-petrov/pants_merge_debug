poetry_requirements(name="nufft")

python_sources(name="nufft0")

resource(name="pyproject", source="pyproject.toml")
resources(
    name="nufft_files",
    sources=[
        "README.rst",
        "LICENSE",
        "MANIFEST.in",
        "src/nufft/*",
        "nufft/nufft.pyf",
    ],
)

python_distribution(
    name="nufft_dist",
    dependencies=[
        ":pyproject",
        ":nufft_files",
        "py/libs/nufft/setup.py:nufft0",
    ],
    provides=python_artifact(
        name="nufft",
        version="0.0.3",
    ),
    wheel_config_settings={"--global-option": ["--python-tag", "py37.py38.py39"]},
    generate_setup=False,
)
