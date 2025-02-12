create table Libro(
    idLibro varchar(10) primary key,
    titolo varchar(20),
    autore varchar(10) foreign key,
    genere varchar(10),
    annoUscita date,
    isbn varchar(13),
    casaEditrice varchar(20),
    noleggio boolean,
)

create table Utente(
    idUtente varchar(10) primary key,
    nome varchar(10),
    cognome varchar(10),
    dataNascita date,
    email varchar(20),
    telefono int(10),
    indirizzo varchar(10),
    pswrd varchar(8),
    dataRegistrazione date,
)

create table Noleggio(
    idNoleggio varchar(10) primary key,
    idUtente varchar(10) foreign key,
    idLibro varchar(10) foreign key,
    inizioNoleggio date,
    fineNoleggio date,
    restituzione boolean,
)

create table Autore(
    idAutore varchar(10) primary key,
    nome varchar(10),
    cognome varchar(10),
    nazionalità varchar(10),
    dataNascita date(10),
    dataMorte date(10),
)
