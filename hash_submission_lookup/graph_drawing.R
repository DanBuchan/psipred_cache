library(ggplot2)
require(scales)

protein_count_data <- read.csv(file="/Users/dbuchan/Code/psipred_cache/hash_submission_lookup/taxa_id_counts_renamed.csv", header=FALSE,  strip.white = TRUE, sep=",",na.strings= c("999", "NA", " ", ""))
colnames(protein_count_data) <- c("clade","organism","taxa_id","protein_count")
protein_count_data$protein_count<-as.numeric(as.character(protein_count_data$protein_count))
sorted_counts<-protein_count_data[ order(protein_count_data$protein_count, decreasing=TRUE), ] 
clade_totals<-aggregate(protein_count~clade, sum, data=sorted_counts)
sorted_totals<-clade_totals[order(clade_totals$protein_count, decreasing=TRUE),]

ggplot(sorted_totals, aes(x=reorder(clade, -protein_count), y=protein_count, fill=clade)) + geom_bar(stat="identity") + xlab("Clade") + ylab("Total Proteins") + scale_y_continuous(labels = comma)

ggplot(sorted_counts[1:50,], aes(x=reorder(organism, -protein_count), y=protein_count, fill=organism)) + geom_bar(stat="identity") + xlab("Organism") + ylab("Total Proteins") + scale_y_continuous(labels = comma) + theme(legend.position="none", axis.text.x = element_text(angle = 75, hjust = 1))
