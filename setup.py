from setuptools import setup, find_packages
import re

required = [l.strip() for l in
            open('requirements.txt') if re.match('^[A-Za-z]', l)]

setup(
    name='api',
    version='1.0.0',
    description='sample api to show off deployment pipeline',
    url='https://github.com/srleyva/sample_api',
    author='Stephen Leyva',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='rest restful api flask swagger openapi flask-restplus',

    packages=find_packages(),

    install_requires=required,
    entry_points={'console_scripts': ['job_api=api:app.main']}
    )
