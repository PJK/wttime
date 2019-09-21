from setuptools import setup

setup(name='wttime',
      version='0.1',
      description='Smart timestamp utility',
      url='TODO',
      author='Pavel Kalvoda',
      author_email='me@pavelkalvoda.com',
      license='MIT',
      packages=['wttime'],
      scripts=['bin/wttime'],
      install_requires=[
            'click',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
