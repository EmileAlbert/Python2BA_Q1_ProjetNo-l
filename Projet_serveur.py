from bottle import*
import json
from random import *
import random
#Ouverture de la base de données :
with open('fichierpays.txt', 'r' ) as file :
        content = file.read()
        dico = json.loads(content)
        #Structure Dictionnaire : dico = {'Pays' : {'superficy' : ... ; 'capital' : ... ; 'population' : ...}}
        #.format(pays,dico[pays]['capital'],dico[pays]['superficy'],dico[pays]['population'])

#Variable du header commun aux pages :
def header(title,h2) :
    return '''
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="/Css/Projet_Main_CSS_2.css"/>
        <title>Les pays Européens - {}</title>
    </head>
    <body>
        <header>
            <h1>Les pays européens</h1>
            <hr/>
            <h2>{}</h2>
        </header>
        <nav>
            <ul id="nav">
                <li id="nav_Accueil"><a href="/Projet/accueil/">Accueil</a></li>
                <li id="nav_Carnet"><a href="/Projet/Carnet_de_Voyage/">Carnet de Voyage</a></li>
                <li id="nav_Recherche"><a href="/Projet/Quizz/Drapeaux">Quizz drapeaux</a></li>
                <li id="nav_Quizz"><a href="/Projet/Quizz/Capitales">Quizz capitales</a></li>
            </ul>
        </nav>'''.format(title,h2)

#Variable footer commun :
def footer():
    return '''</section>
        <footer>
            <hr/>
            <p>François Detry & Emile Albert ECAM Bruxelles 2015 -
               Source : Images et infos sur les pays : www.vikipedia.org et image de fond : extraite d'une photo de la Nasa</p>
        </footer>'''

#Route d'appel du fichier CSS :
@route('/Css/<filename>')
def server_static(filename) :
    return static_file(filename, root ='./Css_Files')


##Route de la page d'accueil :
@route('/Projet/accueil/')
def Acceuil():
    liste = '<ul id="lienspays">\n'
    for n in dico:
        liste += '\t<li><a href="http://localhost:8080/Projet/fiche/{}">{}</a></li>\n'.format(n,n)
    liste += '</ul>'

    return '''
    {}
    <section>
        <article>
            <P id="Desc">Notre site a pour but de fournir une base de données sur les différents pays d'Europe. Vous pourrez retrouver les informations
                relatives aux différents pays mais aussi tester vos connaissances sur ceux-ci.</P>
        </article>

        <article>
            <h3>Les pays</h3>
                {}
        </article>

    </section>

    {}

</body>
</html>'''.format(header('Accueil','Accueil'), liste,footer())


##Route de la page canvas pour les fiches pays :
@route('/Projet/fiche/<pays>')
def FichePays(pays) :
    Imagedrapeau = '<img src="{}" width=32 height=16 title="Drapeau">'.format(dico[pays]['flag'])

    return '''
    {}
    <section>
        <ul>
            <li>Capitale : {}</li>
            <li>Superficie : {} km²</li>
            <li>Population : {} million(s) de personne</li>
            <li>Monnaie : {}</li>
            <li>Langue(s) nationale(s) : {}</li>
        </ul>
    </section>
    <a href="/Projet/accueil/">Retour</a>
    {}
'''.format(header('Fiche Nationale - {}','{} {} - Fiche Nationale').format(pays,Imagedrapeau,pays),
           dico[pays]['capital'],dico[pays]['superficy'],dico[pays]['population'],dico[pays]['currency'],dico[pays]['language'],footer)


