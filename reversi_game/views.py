import json

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import tensorflow as tf
import numpy as np

from . import ReversiAgent
from . import reversi_game


# Create your views here.

def index(request):
    return render_to_response('reversi_game/index.html')

@csrf_exempt
def move(request):
    board = reversi_game.str2board(request.GET['board'])
    turn = int(request.GET['turn'])
    use_agent = request.GET['use_agent'] == '1'

    row = -1
    col = -1
    valid = True
    if use_agent:
        model = tf.keras.models.load_model('reversi_game/reversi_agent.h5')
        agent = ReversiAgent.ReversiAgent(Q=model)
        values = agent.get_move_values(np.multiply(board, turn))
        
        # go through moves by value, pick best one
        moves = reversed(np.argsort(values))
        for move in moves:
            row, col = reversi_game.get_move(move)
            if reversi_game.make_move(board, row, col, turn, True):
                break
    
    else:
        row = int(request.GET['row'])
        col = int(request.GET['col'])

        valid = reversi_game.make_move(board, row, col, turn, True)
    
    # change turn only if the move was valid
    if valid:
        next_to_move = -turn
        if not reversi_game.check_moves(board, -turn):
            if not reversi_game.check_moves(board, turn):
                next_to_move = 0
            else:
                next_to_move = turn
    else:
        next_to_move = turn

    black_count, white_count = reversi_game.count_pieces(board)

    response_dict = {
        "board": reversi_game.board2str(board),
        "valid": 1 if valid else 0,
        "status": next_to_move,
        "black_count": black_count, 
        "white_count": white_count
    }

    # response_str = reversi_game.board2str(board)
    # response_str += '1' if valid else '0'
    # response_str += 'B' if next_to_move == -1 else 'W' if next_to_move == 1 else '0'

    return HttpResponse(json.dumps(response_dict))
    