from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()
packages = find_packages(exclude=["tests?", "*.tests*", "*.tests*.*", "tests*.*", 'pypi_publish.py'])
setup_args = dict(name='django_home_assignment',
                  # https://packaging.python.org/tutorials/packaging-projects/
                  version='1.0.0',
                  description='',
                  long_description=long_description,
                  long_description_content_type="text/markdown",
                  license='MIT',
                  author='Gilad Barnea',
                  author_email='giladbrn@gmail.com',
                  url='https://github.com/giladbarnea/https://github.com/giladbarnea/django_home_assignment.git',
                  packages=packages,
                  keywords=[],
                  install_requires=[
                      "Django==3.1.4",
                      "django-heroku==0.3.1",
                      "gunicorn==20.0.4",
                      "psycopg2-binary==2.8.6",
                      "psycopg2==2.8.6",
                      "rich",
                      ],
                  # pip install -e .[dev]
                  extras_require={
                      'dev': ['pytest',
                              # 'ipdb',
                              # https://stackoverflow.com/a/54794506/11842164
                              'ipdb @ git+ssh://git@github.com/giladbarnea/ipdb@v0.13.4#egg=ipdb'
                              'IPython',
                              'semver',
                              'birdseye',
                              'pyinspect',
                              'requests'
                              ]
                      },
                  # classifiers=[
                  # https://pypi.org/classifiers/
                  # 'Development Status :: 4 - Beta',
                  # 'Environment :: Console',
                  # 'Intended Audience :: Developers',
                  # "License :: OSI Approved :: MIT License",
                  # 'Operating System :: OS Independent',
                  # "Programming Language :: Python :: 3 :: Only",
                  # 'Topic :: Terminals',
                  #  ],
                  python_requires='>=3.8',
                  )
setup(**setup_args)
