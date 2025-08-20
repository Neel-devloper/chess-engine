This is a chess engine that can play chess with you.

NV_Chess_engine.py:
  This file is the main computer that makes the move
  It uses a minimax algorithm that has a depth of three that you can increase to make it smarter and decrease to make it less intelligent.
  Increasing the depth may result in the computer taking more time and decreasing it may make it quicker but less smarter.
  It also uses alpha-beta pruning to make the dicision faster.

Main.py:
  This file takes in inputs from the chess engine and plays those moves.
  This file is concentrated on the UI of the game.
  This uses pygame for the UI infrastructure.
  You can press numbers from 0-9 on your keyboard to change the theme of the chess board.

How to Use:
  You should have python3 installed on you computer
  You are given chess images in this directory you can dowload the whole directory and in main.py change the paths of the images to make the main.py file access and display those images.
  Make sure that NV_Chess_engine.py and main.py are in the directory
  
