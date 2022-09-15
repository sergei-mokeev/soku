from setuptools import setup, find_packages


setup(
    name='soku',
    version='3.0.0',
    author='Sergey Mokeyev',
    author_email='sergey.mokeyev@gmail.com',
    description='Template for microservices',
    url='https://github.com/SergeyMokeyev/soku',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ],
    install_requires=[
        'aiohttp>=3.8.1,<4'
    ]
)
