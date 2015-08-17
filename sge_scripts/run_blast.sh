#!/bin/sh
#$ -t 1-409314

#
# Test we have uniref90 available and if not copy it to /tmp
#
blastdb="/tmp/test_db.fasta"
if [ -f "$blastdb" ]
then
  echo "Blast DB present"
else
  echo "Copying blast db"
  cp /Users/dbuchan/Downloads/test_db.* /tmp/
fi

#Here we get the
FASTA_PROTEOMES="/Users/dbuchan/Code/psipred_cache/get_proteomes/cache_proteomes_single_lines.fasta"
SGE_TASK_ID=1
SEQ_LOC=$(expr $SGE_TASK_ID '*' '2')
HEADER_LOC=$(expr $SEQ_LOC '-' '1')
HEADER=$(awk "NR==$HEADER_LOC  {print;exit}" $FASTA_PROTEOMES)
SEQ=$(awk "NR==$SEQ_LOC  {print;exit}" $FASTA_PROTEOMES)

#write HEADER AND SEQ TO A /tmp/temp file
MATCH=$(echo $HEADER | perl -ne 'while(/>.+\|(.+?)\|.+\s/g){print "$1\n";}')
FILENAME="/tmp/$MATCH.fasta"
OUT="/tmp/$MATCH.bls"
PSSM="/tmp/$MATCH.pssm"
CONTENTS="$HEADER\n$SEQ"
echo $CONTENTS >> $FILENAME

#run blast
echo "RUNNING A BLAST"
/Users/dbuchan/Downloads/ncbi-blast-2.2.31+/bin/psiblast -query $FILENAME -out_pssm $PSSM -out $OUT -db $blastdb -num_iterations 20
FAILFLAG="./$SGE_TASK_ID.failure"
if [ -f "$PSSM" ]
then
  mv $PSSM ./
  mv $OUT ./
  rm $FILENAME
else
  touch $FAILFLAG
fi
#delete our temp file
