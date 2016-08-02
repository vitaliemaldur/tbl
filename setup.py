from distutils.core import setup


setup(
    name='tbl',
    version='1.0.0',
    description='Tech Blogs Links',
    author='Tech Blogs Links',
    author_email='support@localhost',
    packages=['tbl'],
    include_package_data=True,
    install_requires=[
        'aiohttp==0.22.4',
        'motor==0.6.2',
        'beautifulsoup4==4.5.0',
    ],
)

