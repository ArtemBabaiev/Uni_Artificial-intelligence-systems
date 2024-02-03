package edu.ais.lab1;

import java.util.*;

class LabMain {
    public static void main(String[] args) {
        char[][] board = {
            {' ', ' ', ' '},
            {' ', ' ', ' '},
            {' ', ' ', ' '}
        };
        char currentPlayer = 'X';
        
        while (true) {
            printBoard(board);
            
            if (isBoardFull(board) || isWinner(board, 'X') || isWinner(board, 'O')) {
                break;
            }
            
            if (currentPlayer == 'X') {
                makeMove(board, currentPlayer);
                currentPlayer = 'O';
            } else {
                int[] bestMove = findBestMove(board, 'O');
                board[bestMove[0]][bestMove[1]] = 'O';
                currentPlayer = 'X';
            }
        }
        
        printBoard(board);
        
        if (isWinner(board, 'X')) {
            System.out.println("X wins!");
        } else if (isWinner(board, 'O')) {
            System.out.println("O wins!");
        } else {
            System.out.println("It's a draw!");
        }
    }
    
    static void printBoard(char[][] board) {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.print(board[i][j]);
                if (j < 2) {
                    System.out.print(" | ");
                }
            }
            System.out.println();
            if (i < 2) {
                System.out.println("---------");
            }
        }
        System.out.println();
    }
    
    static boolean isBoardFull(char[][] board) {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == ' ') {
                    return false;
                }
            }
        }
        return true;
    }
    
    static boolean isWinner(char[][] board, char player) {
        for (int i = 0; i < 3; i++) {
        	// стовпчик
            if (board[i][0] == player && board[i][1] == player && board[i][2] == player) {
                return true;
            }
            //рядок
            if (board[0][i] == player && board[1][i] == player && board[2][i] == player) {
                return true;
            }
        }
        //діагональ 1
        if (board[0][0] == player && board[1][1] == player && board[2][2] == player) {
            return true;
        }
        //діагональ 2
        if (board[0][2] == player && board[1][1] == player && board[2][0] == player) {
            return true;
        }
        return false;
    }
    
    static int[] findBestMove(char[][] board, char player) {
        int[] bestMove = new int[]{-1, -1};
        int bestScore = (player == 'O') ? Integer.MIN_VALUE : Integer.MAX_VALUE;
        
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == ' ') {
                    board[i][j] = player;
                    // комп'ютер буде йти по шляху максимізації
                    int score = minimax(board, player, (player == 'O'));
                    board[i][j] = ' ';
                    
                    if ((player == 'O' && score > bestScore) || (player == 'X' && score < bestScore)) {
                        bestScore = score;
                        bestMove[0] = i;
                        bestMove[1] = j;
                    }
                }
            }
        }
        
        return bestMove;
    }
    
    // Мінімакс алгоритм
    static int minimax(char[][] board, char currentPlayer, boolean isMaximizing) {
    	// Якщо досягнута кінцева гра або нічия, повертаємо оцінку стану гри
    	if (isWinner(board, 'X')) {
            return -1;
        } else if (isWinner(board, 'O')) {
            return 1;
        } else if (isBoardFull(board)) {
            return 0;
        }
        
        char opponent = (currentPlayer == 'X') ? 'O' : 'X';
        int bestScore = (isMaximizing) ? Integer.MIN_VALUE : Integer.MAX_VALUE;
        
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == ' ') {
                    board[i][j] = currentPlayer;
                    // рекурсія по опоненту, максимізація/мінімізація
                    int score = minimax(board, opponent, !isMaximizing);
                    board[i][j] = ' ';
                    
                    if (isMaximizing) {
                        bestScore = Math.max(score, bestScore);
                    } else {
                        bestScore = Math.min(score, bestScore);
                    }
                }
            }
        }
        
        return bestScore;
    }
    
    static void makeMove(char[][] board, char player) {
        Scanner scanner = new Scanner(System.in);
        int row, col;
        do {
            System.out.print("Enter row (0, 1, 2) and column (0, 1, 2) for " + player + ": ");
            row = scanner.nextInt();
            col = scanner.nextInt();
        } while (row < 0 || row > 2 || col < 0 || col > 2 || board[row][col] != ' ');
        board[row][col] = player;
    }
}
