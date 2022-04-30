from setuptools import setup, find_packages

setup(name="app_server",
      version="0.0.0",
      description="App Server",
      author="Ivan Xartiou",
      author_email="xartiou@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      scripts=['server/server_run']
      )