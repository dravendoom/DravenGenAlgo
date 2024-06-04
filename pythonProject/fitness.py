import random

def detect_conflicts(board):
    conflicts = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def fitness_function(board):
    fitness = 0
    fitness = round(1/(detect_conflicts(board)+1), 4)
    return fitness

