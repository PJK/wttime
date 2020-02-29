from setuptools import setup

setup(name='wttime',
      version='0.1',
      description='Smart timestamp utility',
      url='https://github.com/PJK/wttime/actions',
      author='Pavel Kalvoda',
      author_email='me@pavelkalvoda.com',
      license='MIT',
      packages=['wttime'],
      scripts=['bin/wttime'],
      install_requires=[
            'click',
            'python-dateutil'
      ],
      tests_require=['pytest'],
      zip_safe=False)
