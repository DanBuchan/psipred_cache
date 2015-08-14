#!/bin/sh
#$ -t 1-409314

#
# Test we have uniref90 available and if not copy it to /tmp
#
blastdb="/tmp/test_db.fasta"
if [ -f "$blastdb" ]
then
  echo "found"
else
  echo "not found"
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
FILENAME="$MATCH.fasta"
CONTENTS="$HEADER\n$SEQ"
echo $CONTENTS >> $FILENAME

#run blast
echo "RUNNING A BLAST"

#delete our temp file
rm $FILENAME
