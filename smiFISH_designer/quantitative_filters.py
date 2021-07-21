import pandas as pd

# Calculate deltaG
def deltaG1(probe_sequence):
	table = {"AA":0.2, "AC":-1.4, "AG":-0.4, "AT":-0.4,
	"CA":-1.6, "CC":-2.3, "CG":-1.4, "CT":-1.3,
	"GA":-1.4, "GC":-2.0, "GG":-1.7, "GT":-1.5, 
	"TA":-0.5, "TC":-1.5, "TG":-1.2, "TT":-0.7}

	for p in range(len(probe_sequence)):
		list_of_pairs = [probe_sequence[p:2 + p] for p in range(0, len(probe_sequence))]
		list_of_pairs.pop()
		if len(list_of_pairs) > 0:
			C = pd.Series(list_of_pairs).map(table)
			D = list(C)
			return sum(D)
		else:
			return 'Error'

# Calculate GC percentage
def GC_percent(probe_sequence):
	G = probe_sequence.count('G')
	C = probe_sequence.count('C')
	percent_GC = (G + C)/len(probe_sequence)
	return percent_GC

# Filter for GC content between 40% and 60%
def GC_filter(probe_sequence):
    return 0.40 <= GC_percent(probe_sequence) <= 0.60

# Find start index of probe within complementary strand
def start_index(probe_sequence, comp):
	if probe_sequence in comp:
		start = comp.find(probe_sequence)
		return start

	return 'Error'

# Find end index of probe within complementary strand
def end_index(probe_sequence, comp):
	if probe_sequence in comp:
		end = comp.find(probe_sequence)
		end += len(probe_sequence) - 1
		return end

	return 'Error'