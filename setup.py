import setuptools

setuptools.setup(
      name='sankeyfy',
      version='0.1',
      description='Wrangle dataframes for use in Sankey visualizations',
      long_description=open("README.md", "r").read(),
      keywords = ('sankey plotly D3'),
      install_requires=['numpy', 'pandas'],
      url='https://github.com/MCBoarder289/sankeyfy',
      author='Michael Chapman',
      author_email='chapman.michael.c@gmail.com',
      license='MIT',
      packages=['sankeyfy'],
      zip_safe=False)
