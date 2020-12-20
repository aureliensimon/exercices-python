import mysql.connector

'''
    MCD :

    nomTable
    +-----+-------------+------+
    | id  | nom         | age  |
    +-----+-------------+------+
    | 1   | Aurélien    | 21   |
    | 2   | Victor      | 25   |
    | 3   | Titouan     | 23   |
    +-----+-------------+------+
'''

class Database ():

    '''
        Lors de la création d'une instance de la Class Database, on demande à l'utilisateur
        toutes les variables afin de se connecter à la base de donnée, en ajoutant des arguments, on
        est alors en mesure de créer deux instances de la même class (ici Database) mais de se connecter
        à deux bases de données différentes

        Exemple :
        > bdd1 = Database('monUser', 'monMotDePasse', 'localhost', 'databaseV1')
        > bdd2 = Database('monUser', 'monMotDePasse', 'localhost', 'databaseV2')

        Bien que bdd1 et bdd2 sont de la même classe, elles se sont connectées sur deux bases de données
        différentes (ici databaseV1 et databaseV2)
    '''
    def __init__ (self, user, password, host, database):
        self.connection = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )

        self.cursor = self.connection.cursor()

    '''
        Exemple d'une méthode permettant de faire un SELECT simple sans jointure

        On prend en argument un nom de table et columns, qui indique toutes les colonnes
        que l'on souhaite sélectionner

        Exemple :
        On cherche à récupérer tout les nom et age d'une table

        > bdd = Database('monUser', 'monMotDePasse', 'localhost', 'databaseV1')
        > bdd.select(table='nomTable', column='nom, age')

        Le .format() permet d'insérer des variables dans une chaine de caractères
        ville_depart = 'Brest'
        ville_arrive = 'Paris'

        phrase = "Demain, je prends le train de {depart} en direction de {arrive}".format(
            depart=ville_depart,
            arrive=ville_arrive
        )

        phrase vaudra alors
        "Demain, je prends le train de Brest en direction de Paris"
    '''
    def select (self, table, columns):
        request = "SELECT {columns} FROM {table}".format(
            table=table,
            columns=columns
        )
        self.cursor.execute(request)

        return self.cursor.fetchall()

    '''
        Exemple d'une méthode permettant de faire un INSERT

        Cette méthode prend un nom de table dans le lequel insérer un nouveau élément, dont les
        informations de ce nouvel élément sont stockés dans le 2e argument (element)

        Exemple:
        /!\
            Dans cet exemple d'INSERT, TOUTES les colonnes doivent être indiquées lors de l'INSERT
            Dans le MCD on a 3 colonnes : id, nom et age.
            Ces 3 trois colonnes doivent être remplie pour que l'INSERT soit valide
        /!\

        Cf le MCD de la base de données, 'id' est un auto-incrément, la valeur contenue dans id sera
        alors réécrit par la base de données, le 0 est alors simplement là pour remplir le champ et ne
        pas le laisser vide, 5 ou 2840 sont aussi des possiblités, la base de données s'en tiendra pas
        compte, il faut simplement que la valeur indiqué dans id soit la même que celle de la base de données
        ici id est un INT donc on lui passe par défaut un INT

        > bdd = Database('monUser', 'monMotDePasse', 'localhost', 'databaseV1')
        > bdd.select(table='nomTable', element={'id': 0, 'nom': 'Victor', 'age': 26})
    '''
    def insert (self, table, element):
        values = tuple(element.values())

        request = "INSERT INTO {table} VALUES {values}".format(
            table=table,
            values=values
        )

        self.execute_and_commit(request)

    '''
        Exemple d'une méthode permettant de faire un DELETE

        Ici la tâche se complique un peu, il est pratique de vouloir un élément en fonction
        de plusieurs de ses valeurs, par exemple, on souhaite DELETE simplement l'élément qui
        a pour nom : 'Victor' et pour âge : 25, mais pas supprimer tout les 'Victor' de la table

        en SQL cela se traduit par
        > DELETE FROM nomTable WHERE nom = 'Victor' AND age = 25

        Mais l'on ne connait pas à l'avance le nombre de conditions que l'utilisateur va fournir

        Ici l'idée est de générer la partie "nom = 'Victor' AND age = 25" de manière dynamique,
        en fonction de ce que l'utilisateur envoit dans l'argument 'element'
    '''
    def delete (self, table, element):
        column = tuple(element.keys())
        value = tuple(element.values())

        where = self.create_dynamic_request(column, value, ' AND ')

        request = "DELETE FROM {table} WHERE {conditions}".format(
            table=table,
            conditions=where
        )

        self.execute_and_commit(request)

    '''
        Exemple d'une méthode permettant de faire un UPDATE

        De la même manière que pour le DELETE, le WHERE a été généré dynamiquement
        en fonction de l'entrée, l'UPDATE rajoute une nouvelle couche de difficulté,

        Exemple d'un UPDATE :
        On souhaite remplacer la personne se nommant Victor et ayant 20 ans et la remplacer
        par Victoire et d'un âge de 18 ans

        > UPDATE table SET nom = 'Victoire', age = 18 WHERE nom = 'Victor' AND age = 20

        Dans ce cas il faut générer 2 parties de la requête dynamiquement, le WHERE et le SET
        On utilise exactement la même stratégie à la différence près que ce qui les sépare
        Dans le WHERE,  on sépare chaque condition par un ' AND '
        Dans le SET,    on sépare chaque condition par un ','

        On passe alors le separator en argument de notre fonction de générateur de conditions
        et il s'occupe du reste pour la formater de la même manière que vu précédement
    '''
    def update (self, table, element, update_element):
        update_column = tuple(update_element.keys())
        column = tuple(element.keys())

        update_value = tuple(update_element.values())
        value = tuple(element.values())

        set = self.create_dynamic_request(update_column, update_value, ',')
        where = self.create_dynamic_request(column, value, ' AND ')

        request = "UPDATE {table} SET {update} WHERE {conditions}".format(
            table=table,
            update=set,
            conditions=where
        )

        self.execute_and_commit(request)

    '''
        Cette méthode permet d'executer une requête et de la commit dans la foulée,
        on remplace alors 2 lignes par une seule, réduisant le nombre de lignes total
        et permet de ne pas l'oublier
    '''
    def execute_and_commit (self, request):
        self.cursor.execute(request)
        self.connection.commit()

    '''
        Méthode permettant de fermer la connexion avec la base de données,
        à effectuer à la fin du programme
    '''
    def close_connection (self):
        self.cursor.close()

    '''
        EXPLICATIONS GENERATION WHERE DYNAMIQUE :

        Supposons que l'utilisateur souhaite supprimer l'élément ayant pour
            nom = 'Victor'
            age = 25
            id = 7

        le WHERE devra ressembler à
            nom = 'Victor' AND age = 25 AND id = 7

        On peut alors facilement en extraire un pattern,
            nom_colonne = valeur_colonne AND ...

        Comme colonne vaut le nom des colonnes et value leurs valeurs respectives, il suffit
        de passer sur chaque element et d'ajouter le pattern à la suite

        Voici l'évolution du WHERE dynamique à chaque tour de la boucle :
            ""
            "nom = 'Victor' AND"
            "nom = 'Victor' AND age = 25"
            "nom = 'Victor' AND age = 25 AND id = 7 AND "
    '''
    def create_dynamic_request (self, column, values, separator):
        request = ''

        '''
            Ici c'est l'occasion de voir une fonction utile de python :
            zip()

            Supposons que l'on veut boucler sur deux tableaux simultanéments
            tableau_A = [ 1,  2,  3]
            tableau_B = [40, 50, 60]

            alors zip() va stocker sous forme de tuple la paire des éléments des deux tableaux
            au même index, exemple sur les deux tableaux ci dessus

            > print(zip(tableau_A, tableau_B))
            Résultat :
            > [(1, 40), (2, 50), (3, 60)]
        '''
        for c, v in zip(column, values):
            '''
                En python, isinstance retourne soit Vrai / Faux si la variable est du même
                type que celui recherché (le 2e argument de la fonction)

                > isinstance(maVariable, type)

                Exemple :
                > isinstance(5, int)
                True
                > isinstance('texte', int)
                False

                En quoi cette fonction peut nous être utile ?
                En SQL :
                    SELECT * FROM table WHERE nom = Victor

                cette requête est incorrecte et renverra une erreur car il faut spécifier
                que Victor est une chaine de caractères, donc il faut l'écrire

                    SELECT * FROM table WHERE nom = 'Victor'

                Il faut alors prendre en compte que si la valeur envoyé par l'utilisateur
                est du type str (= chaîne de caractères) alors on doit lui rajouter ' au
                début et la fin de la chaîne
                Ainsi Victor deviendra 'Victor'
                Si le type est autre que str, nul besoin de le modifier
            '''
            if isinstance(v, str): v = "'" + v + "'"
            request += (c + ' = ' + str(v) + separator)

        '''
            A la fin de la création du WHERE dynamique
            "nom = 'Victor' AND age = 25 AND id = 7 AND "

            On observe qu'il y a un ' AND ' en trop
            On peut alors retirer les 5 derniers caractères
            2 espaces + les 3 caractères du AND) du WHERE dynamique à l'aide de chaine[:-5]

            Si le séparator valait ',' alors sa longueur serait de 1 et on ne retirerais
            qu'un seul caractère
        '''
        request = request[:-len(separator)]

        return request


d = Database(user='pythonuser', password='pythonpwd', host='localhost', database='pythondb')

'''
    EXEMPLE DE REQUÊTES
'''
#print(d.select(table='mytable', column='nom, age'))
#d.insert(table='mytable', element={'id': 0, 'nom': 'Victor', 'age': 26})
#d.delete(table='mytable', element={'nom': 'Victori', 'age': 26})
#d.update(table='mytable', element={'nom': 'Victor'}, update_element={'nom': 'Victor', 'age': 20})
