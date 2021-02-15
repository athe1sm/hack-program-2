from setuptools import setup

setup(
    name="chinesemapdrawer",
    version="0.0.1",
    packages=[],
    entry_points={
        'console_scripts': ['ChinaCovid = ChineseMapDrawer.__main__:run_prog']
    }
)