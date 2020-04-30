from setuptools import find_namespace_packages, setup

packages = [package for package in find_namespace_packages(where='./src',
                                                           include='bq_fake_pii_table_creator.*')]

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

setup(
    name='bq-fake-pii-table-creator',
    version='0.0.4',
    author='Marcelo Costa',
    author_email='mesmacosta@gmail.com',
    description='Library for creating BQ tables with fake sensible data',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    platforms='Posix; MacOS X; Windows',
    packages=packages,
    package_dir={
        '': 'src'
    },
    entry_points={
        'console_scripts': [
            'bq-fake-pii-table-creator = bq_fake_pii_table_creator:main',
        ],
    },
    include_package_data=True,
    install_requires=(
        'pandas',
        'faker',
        'google-cloud-bigquery',
        'google-cloud-storage',
    ),
    setup_requires=(
        'pytest-runner',
    ),
    tests_require=(
        'pytest-cov',
    ),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
)
