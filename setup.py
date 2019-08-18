from setuptools import setup, find_packages

setup(
    name             = 'videoTotext',
    version          = '1.0',
    description      = '동영상에서 세부 글자(자막, 타이틀) 추출',
    author           = 'JiHae Kim',
    author_email     = 'jihae6020@gmail.com',
    url              = 'https://github.com/jihaeK/videoTotext',
    download_url     = 'https://githur.com/jihaeK/videoTotext/archive/1.0.tar.gz',
    install_requires = [ ],
    packages         = find_packages(exclude = ['docs', 'tests*']),
    keywords         = ['liquibase', 'db migration'],
    python_requires  = '>=3',
    package_data     =  {
        'pyquibase' : [
            'db-connectors/sqlite-jdbc-3.18.0.jar',
            'db-connectors/mysql-connector-java-5.1.42-bin.jar',
            'liquibase/liquibase.jar'
    ]},
    zip_safe=False,
    classifiers      = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

    ]
)