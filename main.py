#!/usr/bin/python3

from classes import Team, Competition, Match, Score
team = Team()
team3 = Team(name='Liverpool')
team2 = Team()
teams = [team, team2, team3]
comp = Competition('tournament', 20, teams)


print(comp.getMatches(team))
for i in range(17):
    new_team = Team()
    comp.registerTeam(new_team)
print(comp._registrationDone())

comp.generateMatches()

for i in range(38):
    for i in comp.getWeekSchedule():
        results = i.getresult()
        score = Score(i.home, i.away, results)
        print(score)
        score.giveGoal()
        score.givePoints()


table = comp.getTable(True)
print(table)
# for team in comp.teams:
#     for i in comp.getMatches(team):
#         print(i)

# for i in comp.getWeekSchedule():
#     print(i)
# print(f"{team}  {team.position}")
