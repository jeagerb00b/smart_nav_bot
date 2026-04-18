import os
from glob import glob
from setuptools import setup

package_name = 'smart_navigator'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'data'), glob('data/*.csv')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='developer',
    maintainer_email='dev@todo.com',
    description='TurtleBot3 Smart Room Navigator using a Decision Tree ML model and Nav2',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'input_node = smart_navigator.input_node:main',
            'decision_node = smart_navigator.decision_node:main',
            'navigator_node = smart_navigator.navigator_node:main',
        ],
    },
)
