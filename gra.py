#!/usr/bin/python
# coding=UTF-8

import sys
import argparse
import random

class Count(object):
	def __init__(self, _0, _1, _x):
		self._0 = _0
		self._1 = _1
		self._x = _x


def main():
	args = parse_args()

	tab_and = read_file(args.and_file)
	tab_or = read_file(args.or_file)
	tab_impl = read_file(args.impl_file)
	tab_not = read_file(args.not_file)
	
	symbol_map = {
		u'\u2192': tab_impl,
		u'\u2227': tab_and,
		u'\u2228': tab_or,
		u'\u00AC': tab_not
	}
	print "Instrukcja:"
	print """Gra polega na wpisywaniu zdań o odpowiedniej wartości logicznej do tabelki.
Każdy wiersz i każda kolumna ma się ewaluować do takiej wartości jak jest napisane powyżej planszy.
Działania są zawsze wykonywane od lewej do prawej lub od góry do dołu."""
	level = 1
	width = 2
	heigth = 2
	while level != 5:
		print "***********************************************************"
		print "Level", 1
		new_game(symbol_map, width, heigth)
		if level%2 == 0:
			width += 1
		else:
			heigth += 1
		print "-----------------------------------------------------------"
		print "Plansza została poprawnie wypełniona"
		level += 1
	print "Udało Ci się przejść całą grę. Gratulacje!"

	args.and_file.close()
	args.or_file.close()
	args.impl_file.close()
	args.not_file.close()


def new_game(symbol_map, width, heigth):
	sentence = ['0', '1', 'x'] 
	board_number = [[random.choice(sentence) for x in range(width)] for y in range(heigth)] #list of sentence for generating board
	board_number_fill = [['?' for x in range(width)] for y in range(heigth)] #list of sentence for filling by user
	
	#create a board
	board_game = [[random_symbol(x, y) for x in range(3*width-1)] for y in range(2*heigth-1)] #board for displaying
	count = Count(0, 0, 0)
	count._0
	
	#counting value of sentences and change value if not
	for y, y_val in zip(board_game[::2], board_number):
		for i in range(len(y))[::3]:
			if y_val[i/3] == 'x':
				count._x += 1
			elif y_val[i/3] == '0':
				count._0 += 1
				if y[i] == u'\u00AC':
					y_val[i/3] = '1'
			else:
				count._1 += 1
				if y[i] == u'\u00AC':
					y_val[i/3] = '0'		

	#values of sentence in rows and columns
	row_true = create_rows_true(board_number, board_game, symbol_map)
	col_true = create_cols_true(board_number, board_game, symbol_map)
	round = 1
	while(check_end(board_number_fill, board_game, row_true, col_true, symbol_map) != True):
		display_round(board_game, board_number_fill, row_true, col_true, width, heigth, count, round)
		round += 1

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--and', dest='and_file', type=argparse.FileType('r'))
	parser.add_argument('--or', dest='or_file', type=argparse.FileType('r'))
	parser.add_argument('--impl', dest='impl_file', type=argparse.FileType('r'))
	parser.add_argument('--not', dest='not_file', type=argparse.FileType('r'))
	args = parser.parse_args()

	if args.and_file == None or args.or_file == None or args.impl_file == None or args.not_file == None:
		sys.exit(u"Błędne argumenty")
	
	return args


def read_file(file_pointer):
	lines = file_pointer.read().splitlines()
	tab = [line.split() for line in lines]
	return tab


def random_symbol(x, y):
	if x%3 == 0 and y%2 == 0:
		symbols = [' ', u'\u00AC'] #not
	elif x%3 == 1 and y%2 == 0:
		symbols = ['?']
	elif (x%3 == 2 and y%2 == 0) or (x%3 == 1 and y%2 == 1):
		symbols = [u'\u2192', u'\u2227', u'\u2228'] #implication, and, or
	else: 
		symbols = [' ']
	return random.choice(symbols)


def display_board(board_game):
	for row in board_game:
		spaced_row = ' '.join(row)
		filtered_row = [symbol for i, symbol in enumerate(spaced_row) if ((i-1) % 6) != 0]
		print ''.join(filtered_row)
	print	


def check_pair(a, b, symbol, symbol_map):
	for row in symbol_map[symbol]:
		if a == row[0] and b == row[1]:
			return  row[2]


