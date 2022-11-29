
# Chess 4.0.0


// otros atributos
pin_ray_mask = 0
pin_in_position = True
check_ray_bitmask = 0
check = False
double_check = False

Calculate data()
# para sliders
for cada dirección desde la posición del friendly rey:

    friendly_piece_protecting = False
    ray_mask = 0

    for cada cuadrado disponible en esa dirección (dentro a fuera):

        ray_mask = posivion en binario (coon shifting)

        si hay una pieza:

            si es friendly:
                if not friendly_piece_protecting: # primera pieza buena en esa direccion
                    friendly_piece_protecting = True
                else:
                    break # porque si hay dos, seguro que no hay pin

            else:
                if se puede "deslizar" en la direccion que estamos viendo:
                    
                    if friendly_piece_protecting:
                        pin_in_position = True
                        pin_ray_mask += ray_mask
                    else:
                        check_ray_bitmask += ray_mask
                        double_check = check
                        check = True

                    break

                else:
                    break

        
    if double_check:
        break # se tiene que mover el rey

knight_check = False
opponent_knight_attack = 0

for knight in opponent:
    opponent_knight_attack += knight_attack_bitboard[position]

    if not knight_check and (king_pos & opponent_knight_attack != 0):
        knight_check =True
        double_check = check
        check = True
        check_ray_bitmask += pos_bitmask

opponent_pawn_map = 0
pawn_check = False

for pawn in opponent:
    opponent_pawn_map += pos_bitmasp
    if not pawn_check and king_pos & opponent_pawn_map != 0:
        pawn_check =True
        double_check = check
        check = True
        check_ray_bitmask += pos_bitmask

opponent_attack_map_No_pawns = opponent_knight_attack | opponent_slider_map | king_attacks[opKingpos]
opponent_attack_map = opponent_attack_map_No_pawns | opponent_pawn_map
