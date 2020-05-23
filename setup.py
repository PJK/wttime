from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='wttime',
      version='0.2.0',
      description='Smart timestamp utility',
      long_description=long_description,
      long_description_content_type='text/markdown',
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
      tests_require=['pytest', 'mypy'],
      zip_safe=False)
