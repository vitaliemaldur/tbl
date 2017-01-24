from setuptools import setup


setup(
    name='tbl',
    version='1.5.0',
    description='Tech Blog Links',
    author='Tech Blog Links',
    author_email='support@localhost',
    packages=['tbl'],
    include_package_data=True,
    install_requires=[
        'aiohttp==1.1.1',
        'multidict==2.1.4',
        'motor==1.1',
        'feedparser==5.2.1',
    ],
)
