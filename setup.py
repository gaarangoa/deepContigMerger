from setuptools import setup, find_packages

setup(
    name='deepMerge',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click==6.7',
    ],
    entry_points='''
        [console_scripts]
        deepMerge=embeddings.main:process
        deepMerge_embeddings=embeddings.main:process
    ''',
)
