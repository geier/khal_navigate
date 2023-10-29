#!/usr/bin/env python3

from setuptools import setup

requirements = [
    'khal',
]

setup(
    name='khal-navigate',
    description='A khal plugin showing how to add new commands',
    author='khal contributors',
    author_email='khal@lostpackets.de',
    url='http://lostpackets.de/khal/',
    license='Expat/MIT',
    entry_points={
        "khal.commands": [
            'navigate = khal_navigate.navigate:knavigate'
        ]
    },
)
