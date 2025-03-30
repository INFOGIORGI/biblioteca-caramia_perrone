DROP TABLE IF EXISTS Noleggi;
DROP TABLE IF EXISTS Libri;
DROP TABLE IF EXISTS Autori;
DROP TABLE IF EXISTS Utenti;

-- Creazione tabella Autori
CREATE TABLE IF NOT EXISTS Autori (
    idAutore VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(255),
    cognome VARCHAR(255),
    nazionalità VARCHAR(255),
    dataNascita DATE,
    dataMorte DATE
);

-- Creazione tabella Libri
CREATE TABLE IF NOT EXISTS Libri (
    isbn VARCHAR(13) PRIMARY KEY,
    titolo VARCHAR(255),
    idAutore VARCHAR(255),
    genere VARCHAR(255),
    annoUscita DATE,
    casaEditrice VARCHAR(255),
    noleggio BOOLEAN,
    conteggioRicerche INT DEFAULT 0,
    FOREIGN KEY (idAutore) REFERENCES Autori(idAutore)
);

-- Aggiunta di indici per ottimizzare la ricerca per titolo e autore
CREATE INDEX idx_titolo ON Libri(titolo);
CREATE INDEX idx_autore ON Libri(idAutore);

-- Creazione tabella Utenti
CREATE TABLE IF NOT EXISTS Utenti (
    idUtente VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(255),
    cognome VARCHAR(255),
    dataNascita DATE,
    email VARCHAR(255),
    telefono BIGINT, 
    indirizzo VARCHAR(255),
    pswrd VARCHAR(255),
    dataRegistrazione DATE
);

ALTER TABLE Utenti ADD COLUMN isAdmin BOOLEAN DEFAULT FALSE;

-- Creazione tabella Noleggi
CREATE TABLE IF NOT EXISTS Noleggi (
    idNoleggio VARCHAR(10) PRIMARY KEY,
    idUtente VARCHAR(10),
    isbn VARCHAR(13),
    inizioNoleggio DATE,
    fineNoleggio DATE,
    restituzione BOOLEAN,
    FOREIGN KEY (idUtente) REFERENCES Utenti(idUtente), 
    FOREIGN KEY (isbn) REFERENCES Libri(isbn)
);

ALTER TABLE Noleggi ADD COLUMN dataRestituzione DATE;

-- Creazione tabella StatisticheRicerche
CREATE TABLE IF NOT EXISTS StatisticheRicerche (
    idStatistica INT AUTO_INCREMENT PRIMARY KEY,
    genere VARCHAR(10),
    conteggio INT DEFAULT 0
);

INSERT INTO Autori (idAutore, nome, cognome, nazionalità, dataNascita, dataMorte) VALUES
('A004', 'Antoine', 'de Saint-Exupéry', 'Francese', '1900-06-29', '1944-07-31'),
('A005', 'John', 'Boyne', 'Irlandese', '1971-04-30', NULL),
('A006', 'Anna', 'Frank', 'Tedesca', '1929-06-12', '1945-02-01'),
('A007', 'Italo', 'Calvino', 'Italiano', '1923-10-15', '1985-09-19');

INSERT INTO Libri (isbn, titolo, idAutore, genere, annoUscita, casaEditrice, noleggio) VALUES
('9780156013987', 'Il piccolo principe', 'A004', 'Fiaba', '1943-04-06', 'Reynal & Hitchcock', TRUE),
('9780375842207', 'Il bambino col pigiama a righe', 'A005', 'Romanzo', '2006-01-05', 'David Fickling Books', FALSE),
('9788804677319', 'Il diario di Anna Frank', 'A006', 'Biografia', '1947-06-25', 'Contact Publishing', TRUE),
('9788804493810', 'Il barone rampante', 'A007', 'Romanzo', '1957-10-15', 'Einaudi', FALSE);
