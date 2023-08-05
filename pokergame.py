import copy
import importlib
import random

def limit(num, minimum=1, maximum=255):
  """Limits input 'num' between minimum and maximum values.
  Default minimum value is 1 and maximum value is 255."""
  return max(min(num, maximum), minimum)

#A player class - contains name, amount of cash and active-states
class player:

    def __init__(self,name,initMoney):
        self.cash = initMoney
        self.chipsInPlay = 0 #How much has this player betted?
        self.name = name

        #Data Related To Active-States
        self.activeGame = 1 #Does it exist at all? Reasons for non-existance: No cash, no chips and no possibility of re-joining
        self.activeRound = 1 #Does it exist in this round? Reasons for 0: No cash, no chips, folding
        self.activeTurn = 0 #Is it active this turn? Reasons for 0: Another player is active

    #If the player has no money and no stake in the pot, they're out of the game
    def checkIfOut(self):
        if self.cash == 0 and self.chipsInPlay == 0:
            self.activeRound = 0
            self.activeTurn = 0
            self.activeGame = 0

    #Checks if the player has enough money to bet the blind and bets - doesn't check activeTurn - Doesn't change: chipsInPlay,activeTurn
    def blindMoneyBet(self,blind):
        if blind<self.cash or blind == self.cash:
            self.cash = self.cash - blind
            print(f"\nPlayer: {self.name} just bet the blind of {blind}$\nCurrent balance: {self.cash}$\nCurrent money in pot: {self.chipsInPlay}$\n")
            return
        else:
            print("blind()-Player: Imagine an all-in function here")

    #Checks if the player has enough to bet and bets money for the player, the money goes into the pot
    #Checks: If allActiveStates = 1 - Changes: activeTurn = 0*,chipsInPlay = +bet - *: unless endTurn = 0
    def regularMoneyBet(self,moneyChange,min =0,endTurn = 1):
        if self.activeGame == 1 and self.activeRound == 1 and self.activeTurn == 1:
            betLimit = limit(moneyChange,min,self.cash)
            if moneyChange == betLimit: #He cannot bet more, than he has
                self.cash = self.cash - moneyChange
                self.chipsInPlay = self.chipsInPlay + moneyChange
                print(f"\nPlayer: {self.name} just bet {moneyChange}$\nCurrent balance: {self.cash}$\nCurrent money in pot: {self.chipsInPlay}$\n")
                if endTurn == 1:
                    self.activeTurn = 0
            elif moneyChange != betLimit:
                print(f"{self.name} tried to bet: {moneyChange}$, while he only has: {self.cash}$")
        elif self.activeGame != 0 or self.activeRound != 0 or self.activeTurn != 0:
            print(f"Player: {self.name} is not active in the following ways:\nGame: {self.activeGame}\nRound: {self.activeRound}\nTurn: {self.activeTurn}")

    #Turns activeRound = 0
    def fold(self):
        self.activeRound = 0
        print(f"{self.name} just folded")

    def __str__(self):
            return f"\nName: {self.name} \nCash left: {self.cash}\nMoney in pot: {self.chipsInPlay}\nGame active = {self.activeGame}\nRound active = {self.activeRound}\nTurn active = {self.activeTurn}"


