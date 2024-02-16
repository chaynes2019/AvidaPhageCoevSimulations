#Input: a parasite_genome_list file
#Output: a histogram showing the distribution of the number of tasks present in parasite genomes via Matthew's phenotyping script

import AvidaScripts
import sys

resetRunNum = sys.argv[1]
timepoint = sys.argv[2]

population_dataframe = load_population_dataframe(f"data/coevResetRun-{resetRunNum}/detail_{timepoint}.spop")

parasite_sequences = get_parasite_subdataframe(population_dataframe)["Genome Sequence"]

parasite_phenotypes_dataframe = assess_parasite_phenotypes(parasite_sequences,
                                                           get_named_environment_content("Logic9"),
                                                           get_named_instset_content("transsmt"))
