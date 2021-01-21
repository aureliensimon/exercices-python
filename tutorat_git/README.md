# Apprendre à manier git et github

## Qu'elle est la différence entre git et github ?

Git est la technologie qui permet de versionner le code. Github est une platforme qui permet d'héberger et de visualiser des projets gits. Des concurrents existent, comme GitLab, qui utilisent eux aussi la technologie git.

## Pourquoi utiliser git ?

Cela permet de tracker les changements faits dans un fichier. Grâce à cela, on peut revenir plus facilement à des versions antérieures. Cela facilite aussi la collaboration permettant à chaques personnes de suivre les changements effectués dans les différents fichiers.

## Configuration de git

```bash
    > git config --global user.name "John Doe"
    > git config --global user.email johndoe@example.com
```

## Création d'un repository git

Il faut tout d'abord se placer dans un dossier déjà existant. Ensuite, tapez les commandes suivantes:

```bash
    > git init
```

## Liaison entre le repository sur le pc et le serveur github

Nous allons créer un fichier appelé README.md, cela permet d'expliquer le contenu de votre repo.

```bash
    > echo "# redesigned-octo-guacamole" >> README.md
```
Ensuite, nous allons le préparer à l'envoie en écrivant la commande:

```bash    
    > git add README.md
```

On peut remplacer le nom du fichier par un ".", cela indique que vous ajoutez tous les fichiers qui ont été modifiés. On peut le vérifier avec la commande suivante:

```bash
    > git status
```

Métaphoriquement, cela se traduirait par la préparation d'un colis avant l'envoie à la poste.
Justement, la commande suivante permet de sauvegarder les changements:

```bash
    > git commit -m "first commit"
```
Le message entre guillemet permet d'indiquer les changements réalisés. Il se doit d'être court et précis.

Enfin, il faut indiquer l'adresse du repo github et le pousser sur la branch master.

```bash
    > git remote add origin git@github.com:Gouderg/redesigned-octo-guacamole.git
    > git push -u origin master
```

## Exercice 1

Créez un repo qui s'appelle "tutorat-git". Dedans, ajoutez un script python qui affice la somme des nombres de 1 à 10.

Ensuite, effectuez les commandes nécessaires pour l'envoyer sur le repo github et allez regarder le résulat.

## Exercice 2

Supprimez le dossier contenant le .git. Effectuez la commande suivante qui permet de récupérer un dépôts git sur github:

```bash
    > git clone <url_donnée_par_github>
```

Ensuite, modifiez le script python afin d'afficher la somme des nombres de 1 à 20 et mettez le à jour sur github.

## Exercice 3

Créez une nouvelle fonction qui permet d'afficher "Bonjour "+prenom et ensuite le mettre à jour sur le github.

Maintentant, nous allons créer une branch, cela permet de partir d'un même code, de le partager, mais ils seront distincts l'un de l'autre.

Afficher la liste des branches
```bash
    > git branch
```

Créer une branch
```bash
    > git branch ma-nouvelle-branch
```

Aller sur ma nouvelle branch
```bash
    > git checkout ma-nouvelle-branch
```

C'est une bonne pratique de vérifier s'il on se trouve sur la bonne branch en tapant la commande pour afficher les branches.

Maintenant créer une nouvelle fonction qui permet d'afficher "Bonsoir "+prenom et mettez à jour le repo github

Ensuite, retournez sur la branch master et vérifiez le contenu de votre fonction.

