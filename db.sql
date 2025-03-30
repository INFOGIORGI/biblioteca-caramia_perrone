DROP TABLE IF EXISTS Noleggi;
DROP TABLE IF EXISTS Libri;
DROP TABLE IF EXISTS Autori;
DROP TABLE IF EXISTS Utenti;

-- Creazione tabella Autori
CREATE TABLE IF NOT EXISTS Autori (
    idAutore VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(10),
    cognome VARCHAR(10),
    nazionalità VARCHAR(10),
    dataNascita DATE,
    dataMorte DATE
);

-- Creazione tabella Libri
CREATE TABLE IF NOT EXISTS Libri (
    isbn VARCHAR(13) PRIMARY KEY,
    titolo VARCHAR(20),
    idAutore VARCHAR(10),
    genere VARCHAR(10),
    annoUscita DATE,
    casaEditrice VARCHAR(20),
    noleggio BOOLEAN,
    FOREIGN KEY (idAutore) REFERENCES Autori(idAutore)
);

-- Creazione tabella Utenti
CREATE TABLE IF NOT EXISTS Utenti (
    idUtente VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(10),
    cognome VARCHAR(10),
    dataNascita DATE,
    email VARCHAR(20),
    telefono BIGINT, 
    indirizzo VARCHAR(10),
    pswrd VARCHAR(50),
    dataRegistrazione DATE
);

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


INSERT INTO Autori (idAutore, nome, cognome, nazionalità, dataNascita, dataMorte) VALUES
('A004', 'Antoine', 'de Saint-Exupéry', 'Francese', '1900-06-29', '1944-07-31'),
('A005', 'John', 'Boyne', 'Irlandese', '1971-04-30', NULL),
('A006', 'Anna', 'Frank', 'Tedesca', '1929-06-12', '1945-02-01');

INSERT INTO Libri (isbn, titolo, idAutore, genere, annoUscita, casaEditrice, noleggio) VALUES
('9780156013987', 'Il piccolo principe', 'A004', 'Fiaba', '1943-04-06', 'Reynal & Hitchcock', TRUE),
('9780375842207', 'Il bambino col pigiama a righe', 'A005', 'Romanzo', '2006-01-05', 'David Fickling Books', FALSE),
('9788804677319', 'Il diario di Anna Frank', 'A006', 'Biografia', '1947-06-25', 'Contact Publishing', TRUE);