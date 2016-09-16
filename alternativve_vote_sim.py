import random
import numpy
import csv
## A stochastic simulation to predict outcomes of each riding provided that
## an MMP system was used. RCV would be used for for local ridings and #s of
## prop vote determined by average of 2008, 2011, and 2015 party vote.

def data_load():
    elect_res = {}
    district = []
    with open("election_results.csv","rb") as csvfile:
        filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
        row1=next(filereader)
        for row in filereader:
            key = int(row[0])
            if key in district:
                party = row[5]
                votes = int(row[6])
                total_votes = int(row[9])-int(row[8])
                elect_res[key].append([party, votes, total_votes])
            if key not in district:
                district.append(key)
                party = row[5]
                votes = int(row[6])
                total_votes = int(row[9])-int(row[8])
                elect_res[key] = [[party, votes, total_votes]]
            
    return elect_res, district
class second_choice(object):
    def __init__(self): # numbers come from http://www.ekospolitics.com/index.php/2015/10/marginally-significant-narrowing-of-liberal-lead/
        # list order: libs, cons, ndp, greens, bloc, unknown (this will be randomized)
        self.liberal = [0., 0.12, .45, .1, .03, .3]
        self.cons = [.17, 0., 0.10, 0.08, 0.0, 0.75]
        self.ndp = [0.53, 0.06, 0.0, 0.13, 0.06, 0.23]
        self.green = [0.16, 0.08, 0.22, 0.0, 0.15, 0.39]
        self.bloc = [0.16, 0.19, 0.29, 0.06, 0.0, 0.26]
        self.independent = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]


def local_contest(data, districs, sc):
    # a function that goes through a run-off process using the second choices as applied to each district
    winners = []
    for key in districts:
        print key
        vote_percentage = []
        local_winner = []
        local_winner.append(runoff(data[key], sc))
##        for num_parties in range(len(data[key])):
##            party = data[key][num_parties][0]
##            percentage = float(data[key][num_parties][1])/data[key][num_parties][2]
                
        #  print local_winner
        winners.append(local_winner)
    return winners


def runoff(local_race, sc):
    
    local_winner = 0
    lib = 'Liberal'
    con = 'Conservative'
    ndp = 'NDP-New Democratic Party'
    gpc = 'Green Party'
    bloc = 'Bloc Québécois'
    dropped = []
    while local_winner == 0:
        for num_parties in range(len(local_race)):
            party = local_race[num_parties][0]
            percentage = float(local_race[num_parties][1])/local_race[num_parties][2]
        for i in range(len(local_race)):
            if float(local_race[i][1])/local_race[i][2] >= 0.5000: # Check to see if anyone has more than 50%, they are local winner
                local_winner = local_race[i]
                #find biggest loser
        if len(local_race) == 1:
            local_winner = local_race[0]
        if local_winner == 0:
            print local_race
            big_l_val = min([x[1] for x in local_race])
            big_l_ind = [i for i in range(len(local_race)) if local_race[i][1] == big_l_val]
            big_l_ind = big_l_ind[0]
            dropped.append(local_race[big_l_ind][0])
            if dropped[-1] == lib:
                dist = sc.liberal
            elif dropped[-1] == con:
                dist = sc.cons
            elif dropped[-1] == ndp:
                dist = sc.ndp
            elif dropped[-1] == gpc:
                dist = sc.green
            elif dropped[-1] == bloc:
                dist = sc.bloc
            else:
                dist = sc.independent
            if lib not in dropped:
                lib_trans = local_race[big_l_ind][1]*dist[0]
            if con not in dropped:
                con_trans = local_race[big_l_ind][1]*dist[1]
            if ndp not in dropped:
                ndp_trans = local_race[big_l_ind][1]*dist[2]
            if gpc not in dropped:
                gpc_trans = local_race[big_l_ind][1]*dist[3]
            if bloc not in dropped:
                bloc_trans = local_race[big_l_ind][1]*dist[4]
            local_race.pop(big_l_ind)
            i -=1
            for i in range(len(local_race)):
                if local_race[i][0] == lib:
                    local_race[i][1] += lib_trans
                if local_race[i][0] == con:
                    local_race[i][1] += con_trans
                if local_race[i][0] == ndp:
                    local_race[i][1] += ndp_trans
                if local_race[i][0] == gpc:
                    local_race[i][1] += gpc_trans
                if local_race[i][0] == bloc:
                    local_race[i][1] += bloc_trans
    return local_winner
                    
if __name__ =="__main__":

    election_data, districts = data_load()
    sc = second_choice()
    print election_data[districts[0]], float(election_data[districts[0]][0][1])/election_data[districts[0]][0][2]
    winners = local_contest(election_data, districts, sc)
    
