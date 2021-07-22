import pandas as pd

from smiFISH_designer import filters as pnas_filters

from smiFISH_designer import quantitative_filters as quantitative_filters

from smiFISH_designer import overlap as overlap_filters

MBP_seq = 'AAAGACAGGCCCTCAGAGTCCGACGAGCTTCTCAGAGTCCGACGAGCTTCAGACCATCCAAGAAGATCCCACAGCAGCTTCCGAAGGCCTGGATGTGATGGCATCACAGAAGAGACCCTCACAGCGACACGGGTCCAAGTACTTGGCCACAGCAAGTACCATGGACCATGCCCGGCATGGCTTCCTCCCAAGGCACAGAGACACGGGCATCCTTGACTCCATCGGGCGCTTCTTTAGCGGTGACAGGGGTGCGCCCAAGCGGGGCTCTGGCAAGGTACCCTGGCTAAAGCAGAGCCGGAGCCCTCTGCCTTCTCATGCCCGCAGCCGTCCCGGGCTGTGCCACATGTACAAGGACTCACACACAAGAACTACCCACTACGGCTCCCTGCCCCAGAAGTCGCAGAGGACCCAAGATGAAAACCCAGTAGTCCACTTCTTCAAGAACATTGTGACACCTCGTACACCCCCTCCATCCCAAGGAAAGGGGAGAGGCCTGTCCCTCAGCAGATTTAGCTGGGGGGCCGAGGGGCAGAAGCCAGGATTTGGCTACGGAGGCAGAGCTTCCGACTATAAATCGGCTCACAAGGGATTCAAGGGGGCCTACGACGCCCAGGGCACGCTTTCCAAAATCTTTAAGCTGGGAGGAAGAGACAGCCGCTCTGGATCTCCCATGGCAAGACGCTGAGAGCCTCCCTGCTCAGCCTTCCCGAATCCTGCCCTCGGCTTCTTAATATAACTGCCTTAAACGTTTAATTCTACTTGCACCAAATAGCTAGTTAGAGCAGACCCTCTCTTAATCCCGTGGGGCTGTGAACGCGGCGGGGCCAGGCCCACGGCACCCTGACTGGCTAAAACTGTTTGTCCCTTTTTATTTGAAGATTGAGTTTCCTCGGGGTCTTCTCTGCCCCGACTTGCTCCCCGTGTACCTTGGTCGACTCCGGAGGTTCAGGTGCACGGACACCCTTTCAAGTTCACCCCTACTCCATCCTCAGACTTTCTTTTCACGGCGAGGCGCACCCCTCCAGCTTCCGTGGGCACTGCGGATAGACAGGCACACCGCCAAGGAGCCAGAGAGCATGGCGCAGGGGACTGTGTGGTCCAGGCTTCCTTTGTTTTCTTTCCCCTAAAGAGCTTTGTTTTTCCTAACAGGATCAGACAGTCTTGGAGTGGCTTACACAACGGGGGCTTGTGGTATGTGAGCACAGGCTGGGCAGCTGTGAGAGTCCAGAGTGGGGTGGCCCTGGGGACGCTTCCAGGCCAGCGGTTCCCTGCACCCCACCAGCTGATTTCGAGCGTGGCAGAGGGAAGGAAAGGGGCGAGCGGGCTGGGCAATGGACCCGACAGGAAACGGGGACTTAGGGGAACACGCTGGAGATGCCATGTGTGGCTGCCGAAGGTCACCATCTCTCCTCAGTGGCTCCCCAGAGCAGGTGCTTTTAAGAACCCTGTTTCCTCTCAGAGCCCAGGGAGAGTCCAAGGACATGGCGCATCAGGAAGTGGGACTGCAGGAGTTCTCTGGTGGCCTCGTGCTGTCCCTCTGGCCACTTCTCACTTTAGGGTGGTCAGCGGCAGCTCGCCATGGCAGTGCCCATTGGTGCACACTAACCTCAGTGGAAAAGTAACCATTCCCTGCCTCTTAGAAAGAACTCATTCTTAGTTTTAGGAGGGTTCCTGTCGCTGAATCAAGTCGCTGCCCTGGATGCAGGGCTGGCCTGGGCGACCCTCCAGGGATGAGGAGCTCAGAATTCCAGTCTTCTAATGTCCACGGACACCTCCCCATCCCTCTAACGTACTGACTATGTCTTTTGATTTAGCATGTCTTCTATAGACCTTCCAAAGAGACCCACACTGGCACTGTCACCCCCTAGGAGGGAAGGTGATGGTTGATGTAGCCCGACGCGCATCTTGTTAATCCGTTCTAATTCCGAGGAGAGTGTGGGTTTAAGATAACACCTATTAATGCATTGCCACAATAATGTGGGGGTAAGAGAAACGCAGGGACGAAACTTCCAGAAACAAACCCTCCAGATCGTTCCACAGGAGTGTTCGCCCTCCGGTGTGACTGAACGACCGACCTTGCCCATGGCTTCATCCAGACAGCACAGCTGCAGTATGGCTGGACAGAAGCACCTACTGTTCTTGGATATTGAAATAAAATAATAAACTTGCAATGATCTTTG'