def add_char(x, y, symbol, board_game, board_number_fill):
	board_game[2*y][3*x+1] = symbol
	if board_game[2*y][3*x] == u'\u00AC' and symbol != 'x':
		symbol = '1' if symbol == '0' else '0'
	board_number_fill[y][x] = symbol
	


def check_end(board_number_fill, board_game, row_true, col_true, symbol_map):
	width = len(board_number_fill[0])
	for row in board_number_fill:
		for i in range(width):
			if row[i] == '?':
				return False

	if check_rows(board_number_fill, board_game, row_true, symbol_map) == False:
		print "-----------------------------------------------------------"
		print "Błędne wypełnienie planszy"
		return False
	if check_cols(board_number_fill, board_game, col_true, symbol_map) == False:
		print "-----------------------------------------------------------"
		print "Błędne wypełnienie planszy"
		return False
	return True


def check_rows(board_number_fill, board_game, row_true, symbol_map):
	
	for row, h, row_s in zip(board_number_fill, range(len(board_number_fill)), board_game[::2]):
		if bool_row(row, row_s, symbol_map) != row_true[h]:
			return False
	return True		
	

def bool_row(row_fill, row_board, symbol_map):
	prev = row_fill[0]
	gen = (x for i, x in enumerate(row_board) if i%3 == 2)
	for row, symbol in zip(row_fill[1:], gen):
		prev = check_pair(prev, row, symbol, symbol_map)
	return prev	


def create_rows_true(board_number, board_game, symbol_map):
	rows = []
	for row, row_s in zip(board_number, board_game[::2]):
		rows.append(bool_row(row, row_s, symbol_map))
	return rows	


def check_cols(board_number_fill, board_game, col_true, symbol_map):
	for i in range(len(board_number_fill[0])):
		cols = []
		cols_sym = []
		for row in board_number_fill:
			cols.append(row[i])
		for row_board in board_game[1::2]:
			cols_sym.append(row_board[3*i+1])
		if bool_col(cols, cols_sym, symbol_map) != col_true[i]:
			return False
	return True


def bool_col(col_fill, col_sym, symbol_map):
	prev = col_fill[0]
	for row, symbol in zip(col_fill[1:], col_sym):
		prev = check_pair(prev, row, symbol, symbol_map)
	return prev	


def create_cols_true(board_number, board_game, symbol_map):
	col = []
	for i in range(len(board_number[0])):
		cols = []
		cols_sym = []
		for row in board_number:
			cols.append(row[i])
		for row_board in board_game[1::2]:	
			cols_sym.append(row_board[3*i+1])
		col.append(bool_col(cols, cols_sym, symbol_map))
	return col


def display_round(board_game, board_number_fill, row_true, col_true, width, heigth, count, round):
	
	print "-----------------------------------------------------------"
	print "Ruch nr", round
	print "Wartości logiczne po koleji w wierszach:"
	print row_true, "\n"
	print "Wartości logiczne po koleji w kolumnach:"
	print col_true, "\n"
	print "Plansza:"
	display_board(board_game)
	print "Masz do dyspozycji zdania logiczne:"
	print "-o watrości 1 –", count._1
	print "-o watrości 0 –", count._0
	print "-o watrości x –", count._x
	
	print "Proszę podać numer kolumny(od 0 do", width-1, "):"
	
	x = None
	while x < 0 or x >= width:
		try:
			x = int(raw_input())
		except ValueError:
			print "Nie prawidłowa liczba, spróbuj jeszcze raz"
	
	print "Proszę podać numer wiersza(od 0 do", heigth-1, "):"
	
	y = None
	while y < 0 or y >= heigth:
		try:
			y = int(raw_input())
		except ValueError:
			print "Nieprawidłowa liczba, spróbuj jeszcze raz"
		
	print "Proszę podać wartość logiczną(do wyboru: '1', '0', 'x' ):"
	val = None
	val = raw_input()
	while not (val == '1' or val == '0' or val == 'x'):
		print "Nieprawidłowy znak, spróbuj jeszcze raz"
		val = raw_input()
	

	if val == '1':
		count._1 -= 1
	elif val == '0':
		count._0 -= 1
	else:
		count._x -= 1
	
	while count._1 < 0 or count._0 < 0 or count._x < 0:
		if count._1 < 0:
			count._1 += 1
		elif count._0 < 0:
			count._0 += 1
		else:
			count._x += 1
		print "Nie można użyć tego zdania. Proszę podać zdanie o innej wartości logicznej:"
		val = raw_input()
	
	add_char(x, y, val, board_game, board_number_fill)

main()	