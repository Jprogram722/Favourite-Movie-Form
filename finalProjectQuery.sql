/*
	Authors: Dexter, Jared, and Chanyoung
	Description: This script will create a database to store a users info along with their favourite movie and the facts about that movie.
	some of the facts include:
		director
		lead actor
		genre
		release year
		and the movies title

	The data that is inserted into this database is linked to access which will then analyzed through reports
*/


-- creates the database for users favourite movie
CREATE DATABASE FavMovie;
GO -- This statement allows the use of a database directly after creation

-- uses the database
USE FavMovie;

-- creates the region table which will store continents
CREATE TABLE region (
	pk_region_Id INT IDENTITY(1, 1),
	region_name VARCHAR(255) NOT NULL,
	-- creates primary key constraint
	CONSTRAINT PK_region PRIMARY KEY (pk_region_Id)
);

-- creates the genre table. stores one genre that the movie fits into
CREATE TABLE genre (
	pk_genre_Id INT IDENTITY (1, 1),
	genre_name VARCHAR (255) NOT NULL,
	-- creates primary key constraint
	CONSTRAINT PK_genre PRIMARY KEY (pk_genre_Id)
);

-- creates the director table
CREATE TABLE director (
	pk_director_Id INT IDENTITY (1, 1),
	director_firstname VARCHAR (255) NOT NULL,
	director_lastname VARCHAR (255) NOT NULL,
	-- creates primary key constraint
	CONSTRAINT PK_director PRIMARY KEY (pk_director_Id)
);

-- creates the production table. stores info on the production studio
CREATE TABLE production (
	pk_production_Id INT IDENTITY (1, 1),
	production_name VARCHAR (255) NOT NULL,
	-- connects to the region table
	region_Id_fk INT,
	CONSTRAINT PK_production PRIMARY KEY (pk_production_Id),
	CONSTRAINT FK_production_region FOREIGN KEY (region_Id_fk) REFERENCES region (pk_region_Id)
);

-- creates the lead actor table
CREATE TABLE lead_actor (
	pk_lead_actor_Id INT IDENTITY (1, 1),
	lead_actor_firstname VARCHAR (255) NOT NULL,
	lead_actor_lastname VARCHAR (255) NOT NULL,
	-- creates primary key constraint
	CONSTRAINT PK_lead_actor PRIMARY KEY (pk_lead_actor_Id)
);

-- creates the viewer table
CREATE TABLE viewer (
	pk_viewer_Id INT IDENTITY (1, 1),
	viewer_firstname VARCHAR (255) NOT NULL,
	viewer_lastname VARCHAR (255) NOT NULL,
	viewer_age INT CHECK(viewer_age >= 18 AND viewer_age <= 99) NOT NULL,
	viewer_gender CHAR(10) NOT NULL,
	-- connects to the region table
	region_Id_fk INT,
	-- creates primary key constraint
	CONSTRAINT PK_viewer PRIMARY KEY (pk_viewer_Id),
	-- connects to the region table with a foreign key constraint
	CONSTRAINT FK_viewer_region FOREIGN KEY (region_Id_fk) REFERENCES region (pk_region_Id)
);

-- creates the movies table
CREATE TABLE movie (
	pk_movie_Id INT IDENTITY (1, 1),
	movie_title VARCHAR(255) NOT NULL,
	movie_release_year INT CHECK (movie_release_year >= 1900 AND movie_release_year <= 2023) ,
	-- creates primary key constraint
	CONSTRAINT PK_movie PRIMARY KEY (pk_movie_Id),
	genre_Id_fk INT,
	-- connects to the genre table with foreign key constraint
	-- movies can fall into genres that determined over time
	CONSTRAINT FK_genre FOREIGN KEY (genre_Id_fk) REFERENCES genre (pk_genre_Id) ON UPDATE CASCADE,
	-- connects to the director table with foreign key constraint
	-- lead actors can  change names so cascade the update
	director_Id_fk INT,
	CONSTRAINT FK_director FOREIGN KEY (director_Id_fk) REFERENCES director (pk_director_Id) ON UPDATE CASCADE,
	-- connects to the production table with foreign key constraint
	-- production studio that produced it doesn't change
	production_Id_fk INT, 
	CONSTRAINT FK_production FOREIGN KEY (production_Id_fk) REFERENCES production (pk_production_Id),
	-- connects to the lead actor table with foreign key constraint
	-- lead actors can  change names so cascade the update
	lead_actor_Id_fk INT, 
	CONSTRAINT FK_lead_actor FOREIGN KEY (lead_actor_Id_fk) REFERENCES lead_actor (pk_lead_actor_Id) ON UPDATE CASCADE
);
ALTER TABLE viewer
ADD movie_Id_fk INT NOT NULL,
	-- connects the viewer table to the movie table with foreign key constraint.
	-- if we delete the movie in the movie table then it makes sense to delete the viewer as well
	CONSTRAINT FK_movie FOREIGN KEY (movie_Id_fk) REFERENCES movie (pk_movie_Id) ON DELETE CASCADE ON UPDATE CASCADE;

