[![Current PyPI packages](https://badge.fury.io/py/multicombo.svg)](https://pypi.org/project/multicombo/)

# MultiCOMBO

Multilingual POS-Tagger and Dependency-Parser with [COMBO-pytorch](https://gitlab.clarin-pl.eu/syntactic-tools/combo) and [spaCy](https://spacy.io).

## Basic usage

```py
>>> import multicombo
>>> nlp=multicombo.load()
>>> doc=nlp('Who plays "La vie en rose"?')
>>> print(multicombo.to_conllu(doc))
# text = Who plays "La vie en rose"?
1	Who	who	PRON		PronType=Int	2	nsubj	_	Translit=who
2	plays	play	VERB		Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	0	root	_	_
3	"	"	PUNCT		_	5	punct	_	SpaceAfter=No
4	La	le	DET		Definite=Def|Gender=Fem|Number=Sing|PronType=Art	5	det	_	Translit=la
5	vie	vie	NOUN		Gender=Fem|Number=Sing	2	obj	_	_
6	en	en	ADP		_	7	case	_	_
7	rose	rose	NOUN		Number=Sing	5	nmod	_	SpaceAfter=No
8	"	"'	PUNCT		_	5	punct	_	SpaceAfter=No
9	?	?	PUNCT		_	2	punct	_	SpaceAfter=No

>>> import deplacy
>>> deplacy.render(doc)
Who   PRON  <════════════╗   nsubj
plays VERB  ═══════════╗═╝═╗ ROOT
"     PUNCT <══════╗   ║   ║ punct
La    DET   <════╗ ║   ║   ║ det
vie   NOUN  ═══╗═╝═╝═╗<╝   ║ obj
en    ADP   <╗ ║     ║     ║ case
rose  NOUN  ═╝<╝     ║     ║ nmod
"     PUNCT <════════╝     ║ punct
?     PUNCT <══════════════╝ punct

>>> deplacy.serve(doc)
http://127.0.0.1:5000
```
![trial.svg](https://raw.githubusercontent.com/KoichiYasuoka/MultiCOMBO/main/trial.png)
`multicombo.load(lang="xx")` loads spaCy Language pipeline with [bert-base-multilingual-cased](https://huggingface.co/bert-base-multilingual-cased) and `spacy.lang.xx.MultiLanguage` tokenizer. Other language specific tokenizers can be loaded with the option `lang`, while several languages require additional packages:
* `lang="ja"` Japanese requires [SudachiPy](https://pypi.org/project/SudachiPy/) and [SudachiDict-core](https://pypi.org/project/SudachiDict-core/).
* `lang="th"` Thai requires [PyThaiNLP](https://pypi.org/project/pythainlp/).
* `lang="vi"` Vietnamese requires [pyvi](https://pypi.org/project/pyvi/).

## Installation for Linux

```sh
pip3 install multicombo --user
```

