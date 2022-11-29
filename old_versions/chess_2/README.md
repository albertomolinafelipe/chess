# CHESS engine 2.0.0
I want to minimize the things I look up, so the way I encoded the board is probably not the best, or my minimax algorithm is inneficient
The only insipiration I've received is from  Sebastian Lague "Coding Adventure: Chess AI"
Its just a learning experience, once I'm happy with it I'll try to make it as close to SOTA

# to do
Add stalemate, add 100 move draw, add 3 fold draw
Add new select and moved colors


## Encoding the board
    - The board is flatten to rows, from A8 - H8, like playing with white at the bottom
    - Piece encoding
        - Black pieces will be uppercase, white lower
        - Queen q/Q
        - Rook r/R
        - Bishop b/B
        - Knight n/N
        - Pawn p/P, followed by 1 if it has just moved foward to positions or 0 otherwise
        - King k/K
    - The items
        - If the white can castle 0 no, 1 king, 2 queen, 3 both
        - Same with black
        - 100 move rule draw status
        - Players turn 1 black 0 white
        - If someone lost 0 white, 1 black, 2 draw, 3 none

    - To work with the board in the array, the pieces will be encoded as a number
    - A decial number [special][piece][color]
        - Special data
            - Pawn didnt just move two 1
              Not pawn
            - Pawn just moved two 2
        - Piece code
            - Empty 0
            - Pawn 1
            - Bishop 2 
            - Knight 3 
            - Rook 4 
            - Queen 5 
            - King 6 
        - Color
            - White or empty 0
            - Black 1
    
    - Move encoding, 4 numberdigit original row, original col , color code, then target row, target column
