from setuptools import setup

if __name__ == "__main__":
    console_scripts = ["hmmer-show = hmmer_reader:cli"]
    setup(entry_points=dict(console_scripts=console_scripts))
