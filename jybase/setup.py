from distutils.core import setup


setup(
    name='jybase',
    version='0.1.0',
    description='jybase python utils',
    author='cnds',
    author_email='dingsong87@gmail.com',
    keywords='jybase',
    packages=['jybase'],
    package_dir={'jybase': '.'},
    package_data={'jybase': ['database/*', 'utils/*']},
    install_requires=[
        'Flask==0.12.2',
        'jsonschema==2.6.0',
        'PyJWT==1.5.3',
        'pymongo>=3.6.0',
        'redis==2.10.6',
        'pycrypto==2.6.1'
    ]
)
