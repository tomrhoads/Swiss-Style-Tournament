#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    query = "UPDATE Players SET score = 0, matches = 0;"
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    query = "DELETE FROM Players;"
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    query = "SELECT count(*) FROM Players;"
    c.execute(query)
    count = c.fetchone()[0]
    db.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    query = "INSERT INTO Players (playername, score, matches) \
    VALUES (%s,0,0);"
    c.execute(query, (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    playerwins = "SELECT Players.id, Players.playername, Players.score,\
    Players.matches \
    FROM Players \
    ORDER BY Players.score DESC;"
    c.execute(playerwins)
    leaderboard = [(row[0], row[1], row[2], row[3])
                   for row in c.fetchall()]
    db.close()
    return leaderboard


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
    winner:  the id number of the player who won
    loser:  the id number of the player who lost
    """
    winscore = 1
    lossscore = 0
    db = connect()
    c = db.cursor()
    won = "UPDATE Players SET score = score + 1, matches = matches + 1 \
    WHERE Players.id = %s"
    lost = "UPDATE Players SET matches = matches + 1 \
    WHERE Players.id = %s"
    c.execute(won, (winner,))
    c.execute(lost, (loser,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name"""
    playerstats = playerStandings()
    pairings = []
    i = 0
    while (i < len(playerstats)):
        player1id = playerstats[i][0]
        player1name = playerstats[i][1]
        player2id = playerstats[i+1][0]
        player2name = playerstats[i+1][1]
        pairings.append((player1id, player1name, player2id, player2name))
        i += 2
    return pairings
