import setuptools


setuptools.setup(
    name='soku',
    version='2.0.2',
    author='Sergey Mokeyev',
    author_email='sergey.mokeyev@gmail.com',
    description='Serialize and deserialize python object to JSON and back',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SergeyMokeyev/soku',
    data_files=[
        ('README.md', ['README.md'])
    ],
    packages=[
        'soku'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ],
    install_requires=[]
)
