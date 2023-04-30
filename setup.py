from setuptools import setup, find_namespace_packages

setup(
    name="chef_helper",
    version="5",
    description="Helping the chef find meal cooking instructions.",
    url="http://github.com/osandrey/Chef_helper",
    author="OSA",
    author_email="osandreyman@gmail.com",
    license="MIT",
    packages=find_namespace_packages(),
    install_requires=["requests==2.29.0"],
    entry_points={"console_scripts": ["chef-helper=app.client_app:run_client"]}
)