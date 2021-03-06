from setuptools import setup, find_packages

setup(
    name='deepMerge',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'gensim',
        'BioPython',
        'h5py',
        'tqdm'
    ],
    entry_points='''
        [console_scripts]
        deepMerge=deepMerge.entry:cli
    ''',
)
