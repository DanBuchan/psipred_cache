#!/bin/sh
#$ -S /bin/sh
#$ -t 1-409314
#$ -l h_rt=2:0:0
#$ -l tmem=1.9G -l h_vmem=1.9G
#$ -e /home/dbuchan/psipred_cache/error/$TASK_ID.err
#$ -o /home/dbuchan/psipred_cache/output/$TASK_ID.out
#$ -l tscr=32G

# for i in `qhost | cut -f 1 -d " " ` ; do ssh  -oBatchMode=yes $i "echo $i; mkdir -p /scratch0/dbuchan/psi_cache; scp morecambe2:/home/dbuchan/psipred_cache/proteomes_greater_than_ten_percent_prepped.fasta /scratch0/dbuchan/psi_cache/" ; done
# for i in `qhost | cut -f 1 -d " " ` ; do ssh  -oBatchMode=yes $i "echo $i; scp morecambe2:/home/dbuchan/uniref/uniref90.fasta.* /scratch0/dbuchan/psi_cache/" ; done
# for i in `cat free_nodes.csv | cut -f 1 -d "  " `; do echo $i; done

# for i in `qhost | cut -f 1 -d " " ` ; do ssh  -oBatchMode=yes $i "echo $i; rm -rf /scratch0/dbuchan" ; done
# once we're done we can use this to clean up

# Test we have uniref90 available and if not copy it to /tmp
#
# LOCAL CONFIG
# This config for testing
# TMP="tmp/psi_cache"
# FASTA_PROTEOMES="/Users/dbuchan/Code/psipred_cache/get_proteomes/cache_proteomes_single_lines.fasta"
# BLAST_EXE="/Users/dbuchan/Downloads/ncbi-blast-2.2.31+/bin/psiblast"
# FINAL="./"
# blastdb_name="test_db"
# blastdb_location="/Users/dbuchan/Downloads/"
# blastdb="/$TMP/$blastdb_name.fasta"
# SGE_TASK_ID=1
# This config for morecambe/sge
hostname
TMP="/scratch0/dbuchan/psi_cache"
LOCK="$TMP/lock"
FASTA_PROTEOMES="/home/dbuchan/psipred_cache/cache_proteomes_single_lines.fasta"
LOCAL_PROTEOMES="$TMP/cache_proteomes_single_lines.fasta"
BLAST_EXE="/home/dbuchan/ncbi-blast-2.2.31+-src/c++/ReleaseMT/bin/psiblast"
FINAL="/home/dbuchan/psipred_cache/batch_1/"
blastdb_name="uniref90"
blastdb_location="/home/dbuchan/uniref/"
blastdb="/$TMP/$blastdb_name.fasta"
FAILFLAG="./$SGE_TASK_ID.failure"
# SGE_TASK_ID=1

while [ -f $LOCK ]
do
  echo "waiting"
  sleep 10
done
#Check if we have a copy of the db and mv it if neccessary
if [ -f "$blastdb" ]
then
  echo "Blast DB present"
else
  echo "Copying blast db"
  # touch $FINAL/$FAILFLAG
  mkdir -p $TMP
  touch $LOCK
  cp $FASTA_PROTEOMES /$TMP
  cp $blastdb_location/$blastdb_name.* /$TMP
  rm $LOCK
  # I should check if the last files makes it
fi

#Here we get the sequence
SEQ_LOC=$(expr $SGE_TASK_ID '*' '2')
HEADER_LOC=$(expr $SEQ_LOC '-' '1')
HEADER=$(awk "NR==$HEADER_LOC  {print;exit}" $LOCAL_PROTEOMES)
SEQ=$(awk "NR==$SEQ_LOC  {print;exit}" $LOCAL_PROTEOMES)

#write HEADER AND SEQ TO A /tmp/temp file
MATCH=$(echo $HEADER | perl -ne 'while(/>.+\|(.+?)\|.+\s/g){print "$1\n";}')
FILENAME="$TMP/$MATCH.fasta"
OUT="$TMP/$MATCH.bls"
PSSM="$TMP/$MATCH.pssm"
printf "$HEADER\n$SEQ" >> $FILENAME

#run blast
echo "RUNNING A BLAST"
$BLAST_EXE -query $FILENAME -out_pssm $PSSM -out $OUT -db $blastdb -num_iterations 20 -outfmt "7 qseqid qlen qstart qend sseqid slen sstart send evalue bitscore score length pident qcovs"
if [ -f "$PSSM" ]
then
  mv $PSSM $FINAL
  mv $OUT $FINAL
  rm $FILENAME
else
  touch $FINAL/$FAILFLAG
fi
#delete our temp file
