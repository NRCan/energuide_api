import setuptools


setuptools.setup(
    name='energuide-etl',
    version='0.0.1',
    long_description='',
    author='CDS-SNC',
    url='https://github.com/cds-snc/nrcan_api',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    entry_points='''
        [console_scripts]
        energuide=energuide.cli:main
    '''
)
