def chek_wins_player(state, player):
	count = 0
	if state[0][0] in [0, player] and state[1][0] in [0, player] and state[2][0] in [0, player]:
		count += 1
	if state[0][1] in [0, player] and state[1][1] in [0, player] and state[2][1] in [0, player]:
		count += 1
	if state[0][2] in [0, player] and state[1][2] in [0, player] and state[2][2] in [0, player]:
		count += 1

	if state[0][0] in [0, player] and state[0][1] in [0, player] and state[0][2] in [0, player]:
		count += 1
	if state[1][0] in [0, player] and state[1][1] in [0, player] and state[1][2] in [0, player]:
		count += 1
	if state[2][0] in [0, player] and state[2][1] in [0, player] and state[2][2] in [0, player]:
		count += 1

	if state[0][0] in [0, player] and state[1][1] in [0, player] and state[2][2] in [0, player]:
		count += 1
	if state[0][2] in [0, player] and state[1][1] in [0, player] and state[2][0] in [0, player]:
		count += 1
	return count


def get_rsult_of_playeer(state, player):
	best = -100
	for i in range(3):
		for j in range(3):
			if state[i][j] == 0:
				try_state = [l.copy() for l in state]
				try_state[i][j] = player
				number_of_posibel_wins = chek_wins_player(try_state, player)
				number_of_posibel_lose = chek_wins_player(try_state, player * -1)
				h = number_of_posibel_wins - number_of_posibel_lose
				best = max(best, h)
	return best


if __name__ == '__main__':
	a = 1
	state = [
		[0 for i in range(3)]
		for j in range(3)
	]
	get_rsult_of_playeer(state, 1)
	print(state)