#Contains previous turns
class gameRound:
    def __init__(self,players,startingPlayer = 0,bigBlind = 0, smallBlind = 0, tableSize = 5):

        #Data related to players in the round
        self.startingPlayer = startingPlayer #Given by the game object at initialization (Object)
        self.roundPlayers = players #Players who're still in play in the round (list with player objects)
        self.playersActiveRound = len(players) #Amount of players in the game (integer)

        #Data related to turns
        self.turns = []
        self.lastTurnType = 0 #For keeping tack of possible actions (Integer)
        self.latestBet = 0 #The last bet, that was made in this round - To decide how much to raise or check (integer)
        self.turnNumber = 0 #For keeping track of which turn number, this is (integer)

        #Data related to who is active this turn
        self.activeThisTurn = 0 #Which player is active (object)
        self.activeThisTurnNumber = 0 #What number in the list of active players is the current active player (integer)
        self.playersActiveTurn = 0 #How many players have self.activeTurn = 1 - used for debugging (integer)

        #Data related to initial setup
        self.bigBlind = bigBlind #The bet that the first activeThisTurn has to bet (integer)
        self.smallBlind = smallBlind #The bet that roundPlayers[activeThisTurnNumber -1] has to bet i.e Player to the left of BBL. (integer)
        self.saveTurn() #Saves the initial player data at turn X (list with player objects)
        self.tableSize = tableSize

    #Debug methods below

    #Finds how many players are active - integer, not the actual player objects
    def findPlayersActiveTurn(self):
        g = 0
        for x in self.roundPlayers:
            if x.activeTurn == 1:
                g += g
        self.playersActiveTurn = g

    #Sets the person who is active this turn, and sets the previous active player as inactive (turn)
    def setActiveTurn(self,playerName): #Startingplayer, which is the optional argument in the game object, which is passed down into playerName is by default 0
        if type(self.activeThisTurn) == player:
            self.activeThisTurn.activeTurn = 0

        if playerName == 0: #If no name is given
            x = self.roundPlayers[random.randint(0, self.playersActiveRound - 1)]
            self.activeThisTurn = x
            self.findActiveNumber()
            x.activeTurn = 1
        elif playerName != 0: #If a name is given
            for x in self.roundPlayers:
                if x.name == playerName:
                    x.activeTurn = 1
                    self.activeThisTurn = x

    #Saves the current player data as a nested list in the self.turns list
    def saveTurn(self):
        z = [] #For storing playerdata
        for x in self.roundPlayers:
            y = copy.copy(x) #Makes a copy of the player objects
            z.append(y)

        self.turns.append(0) #Adds a new index
        self.turns[self.turnNumber] = z #Turns this index into z

    #Finds the current active player's number in the turn order
    def findActiveNumber(self):
        g= -1 #List indexes start at 0
        for x in self.roundPlayers:
            g = g +1
            if x == self.activeThisTurn:
                self.activeThisTurnNumber = g
                #Make a debug such that, if there are more actives this turn, it will say so

    #Selects the closest roundActive player to the right of the current activeTurnPlayer as the next activeTurn.
    def nextActive(self):
        self.findActiveNumber()

        y = (self.activeThisTurnNumber+1)%len(self.roundPlayers) #Goes one player to the right, modulo so it restarts at 0 if y +1 is out of bounds

        for x in range(y,len(self.roundPlayers)): #x in [y;self.playersActiveRound[
            h = x%len(self.roundPlayers)
            self.roundPlayers[h].checkIfOut()

            if self.roundPlayers[h].activeRound == 1 and self.roundPlayers[h] != self.activeThisTurn: #First activeRound player to the right of this current active player
                self.roundPlayers[h].activeTurn = 1
                self.activeThisTurn = self.roundPlayers[h]
                return() #Ends it
            else:
                print(f"\nNo other active players than {self.activeThisTurn.name}")

    #Removes inactive players from the round list
    def removeInactiveRound(self):
        listOfActivePlayers = []
        for x in self.roundPlayers:
            x.checkIfOut()
            if x.activeRound == 1 and x.activeGame == 1:
                listOfActivePlayers.append(x)
        self.playersActiveRound = len(listOfActivePlayers)
        self.roundPlayers = listOfActivePlayers

    #Increments the turn by 1, changes the activeTurn player, removes inactive players and saves the player data to the turnlist
    def endTurn(self):
        self.turnNumber = self.turnNumber + 1
        self.nextActive()
        self.removeInactiveRound()
        self.saveTurn()

    def startingTurn(self):
        self.setActiveTurn(self.startingPlayer) #Starting player is provided by the game-object whenever a round is initialized
        self.activeThisTurn.blindMoneyBet(self.bigBlind) #Blind instead of moneybet, as there are no restrictions in terms of active status
        print(self.activeThisTurnNumber)
        self.roundPlayers[self.activeThisTurnNumber-1].blindMoneyBet(self.smallBlind) #This works because -1 = highest number, so if 0 -1 = -1 = highest index in the list


class game:
    def __init__(self,initPlayers,startingPlayer = 0,bigBlind = 25, smallBlind = 10):
        self.players = initPlayers
        self.updateValuesPlayersSum()
        self.playersCash = self.sumList[0] #How Much Money The Players Have excl. In Pot
        self.playersActiveGame = self.sumList[1] #How Many Players Are Active In The Game (int)
        self.chipsInPlay = self.sumList[2] #The Current Pot Size
        self.bigBlind = bigBlind
        self.smallBlind = smallBlind
        self.startingPlayer = startingPlayer #The initial starting player for this or the next round
        self.startRound() #Creates a gameRound object, chooses the initial starting player and makes the players bet BBL and SBL
        self.currentRound

    #Sums up the amount of cash held by all players and returns a float
    def cashPlayersSum(self,players):
        sum = 0
        for x in players:
            sum = x.cash + sum
        return sum

    #Sums the amount of active players and returns an integer
    def playersActiveGameSum(self,players):
        sum = 0
        for x in players:
            sum = x.activeGame + sum
        return sum

    #Sums the chips in play AKA the Pot and returns number
    def chipsInPlayPlayersSum(self,players):
        sum = 0
        for x in players:
            sum = x.chipsInPlay + sum
        return sum

    # Sums up all sum-values and adds them to a list
    def valuesPlayersSum(self,players):
        totalSum = []
        totalCash = self.cashPlayersSum(players)
        totalActivesGame = self.playersActiveGameSum(players)
        totalChipsInPlay = self.chipsInPlayPlayersSum(players)

        totalSum.append(totalCash)
        totalSum.append(totalActivesGame)
        totalSum.append(totalChipsInPlay)

        return totalSum

    #Updates the game's player-based sums
    def updateValuesPlayersSum(self):

        totalSum = self.valuesPlayersSum(self.players)

        self.sumList = totalSum
        self.playersCash = self.sumList[0]
        self.totalActivesGame = self.sumList[1]
        self.chipsInPlay = self.sumList[2]

    #Sets a person to be active in the round, and makes the first active player bet, and the player left to him on the list bet.
    def startRound(self):
        self.currentRound = gameRound(self.players,self.startingPlayer,self.bigBlind,self.smallBlind)

    def gameEndTurn(self):
        self.currentRound.endTurn()
    #Needs a function that continously allows for each active player to choose an action, unless all - 1 have folded, all have checked, or all have called the bet enough times to end round

    def __str__(self):
        return f"\nPlayers in game : {str(self.players)} \nActive players: {str(self.playersActiveGame)} \nPot size: {str(self.chipsInPlay)} \nCash on hand:  {str(self.playersCash)} "


def testNoob():
    player0 = player("player0",125)
    player1 = player("player1",125)
    player2 = player("player2",125)

    players = [player0,player1,player2]

    aGame = game(players)
    return aGame
