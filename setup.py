from setuptools import setup, find_packages
from pip.req import parse_requirements


# Dynamically calculate the version based on pymal.__version__.
version = __import__('pymal').__version__

# Dynamically calculate the license based on pymal.__license__.
license = __import__('pymal').__license__

# Dynamically calculate the authors based on pymal.__authors__.
authors = __import__('pymal').__authors__

requirements_path = 'requirements.txt'

description = 'A python api for the website MyAnimeList (or MAL).'

setup(
    name='pymal',
    packages=find_packages(exclude=['tests*']),
    version=version,
    description=description,
    long_description=description,
    author=authors,
    license=license,
    url='https://github.com/tomerghelber/pymal',
    keywords=[
        "MyAnimeList", "myanimelist",
        "MAL", "mal",
        "pymal",
        "my anime list", "anime list", "anime"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Natural Language :: Japanese',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Topic :: Home Automation',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
    ],

    # Dynamically calculate the install_requires based on requirements_path.
    install_requires=[str(ir.req) for ir in parse_requirements(requirements_path)],
)
