from Singleton import*

class Prospect:
    def __init__(self, id):
        db = DBSingleton.Instance()
        sql = "select nom, adressePostale, codePostal, ville, NSiret from prospect where idprospect = %s"
        param = (id,)
        element = (db.query(sql,param))[0]
        print(element)
        self.nom_prospect = element[0]
        self.adresse_prospect = element[1]
        self.code_postal_prospect = str(element[2])
        self.ville_prospect = element[3]
        self.N_siret = element[4]

class Contact:
    def __init__(self,id):
        db = DBSingleton.Instance()
        sql = "select nom, prenom, email, telephone from contact where idcontacct = %s"
        param = (id,)
        element = (db.query(sql,param))[0]
        self.nom_contact = element[0]
        self.prenom_contact = element[1]
        self.email_contact = element[2]
        self.telephone_contact = element[3]

class Details_facture:
    def __init__(self,id):
        db = DBSingleton.Instance()
        sql = "select dateFacture, numeroFacture, montant FROM facture where idFacture = %s "
        param = (id,)
        element = db.query(sql,param)[0]
        self.dateFacture_facture = element[0]
        self.numeroFacture_facture = element[1]
        self.montant_facture = element [2]
        print(self.numeroFacture_facture)


class Entreprise:
    def __init__(self ,nom ,IBAN, email, telephone, cedex, codepostal, ville, adresse ,numero_siren ):
        self.nom = nom
        self.IBAN = IBAN
        self.email = email
        self.telephone = telephone
        self.cedex = cedex
        self.codepostal = codepostal
        self.ville = ville
        self.adresse = adresse
        self.numero_siren = numero_siren

