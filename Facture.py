from docxtpl import DocxTemplate
from models import *
from docx2pdf import convert
import pythoncom


class Facture:
    def __init__(self, entreprise: Entreprise, prospect: Prospect, contact: Contact, details_facture: Details_facture):
        self.entreprise = entreprise
        self.prospect = prospect
        self.contact = contact
        self.details_facture = details_facture
        self.nomFacture = "facture_" + self.details_facture.numeroFacture_facture

    def generate(self):

        pythoncom.CoInitialize()
        document = DocxTemplate("facture/template/template.docx")
        template_values = {
            'nom_e': self.entreprise.nom,
            'adresse_e': self.entreprise.adresse,
            'code_postal_e': self.entreprise.codepostal,
            'ville_e': self.entreprise.ville,
            'cedex_e': self.entreprise.cedex,
            'siren_e': self.entreprise.numero_siren,
            'tel_e': self.entreprise.telephone,
            'email_e': self.entreprise.email,
            'iban_e': self.entreprise.IBAN,
            'nom_p': self.prospect.nom_prospect,
            'nom_c': self.contact.nom_contact,
            'adresse_p': self.prospect.adresse_prospect,
            'code_postal_p': self.prospect.code_postal_prospect,
            'ville_p': self.prospect.ville_prospect,
            'numero_f': self.details_facture.numeroFacture_facture,
            'date_f': self.details_facture.dateFacture_facture,
            'montant_f': str(self.details_facture.montant_facture)
        }
        document.render(template_values)
        document.save("C:/Users/Hugol/OneDrive/Bureau/Projet-Transversal-TPRE215-Axel-Le-Bihan-Yohann-Barcola-Hugo-Labord-main/facture/"+self.nomFacture+".docx")

        convert("C:/Users/Hugol/OneDrive/Bureau/Projet-Transversal-TPRE215-Axel-Le-Bihan-Yohann-Barcola-Hugo-Labord-main/facture/"+self.nomFacture+".docx")