##Route de la page Carnet de voyage :
@route('/Projet/Carnet_de_Voyage/')
def Carnet():
    with open ('carnet.txt', 'r') as file:
        content = file.read()
        dicocarnet = json.loads(content)

    liste = '''Les pays que j'ai déjà visités :
               <ul>'''

    for n in dicocarnet:
        liste += '''<li>Pays : {}
                        <ul>
                            <li>Année : {}</li>
                            <li>Souvenir : {}</li>
                        </ul>'''.format(n, dicocarnet[n]['year'], dicocarnet[n]['souvenir'])
    liste+='</ul>'

    return'''
    {}
    <body>
        <br>
        <form method="post" action="/Traitement/">
            <fieldset>
                    <input type="text" name="paysvoyage" id="year" placeholder="Pays voyagé"/><br>
                    <input type="text" name="anneevoyage" id="year" placeholder="Année du voyage"/><br>
                    <textarea name="souvenirvoyage" id="souvenir" placeholder="Moments forts/Souvenirs du voyage" rows ="5" cols="40"></textarea><br>
                    <input type="submit" name="ajouter" value="Ajouter un souvenir">
            </fieldset>
        </form>
        <br>
        {}
    </body>'''.format(header('Carnet de voyage','Remplis ton carnet de voyage ici !'), liste,footer())

#Traitement du formulaire (Carnet de voyage) :
@post('/Traitement/')
def Traitement():
    with open ('carnet.txt', 'r')as file:
        content = file.read()
        dicocarnet = json.loads(content)

        dicocarnet[request.forms.get('paysvoyage')]={'year': request.forms.get('anneevoyage'), 'souvenir': request.forms.get('souvenirvoyage')}

    with open ('carnet.txt', 'w') as file:
        file.write(json.dumps(dicocarnet))

    redirect('/Projet/Carnet_de_Voyage/')


##Route de la page du Quizz capitale :
@route('/Projet/Quizz/Capitales')
def quizzpage() :
    return'''
    {}
    <body>
    <p>Sur cette page vous allez pouvoir tester vos connaissances sur les capitales des pays européens. Pour chaque pays, sélectionnez //
    dans la liste déroulante la capitale correspondante et ensuite cliquez sur Terminer pour voir votre correction.</p>

    <section>
        <form action='/QuizzC' method='post'>
            {}
            <br>{}
            <br>{}
            <br><br><input type='submit' value='Terminer' />
        </form>
    </section>
    {}
    </body>'''.format(header('Quizz','Quizz sur les capitales'),QuestionCap(1),QuestionCap(2),QuestionCap(3),footer,)

#Fonction résultat (Quizz capitale) :
def result(x,y) :
    if dico[x]['capital'] == y :
        return 1, '''Félicitation, la capitale de {} est bien {}\n'''.format(x,y)
    else :
        return 0,'''Attention, la capitale de {} est {} et pas {} \n'''.format(x,dico[x]['capital'],y )

#Fonction génératrice de question (Quizz capitale) :
def QuestionCap(x) :
        form = '''Quelle est la capitale de {} ?\n<SELECT name="reponse{}">\n'''
        i = 0
        listepays = []
        liste = []

        for n in dico :
            listepays.append(n)
        random.shuffle(listepays)#Utilisé dans le but de ne pas avoir les mêmes pays tout le temps.

        for n in listepays :
            if i < 5:
                liste.append("\t<OPTION>{}\n".format(dico[n]['capital']))
                pays = n
                i += 1

        random.shuffle(liste) #Utilisé dans le but que la réponse ne sois pas tout le temps au même endroit.
        for n in liste :
            form += n
        form += '</SELECT>'

        inputpays = '''<input type='text'
                        style='background-color : transparent; color:white; border-color : transparent; width : 120px '
                        value = '{}' name='paysq{}'>'''.format(pays,x)

        return form.format(inputpays,x)

#Methode de traitement des reponses (Quizz capitale) :
@post('/QuizzC')
def AnswerCorrectionC() :
    pays1 = request.forms.get('paysq1')
    reponse1 = request.forms.get('reponse1')
    pays2 = request.forms.get('paysq2')
    reponse2 = request.forms.get('reponse2')
    pays3 = request.forms.get('paysq3')
    reponse3 = request.forms.get('reponse3')

    final = result(pays1,reponse1)[0] + result(pays2,reponse2)[0] + result(pays3,reponse3)[0]

    return '''
        {}
        <body>
            <br>
            Merci d'avoir joué avec nous !
            Votre score est de {} point(s) <br>
                <ul>
                    <li>{}</li>
                    <li>{}</li>
                    <li>{}</li>
                </ul>
            <br>
            <a href="/Projet/Quizz/Capitales">Je veux rejouer !</a>
             ||
            <a href="/Projet/accueil/">Arrêtons le massacre... Je veux retourner a l'accueil</a>

        </body>

        '''.format(header('Resultat','Résultat du quizz'),final, result(pays1,reponse1)[1],result(pays2,reponse2)[1],result(pays3,reponse3)[1])


