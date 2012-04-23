# -*- coding: utf-8 -*-
"""
This module contains medialog.issuu, a plone product to show pdf files in plone with issuu.com 's viewer.
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.2.1'

long_description = (
    read('README.txt'))

tests_require = ['zope.testing']

setup(name='medialog.issuu',
      version=version,
      description="The goal is to integrate issuu.com's API with plone",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['medialog', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'requests >= 0.9, < 1.0'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='medialog.issuu.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
