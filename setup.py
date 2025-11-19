"""Setup script for EchoLayerApp."""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='echolayerapp',
    version='1.0.0',
    author='EchoLayerApp Team',
    description='Ultrasonic overlay latency benchmark tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/KingofLumena/EchoLayerApp',
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'echolayerapp=echolayerapp.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
)
