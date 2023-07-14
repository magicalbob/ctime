import setuptools

setuptools.setup(
    name="ctime-package",
    version="2.1",
    packages=setuptools.find_packages(exclude=["docker", "images", "sounds", "selenium"]),
    zip_safe=True,
)
