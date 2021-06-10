from setuptools import setup, find_packages

with open('readme.md', 'r') as f :
    readme_content = f.read()

setup(
    name='petit_python_publipost_connector',
    version='0.1.1',
    description='Connect your templates to the petit_publipost gateway',
    packages=find_packages(),
    url='https://github.com/Plawn/petit_python_publipost_connector',
    license='apache-2.0',
    author='Plawn',
    author_email='plawn.yay@gmail.com',
    long_description=readme_content,
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
    # install_requires=['petit_type_system>=0.1.6'],
)
