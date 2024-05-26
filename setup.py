from setuptools import find_packages, setup

with open('README.md', mode='r', encoding='utf8') as f:
    long_description = f.read()

requirements = []
with open('requirements.txt', 'r') as fd:
    for line in fd:
        line.strip()
        if line and not line.startswith("#"):
            requirements.append(line)


setup(
    name='malmoext',
    description='A wrapper for Microsoft\'s Malmo Platform capable of creating automated agent action sequences in Minecraft.',
    long_description=long_description,
    license='MIT License',
    url='https://github.com/NateRex/malmoext',
    version='0.36.0.0.1',
    author='Nate Rex',
    maintainer='Nate Rex',
    install_requires=requirements,
    keywords=['malmoext'],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)