def main():

	# List of 5 PNAS rules for optimum probe performance
	filters = ['pnas1', 'pnas2', 'pnas3', 'pnas4', 'pnas5']

	# Flip the inputed target RNA and replace bases to create complement strand
	reverse = MBP_seq[::-1]
	comp = MBP_seq.lower()[::-1].replace("g", "C").replace("c", "G").replace("t", "A").replace("a", "T").replace("u", "A")

	# Split complement strand (comp) into all possible probes between range (ex. 20-30 bases long)
	split_probes = []
	for n in range(20, 31): 
		for i in range(0, len(comp), n):
			probe = comp[i:i + n]

			# If length of probe is shorter than minimum range, remove from list
			if len(probe) > 20:
				split_probes.append(probe)


	# Main DataFrame
	df = pd.DataFrame()

	# Inputed names/sequences for FLAP and target RNA
	target_name = 'MBP'
	FLAP_name = 'X'
	FLAP_sequence = 'CCTCCTAAGTTTCGAGCTGGACTCAGTG'
	final_sequence = [FLAP_sequence + probe for probe in split_probes]

	# Adding columns to main DataFrame (boolean --> integers)
	df['probe_sequence'] = split_probes
	df['probe_length'] = df['probe_sequence'].apply(len)
	df['start'] = df['probe_sequence'].apply(quantitative_filters.start_index, comp=comp)
	df['end'] = df['probe_sequence'].apply(quantitative_filters.end_index, comp=comp)
	df['pnas1'] = df['probe_sequence'].apply(pnas_filters.pnas_filter_1).astype(int)
	df['pnas2'] = df['probe_sequence'].apply(pnas_filters.pnas_filter_2).astype(int)
	df['pnas3'] = df['probe_sequence'].apply(pnas_filters.pnas_filter_3).astype(int)
	df['pnas4'] = df['probe_sequence'].apply(pnas_filters.pnas_filter_4).astype(int)
	df['pnas5'] = df['probe_sequence'].apply(pnas_filters.pnas_filter_5).astype(int)
	df['deltaG'] = df['probe_sequence'].apply(quantitative_filters.deltaG1)
	df['GC'] = df['probe_sequence'].apply(quantitative_filters.GC_percent)
	df['GC_filter'] = df['probe_sequence'].apply(quantitative_filters.GC_filter).astype(int)
	df['target_name'] = target_name
	df['FLAP_name'] = FLAP_name
	df['FLAP_sequence'] = FLAP_sequence
	df['final_sequence'] = final_sequence

	# Create DataFrame using filters found in overlap_filters file
	fdf = overlap_filters.iteratively_find_probe_set(df, filters)

	# Final sequence name (target name + FLAP name + ranking number)
	fdf_index_reset = fdf.reset_index()
	fdf_index = fdf_index_reset.index.map(str)
	final_sequence_name = (target_name + '-' + FLAP_name + '-' + fdf_index)

	# Output of final, filtered DataFrame
	fdf['final_sequence_name'] = final_sequence_name
	print(fdf)

	# Output excel for all columns of final DataFrame
	fdf.to_excel('draft_probes_output.xlsx')



if __name__ == "__main__":
	main()