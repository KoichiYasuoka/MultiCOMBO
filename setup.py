import os,setuptools
with open("README.md","r",encoding="utf-8") as r:
  long_description=r.read()
URL="https://github.com/KoichiYasuoka/MultiCOMBO"

setuptools.setup(
  name="multicombo",
  version="0.8.0",
  description="Multilingual POS-tagger and Dependency-parser",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url=URL,
  author="Koichi Yasuoka",
  author_email="yasuoka@kanji.zinbun.kyoto-u.ac.jp",
  license="GPL",
  keywords="NLP Multilingual",
  packages=setuptools.find_packages(),
  install_requires=["unidic_combo>=1.3.2","transformers>=4.0.1"],
  python_requires=">=3.6",
  package_data={"multicombo":["download/*.txt"]},
  classifiers=[
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "Topic :: Text Processing :: Linguistic"
  ],
  project_urls={
    "COMBO-pytorch":"https://gitlab.clarin-pl.eu/syntactic-tools/combo",
    "Source":URL,
    "Tracker":URL+"/issues",
  }
)
