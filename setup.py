from setuptools import setup, find_packages

setup(
    name='deepMerge',
    version='0.1',
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    include_package_data=False,
    install_requires=[
        'Click',
        'gensim',
        'BioPython',
        'h5py',
        'tqdm'
    ],
    entry_points='''
        [console_scripts]
        nuc2vec=deepMerge.entry:cli
    ''',
)
