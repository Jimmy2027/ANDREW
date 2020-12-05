from setuptools import setup, find_packages

packages = find_packages()

setup(
    name="NORBY",
    version="9999",
    description="Communication via telegram bot when bash command finishes executing",
    author="Hendrik Klug",
    author_email="klugh@ethz.ch",
    url="https://github.com/Jimmy2027/ANDREW",
    keywords=["telegram-bot"],
    scripts=['bin/norby']
)
