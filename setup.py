from setuptools import setup, find_packages

setup(
    name='Ylam',
    version='1.3.0',
    author='Cheshire',
    author_email='ladaganegra@gmail.com',
    description='Sistema de configuracion YAML',
    long_description=open('README.md').read(),
    license=open('LICENSE').read(),
    url='https://github.com/ladaganegra/Ylam.git',
    py_modules=['Ylam'],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=[
        'ruamel.yaml>=0.15',
        'Click'
    ]
)
