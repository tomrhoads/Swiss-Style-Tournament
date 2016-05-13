-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

--Delete any old databases
DROP DATABASE IF EXISTS tournament;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Matches;
DROP TABLE IF EXISTS Scoreboard;

--Create the database tournament
CREATE DATABASE tournament;

--Connect to tournament database
\c tournament;

--Players Table
CREATE TABLE Players (
	id SERIAL PRIMARY KEY,
	playername TEXT NOT NULL,
	score INTEGER,
	matches INTEGER
	);