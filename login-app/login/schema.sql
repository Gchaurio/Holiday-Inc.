DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS logger;
DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS car;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  password TEXT NOT NULL,
  project INTEGER,
  role TEXT NOT NULL,
  verified INTEGER
);

CREATE TABLE project (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  description TEXT UNIQUE NOT NULL,
  init DATE NOT NULL,
  end DATE NOT NULL,
  status INTEGER NOT NULL
);

CREATE TABLE logger (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  event TEXT NOT NULL,
  date TEXT NOT NULL,
  user TEXT NOT NULL
);

CREATE TABLE client (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  dni TEXT UNIQUE NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  birthdate DATE NOT NULL,
  phone TEXT NOT NULL,
  email TEXT NOT NULL,
  address TEXT NOT NULL
);

CREATE TABLE car (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  plaque TEXT UNIQUE NOT NULL,
  brand TEXT NOT NULL,
  model TEXT NOT NULL,
  year INTEGER NOT NULL,
  serial_car TEXT UNIQUE NOT NULL,
  serial_mot TEXT UNIQUE NOT NULL,
  color TEXT NOT NULL,
  issue TEXT NOT NULL,
  owner TEXT NOT NULL
);