from setuptools import setup, find_packages

setup(
    name='deepMerge',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'gensim',
        'BioPython'
    ],
    entry_points='''
        [console_scripts]
        dmerge=deepMerge.main:process
        dmerge_embeddings=deepMerge.main:process
    ''',
)
