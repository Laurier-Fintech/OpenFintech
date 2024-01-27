from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="OpenFintech",
    version="0.2.2",
    author = 'Laurier Fintech',
    author_email = 'team@wlufintech.com',
    url = 'https://github.com/Laurier-Fintech/OpenFintech',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
          'requests',
          'pandas',
          'python-dotenv',
    ]
)