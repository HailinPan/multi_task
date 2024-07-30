from setuptools import setup


def read_requirements(path):
    with open(path, "r") as f:
        return [line.strip() for line in f if not line.isspace()]


with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

exec(open('multi_task/version.py').read())

setup(
    name="multi_task",
    version=__version__,
    python_requires=">=3.8",
    install_requires=read_requirements("requirements.txt"),
    packages=["multi_task"],
    author="Hailin Pan",
    author_email="panhailin@genomics.cn",
    description="multi_task",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD 2-Clause License",
    url="https://github.com/HailinPan/multi_task.git",
)