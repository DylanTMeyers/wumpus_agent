from wumpus import ExplorerAgent
import random
import collections
import copy
import time

class KB():

    def __init__(self):
        self.curr_location = (1,1)
        self.facing_direction = "North"
        self.breeze_dict = {}
        self.has_gold = False
        self.has_arrow = True
        self.steps = 0
        self.last_step_was_move = False
        self.shot_at = ()
        self.home_dir = []
        self.wumpus_dir = ""
        self.wumpus_move = ""
        self.all_values = []
        self.home_solution  = []
        self.go_right = False
        self.go_left = False
        self.go_up = False
        self.go_down = False
        self.already_found_wump = False
        self.gold_location = ()
        self.I_found_gold =  False
        self.shoot_at = ""


    def tell_breeze(self,percept):
        left_two, up_two, diag, opp_diag, up, right, down, left = self.get_all_sides(self.curr_location)
        if "Stench" not in percept:
            if self.in_bounds(up):
                if up not in self.breeze_dict:
                    self.breeze_dict[up] = [None, "Not Been", None ,None, None,"IDK", "Def not wump"]
                else:
                    self.breeze_dict[up][6] = "Def not wump"
            if self.in_bounds(right):
                if right not in self.breeze_dict:

                    self.breeze_dict[right] = [None, "Not Been", None ,None, None,"IDK", "Def not wump"]
                else:
                    self.breeze_dict[right][6] = "Def not wump"            
            if self.in_bounds(left):
                if left not in self.breeze_dict:

                    self.breeze_dict[left] = [None, "Not Been", None ,None, None,"IDK", "Def not wump"]
                else:
                    self.breeze_dict[left][6] = "Def not wump"  
            if self.in_bounds(down):
                if down not in self.breeze_dict:

                    self.breeze_dict[down] = [None, "Not Been", None ,None, None, "IDK", "Def not wump"]
                else:
                    self.breeze_dict[down][6] = "Def not wump"  
        if self.curr_location not in self.breeze_dict:
            self.breeze_dict[self.curr_location] = [percept[1], "Been", "IDK",percept[2], percept[0], "IDK", "IDK"]


        else:
                self.breeze_dict[self.curr_location][1] ="Been"

                self.breeze_dict[self.curr_location][0] = percept[1]
                self.breeze_dict[self.curr_location][3] = percept[2]
                self.breeze_dict[self.curr_location][4] = percept[0]


    def change_direction(self,turn):
        if self.facing_direction == "West":
            if turn == "TurnRight":
                self.facing_direction = "South"
            else:
                self.facing_direction = "North"
        elif self.facing_direction == "East":
            if turn == "TurnRight":
                self.facing_direction = "North"
            else:
                self.facing_direction = "South"
        elif self.facing_direction == "North":
            if turn == "TurnRight":
                self.facing_direction = "West"
            else:
                self.facing_direction = "East"
        else:
            if turn == "TurnRight":
                self.facing_direction = "East"
            else:
                self.facing_direction = "West"


    def no_wump_here(self, location, not_dir):
        left_two, up_two, diag, opp_diag, north_temp_curr_location, west_temp_curr_location, south_temp_curr_location, east_temp_curr_location = self.get_all_sides(location)

        if self.in_bounds(tuple(north_temp_curr_location)) and not_dir != "North":

            if tuple(north_temp_curr_location) not in self.breeze_dict:
                self.breeze_dict[tuple(north_temp_curr_location)] = ["None", 'Not Been', "Safe", "None", "None", "IDK", "IDK"]
            else:
                self.breeze_dict[tuple(north_temp_curr_location)][2] = "Safe"
        if self.in_bounds(tuple(south_temp_curr_location)) and not_dir != "South":
            if tuple(south_temp_curr_location) not in self.breeze_dict :
                self.breeze_dict[tuple(south_temp_curr_location)] = ["None", 'Not Been', "Safe","None", "None", "IDK","IDK"]
            else:
                self.breeze_dict[tuple(south_temp_curr_location)][2] = "Safe"
        if self.in_bounds(tuple(east_temp_curr_location)) and not_dir != "East":

            if tuple(east_temp_curr_location) not in self.breeze_dict:
                self.breeze_dict[tuple(east_temp_curr_location)] = ["None", 'Not Been', "Safe", 'None', "None", "IDK","IDK"]
            else:
                self.breeze_dict[tuple(east_temp_curr_location)][2] = "Safe"
        if self.in_bounds(tuple(west_temp_curr_location)) and not_dir != "West":

            if tuple(west_temp_curr_location) not in self.breeze_dict :
                self.breeze_dict[tuple(west_temp_curr_location)] = ["None", 'Not Been', "Safe","None", "None", "IDK", "IDK"]
            else:
                self.breeze_dict[tuple(west_temp_curr_location)][2] = "Safe"
                

    def change_position(self):
        if self.facing_direction == 'West':
            temp_curr_location = list(self.curr_location)
            
            temp_curr_location[0] = temp_curr_location[0] + 1
            self.curr_location = tuple(temp_curr_location)
        elif self.facing_direction == 'East':
            temp_curr_location = list(self.curr_location)
            
            temp_curr_location[0] = temp_curr_location[0] - 1
            self.curr_location = tuple(temp_curr_location)        
        elif self.facing_direction == 'South':
            temp_curr_location = list(self.curr_location)
            
            temp_curr_location[1] = temp_curr_location[1] - 1
            self.curr_location = tuple(temp_curr_location)
        else:
            temp_curr_location = list(self.curr_location)
            
            temp_curr_location[1] = temp_curr_location[1] + 1
            self.curr_location = tuple(temp_curr_location)
    def no_breeze(self,percept):
        if self.curr_location not in self.breeze_dict:
            self.breeze_dict[self.curr_location] = ["None", "Been", "Safe",percept[2], percept[0], "IDK", "IDK"]
        else:
                self.breeze_dict[self.curr_location][1] = "Been"
                self.breeze_dict[self.curr_location][3] = percept[2]
                self.breeze_dict[self.curr_location][4] = percept[0]
        left_two, up_two, diag, opp_diag, north_temp_curr_location, west_temp_curr_location, south_temp_curr_location, east_temp_curr_location = self.get_all_sides(self.curr_location)


        if self.in_bounds(tuple(north_temp_curr_location)):

            if tuple(north_temp_curr_location) not in self.breeze_dict:
                self.breeze_dict[tuple(north_temp_curr_location)] = ["None", 'Not Been', "Safe", "None", "None", "IDK", "IDK"]
            else:
                self.breeze_dict[tuple(north_temp_curr_location)][2] = "Safe"
        if self.in_bounds(tuple(south_temp_curr_location)):
            if tuple(south_temp_curr_location) not in self.breeze_dict :
                self.breeze_dict[tuple(south_temp_curr_location)] = ["None", 'Not Been', "Safe","None", "None", 'IDK', "IDK"]
            else:
                self.breeze_dict[tuple(south_temp_curr_location)][2] = "Safe"
        if self.in_bounds(tuple(east_temp_curr_location)):

            if tuple(east_temp_curr_location) not in self.breeze_dict:
                self.breeze_dict[tuple(east_temp_curr_location)] = ["None", 'Not Been', "Safe", 'None', "None", "IDK", "IDK"]
            else:
                self.breeze_dict[tuple(east_temp_curr_location)][2] = "Safe"
        if self.in_bounds(tuple(west_temp_curr_location)):

            if tuple(west_temp_curr_location) not in self.breeze_dict :
                self.breeze_dict[tuple(west_temp_curr_location)] = ["None", 'Not Been', "Safe","None", "None","IDK", "IDK"]
            else:
                self.breeze_dict[tuple(west_temp_curr_location)][2] = "Safe"




    def no_position_safe(self):
        for position in list(self.breeze_dict.values()):
            if position[2] == "Safe":
                return False
        return True

        


    def find_home(self):
        go_direction = None
        if self.curr_location[0] > self.home_dir[0][0]:
            go_direction = "East"
        elif self.curr_location[0] < self.home_dir[0][0]:
            go_direction = "West"

        elif self.curr_location[1] < self.home_dir[0][1]:
            go_direction = "North"

        elif self.curr_location[1] > self.home_dir[0][1]:
            go_direction = "South"
        if self.facing_direction != go_direction and ((go_direction == "South" and self.facing_direction == "East" ) or (go_direction == "West" and self.facing_direction == "South" ) or (go_direction == "North" and self.facing_direction == "West" ) or (go_direction == "East" and self.facing_direction == "North" )  ) :
            self.last_step_was_move = False

            self.change_direction('TurnLeft')
            return 'TurnLeft'
        if self.facing_direction != go_direction :
            self.last_step_was_move = False
            self.change_direction('TurnRight')
            return 'TurnRight'
        else:
            self.last_step_was_move = True

            self.home_dir.remove(self.home_dir[0])
            return "Forward"
    def add_edge(self,adj, src, dest):
 
        adj[src].append(dest)
        adj[dest].append(src)


    def num_in_list(self,move2):

        for move in range(len(self.all_values)):
            if self.all_values[move] == move2:
                return move

    def add_all(self,graph):
        self.all_values = list(self.breeze_dict.keys())
        for move in range(len(self.all_values)):
            left_two, up_two, diag, opp_diag, above, right, down, left = self.get_all_sides(self.all_values[move])
            if above in self.breeze_dict and "Been" in self.breeze_dict[above] and "Been" in self.breeze_dict[self.all_values[move]]:
                self.add_edge(graph,move,self.num_in_list(above))
            if right in self.breeze_dict and "Been" in self.breeze_dict[right] and "Been" in self.breeze_dict[self.all_values[move]]:
                self.add_edge(graph,move,self.num_in_list(right))
            if down in self.breeze_dict and "Been" in self.breeze_dict[down] and "Been" in self.breeze_dict[self.all_values[move]]:
                self.add_edge(graph,move,self.num_in_list(down))
            if left in self.breeze_dict and "Been" in self.breeze_dict[left] and "Been" in self.breeze_dict[self.all_values[move]]:
                self.add_edge(graph,move,self.num_in_list(left))


    def add_graph(self,location):
        self.breeze_dict[self.curr_location][1] = "Been"

        graph={_:[] for _ in range(len(self.breeze_dict))}
        self.add_all(graph)
        self.Bread_first_algo(graph, self.num_in_list(self.curr_location) ,self.num_in_list(location))
        self.create_home_dir()

        
    def Bread_first_algo(self,graph, start_location, goal_location):
        been = []
        order_queue = [[start_location]]
        if start_location == goal_location:
            return True

        while order_queue:
            path = order_queue.pop(0)
            node = path[-1]
            if node == None:
                return False

            if node not in been:
                neighbours_nodes = graph[node]

                for neighbour in neighbours_nodes:
                    new_path = list(path)
                    new_path.append(neighbour)
                    order_queue.append(new_path)
   
                    if neighbour == goal_location:
                        self.home_solution = new_path
                        return True

                been.append(node)
        return False

    def create_home_dir(self):
        self.home_dir = []
        num = 0
        for i in self.home_solution:
            if num !=0:
                self.home_dir.append(self.all_values[i])
            num = num + 1


    def in_bounds(self,cord):
        return cord[0]> 0 and cord[1]>0 and cord[0]<5 and cord[1]<5


    def local_safe(self):
        above_safe = []
        left_safe = []
        above_save2 = []
        for move in self.breeze_dict:
            left_two, up_two, diag, opp_diag, above, right, down, left = self.get_all_sides(move)

            if left in self.breeze_dict and "Been" in self.breeze_dict[left] and move in self.breeze_dict and "Been" in self.breeze_dict[move] and opp_diag in self.breeze_dict and "Been" in self.breeze_dict[opp_diag]:

                if ("Stench" not in self.breeze_dict[move] or "Stench" not in self.breeze_dict[opp_diag]) and ("Breeze" not in self.breeze_dict[move] or "Breeze" not in self.breeze_dict[opp_diag]):

                    above_safe.append(above)

            if above in self.breeze_dict and "Been" in self.breeze_dict[above] and move in self.breeze_dict and "Been" in self.breeze_dict[move] and opp_diag in self.breeze_dict and "Been" in self.breeze_dict[opp_diag]:

                if ("Stench" not in self.breeze_dict[move] or "Stench" not in self.breeze_dict[opp_diag]) and ("Breeze" not in self.breeze_dict[move] or "Breeze" not in self.breeze_dict[opp_diag]):

                    left_safe.append(left)
            if right in self.breeze_dict and "Been" in self.breeze_dict[right] and move in self.breeze_dict and "Been" in self.breeze_dict[move] and diag in self.breeze_dict and "Been" in self.breeze_dict[diag]:

                if ("Stench" not in self.breeze_dict[move] or "Stench" not in self.breeze_dict[diag]) and ("Breeze" not in self.breeze_dict[move] or "Breeze" not in self.breeze_dict[diag]):

                    above_save2.append(above)

        for move in above_safe:

            if move not in self.breeze_dict:
                self.breeze_dict[move] =  ["None", 'Not Been', "Safe", "None", "None", "IDK", "IDK"]
            else:
                self.breeze_dict[move][2] =  "Safe"
            
        for move in left_safe:
            if move not in self.breeze_dict:
                self.breeze_dict[move] =  ["None", 'Not Been', "Safe", "None", "None", "IDK", 'IDK']
            else:
                self.breeze_dict[move][2] =  "Safe"


        for move in above_save2:
            if move not in self.breeze_dict:
                self.breeze_dict[move] =  ["None", 'Not Been', "Safe", "None", "None","IDK", "IDK"]
            else:
                self.breeze_dict[move][2] =  "Safe"


    def ik_everything(self):
        num = 0
        all_board = []

        for i in range(1,5):
            for n in range(1,5):
                all_board.append((i,n))
        for move in self.breeze_dict:
            if self.has_gold == False and ("Bump" in self.breeze_dict[move] or "Pit Definite" in self.breeze_dict[move] or "Been" in self.breeze_dict[move] ):
                try:
                    all_board.remove(move)
                except:
                    print(move)
                    quit()
                num = num + 1

        if len(all_board) == 1 :
            self.breeze_dict[all_board[0]] =  ["None", 'Been', "Safe", "None", "None", "IDK", "IDK"]
            graph={_:[] for _ in range(len(self.breeze_dict))}
            self.add_all(graph)
            if self.Bread_first_algo(graph, self.num_in_list(all_board[0]) ,self.num_in_list((1,1))):
                self.gold_location = all_board[0]
                self.I_found_gold = True
                return
            else:
                del self.breeze_dict[all_board[0]]

  

    def ik_where_pit(self):
        temp_dict  = copy.copy(self.breeze_dict)
        for move in self.breeze_dict:
            left_two, up_two, diag, opp_diag, above, right, down, left = self.get_all_sides(move)

            if "Breeze" in self.breeze_dict[move] and (left in self.breeze_dict or self.in_bounds(left) == False ) and down in self.breeze_dict and (right in self.breeze_dict or self.in_bounds(right) == False )  and (self.in_bounds(left) == False or ("Been" in self.breeze_dict[left]) or "Bump" in self.breeze_dict[left]  )  and (self.in_bounds(right) == False or ("Been" in self.breeze_dict[right]) or "Bump" in self.breeze_dict[right] )  and (("Been" in self.breeze_dict[down]) or "Bump" in self.breeze_dict[down]):

                if self.in_bounds(above):
                    temp_dict[above] = [None, None, "IDK",None, None, "Pit Definite", "IDK"]

            if "Breeze" in self.breeze_dict[move] and left in self.breeze_dict and (down in self.breeze_dict or self.in_bounds(down) == False )  and (above in self.breeze_dict or self.in_bounds(above) == False ) and (("Been" in self.breeze_dict[left]) or "Bump" in self.breeze_dict[left])  and (self.in_bounds(above) == False or ("Been" in self.breeze_dict[above]) or "Bump" in self.breeze_dict[above] )  and ((self.in_bounds(down) == False or "Been" in self.breeze_dict[down]) or "Bump" in self.breeze_dict[down]):
                if self.in_bounds(right):
                    temp_dict[right] = [None, None, "IDK",None, None, "Pit Definite", "IDK"]

            if "Breeze" in self.breeze_dict[move] and (left in self.breeze_dict or self.in_bounds(left) == False )  and (right in self.breeze_dict or self.in_bounds(right) == False )  and above in self.breeze_dict and ( self.in_bounds(left) == False or ("Been" in self.breeze_dict[left]) or "Bump" in self.breeze_dict[left])  and (("Been" in self.breeze_dict[above]) or "Bump" in self.breeze_dict[above])  and (self.in_bounds(right) == False or ("Been" in self.breeze_dict[right]) or "Bump" in self.breeze_dict[right]):

                if self.in_bounds(down):

                    temp_dict[down] = [None, None, "IDK",None, None, "Pit Definite", "IDK"]


            if "Breeze" in self.breeze_dict[move] and (down in self.breeze_dict or self.in_bounds(down) == False ) and right in self.breeze_dict and (above in self.breeze_dict or self.in_bounds(above) == False ) and (self.in_bounds(down) == False or ("Been" in self.breeze_dict[down]) or "Bump" in self.breeze_dict[down])  and (self.in_bounds(above) == False or ("Been" in self.breeze_dict[above]) or "Bump" in self.breeze_dict[above])  and (("Been" in self.breeze_dict[right]) or "Bump" in self.breeze_dict[right]):

                if self.in_bounds(left):

                    temp_dict[left] = [None, None,  "IDK",None, None, "Pit Definite", "IDK"]

        self.breeze_dict = copy.copy(temp_dict)



    def ik_where_wumps(self):
        for move in self.breeze_dict:
            left_two, up_two, diag, opp_diag, above, right, down, left = self.get_all_sides(move)

            if "Stench" in self.breeze_dict[move] and diag in self.breeze_dict and "Stench" in self.breeze_dict[diag] and above in self.breeze_dict and ("Been" in self.breeze_dict[above] or "Bump" in self.breeze_dict[above] or "Pit Definite" in self.breeze_dict[above] or "Def not wump" in self.breeze_dict[above] ):
                if "Breeze" not in self.breeze_dict[move] and self.already_found_wump == False:
                    self.no_wump_here(move,"West")
                if "Breeze" not in self.breeze_dict[diag] and self.already_found_wump == False :
                    self.no_wump_here(diag,"South")
                self.already_found_wump = True
                if diag == self.curr_location:
                    self.wumpus_move = self.curr_location
                    self.wumpus_dir = "South"
                    self.shot_at = right
                    return True

                self.wumpus_dir = "West"
                self.wumpus_move = move
                self.shot_at = right
                return True

            if "Stench" in self.breeze_dict[move] and diag in self.breeze_dict and "Stench" in self.breeze_dict[diag] and right in self.breeze_dict and ("Been" in self.breeze_dict[right] or "Bump" in self.breeze_dict[right] or "Pit Definite" in self.breeze_dict[right] or "Def not wump" in self.breeze_dict[right]):
                if "Breeze" not in self.breeze_dict[move]:
                    self.no_wump_here(move,"North") and self.already_found_wump == False
                if "Breeze" not in self.breeze_dict[diag] and self.already_found_wump == False:
                    self.no_wump_here(diag,"East")
                self.already_found_wump = True

                if diag == self.curr_location:
                    self.wumpus_move = self.curr_location
                    self.wumpus_dir = "East"
                    self.shot_at = above
                    return True

                self.wumpus_dir = "North"
                self.wumpus_move = move
                self.shot_at = above
                return True


            if "Stench" in self.breeze_dict[move] and opp_diag in self.breeze_dict and "Stench" in self.breeze_dict[opp_diag]  and above in self.breeze_dict and ("Been" in self.breeze_dict[above] or "Bump" in self.breeze_dict[above] or "Pit Definite" in self.breeze_dict[above] or "Def not wump" in self.breeze_dict[above]):
                if "Breeze" not in self.breeze_dict[move] and self.already_found_wump == False:
                    self.no_wump_here(move,"East")
                if "Breeze" not in self.breeze_dict[opp_diag] and self.already_found_wump == False:
                    self.no_wump_here(opp_diag,"South")
                self.already_found_wump = True

                if opp_diag == self.curr_location:
                    self.wumpus_move = self.curr_location
                    self.wumpus_dir = "South"
                    self.shot_at = left
                    return True
                self.wumpus_dir = "East"
                self.wumpus_move = move
                self.shot_at = left
                return True
            if "Stench" in self.breeze_dict[move] and opp_diag in self.breeze_dict and ("Stench" in self.breeze_dict[opp_diag])  and left in self.breeze_dict and ("Been" in self.breeze_dict[left] or "Bump" in self.breeze_dict[left] or "Pit Definite" in self.breeze_dict[left] or "Def not wump" in self.breeze_dict[left]):
                if "Breeze" not in self.breeze_dict[move] and self.already_found_wump == False:
                    self.no_wump_here(move,"North")
                if "Breeze" not in self.breeze_dict[opp_diag] and self.already_found_wump == False:
                    self.no_wump_here(opp_diag,"West")
                self.already_found_wump = True

                if opp_diag == self.curr_location:
                    self.wumpus_move = self.curr_location
                    self.wumpus_dir = "West"
                    self.shot_at = above
                    return True
                self.wumpus_dir = "North"
                self.wumpus_move = move
                self.shot_at = above
                return True


            if "Stench" in self.breeze_dict[move] and (left in self.breeze_dict or self.in_bounds(left) == False ) and down in self.breeze_dict and (right in self.breeze_dict or self.in_bounds(right) == False )  and (self.in_bounds(left) == False or ("Stench" not in self.breeze_dict[left] and "Been" in self.breeze_dict[left]) or "Bump" in self.breeze_dict[left] or "Pit Definite" in self.breeze_dict[left] or "Def not wump" in self.breeze_dict[left]  )  and (self.in_bounds(right) == False or ("Stench" not in self.breeze_dict[right] and "Been" in self.breeze_dict[right]) or "Bump" in self.breeze_dict[right] or "Pit Definite" in self.breeze_dict[right] or "Def not wump" in self.breeze_dict[right] )  and (("Stench" not in self.breeze_dict[down] and "Been" in self.breeze_dict[down]) or "Bump" in self.breeze_dict[down] or "Pit Definite" in self.breeze_dict[down] or "Def not wump" in self.breeze_dict[down]):
                self.wumpus_dir = "North"
                self.wumpus_move = move
                self.shot_at = above
                return True

            if "Stench" in self.breeze_dict[move] and left in self.breeze_dict and (down in self.breeze_dict or self.in_bounds(down) == False )  and (above in self.breeze_dict or self.in_bounds(above) == False ) and (("Stench" not in self.breeze_dict[left] and "Been" in self.breeze_dict[left]) or "Bump" in self.breeze_dict[left] or "Pit Definite" in self.breeze_dict[left] or "Def not wump" in self.breeze_dict[left] )  and (self.in_bounds(above) == False or ("Stench" not in self.breeze_dict[above] and "Been" in self.breeze_dict[above]) or "Bump" in self.breeze_dict[above] or "Pit Definite" in self.breeze_dict[above] or "Def not wump" in self.breeze_dict[above]  )  and ((self.in_bounds(down) == False or "Stench" not in self.breeze_dict[down] and "Been" in self.breeze_dict[down]) or "Bump" in self.breeze_dict[down] or "Pit Definite" in self.breeze_dict[down] or "Def not wump" in self.breeze_dict[down]):
                self.wumpus_dir = "West"
                self.wumpus_move = move
                self.shot_at = right
                return True

            if "Stench" in self.breeze_dict[move] and (left in self.breeze_dict or self.in_bounds(left) == False )  and (right in self.breeze_dict or self.in_bounds(right) == False )  and above in self.breeze_dict and ( self.in_bounds(left) == False or ("Stench" not in self.breeze_dict[left] and "Been" in self.breeze_dict[left]) or "Bump" in self.breeze_dict[left] or "Pit Definite" in self.breeze_dict[left] or "Def not wump" in self.breeze_dict[left] )  and (("Stench" not in self.breeze_dict[above] and "Been" in self.breeze_dict[above]) or "Bump" in self.breeze_dict[above] or "Pit Definite" in self.breeze_dict[above] or "Def not wump" in self.breeze_dict[above])  and (self.in_bounds(right) == False or ("Stench" not in self.breeze_dict[right] and "Been" in self.breeze_dict[right]) or "Bump" in self.breeze_dict[right] or "Pit Definite" in self.breeze_dict[right] or "Def not wump" in self.breeze_dict[right]):
                self.wumpus_dir = "South"
                self.wumpus_move = move
                self.shot_at = down
                return True

            if "Stench" in self.breeze_dict[move] and (down in self.breeze_dict or self.in_bounds(down) == False ) and right in self.breeze_dict and (above in self.breeze_dict or self.in_bounds(above) == False ) and (self.in_bounds(down) == False or ("Stench" not in self.breeze_dict[down] and "Been" in self.breeze_dict[down]) or "Bump" in self.breeze_dict[down] or "Pit Definite" in self.breeze_dict[down] or "Def not wump" in self.breeze_dict[down])  and (self.in_bounds(above) == False or ("Stench" not in self.breeze_dict[above] and "Been" in self.breeze_dict[above]) or "Bump" in self.breeze_dict[above] or "Pit Definite" in self.breeze_dict[above] or "Def not wump" in self.breeze_dict[above])  and (("Stench" not in self.breeze_dict[right] and "Been" in self.breeze_dict[right]) or "Bump" in self.breeze_dict[right] or "Pit Definite" in self.breeze_dict[right] or "Def not wump" in self.breeze_dict[right]):
                self.wumpus_dir = "East"
                self.wumpus_move = move
                self.shot_at = left
                return True


            if "Stench" in self.breeze_dict[move] and (self.in_bounds(left) == False or (left in self.breeze_dict and ( self.in_bounds(left) == False or "Been" in self.breeze_dict[left] or "Bump" in self.breeze_dict[left] or "Pit Definite" in self.breeze_dict[left] or "Def not wump" in self.breeze_dict[left]))) and ( self.in_bounds(right) == False or (right in self.breeze_dict and ( self.in_bounds(right) == False or "Been" in self.breeze_dict[right] or "Bump" in self.breeze_dict[right] or "Pit Definite" in self.breeze_dict[right] or "Def not wump" in self.breeze_dict[right]))) and (self.in_bounds(down) == False or (down in self.breeze_dict and ( self.in_bounds(down) == False or "Been" in self.breeze_dict[down] or "Bump" in self.breeze_dict[down] or "Pit Definite" in self.breeze_dict[down] or "Def not wump" in self.breeze_dict[down]))):
                self.wumpus_dir = "North"
                self.wumpus_move = move
                self.shot_at = above
                return True
            if "Stench" in self.breeze_dict[move] and (self.in_bounds(left) == False or (left in self.breeze_dict and ( self.in_bounds(left) == False or "Been" in self.breeze_dict[left] or "Bump" in self.breeze_dict[left] or "Pit Definite" in self.breeze_dict[left] or "Def not wump" in self.breeze_dict[left]))) and ( self.in_bounds(above) == False or (above in self.breeze_dict and ( self.in_bounds(above) == False or "Been" in self.breeze_dict[above] or "Bump" in self.breeze_dict[above] or "Pit Definite" in self.breeze_dict[above] or "Def not wump" in self.breeze_dict[above]))) and (self.in_bounds(down) == False or (down in self.breeze_dict and ( self.in_bounds(down) == False or "Been" in self.breeze_dict[down] or "Bump" in self.breeze_dict[down] or "Pit Definite" in self.breeze_dict[down] or "Def not wump" in self.breeze_dict[down]))):
                self.wumpus_dir = "West"
                self.wumpus_move = move
                self.shot_at = right
                return True
            if "Stench" in self.breeze_dict[move] and (self.in_bounds(left) == False or (left in self.breeze_dict and ( self.in_bounds(left) == False or "Been" in self.breeze_dict[left] or "Bump" in self.breeze_dict[left] or "Pit Definite" in self.breeze_dict[left] or "Def not wump" in self.breeze_dict[left]))) and ( self.in_bounds(above) == False or (above in self.breeze_dict and ( self.in_bounds(above) == False or "Been" in self.breeze_dict[above] or "Bump" in self.breeze_dict[above] or "Pit Definite" in self.breeze_dict[above] or "Def not wump" in self.breeze_dict[above]))) and (self.in_bounds(right) == False or (right in self.breeze_dict and ( self.in_bounds(right) == False or "Been" in self.breeze_dict[right] or "Bump" in self.breeze_dict[right] or "Pit Definite" in self.breeze_dict[right] or "Def not wump" in self.breeze_dict[right]))):

                self.wumpus_dir = "South"
                self.wumpus_move = move
                self.shot_at = down
                return True
            if "Stench" in self.breeze_dict[move] and (self.in_bounds(down) == False or (down in self.breeze_dict and ( self.in_bounds(down) == False or "Been" in self.breeze_dict[down] or "Bump" in self.breeze_dict[down] or "Pit Definite" in self.breeze_dict[down] or "Def not wump" in self.breeze_dict[down]))) and ( self.in_bounds(above) == False or (above in self.breeze_dict and ( self.in_bounds(above) == False or "Been" in self.breeze_dict[above] or "Bump" in self.breeze_dict[above] or "Pit Definite" in self.breeze_dict[above] or "Def not wump" in self.breeze_dict[above]))) and (self.in_bounds(right) == False or (right in self.breeze_dict and ( self.in_bounds(right) == False or "Been" in self.breeze_dict[right] or "Bump" in self.breeze_dict[right] or "Pit Definite" in self.breeze_dict[right] or "Def not wump" in self.breeze_dict[right]))):
                self.wumpus_dir = "East"
                self.wumpus_move = move
                self.shot_at = left
                return True

            if "Stench" in self.breeze_dict[move] and up_two in self.breeze_dict and "Stench" in self.breeze_dict[up_two] :
                self.wumpus_dir = "North"
                self.wumpus_move = move
                self.shot_at = above
                return True

            if "Stench" in self.breeze_dict[move] and left_two in self.breeze_dict and "Stench" in self.breeze_dict[left_two] :
                self.wumpus_dir = "East"
                self.wumpus_move = move
                self.shot_at = left
                return True


    def bump(self):
        bump_location = ()
        if self.facing_direction == 'West':
            temp_curr_location = list(self.curr_location) 
            temp_curr_location[0] = temp_curr_location[0] + 1
            bump_location = tuple(temp_curr_location)

        elif self.facing_direction == 'East':
            temp_curr_location = list(self.curr_location)
            temp_curr_location[0] = temp_curr_location[0] - 1
            bump_location = tuple(temp_curr_location)  

        elif self.facing_direction == 'South':
            temp_curr_location = list(self.curr_location)
            temp_curr_location[1] = temp_curr_location[1] - 1
            bump_location = tuple(temp_curr_location)

        else:
            temp_curr_location = list(self.curr_location)
            temp_curr_location[1] = temp_curr_location[1] + 1
            bump_location = tuple(temp_curr_location)

        self.breeze_dict[bump_location] = ["Bump", 'Bump', "Bump", "Bump", "Bump", "Bump", "BUMP"]


    def none_more_search(self):
        for move in self.breeze_dict:
            if "Bump" not in self.breeze_dict[move] and "Safe" in self.breeze_dict[move] and "Been" not in self.breeze_dict[move] :
                return False
        return True


    def get_all_sides(self,location):
            left_two = list(location)
            left_two[1] = left_two[1] + 2
            left_two = tuple(left_two)  

            up_two = list(location)
            up_two[1] = up_two[1] + 2
            up_two = tuple(up_two)  

            diag = list(location)
            diag[0] = diag[0] + 1
            diag[1] = diag[1] + 1
            diag = tuple(diag)

            opp_diag = list(location)
            opp_diag[0] = opp_diag[0] - 1
            opp_diag[1] = opp_diag[1] + 1
            opp_diag = tuple(opp_diag)
            
            above = list(location)
            above[1] = above[1] + 1
            above = tuple(above)

            right = list(location)
            right[0] = right[0] + 1
            right = tuple(right)

            down = list(location)
            down[1] = down[1] - 1
            down = tuple(down)

            left = list(location)
            left[0] = left[0] - 1
            left = tuple(left)
            return left_two, up_two, diag, opp_diag, above, right, down, left


    def smell_area(self):
        for move in self.breeze_dict:

            left_two, up_two, diag, opp_diag, above, right, down, left = self.get_all_sides(move)

            if "Stench" in self.breeze_dict[move] and above not in self.breeze_dict and self.in_bounds(above):
                self.shoot_at = "North"
                self.shot_at = above
                
                return move
            if "Stench" in self.breeze_dict[move] and right not in self.breeze_dict and self.in_bounds(right):
                self.shoot_at = "West"
                self.shot_at = right
                return move
            if "Stench" in self.breeze_dict[move] and down not in self.breeze_dict and self.in_bounds(down):
                self.shoot_at = "South"
                self.shot_at = down

                return move
            if "Stench" in self.breeze_dict[move] and left not in self.breeze_dict and self.in_bounds(left):
                self.shoot_at = "East"
                self.shot_at = left

                return move


    def get_next_not_been(self):
        temp_dict = {}
        for move in self.breeze_dict:
            if "Been" not in self.breeze_dict[move] and "Safe" in self.breeze_dict[move]  and "Bump" not in self.breeze_dict[move] :
                self.breeze_dict[move][1] = "Been"
                self.add_graph(move)
                self.breeze_dict[move][1] = "Not Been"
                temp_dict[move] = len(self.home_dir)

        self.breeze_dict[min(temp_dict, key=temp_dict.get)][1] ="Been"
        return min(temp_dict, key=temp_dict.get)
        


