"""
Day 19
"""
from typing import Tuple


def read_input(path: str) -> Tuple[dict, list]:
	rules = {}
	messages = []
	with open(path, "r") as file_handle:
		line = file_handle.readline()
		# Parse rules
		while line != '\n':
			line = line[:-1] if line[-1] == '\n' else line
			key_value_split = line.split(':')
			key = key_value_split[0]
			rules[key] = [msg.strip().replace('"', '').split(' ') for msg in key_value_split[1].split('|')]
			line = file_handle.readline()
		line = file_handle.readline()
		# Parse messages
		while line != '':
			line = line[:-1] if line[-1] == '\n' else line
			messages.append(line)
			line = file_handle.readline()
	
	return rules, messages


def transform_grammar_for_part1_into_cnf(rules: dict) -> dict:
	# Note: since we do not try to create a general solution, we just fix it manually. This is
	# by far easier than writing a general solution.
	# My input is not in CNF since we have the produciton 8 -> 42 and 28 -> 104 | 95. However,
	# we can easily manually fix it by moving 8 -> 42 into 0 -> 8 11 since 8 is only
	# used by the start production and we get rid off the only single production.
	rules['0'][0][0] = '42'  # Move 8 -> 42 into 0 -> 8 11
	del rules['8']  # Remove the produciton 8 -> 42 since it is not needed anymore
	# We also now need to fix 28 -> 104 | 95. Since 104 -> "a" and 95 -> "b", we can easily 
	# fix the production by replacing it with 28 -> "a" | "b"
	rules['28'] = [['a'], ['b']]

	return rules


def cyk(reversed_rules: dict, word: str, start_symbol: str = '0') -> bool:
	"""
		DP table structure:

		N-1  ()
		N-2  ()      ()
		.
		.
		.
		1    ()      ()               ()
		0    ()      ()               ()         ()
				word[0] word[1]  ...   word[N-2]  word[N-1]

		If DP[N-1][0] contains 0, then the word can be produced by the grammar
	"""
	dp = [[[] for _ in range(len(word) + 1)] for _ in range(len(word) + 1)]

	# Initialize the DP table
	for i, w in enumerate(word):
		key = f'{w}'
		if key in reversed_rules.keys():
			dp[1][i + 1] = reversed_rules[key]
	
	for length in range(2, len(word) + 1):  # length also defines the row of the DP table
		for i in range(1, len(word) - length + 2):
			for k in range(1, length):
				for p1 in dp[k][i]:
					for p2 in dp[length - k][i + k]:
						key = f'{p1} {p2}'
						if key in reversed_rules.keys():
							dp[length][i] += reversed_rules[key]

				dp[length][i] = list(set(dp[length][i]))

	return start_symbol in dp[len(word)][1]


def create_reversed_rules(rules: dict) -> dict:
	reversed_rules = {}
	for key in rules.keys():
		for rev_key in rules[key]:
			rev_key_str = " ".join(rev_key)
			if rev_key_str in reversed_rules.keys():
				reversed_rules[rev_key_str].append(key)
			else:
				reversed_rules[rev_key_str] = [key]
	return reversed_rules


def solve1(rules: dict, messages: list, read_file_is_input_txt: bool = True) -> int:
	# Transform the input rules into CNF
	if read_file_is_input_txt:
		rules = transform_grammar_for_part1_into_cnf(rules)
	
	# First, we reverse the rules
	reversed_rules = create_reversed_rules(rules)

	cnt = 0
	for msg in messages:
		if cyk(reversed_rules, msg):
			cnt += 1

	return cnt


def adapt_grammar_for_part2_and_turn_into_cnf(rules: dict) -> dict:
	# We now need to update the following productions:
	# 8 -> 42 | 42 8
	# 11 -> 42 31 | 42 11 31
	# Since CYK requires the grammar in CNF, we need to fix the given grammar.
	# 1) 8 -> 42 into 8 -> 29 104 | 115 95 and hence, 8 -> 29 104 | 115 95 | 42 8
	rules['8'] = [['29', '104'], ['115', '95'], ['42', '8']]
	# 2) 11 -> 42 11 31, we add a new production 1000 -> 11 31 and 11 -> 42 1000
	rules['11'] = [['42', '31'], ['42', '1000']]
	rules['1000'] = [['11', '31']]

	# We also need to fix 28 -> 104 | 95. Since 104 -> "a" and 95 -> "b", we can easily 
	# fix the production by replacing it with 28 -> "a" | "b"
	rules['28'] = [['a'], ['b']]
	
	return rules


def solve2(rules: dict, messages: list) -> int:
	# Transform the rules into CNF
	rules = adapt_grammar_for_part2_and_turn_into_cnf(rules)
	
	# First, we reverse the rules
	reversed_rules = create_reversed_rules(rules)

	cnt = 0

	for msg in messages:
		if cyk(reversed_rules, msg):
			cnt += 1

	return cnt


def cyk_test1():
	grammar = {
		'S': [['A', 'T'], ['A', 'B']],
		'T': [['S', 'B']],
		'A': [['a']],
		'B': [['A', 'C'], ['a'], ['c']],
		'C': [['c']]
	}
	reversed_grammar = create_reversed_rules(grammar)
	word = 'aaaca'
	assert cyk(reversed_grammar, word, 'S')


def cyk_test2():
	grammar = {
		'S': [['A', 'B'], ['C', 'D'], ['A', 'T'], ['C', 'U'], ['S', 'S']],
		'T': [['S', 'B']],
		'U': [['S', 'D']],
		'A': [['(']],
		'B': [[')']],
		'C': [['[']],
		'D': [[']']]
	}
	reversed_grammar = create_reversed_rules(grammar)
	word = '()[()]'
	assert cyk(reversed_grammar, word, start_symbol='S')


def cyk_test3():
	grammar = {
		'S': [['A', 'B'], ['B', 'C']],
		'A': [['B', 'A'], ['a']],
		'B': [['C', 'C'], ['b']],
		'C': [['A', 'B'], ['a']]
	}
	reversed_grammar = create_reversed_rules(grammar)
	word = 'baaba'
	assert cyk(reversed_grammar, word, 'S')


if __name__ == "__main__":
	file_name = 'input.txt'
	rules, messages = read_input(f'/Users/danielgrittner/development/advent-of-code2020/day19/{file_name}')
	# Solve part 1
	# print(solve1(rules, messages, file_name == 'input.txt'))

	# Solve part 2
	print(solve2(rules, messages))
	
	# Tests for CYK:
	# cyk_test1()
	# cyk_test2()
	# cyk_test3()