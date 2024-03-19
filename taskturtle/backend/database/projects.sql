

CREATE TABLE IF NOT EXISTS users (
    id INT,
    nom TEXT,
    prenom TEXT,
    email TEXT,
    password TEXT,
    balance INTEGER,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS transactions (
    id_transaction INT,
    nom TEXT,
    description TEXT,
    demandeur INT,
    executant INT,
    prix INTEGER,
    note INT, 
    accepted BOOLEAN DEFAULT FALSE,
    completed BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(id_transaction),
    FOREIGN KEY(executant) REFERENCES users(id),
    FOREIGN KEY(demandeur) REFERENCES users(id)

);

/* INSERT INTO transactions VALUES 
    (1, "Toujours plus de Monster Hunter", "Avoir des cours sur le lore de Monster Hunter, les cours de SVT remplacés par des cours sur la biologie des Grands Monstres en préparation d'un attaque.", 1,-1, 20 ,0,FALSE,FALSE),
    (2, "One Piece", "Cours d'Histoire remplacés par des excursions sur Ohara pour des cours sur le siècle oublié", 2, -1, 5000,0,FALSE,FALSE),
    (3, "Projé", "GNGNGNGN on crée des projets et il sert uniquement à voir si on gère plus de 3 éléments", 1, -1,369852147, 0,FALSE,FALSE); */

INSERT INTO users VALUES 
    (1, "Wirth", "Maxime", "test1@test1.fr", "test1", 1000),
    (2, "Laurent", "Noé-Laurent", "test2@test2.fr", "test2", 1000);
