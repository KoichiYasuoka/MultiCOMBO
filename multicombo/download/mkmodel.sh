#! /bin/sh
if [ -f multicombo.tar.gz ]
then exit 0
fi
if [ ! -d ud-treebanks-v2.7 ]
then curl -L https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3424/ud-treebanks-v2.7.tgz | tar xzf -
fi
if [ ! -f ud-v2.7.conllu ]
then find ud-treebanks-v2.7 -name '*.conllu' -ls | awk '{printf("%d %s\n",$7,$NF)}' |
     ( while read S F
       do if [ $S -le 100000 ]
          then continue
          fi
          case $F in
          *Swedish_Sign*) continue ;;
          *Korean-Kaist*) continue ;;
          *Japanese-BCCWJ*) continue ;;
          esac
          python3 -c '
n=0
c=[]
f=True
while True:
  try:
    s=input()
  except:
    quit()
  t=s.split("\t")
  if len(t)==10:
    if t[0]!="#":
      if t[1]=="_":
        f=False
      if t[2]=="_":
        t[2]=t[1]
      if t[3] not in {"ADJ","ADP","ADV","AUX","CCONJ","DET","INTJ","NOUN","NUM","PART","PRON","PROPN","PUNCT","SCONJ","SYM","VERB"}:
        f=False
      if t[4]=="_":
        t[4]=t[3]
      if t[7]=="_" or t[7]=="dep":
        f=False
      c.append("\t".join(t))
  elif s.strip()=="":
    if f and len(c)>1 and len(c)<100:
      print("\n".join(c)+"\n")
      n+=1
      if n>500:
        quit()
    c=[]
    f=True
' < $F
       done
     ) > ud-v2.7.conllu
fi

# AllenNLP < 2 recommended for training
python3 -m unidic_combo.main --mode train --cuda_device 0 --num_epochs 30 --config_path config.template.jsonnet --word_batch_size 1200 --training_data_path ud-v2.7.conllu --pretrained_transformer_name bert-base-multilingual-cased --targets deprel,head,upostag,feats,lemma --features token,char

cp `ls -1t /tmp/allennlp*/model.tar.gz | head -1` multicombo.tar.gz
split -a 1 -b 83886080 --numeric-suffixes=1 multicombo.tar.gz multicombo.tar.gz.
ls -ltr *.tar.gz | awk '{printf("%s %d\n",$NF,$5)}' > filesize.txt
exit 0
