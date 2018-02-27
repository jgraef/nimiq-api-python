from setuptools import setup

setup(
    name='nimiq-api-python',
    version='0.0.1',
    description='A python client for the Nimiq JSON-RPC API',
    url='http://github.com/jgraef/nimiq-api-python',
    author='Janosch Gräf',
    author_email='janosch.graef@cispa.saarland',
    license='MIT',
    packages=['nimiqrpc'],
    zip_safe=True,
    install_requires=[
        'requests'
    ],
)
