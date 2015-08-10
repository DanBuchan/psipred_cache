Taxonomy_investigation
======================

Looking briefly at selecting a canonical set of genomes which 'evenly' 
cover all the clased, generas or families

Conclusion: Even at a very low resolution this would imply 
pre-calculating ~1,000,000 PSI-BLAST matrices

hash_submission_lookup
======================

This time we take the md5 hash of all the sequences sent to PSIPRED in the
last year (approx 333,333), discarding the test sequence. Count the identical
ones and then loop over uniref to find the identical sequences.
