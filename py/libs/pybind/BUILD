poetry_requirements(name="pybind")

python_sources(
    name="pybind0",
)

resource(name="pyproject", source="pyproject.toml")
resources(
    name="pybind_files",
    sources=[
        "README.rst",
        "VERSION",
        "MANIFEST.in",
        "pybind/cnufft/*",
        "pybind/cnufft/src/*",
    ],
)

python_distribution(
    name="pybind_dist",
    dependencies=[
        ":pyproject",
        ":pybind_files",
        "py/libs/pybind/setup.py:pybind0",
    ],
    provides=python_artifact(
        name="pybind",
        version="0.2.1",
    ),
    wheel_config_settings={"--global-option": ["--python-tag", "py37.py38.py39"]},
    generate_setup=False,
)
