from setuptools import setup, find_packages

packages = find_packages()

setup(
    name="NORBY",
    version="1.0",
    description="Communication via telegram bot when bash command finishes executing",
    author="Hendrik Klug",
    author_email="klugh@ethz.ch",
    url="https://github.com/Jimmy2027/NORBY",
    keywords=["telegram-bot"],
    packages=["norby"],
    entry_points={
        "console_scripts": ["norby = norby.__main__:main"]
    },
    install_requires=['requests', 'subprocess-tee'],
    python_requires='>=3.7',
)
