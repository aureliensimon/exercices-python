'''
    Table personne
    +-------+---------+----------+-----+---------+-------------------+
    | id(PK)| nom     | prenom   | age | salaire | id_entreprise(FK) |
    +-------+---------+----------+---------+-------------------------+
    | 1     | Simon   | Aurelien | 20  | 423     | 2                 |
    | 2     | Illien  | Victor   | 22  | 1200    | 2                 |
    | 3     | Allain  | Titouan  | 21  | 523     | 3                 |
    +-------+---------+----------+-----+---------+-------------------+

    Table entreprise
    +--------------------+---------------------+-----------+
    | id_entreprise (PK) | nom_entreprise      | num_siret |
    +--------------------+---------------------+-----------+
    | 2                  | ISEN                | 546324    |
    | 3                  | ENIB                | 56452135  |
    +--------------------+---------------------+-----------+
'''
import mysql.connector  # Lien pour la doc: https://www.w3schools.com/python/python_mysql_select.asp


class BDD:

    # Constructeur de la class: Initialise la connexion avec la bdd et créer un curseur
    def __init__(self):
        self.database = mysql.connector.connect(
                host = "localhost",
                database = "tutorat_exemple",
                user = "class_tutorat",
                password = "mJ6fVk775cyRgTH5aWKA9zk25Xt9W9k2!",
            )
        self.curseur = self.database.cursor()

    # Méthode qui récupère tous les informations de la table personne
    def dbRequestAllPersonne(self):
        request = "SELECT * FROM personne"
        #request = "SELECT nom FROM entreprise"
        #request = "SELECT * FROM personne p
        #           JOIN entreprise e ON p.id_entreprise = e.id_entreprise"

        self.curseur.execute(request)
        response = self.curseur.fetchall()
        return response

    # Méthode qui modifie les valeurs de la base de données en fonction d'un paramètre
    def dbModifyPersonne(self, nom, age, salaire):
        request = "UPDATE personne SET age = %s, salaire = %s WHERE nom = %s "      # Requête
        parametre = (age, salaire, nom, )                                           # Paramètre de la requête
        self.curseur.execute(request, parametre)                                    # Exécute la requête en associant les paramètres
        self.database.commit()                                                      # Applique les changements à la base de donnée

    # Méthode qui ajoute un utilisateur dans la base de donnée
    def dbInsertPersonne(self, nom, prenom, age, salaire, id_entreprise):
        request = "INSERT INTO personne (nom, prenom, age, salaire, id_entreprise) VALUES (%s, %s, %s, %s, %s)"
        parametre = (nom, prenom, age, salaire, id_entreprise, )
        self.curseur.execute(request, parametre)
        self.database.commit()

    # Méthode qui supprime une personne
    def dbDeletePersonne(self, nom):
        request = "DELETE FROM personne WHERE nom = %s"
        parametre = (nom,  )
        self.curseur.execute(request, parametre)
        self.database.commit()

    # Méthode qui ferme la connexion avec la base de donnée
    def dbCloseConnection(self):
        self.curseur.close()

hello = BDD()

print(hello.dbRequestAllPersonne())                           # Affichage
hello.dbModifyPersonne('Simon', 98, 25)                       # On modifie une personne
print(hello.dbRequestAllPersonne())                           # Affichage
hello.dbInsertPersonne('Pralain', 'Leopold', 25, 165651, 2)   # On ajoute une personne
print(hello.dbRequestAllPersonne())                           # Affichage
hello.dbDeletePersonne('Pralain')                             # On supprime une personne
print(hello.dbRequestAllPersonne())                           # Affichage
hello.dbCloseConnection()                                     # On ferme la connexion à la base de donnée
