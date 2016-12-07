from setuptools import setup


setup(
    name='tbl',
    version='1.0.0',
    description='Tech Blog Links',
    author='Tech Blog Links',
    author_email='support@localhost',
    packages=['tbl'],
    include_package_data=True,
    install_requires=[
        'aiohttp==0.22.4',
        'motor==1.1',
        'beautifulsoup4==4.5.0',
        'feedparser==5.2.1',
    ],
)
