from setuptools import setup


setup(name='esgetfamily',
      version='0.5',
      description='Fetch Parent and Child documents in Elasticsearch',
      classifiers=[
          'Programming Language :: Python :: 2.7'
      ],
      url='https://github.com/plotlabs/esgetfamily-python.git',
      keywords=["elasticsearch", "elastic-search",
                "parent_child_single_result", "es combined result",
                "join type result", "parent child", "join type result",
                "parent child", "parent child single result",
                "elasticsearch parent child"],
      author='Nayan Jain',
      author_email='nayanjain1994@gmail.com',
      license='LICENSE.txt',
      packages=['esgetfamily'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['elasticsearch']
      )
