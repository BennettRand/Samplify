from setuptools import setup, find_packages

setup(name="samplify",
	version="0.1.1",
	url="http://github.com/BennettRand/Samplify/",
	description="Take, save, and manipulate objects that store both maginitude and measurement information.",
	author="Bennett Rand",
	author_email="bennett.h.rand@gmail.com",
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Topic :: Utilities",
		"Operating System :: OS Independent"
	],
	packages=find_packages(),
	install_requires=[],
	license="MIT",
	platforms=["Linux", "Win"]
)