class dmeyers_ExplorerAgent(ExplorerAgent):

    def __init__(self):
        super().__init__()
        self.kb = KB()
        self.gottem_num = 0
        self.used_num = 0
        self.all_done = False
        self.shoot_done = False
        self.move = 0
        self.only_once = False
        self.only_find_gold_once = True
        self.area = None
        self.not_been = ()
        self.need_another_area = False


    def program(self, percept):
        random.seed(time.process_time())
        self.move = self.move  + 1


        if self.move >10000:
            print("pass max")
            print(self.kb.breeze_dict)
            quit()

        if percept[3] == "Bump":
            self.kb.bump()

        if self.kb.last_step_was_move and percept[3] != "Bump":

            self.kb.change_position()

        if percept[2] == "Glitter":
            self.kb.has_gold = True
            self.kb.add_graph((1,1))
            self.kb.last_step_was_move = False
            return "Grab"
        
        if percept[4] == "Scream":
            print("gottem")
            self.kb.breeze_dict[self.kb.shot_at] = ["None", 'Not Been', "Safe", "None", "None", 'IDK', "IDK"]
        

        
        if self.kb.curr_location == (1,1) and self.kb.has_gold:
            self.used_num = self.used_num + 1
            if 3< self.used_num:
                print("used")
                quit()
            print("USEDDDDDDD")
            return 'Climb'
        if self.kb.curr_location == (1,1) and self.all_done:
            return 'Climb'

        if percept[1] == "Breeze" or percept[0] == "Stench":
            self.kb.tell_breeze(percept)
        else:
            self.kb.no_breeze(percept)
        self.kb.ik_where_pit()
        self.kb.ik_everything()
        if self.kb.I_found_gold:
            if self.only_find_gold_once:
                self.only_find_gold_once = False
                self.kb.add_graph(self.kb.gold_location)

            return self.kb.find_home()



        if self.kb.ik_where_wumps()  and self.kb.has_arrow and not self.kb.has_gold:


            if self.kb.curr_location == self.kb.wumpus_move and self.kb.wumpus_dir != self.kb.facing_direction:
                self.kb.last_step_was_move = False
                self.kb.change_direction('TurnRight')
                return "TurnRight"

            self.kb.go_left = False
            self.kb.go_up = False
            self.kb.go_right = False
            self.kb.go_down = False

            if self.kb.curr_location == self.kb.wumpus_move and self.kb.wumpus_dir == self.kb.facing_direction:
                self.kb.has_arrow = False
                self.kb.last_step_was_move = False

                self.kb.breeze_dict[self.kb.shot_at] = ["None", 'Not Been', "Safe", "None", "None", 'IDK', "IDK"]
                self.need_another_area = True
                return "Shoot" 

            if self.only_once == False:
                self.only_once = True
                self.kb.add_graph(self.kb.wumpus_move)

            return self.kb.find_home()
        if self.area == None:
            self.area = self.kb.smell_area()
        if self.kb.none_more_search()  and self.kb.has_arrow and not self.shoot_done and self.area != None :
            self.shoot_done = True
            self.kb.add_graph(self.area)

        if self.shoot_done and self.kb.has_arrow and self.kb.has_gold != True:
            if self.kb.curr_location == self.area and self.kb.shoot_at != self.kb.facing_direction:
                self.kb.last_step_was_move = False
                self.kb.change_direction('TurnRight')
                return "TurnRight"
            if self.kb.curr_location == self.area and self.kb.shoot_at == self.kb.facing_direction:
                self.kb.has_arrow = False
                self.kb.last_step_was_move = False
                self.need_another_area = True

                if "Breeze" not in percept:
                    self.kb.breeze_dict[self.kb.shot_at] = ["None", 'Not Been', "Safe", "None", "None", 'IDK', "IDK"]
                return "Shoot" 
            return self.kb.find_home()


        if self.kb.none_more_search() and self.move>2 and not self.all_done :
            if self.kb.curr_location == (1,1):
                return "Climb"
            self.all_done = True
            self.kb.add_graph((1,1))
        if self.kb.has_gold or self.all_done:
            return self.kb.find_home()


        self.kb.local_safe()
        if self.kb.curr_location == (1,1) and self.kb.has_arrow == True and percept[0] == "Stench":
            self.kb.shot_at = (1,2)

            self.kb.has_arrow = False
            if percept[1] != "Breeze":
                self.kb.breeze_dict[self.kb.shot_at] = ["None", 'Not Been', "Safe", "None", "None", "IDK", "IDK"]
            self.kb.last_step_was_move = False
            return "Shoot"

        if self.kb.curr_location == (1,1) and percept[1] == "Breeze" and self.kb.no_position_safe() :
            return 'Climb'

        self.kb.last_step_was_move = False
        if self.kb.curr_location == self.not_been or self.not_been == () or "Bump" in self.kb.breeze_dict[self.not_been]:
            self.need_another_area = True

        if self.need_another_area == True:
            self.need_another_area = False
            self.not_been =  self.kb.get_next_not_been()
            self.kb.add_graph(self.not_been)
            self.kb.breeze_dict[self.not_been][1] = "Not Been"
        return self.kb.find_home()
        