##Route de la page du Quizz drapeaux :
@route("/Projet/Quizz/Drapeaux")
def quizzpage() :
    with open('transfert.txt','w') as file :
        file.write('')
    return'''
        {}
        <p>Sur cette page, vous allez pouvoir vous tester ! Connaissez-vous bien les drapeaux des pays du continent européen ? Testez vous ci-dessous !
           Pour les 3 pays, glissez le curseur sous le drapeau correspondant a chacun d'eux et cliquez ensuite sur Terminer pour voir votre score.</p>
        <form action='/QuizzDrap' method='post'>
            {}<br>
            {}<br>
            {}</br>
            <input type='submit' value='Terminer' style="margin-left : 125px" />
        </form>
        {}'''.format(header('Quizz','Quizz sur les drapeaux'), QuestionDrap(1),QuestionDrap(2),QuestionDrap(3),footer())

#Fonction génératrice de questions (Quizz drapeaux) :
def QuestionDrap(x):
    i = 0
    liste2 = []
    form = "<br>Quel est le drapeau de {} ? <br> <br>"
    listepays = []
    for n in dico :
        listepays.append(n)
    random.shuffle(listepays)

    listereponse = []
    for n in listepays :
        if i < 3 :
            listereponse.append('<img src="{}" width="80px" height="45px" hspace="10px"/>'.format(dico[n]['flag']))
            liste2.append(n)
            i+=1

    for n in listereponse :
        form += n

    with open('transfert.txt','a') as file :
        var = int(randint(0,2))
        file.write('/'+str(var*5)+'/'+liste2[var])

    form += '''<br><input type="range" name='reponse{}' style='width:280px' min="0" max="10" step="5" value="0" /> '''.format(x)

    return form.format(liste2[var], x)

#Fonction résultat (Quizz drapeaux) :
def resultD(x,y) :
    with open ('transfert.txt','r') as file :
        content = file.read().split('/')

    if int(x) == int(content[int(y)]) :
        return 1, 'Bravo ! Le drapeau de {} est bien <img src="{}" width="32px" height="18px">'.format(content[int(y)+1],dico[content[int(y)+1]]['flag'])
    else :
        return 0,'Attention, le drapeau de {} est <img src="{}" width="32px" height="18px">'.format(content[int(y)+1],dico[content[int(y)+1]]['flag'])

#Méthode traitement du formulaire (Quizz drapeaux) :
@post('/QuizzDrap')
def AnswerCorrectionD():
    reponse1 = request.forms.get('reponse1')
    reponse2 = request.forms.get('reponse2')
    reponse3 = request.forms.get('reponse3')

    res = int(resultD(reponse1,1)[0]) + int(resultD(reponse2,3)[0]) +int(resultD(reponse3,5)[0])

    return '''
        {}
        <body>
            <br>
            Merci d'avoir joué avec nous !<br>
            Votre score est de {} point(s) <br>
            <br>
            <ul>
                <li>{}
                <li>{}
                <li>{}
            </ul>
            <br>
            <a href="/Projet/Quizz/Drapeaux">Je veux rejouer !</a>
             ||
            <a href="/Projet/accueil/">Arrêtons le massacre... Je veux retourner a l'accueil</a>
        </body>'''.format(header('Resultat','Résultat du quizz'),res,resultD(reponse1,1)[1],resultD(reponse2,3)[1],resultD(reponse3,5)[1])

run(host='localhost',port=8080)