-- inserts all the continents into the region table
INSERT INTO region
VALUES ('north america'),
('south america'),
('asia'),
('africa'),
('europe'),
('australia'),
('antarctica');

-- inserts all the given genres into the genre table
INSERT INTO genre
VALUES ('drama'),
('fantasy'),
('comedy'),
('action'),
('adventrue'),
('horror'),
('romance'),
('sci-fi'),
('super hero'),
('psychological thriller');

-- inserts the given directors into the director tables
INSERT INTO director
VALUES ('Nick', 'Cassavettes'),
('Clint','Eastwood'),
('James', 'Cameron'),
('Joe', 'Wright'),
('Patty', 'Jenkins'),
('Dennis', 'Villeneuve'),
('Hayao', 'Miyazaki'),
('Ridly', 'Scott'),
('Peter', 'Jackson'),
('Joaquim', 'Dos Santos'),
('Michel', 'Gondry'),
('David', 'Yates'),
('Robert', 'Zemeckis'),
('Andrzej', 'Żuławski'),
('Nahnatchka', 'Khan'),
('David', 'Fincher');

-- inserts the production studios and region foreign key into the production table
INSERT INTO production
VALUES ('20th century fox', 1),
('warner bros', 1),
('universal studios', 1),
('studio ghibli', 3),
('sony animation', 1),
('oliane productions', 5),
('anonymous content', 1),
('orion pictures', 1),
('malpaso productions', 1),
('new line cinema', 1),
('micro_scope', 1),
('good universe', 1);


-- inserts the given lead actors into the table
INSERT INTO lead_actor
VALUES ('Ryan', 'Gosling'),
('Kevin', 'Hart'),
('Clint', 'Eastwood'),
('Arnold', 'Schwarzenegger'),
('Keira', 'Knightley'),
('Gal', 'Gadot'),
('Lubna', 'Azabal'),
('Christian','Bale'),
('Matt', 'Damon'),
('Elijah', 'Wood'),
('Shameik', 'Moore'),
('Jim', 'Carrey'),
('Daniel', 'Radcliffe'),
('Micheal', 'Fox'),
('Sam', 'Neil'),
('Ali', 'Wong'),
('Brad', 'Pit');

-- inserts the given movies, production foreign key, director foreign key, lead actor foreign key, and genre foreign key into the movie table
INSERT INTO movie
VALUES ('The Notebook', 2004, 1, 1, 10, 1),
('The Bridges of Madison County', 1995, 7, 2, 9, 3),
('The Terminator', 1984, 8, 3, 8, 4),
('Pride and Prejudice', 2005, 1, 4, 3, 5),
('Wonder Woman', 2017, 9, 5, 2, 6),
('Incendies', 2010, 1, 6, 11, 7),
('Howls Moving Castle', 2004, 7, 7, 4, 8),
('The Martian', 2015, 8, 8, 1, 9),
('Lord Of The Rings: Fellowship Of The Ring', 2001, 2, 9, 10, 10),
('Spider-Man across the spider verse', 2023, 9, 10, 1, 11),
('Eternal Sunshine', 2004, 7, 11, 7, 12),
('Harry Potter and the half blood prince', 2009, 2, 12, 2, 13),
('Back to the future', 1985, 8, 13, 3, 14),
('Possession', 1981, 6, 14, 6, 15),
('Always be my maybe', 2019, 3, 15, 12, 16),
('Fight Club', 1999, 10, 16, 1, 17);


-- inserts the given viewer into, region foreign key, and movie foreign key into the viewer table
/*
  This would contain data on real people
*/
--INSERT INTO viewer
--VALUES
