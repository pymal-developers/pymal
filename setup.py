from setuptools import setup


# Dynamically calculate the version based on pymal.VERSION.
version = __import__('pymal').get_version()


setup(
    name='pymal',
    packages=['pymal'],
    version=version,
    description='A pythonapi for the website MyAnimeList (or MAL).',
    author='pymal-developers',
    license = "BSD",
    url='https://bitbucket.org/pymal-developers/pymal/',
    keywords=["MyAnimeList", "MAL", "pymal"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Natural Language :: Japanese',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
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

)
