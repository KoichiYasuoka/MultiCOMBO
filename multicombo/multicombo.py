#! /usr/bin/python3 -i
# coding=utf-8

import os,numpy
from spacy.symbols import POS,DEP,HEAD
from spacy.tokens import Doc
from spacy.language import Language

PACKAGE_DIR=os.path.abspath(os.path.dirname(__file__))
DOWNLOAD_DIR=os.path.join(PACKAGE_DIR,"download")
MODEL_URL="https://raw.githubusercontent.com/KoichiYasuoka/MultiCOMBO/main/multicombo/download/"
SPACY_V3=hasattr(Language,"component")

filesize={}
with open(os.path.join(DOWNLOAD_DIR,"filesize.txt"),"r") as f:
  r=f.read()
for t in r.split("\n"):
  s=t.split()
  if len(s)==2:
    filesize[s[0]]=int(s[1])
multicombo_parser=None

class MultiComboParser(object):
  name="MultiCOMBO"
  def __init__(self,lang,vocab):
    global multicombo_parser
    self.lang=lang
    self.vocab=vocab
    if multicombo_parser==None:
      import unidic_combo.predict
      m="multicombo.tar.gz"
      f=os.path.join(DOWNLOAD_DIR,m)
      try:
        s=os.path.getsize(f)
      except:
        s=-1
      if filesize[m]!=s:
        from unidic_combo import download
        download(MODEL_URL,m,DOWNLOAD_DIR)
      multicombo_parser=unidic_combo.predict.COMBO.from_pretrained(f)
    self.parser=multicombo_parser
  def __call__(self,doc):
    from unidic_combo.data import Token,Sentence
    u=[]
    for s in doc.sents:
      e=[Token(id=i+1,token=t.orth_) for i,t in enumerate(s)]
      u.append(Sentence(tokens=e))
    u=self.parser(u)
    vs=self.vocab.strings
    r=vs.add("ROOT")
    pos=[]
    morphs=[]
    heads=[]
    deps=[]
    for s in u:
      for t in s.tokens:
        if t.deprel=="root":
          if t.head!=0:
            t.deprel="advcl" if t.head>t.id else "parataxis"
        pos.append(vs.add(t.upostag))
        morphs.append(t.feats)
        if t.head==0 or t.head==t.id:
          heads.append(0)
          deps.append(r)
        else:
          heads.append(t.head-t.id)
          deps.append(vs.add(t.deprel))
    a=numpy.array(list(zip(pos,deps,heads)),dtype="uint64")
    doc.from_array([POS,DEP,HEAD],a)
    if SPACY_V3:
      for i,j in enumerate(morphs):
        if j!="_" and j!="" and j!=None:
          doc[i].set_morph(j)
    else:
      doc.is_tagged=True
      doc.is_parsed=True
    return doc

def load_spacy(lang):
  try:
    exec("import spacy.lang."+lang+" as p")
    exec("q=p."+locals()["p"].__all__[0])
    return locals()["q"]()
  except:
    if lang=="lzh":
      from spacy.lang.zh import Chinese
      if not SPACY_V3:
        from spacy.lang.zh import ChineseDefaults
        ChineseDefaults.use_jieba=False
      return Chinese()
    from spacy.lang.xx import MultiLanguage
    return MultiLanguage()

def load(lang="xx"):
  nlp=load_spacy(lang)
  if SPACY_V3:
    nlp.add_pipe("sentencizer")
    Language.component("MultiCOMBO",func=MultiComboParser(lang,nlp.vocab))
    nlp.add_pipe("MultiCOMBO")
  else:
    nlp.add_pipe(nlp.create_pipe("sentencizer"))
    nlp.add_pipe(MultiComboParser(lang,nlp.vocab))
  nlp.meta["lang"]=lang+"_MultiCOMBO"
  return nlp

