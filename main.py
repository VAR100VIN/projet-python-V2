import flask
import flask_login
from imports import *
from classes import *
from datetime import timedelta
from flask import session, g
from flask_login import LoginManager, login_required, login_user, logout_user
from Facture import *
if __name__ == '__main__':
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    Bootstrap(app)
    app.config.from_object(__name__)

    app.permanent_session_lifetime = timedelta(minutes=60)
    db = DBSingleton.Instance()
    app.config['SECRET_KEY'] = 'this is not a secret'
    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)
        flask.session.modified = True
        flask.g.user = flask_login.current_user

    def verificationprospect(nom):
        lenom: tuple = (nom,)
        sql = "SELECT id FROM prospect WHERE nom = %s;"
        db.query(sql, lenom)
        if db.result == []:
            return False
        else:
            return True

    def verificationContactDejaExistant(nom):
        contact: tuple = (nom,)
        sql = "SELECT nom FROM contact WHERE nom = %s;"
        reponse = db.query(sql, contact)
        if reponse == []:
             return False
        else:
             return True



    @app.route('/form', methods=['GET', 'POST'])
    def ajoutprospect():
        if 'user' in session:
            form = FormulaireCreationprospect()
            if form.validate_on_submit():
                params: tuple = (
                form.nom.data, form.numSiret.data, form.adressePostale.data,
                form.codePostal.data, form.ville.data,
                form.description.data, form.url.data)

                sql = "INSERT INTO prospect (nom, NSiret, adressePostale, codePostal, ville, description, url) VALUES (%s,%s,%s,%s,%s,%s,%s); "
                db.query(sql, params)
                print("ça marche")
            else:
                print(" ça marche pas")
        else:
            retourner = redirect('/')
            return retourner
        return render_template('login.html', form=form)


    def stringer(tuple):
        return str(tuple).strip("(),")


    def getidprospect(nom):
        tab: tuple = (nom,)
        sql = "SELECT idprospect FROM prospect WHERE nom = %s;"
        reponse = db.query(sql, tab)
        idprospect = reponse[0]
        return stringer(idprospect)

    def getidcontact(nom):
        tab: tuple = (nom,)
        sql = "SELECT idcontacct FROM contact WHERE nom = %s;"
        reponse = db.query(sql, tab)
        idcontact = reponse[0]
        return stringer(idcontact)

    @app.route('/ajout-contact', methods=['GET', 'POST'])
    def ajoutContact():
        print(session['key'])
        if 'user' in session:
            sql = "SELECT idprospect, nom FROM prospect"
            db.query(sql, )
            reponse = db.query(sql, )
            if request.method == 'POST':
                nom = request.form['nom']
                prenom = request.form['prenom']
                email = request.form['email']
                poste = request.form['poste']
                telephone = request.form['telephone']
                print(request.form)
                actif = 1 if 'statut' in request.form else 0
                prospect_idprospect = request.form['prospect_idprospect']
                record = (nom, prenom, email, poste, telephone, actif, prospect_idprospect)
                print(record)
                try:
                    sql = """INSERT INTO contact (nom, prenom, email, poste, telephone, statut, prospect_idprospect) 
                                VALUES ('%s', '%s', '%s', '%s', %s, '%s', %s);""" % record
                    db_instance = DBSingleton.Instance()
                    db_instance.query(sql)
                except:
                    print('pas bon')
        else:
            retourner = redirect('/')
            return retourner
        return render_template('ajoutcontact.html', reponses=reponse)


    @app.route('/', methods=['POST', 'GET'])
    def appeLogin():
        session['key'] = 'value'
        return LogUser()

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect('/')
    @app.route('/user', methods=['POST', 'GET'])
    def user():
        if 'user' in session:
            title = 'formulaire'
            sql = """SELECT nom,NSiret,adressePostale,codePostal,ville,description,url,COUNT(numeroFacture) FROM prospect LEFT JOIN facture ON idprospect = facture.prospect_idprospect GROUP BY nom ORDER BY nom"""
            db_instance = DBSingleton.Instance()
            posts = db_instance.query(sql)
            retourner = render_template('interface.html', title=title, posts=posts)
        else:
            retourner = redirect('/')
        return retourner


    @app.route('/del', methods=['POST', 'GET'])
    def deluser():
        if 'user' in session:
            title = 'formulaire'
            sql = """SELECT nom,NSiret,adressePostale,codePostal,ville,description,url,idprospect,COUNT(numeroFacture) FROM prospect LEFT JOIN facture ON idprospect = facture.prospect_idprospect GROUP BY nom ORDER BY nom"""
            db_instance = DBSingleton.Instance()
            posts = db_instance.query(sql)
            retourner = render_template('delentreprise.html', title=title, posts=posts)
            if request.method == "POST":
                ID = request.form['post_id']
                sql = f"DELETE FROM prospect WHERE idprospect NOT IN (SELECT prospect_idprospect FROM facture) AND idprospect = {ID}"
                print(sql)
                db_instance = DBSingleton.Instance()
                db_instance.query(sql)
                print('bon')
                retourner = redirect('/user')
        else:
            retourner = redirect('/')
        return retourner


    @app.route('/contact', methods=['POST', 'GET'])
    def contact():
        if 'user' in session:
            title = 'formulaire'
            sql = """SELECT  contact.nom,prenom,email,poste,telephone,CASE statut WHEN 1 then 'actif' WHEN 0 THEN 'inactif' END,prospect.nom AS 'nom prospect' FROM contact JOIN prospect ON prospect_idprospect=prospect.idprospect """
            db_instance = DBSingleton.Instance()
            posts = db_instance.query(sql)
            retourner = render_template('interfacecontact.html', title=title, posts=posts)
            form = BarreDeRecherche()
        #essai de la barre de recherche
            if form.validate_on_submit():
                recherche = request.form["filtre"]
                sql = f"SELECT nom,email FROM contact WHERE nom OR email LIKE '{recherche}%'"
                print(sql)
                db_instance = DBSingleton.Instance()
                db_instance.query(sql)
                print('bon')
        else:
            retourner = redirect('/')
        return retourner


    @app.route('/editer-contact', methods=['GET', 'POST'])
    def modifContact():
        if 'user' in session:
            sql = "SELECT idprospect, nom FROM prospect"
            db.query(sql, )
            nom_prospet = db.query(sql, )
            sql2 = "SELECT idcontacct, nom FROM contact"
            db.query(sql2, )
            nom_contact = db.query(sql2)
            retourner = render_template('contactForm.html', reponses=nom_prospet, choices=nom_contact)
            if request.method == 'POST':
                modified = request.form['id']
                nom = request.form['nom']
                prenom = request.form['prenom']
                email = request.form['email']
                poste = request.form['poste']
                telephone = request.form['telephone']
                actif = 1 if 'statut' in request.form else 0
                prospect = request.form['prospect']
                sql = f"""UPDATE contact SET nom = '{nom}', prenom = '{prenom}', email = '{email}',
                          poste = '{poste}', telephone = {telephone}, statut = {actif},
                          prospect_idprospect = {prospect} WHERE idcontacct ={modified}"""
                print(sql)
                db_instance = DBSingleton.Instance()
                db_instance.query(sql)
        else:
            retourner = redirect('/')
        return retourner



    @app.route('/com', methods=['POST', 'GET'])
    def commentaire():
        if 'user' in session:
            title = 'formulaire'
            sql = """SELECT  auteur,description,dateDeCreation FROM commentaire ORDER BY dateDeCreation"""
            db_instance = DBSingleton.Instance()
            posts = db_instance.query(sql)
            retourner = render_template('interfacecom.html', title=title, posts=posts)
        else:
            retourner = redirect('/')
        return retourner
    @app.route('/ajout-com', methods=['POST', 'GET'])
    def ajoutcom():
        if 'user' in session:
            title = 'formulaire'
            sql = "SELECT auteur FROM commentaire"
            db.query(sql, )
            reponse = db.query(sql, )
            if request.method == 'POST':
                auteur = request.form['auteur']
                description = request.form['description']
                date = request.form['date']
                print(request.form)
                record = (auteur, description, date)
                print(record)
                try:
                    sql = """INSERT INTO commentaire (auteur, description, dateDeCreation) 
                                                VALUES ('%s', '%s', '%s');""" % record
                    db_instance = DBSingleton.Instance()
                    db_instance.query(sql)
                except:
                    print('pas bon')
            retourner = render_template('comForm.html')
        else:
            retourner = redirect('/')
        return retourner

    @app.route('/ajout-facture', methods=['POST', 'GET'])
    def ajoutfacture():
        if 'user' in session:
            #sql = "SELECT idprospect, nom FROM prospect"
            #db.query(sql, )
            # nom_prospect = db.query(sql, )
            sql2 = "SELECT idcontacct, nom FROM contact"
            db.query(sql2, )
            nom_contact = db.query(sql2)
            retourner = render_template('factureForm.html', reponses=nom_contact)
            if request.method == 'POST':
                numero = request.form['numero']

                personne_idcontacts = request.form['personne_idcontacts']
                montant = request.form['montant']

                sql = "SELECT prospect_idprospect from contact where idcontacct=%s "
                param =(str(personne_idcontacts)),
                db_instance = DBSingleton.Instance()
                id_prospect = db_instance.query(sql,param)[0]


                #prospect_idprospect = request.form['prospect_idprospect']
                personne_idcontacts = request.form['personne_idcontacts']
                record = ( numero,id_prospect[0], personne_idcontacts, montant)

                print(record)
                sql = """INSERT INTO facture (numeroFacture ,prospect_idprospect, personne_idcontact, montant) 
                         VALUES ('%s', '%s', '%s','%s');""" % record
                db_instance.query(sql)
                sql = "select max(idfacture) from facture"
                idfacture = (db_instance.query(sql))[0]
                print(idfacture)
                prospect = Prospect (id_prospect[0])
                contact = Contact (personne_idcontacts)
                details_facture = Details_facture(idfacture[0])

                entreprise = Entreprise("Afondlaforme" ,"FR7630004015870002601171220", "Afondlaforme@gmail.com", "0233333333", "Rennes CEDEX 35", "35000", "Rennes", "3 rue sportif" , "306138900")
                LaFacture = Facture(entreprise, prospect, contact, details_facture)
                LaFacture.generate()





        else:
            retourner = redirect('/')
        return retourner
    @app.route('/facture', methods=['POST', 'GET'])
    def facture():
        if 'user' in session:
            title = 'formulaire'
            sql = """SELECT  prenom,contact.nom,dateFacture,numeroFacture,prospect.nom AS 'nom prospect',email,telephone,prenom FROM facture JOIN prospect ON prospect_idprospect=prospect.idprospect JOIN contact ON personne_idcontact=contact.idcontacct"""
            db_instance = DBSingleton.Instance()
            posts = db_instance.query(sql)
            retourner = render_template('interfacefacture.html', title=title, posts=posts)
        else:
            retourner = redirect('/')
        return retourner



    #essai d'affichage de facture en pdf non réussi
    # @app.route('/pdf/<facture_id>')
    #     def display_pdf(facture_id):
    #             return send_file('canvas_form.pdf', attachment_filename='file.pdf')
    #
    # @app.route('/facture', methods=['POST', 'GET'])
    #     def form(path, prospect_nom, nom_contact):
    #         my_canvas = canvas.Canvas(path, pagesize=letter)
    #         my_canvas.setLineWidth(.4)
    #         my_canvas.setFont('Helvetica', 12)
    #         my_canvas.drawString(30, 750, 'La jolie boite à code')
    #         my_canvas.drawString(30, 715, 'adresse : ')
    #         my_canvas.drawString(400, 680, 'FACTURE:')
    #         my_canvas.drawString(30, 700, 'adresse entreprise:')
    #         my_canvas.drawString(30, 640, 'N° de SIREN:')
    #         my_canvas.drawString(30, 590, f'Tel. :{prospect_nom}')
    #         my_canvas.drawString(30, 570, 'Email:')
    #         my_canvas.drawString(30, 550, 'IBAN:')
    #         my_canvas.drawString(30, 470, f'Numéro {nom_contact}:')
    #         my_canvas.drawString(160, 470, f'Date {nom_contact}:')
    #         my_canvas.drawString(350, 520, f'Nom du prospect : {prospect_nom} ')
    #         my_canvas.drawString(350, 500, f'Nom du contact : {nom_contact}')
    #         my_canvas.drawString(350, 480, f'Adresse du prospect :{prospect_nom}')
    #         my_canvas.drawString(350, 460, f'Code et Ville du prospect :{prospect_nom}')
    #         my_canvas.save()
    #     return send_file('canvas_form.pdf', attachment_filename='file.pdf')

    #if __name__ == '__main__':
     #   form('canvas_form.pdf', 'EPSI', ' PANNETIER_Magali')

app.run(debug=True)