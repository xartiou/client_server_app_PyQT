from setuptools import setup, find_packages

setup(name="app_client",
      version="0.0.0",
      description="App Client",
      author="Ivan Xartiou",
      author_email="xartiou@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )