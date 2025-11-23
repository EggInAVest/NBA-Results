import sys
import requests
import json
import http.client
from nba_api.stats.endpoints import leaguestandings
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leagueleaders


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

FILENAME = "data.json"
FILENAME2 = "players.json"


# Defining main function
def main():
    print(f"\n======    {bcolors.BOLD}{bcolors.OKBLUE}N{bcolors.ENDC}B{bcolors.BOLD}{bcolors.FAIL}A{bcolors.ENDC} STATS     ======")
    print("\nPlease choose...\n")
    num = input("1. Last nights results (Overview)\n"
                "2. Last nights results (Detailed)\n"
                "3. Standings\n"
                "4. Season leaders\n"
                "5. Bet scoreboard\n"
                "6. EXIT\n\n"
                "Your choice: ")
    if (int(num) == 1):
        getGameStats()
    elif (int(num) == 2):
        getDetailedStats()
    elif (int(num) == 3):
        getStandings()
    elif (int(num) == 4):
        getLeaders()
    elif (int(num) == 5):
        getBetLeaderboard()
    elif (int(num) == 6):
        print("Good bye!")
        exit()
    else:
        print("Invalid input\n")

def getGameStats():
    print(f"\n===========    {bcolors.BOLD}LAST NIGHTS STATS (OVERVIEW){bcolors.ENDC}     ===========\n")
    url = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        #with open(FILENAME, "w", encoding="utf-8") as outfile:
            #json.dump(data, outfile, indent=4, sort_keys=True, ensure_ascii=False)
        games = data["scoreboard"]["games"]
        for game in games:
            awayCity = game["awayTeam"]["teamCity"]
            homeCity = game["homeTeam"]["teamCity"]
            awayTeam = game["awayTeam"]["teamName"]
            homeTeam = game["homeTeam"]["teamName"]
            awayScore = game["awayTeam"]["score"]
            homeScore = game["homeTeam"]["score"]
            left = f"{awayCity} {awayTeam}"
            right = f"{homeCity} {homeTeam}"
            left_padded = f"{left:<25}"
            right_padded = f"{right:<10}"

            if awayScore > homeScore:
                left_out = f"{bcolors.OKGREEN}{left_padded}{bcolors.ENDC}"
                right_out = f"{bcolors.FAIL}{right_padded}{bcolors.ENDC}"
            elif homeScore > awayScore:
                left_out = f"{bcolors.FAIL}{left_padded}{bcolors.ENDC}"
                right_out = f"{bcolors.OKGREEN}{right_padded}{bcolors.ENDC}"
            else:
                left_out = left_padded
                right_out = right_padded

            print(f"{left_out} {awayScore:>3} - {homeScore:<10} {right_out}")

def getDetailedStats():
    print(f"\n===========    {bcolors.BOLD}LAST NIGHTS STATS (DETAILED){bcolors.ENDC}     ===========\n")
    scoreboardUrl = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"
    response = requests.get(scoreboardUrl)
    if (response.status_code == 200):
        scoreData = response.json()
        games = scoreData["scoreboard"]["games"]
        gameCount = 0
        for game in games:
            gameId = game["gameId"]
            boxScoreUrl = f"https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{gameId}.json"
            boxResponse = requests.get(boxScoreUrl)
            if boxResponse.status_code == 200:
                gameCount += 1
                boxData = boxResponse.json()
                with open(FILENAME2, "w", encoding="utf-8") as outfile:
                    json.dump(boxData, outfile, indent=4, sort_keys=True, ensure_ascii=False)
                awayTeam = boxData["game"]["awayTeam"]
                awayTeamCode = awayTeam["teamTricode"]
                homeTeam = boxData["game"]["homeTeam"]
                homeTeamCode = homeTeam["teamTricode"]
                awayTeamScore = awayTeam["score"]
                homeTeamScore = homeTeam["score"]

                awayStatus = "W" if awayTeamScore > homeTeamScore else "L"
                homeStatus = "W" if homeTeamScore > awayTeamScore else "L"

                print(f"AWAY TEAM {awayTeamCode} {awayTeamScore} {awayStatus}\n")
                print(f"{'NAME':<25} {'MIN':>4} {'PTS':>4} {'REB':>4} {'AST':>4} {'BLK':>4} {'STL':>4} {'TO':>4} {'FG':>8} {'3P':>8} {'FG%':>6}")
                for player in awayTeam["players"]:
                    name = player["name"]
                    status = player.get("status", "")
                    played = player.get("played", "0")
                    if status == "ACTIVE" and played == "1":
                        minutes = player["statistics"]["minutesCalculated"]
                        mins = "".join(c for c in minutes if c.isdigit())
                        points = player["statistics"]["points"]
                        rebounds = player["statistics"]["reboundsTotal"]
                        assists = player["statistics"]["assists"]
                        blocks = player["statistics"]["blocks"]
                        steals = player["statistics"]["steals"]
                        turnovers = player["statistics"]["turnovers"]
                        FGM = player["statistics"]["fieldGoalsMade"]
                        FGA = player["statistics"]["fieldGoalsAttempted"]
                        FG = str(FGM) + "/" + str(FGA)
                        TPM = player["statistics"]["threePointersMade"]
                        TPA = player["statistics"]["threePointersAttempted"]
                        threes = str(TPM) + "/" + str(TPA)
                        FGP = player["statistics"]["fieldGoalsPercentage"]
                        FGP = FGP * 100
                        FGP = round(FGP, 2)
                        print(f"{name:<25} {mins:>4} {points:>4} {rebounds:>4} {assists:>4} {blocks:>4} {steals:>4} {turnovers:>4} {FG:>8} {threes:>8} {FGP:>6}")
                    else:
                        reason = player.get("notPlayingReason", "DID NOT PLAY")
                        print(f"{name:<24}   DNP {reason}")
                print()
                print(f"HOME TEAM {homeTeamCode} {homeTeamScore} {homeStatus}\n")
                print(f"{'NAME':<25} {'MIN':>4} {'PTS':>4} {'REB':>4} {'AST':>4} {'BLK':>4} {'STL':>4} {'TO':>4} {'FG':>8} {'3P':>8} {'FG%':>6}")
                for player in homeTeam["players"]:
                    name = player["name"]
                    status = player.get("status", "")
                    played = player.get("played", "0")
                    if status == "ACTIVE" and played == "1":
                        minutes = player["statistics"]["minutesCalculated"]
                        mins = "".join(c for c in minutes if c.isdigit())  
                        points = player["statistics"]["points"]
                        rebounds = player["statistics"]["reboundsTotal"]
                        assists = player["statistics"]["assists"]
                        blocks = player["statistics"]["blocks"]
                        steals = player["statistics"]["steals"]
                        turnovers = player["statistics"]["turnovers"]
                        FGM = player["statistics"]["fieldGoalsMade"]
                        FGA = player["statistics"]["fieldGoalsAttempted"]
                        FG = str(FGM) + "/" + str(FGA)
                        TPM = player["statistics"]["threePointersMade"]
                        TPA = player["statistics"]["threePointersAttempted"]
                        threes = str(TPM) + "/" + str(TPA)
                        FGP = player["statistics"]["fieldGoalsPercentage"]
                        FGP = FGP * 100
                        FGP = round(FGP, 2)
                        print(f"{name:<25} {mins:>4} {points:>4} {rebounds:>4} {assists:>4} {blocks:>4} {steals:>4} {turnovers:>4} {FG:>8} {threes:>8} {FGP:>6}")
                    else:
                        reason = player.get("notPlayingReason", "DID NOT PLAY")
                        print(f"{name:<24}   DNP {reason}")
                print(80 * "-")   
        if gameCount == 0:
            print("No games started yet")

def getStandings():
    print(f"\n===========    {bcolors.BOLD}SEASON STANDINGS{bcolors.ENDC}     ===========\n")
    
    class Team:
        def __init__(self, name, wins, losses):
            self.name = name
            self.wins = wins
            self.losses = losses

    standings = leaguestandings.LeagueStandings(
        league_id="00",
        season="2025-26",
        season_type="Regular Season"
    )

    dataFrame = standings.get_data_frames()[0]

    westTeams = []
    eastTeams = []

    for index, row in dataFrame.iterrows():
        teamName = row["TeamCity"] + " " + row["TeamName"]
        wins = int(row["WINS"])
        losses = int(row["LOSSES"])
        if row["Conference"] == "West":
            westTeams.append(Team(teamName, wins, losses))
        else:
            eastTeams.append(Team(teamName, wins, losses))

    westTeams.sort(key=lambda x: x.wins, reverse=True)
    eastTeams.sort(key=lambda x: x.wins, reverse=True)

    print("Western Conference\n")
    for team in westTeams:
        print(f"{team.name:<24} {team.wins:>4} - {team.losses}")
    print()
    print("Easter Conference\n")
    for team in eastTeams:
        print(f"{team.name:<24} {team.wins:>4} - {team.losses}")

def getLeaders():
    print(f"\n===========    {bcolors.BOLD}LEAGUE LEADERS{bcolors.ENDC}     ===========\n")
    
    statCategories = [
        ("PTS", "Points per game"),
        ("REB", "Rebounds per game"),
        ("AST", "Assists per game"),
        ("BLK", "Blocks per game"),
        ("STL", "Steals per game")
    ]
    
    for statShort, statName in statCategories:
        leaders = leagueleaders.LeagueLeaders(
        league_id="00",
        per_mode48="PerGame",
        scope="RS",
        season="2025-26",
        season_type_all_star="Regular Season",
        stat_category_abbreviation=statShort
        )

        data = leaders.get_data_frames()[0].head(5)
        print(f"\n-------  {statName}  -------\n")
        for _, row in data.iterrows():
            print(f"{row['RANK']:<2} {row['PLAYER']:<24} {row[statShort]:>4}")


def getBetLeaderboard():
    print(f"\n===========    {bcolors.BOLD}BET LEADERBOARD{bcolors.ENDC}     ===========\n")

    class Team:
        def __init__(self, name: str = "", points: int = 0):
            self.name = name
            self.points = points

    class Player:
        def __init__(self, name: str, winner1: Team, winner2: Team, loser1: Team, loser2: Team):
            self.name = name
            self.winner1 = winner1
            self.winner2 = winner2
            self.loser1 = loser1
            self.loser2 = loser2
            self.totalPoints = 0
    
    def scorePlayer(player: Player, teamName: str, wins: int, losses: int):
        if teamName == player.winner1.name:
            player.winner1.points = wins
        elif teamName == player.winner2.name:
            player.winner2.points = wins
        elif teamName == player.loser1.name:
            player.loser1.points = losses
        elif teamName == player.loser2.name:
            player.loser2.points = losses

        player.totalPoints = player.winner1.points + player.winner2.points + player.loser1.points + player.loser2.points

    standings = leaguestandings.LeagueStandings(
        league_id="00",
        season="2025-26",
        season_type="Regular Season"
    )

    dataFrame = standings.get_data_frames()[0]

    Roni = Player("Roni",
                      Team("Oklahoma City Thunder", 0),
                      Team("New York Knicks", 0),
                      Team("New Orleans Pelicans", 0),
                      Team("Philadelphia 76ers", 0),
                      )
    Rasmus = Player("Rasmus",
                      Team("Cleveland Cavaliers", 0),
                      Team("Minnesota Timberwolves", 0),
                      Team("Charlotte Hornets", 0),
                      Team("Phoenix Suns", 0),
                      )
    Tony = Player("Tony",
                      Team("Dallas Mavericks", 0),
                      Team("Milwaukee Bucks", 0),
                      Team("Toronto Raptors", 0),
                      Team("Washington Wizards", 0),
                      )
    Sakari = Player("Sakari",
                      Team("Houston Rockets", 0),
                      Team("Orlando Magic", 0),
                      Team("Utah Jazz", 0),
                      Team("Chicago Bulls", 0),
                      )
    Tomi = Player("Tomi",
                      Team("Denver Nuggets", 0),
                      Team("Los Angeles Lakers", 0),
                      Team("Brooklyn Nets", 0),
                      Team("Boston Celtics", 0),
                      )
    
    for index, row in dataFrame.iterrows():
        teamName = row["TeamCity"] + " " + row["TeamName"]

        # Check Ronis teams
        if teamName in (Roni.winner1.name, Roni.winner2.name, Roni.loser1.name, Roni.loser2.name):
            teamWins = int(row["WINS"])
            teamLosses = int(row["LOSSES"])
            scorePlayer(Roni, teamName, teamWins, teamLosses)
        
        # Check Rasmus teams
        elif teamName in (Rasmus.winner1.name, Rasmus.winner2.name, Rasmus.loser1.name, Rasmus.loser2.name):
            teamWins = int(row["WINS"])
            teamLosses = int(row["LOSSES"])
            scorePlayer(Rasmus, teamName, teamWins, teamLosses)
        # Check Tonys teams
        elif teamName in (Tony.winner1.name, Tony.winner2.name, Tony.loser1.name, Tony.loser2.name):
            teamWins = int(row["WINS"])
            teamLosses = int(row["LOSSES"])
            scorePlayer(Tony, teamName, teamWins, teamLosses)

        # Check Sakaris teams
        elif teamName in (Sakari.winner1.name, Sakari.winner2.name, Sakari.loser1.name, Sakari.loser2.name):
            teamWins = int(row["WINS"])
            teamLosses = int(row["LOSSES"])
            scorePlayer(Sakari, teamName, teamWins, teamLosses)
        
        # Check Tomis teams
        elif teamName in (Tomi.winner1.name, Tomi.winner2.name, Tomi.loser1.name, Tomi.loser2.name):
            teamWins = int(row["WINS"])
            teamLosses = int(row["LOSSES"])
            scorePlayer(Tomi, teamName, teamWins, teamLosses)

        leaderBoard:dict[str, int] = {Roni.name:Roni.totalPoints,
                            Rasmus.name:Rasmus.totalPoints,
                            Tony.name:Tony.totalPoints,
                            Sakari.name:Sakari.totalPoints,
                            Tomi.name:Tomi.totalPoints}
    
    print("\n-------  Ronis teams  -------\n")
    print("Winners")
    print(f"{Roni.winner1.name:<25} {Roni.winner1.points:>3}")
    print(f"{Roni.winner2.name:<25} {Roni.winner2.points:>3}")
    print("\nLoosers")
    print(f"{Roni.loser1.name:<25} {Roni.loser1.points:>3}")
    print(f"{Roni.loser2.name:<25} {Roni.loser2.points:>3}")
    print(f"\nTotal points {Roni.totalPoints:>16}")

    print("\n-------  Rasmus teams  -------\n")
    print("Winners")
    print(f"{Rasmus.winner1.name:<25} {Rasmus.winner1.points:>3}")
    print(f"{Rasmus.winner2.name:<25} {Rasmus.winner2.points:>3}")
    print("\nLoosers")
    print(f"{Rasmus.loser1.name:<25} {Rasmus.loser1.points:>3}")
    print(f"{Rasmus.loser2.name:<25} {Rasmus.loser2.points:>3}")
    print(f"\nTotal points {Rasmus.totalPoints:>16}")

    print("\n-------  Tonys teams  -------\n")
    print("Winners")
    print(f"{Tony.winner1.name:<25} {Tony.winner1.points:>3}")
    print(f"{Tony.winner2.name:<25} {Tony.winner2.points:>3}")
    print("\nLoosers")
    print(f"{Tony.loser1.name:<25} {Tony.loser1.points:>3}")
    print(f"{Tony.loser2.name:<25} {Tony.loser2.points:>3}")
    print(f"\nTotal points {Tony.totalPoints:>16}")

    print("\n-------  Sakaris teams  -------\n")
    print("Winners")
    print(f"{Sakari.winner1.name:<25} {Sakari.winner1.points:>3}")
    print(f"{Sakari.winner2.name:<25} {Sakari.winner2.points:>3}")
    print("\nLoosers")
    print(f"{Sakari.loser1.name:<25} {Sakari.loser1.points:>3}")
    print(f"{Sakari.loser2.name:<25} {Sakari.loser2.points:>3}")
    print(f"\nTotal points {Sakari.totalPoints:>16}")

    print("\n-------  Tomis teams  -------\n")
    print("Winners")
    print(f"{Tomi.winner1.name:<25} {Tomi.winner1.points:>3}")
    print(f"{Tomi.winner2.name:<25} {Tomi.winner2.points:>3}")
    print("\nLoosers")
    print(f"{Tomi.loser1.name:<25} {Tomi.loser1.points:>3}")
    print(f"{Tomi.loser2.name:<25} {Tomi.loser2.points:>3}")
    print(f"\nTotal points {Tomi.totalPoints:>16}")


    sortedLeaderboard = sorted(leaderBoard.items(), key=lambda item: item[1], reverse=True)
    position = 1
    prizeMoney = 0

    print("\n======     LEADERBOARD     ======\n")
    for name, points in sortedLeaderboard:
        print(f"{position}. {name:<10} {points:>3} pts")
        if position == 1:
            leaderPoints = points
            leaderName = name
        else:
            prizeMoney = prizeMoney + (leaderPoints - points)
        position += 1
    print(f"\nCurrent winnings for {leaderName}: {prizeMoney}€\n")

# Using the special variable
# __name__
if __name__=="__main__":
    main()
