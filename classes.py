import random
import time

random.seed(time.time())


class Base:
    def __init__(self, *args, **kwargs) -> None:
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)
        else:
            pass

class TeamAdditionError(Exception):
    pass

class Team(Base):
    count = 1
    _instances = []

    def __new__(cls, *args, **kwargs):
        for instance in cls._instances:
            if instance._compare(args, kwargs):
                return instance
        instance = super(Team, cls).__new__(cls)
        cls._instances.append(instance)
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = 0
        self.goals = 0
        try:
            if self.name and not self.abv_name:
                self.abv_name = self.name[:3].upper()
        except Exception:
            self.name = f"New Team {Team.count}"
            self.abv_name = f"NT{Team.count}"
            Team.count += 1

    def _compare(self, args, kwargs):
        return self.name == kwargs.get('name')

    def __repr__(self) -> str:
        return f"{self.name} ({self.abv_name})"

class Competition:
    def __init__(self, type, totalTeams, teams):
        self.type = type
        self.totalTeams = totalTeams
        self.teamsCount = 0
        self.teams = []
        self.matches = []
        if teams and isinstance(teams, list):
            for team in teams:
                if not isinstance(team, Team):
                    raise TeamAdditionError(f"Team {team} is not an instance of the Team class.")
                elif self.teamsCount >= self.totalTeams:
                    raise TeamAdditionError(f"Maximum team count reached. Cannot add {team}.")
                elif team in self.teams:
                    raise TeamAdditionError(f"Team {team} is already added to the competition.")
                else:
                    self.teams.append(team)
                    self.teamsCount += 1
                
    def registerTeam(self, team):
        if not isinstance(team, Team):
            raise TeamAdditionError(f"Team {team} is not an instance of the Team class.")
        elif self.teamsCount >= self.totalTeams:
            raise TeamAdditionError(f"Maximum team count reached. Cannot add {team}.")
        elif team in self.teams:
            raise TeamAdditionError(f"Team {team} is already added to the competition.")
        else:
            self.teams.append(team)
            self.teamsCount += 1


    def _registrationDone(self):
        return self.teamsCount == self.totalTeams
    
    def generateMatches(self):
        if Competition._registrationDone(self):
            for home in self.teams[:]:
                remainingTeams = self.teams[:]
                for i in range(self.totalTeams):
                    if not remainingTeams:
                        break
                    away = random.choice(remainingTeams)
                    remainingTeams.remove(away)
                    if home is not away:
                        new_match = Match(home, away)
                        self.matches.append(new_match)
            return self.matches
        else:
            raise Exception("Registration of teams not completed yet")


    def getMatches(self, team):
        matches = []
        if len(self.matches) != 0:
            for match in self.matches:
                if match.home == team or match.away == team:
                    matches.append(match)
        else:
            print(f"No matches for {team}")
        return matches
    
    def getTable(self, display=False):
        self.teams.sort(key=lambda x: (-x.points, -x.goals, x.name))
        if display:
            print(f"No.\tTeam\t\t\t\tPTS\t\tGD")
            print("----\t----\t\t\t\t----\t\t-----")
            for i, team in enumerate(self.teams[:]):
                setattr(team, 'position', i+1)
                print(f"{i+1}.\t{str(team):<20}\t\t{team.points}\t\t {team.goals}")
        return self.teams


    def getWeekSchedule(self):
        thisWeekMatches = []
        count = 0
        while len(thisWeekMatches) < self.totalTeams / 2:
            error = False
            i = 0
            totalmatches = self.totalTeams * 2 -2
            available_matches = self.teams[:]
            team = self.teams[count % self.totalTeams]
            match = self.getMatches(team)[count % totalmatches]
            
            while True:
                if not Competition._check_validity(match, thisWeekMatches):
                    try:
                        match = self.getMatches(team)[i]
                        i += 1
                        if i == totalmatches:
                            # print('broke')
                            error = True
                            break
                        continue
                    except IndexError:
                        error = True
                        break
                else:
                    break
            if error is False:
                if not match.done:
                    thisWeekMatches.append(match)
                
            count += 1

        return thisWeekMatches
    

    def _check_validity(match, matches):
        for m in matches:
            if match is m or match.away == m.home or match.home == m.away or match.home == m.home or match.away == m.away:
                return False
        return True


class Score:
    def __init__(self, home, away, result):
        if home and isinstance(home, Team):
            self.home = home
        if away and isinstance(away, Team):
            self.away = away
        if result and isinstance(result, list) and len(result) == 2:
            self.result = result

    def givePoints(self):
        if self.result[0] > self.result[1]:
            self.home.points += 3
        elif self.result[0] == self.result[1]:
            self.home.points += 1
            self.away.points += 1
        else:
            self.away.points += 3
    
    def giveGoal(self):
        self.home.goals += self.result[0] - self.result[1]
        self.away.goals += self.result[1] - self.result[0]

    def __repr__(self) -> str:
        return f"{str(self.home):<20} ({self.result[0]}) - ({self.result[1]}) {str(self.away):>20}"


class Match:
    _count = 1
    _instances = []

    def __new__(cls, home, away):
        for instance in cls._instances:
            if instance._compare(home, away):
                return instance
        instance = super(Match, cls).__new__(cls)
        cls._instances.append(instance)
        return instance
        
    def __init__(self, home, away):
        
        if home and isinstance(home, Team):
            self.home = home
        else:
            raise ValueError("Home team should be of type Team")
        if away and isinstance(away, Team):
            self.away = away
        else:
            raise ValueError("Away team should be of type Team")
        self.done = False
        self.name = f"Match {Match._count}"
        Match._count += 1

    def getresult(self):
        if self.done == False:
            self.result = [random.randint(0, 5), random.randint(0, 5)]
            self.done = True
            return self.result
        return self.result
    
    def _compare(self, home, away):
        return (self.home, self.away) == (home, away)
    
    def __repr__(self) -> str:
        return f"{self.name}:: {self.home} Vs {self.away}"
    