import os, io
import requests
#import PyPDF4
from ebooklib import epub
from pypdf import PdfReader

class base_livre:
    def __init__(self,ressource=None):
        """ressource désigne soit le nom de fichier (local) correspondant au livre,
            soit une URL pointant vers un livre."""
        self.ressource = ressource

    def type(self):
        """ renvoie le type (EPUB, PDF, ou autre) du livre """
        if self.ressource.endswith(".pdf"):
            return str(PDF)
        elif self.ressource.endswith(".epub"):
            return str(EPUB)
        else:
            raise NotImplementedError("format non pris en charge!")

    def titre(self):
        """ renvoie le titre du livre """
        return self.type()(self.ressource).titre()

    def auteur(self):
        """ renvoie l'auteur du livre """
        return self.type()(self.ressource).auteur()

    def langue(self):
        """ renvoie la langue du livre """
        return self.type()(self.ressource).langue()

    def sujet(self):
        """ renvoie le sujet du livre """
        return self.type()(self.ressource).sujet()

    def date(self):
        """ renvoie la date de publication du livre """
        return self.type()(self.ressource).date()


# La sous-classe PDF
class PDF(base_livre):
    def __init__(self,ressource):
        super().__init__(ressource)
        if "://" in self.ressource :
            response = requests.get(self.ressource)
            if response.status_code == 200:
                self.ressource = PdfReader(io.BytesIO(response.content))
            else :
                raise FileNotFoundError(" Ressource inaccessible")
        else:
            if not os.path.exists(self.ressource):
                raise FileNotFoundError(f"File '{self.ressource}' does not exist.")
            self.ressource = PdfReader(self.ressource)

    def type(self):
        return "PDF"

    def titre(self):
        return self.ressource.metadata.title

    def auteur(self):
        return self.ressource.metadata.author

    def langue(self):
        return NotImplementedError(None)

    def sujet(self):
        return self.ressource.metadata.subject

    def date(self):
       return self.ressource.metadata.creation_date

    # def __repr__(self):
    #     return self.titre(), self.auteur(), self.Type(), self.date(), self.sujet()
    #
    # def __str__(self):
    #     return f"Titre: {self.titre()}, \nAuteur(s): {self.auteur()},\nType de fichier: {self.Type()}, \nDate de publication: {self.date()[2:10]}"



# la sous-classe epub
class EPUB(base_livre):

    def __init__(self,ressource):
        super().__init__(ressource)
        if "://" in self.ressource:
            response = requests.get(self.ressource)
            # Raise an exception for bad responses and bad links
            if response.status_code == 200:
                self.ressource = epub.read_epub(io.BytesIO(response.content))
            else:
                raise FileNotFoundError("ressource inaccessible")
        # Check if the resource is a file path
        else:
            if not os.path.exists(self.ressource):
                raise FileNotFoundError(f"File '{self.ressource}' does not exist.")
            self.ressource = epub.read_epub(self.ressource)

    def type(self):
        return "EPUB"

    def titre(self):
        return self.ressource.get_metadata("DC","title")[0][0]

    def auteur(self):
        return self.ressource.get_metadata("DC","creator")[0][0]

    def langue(self):
        return self.ressource.get_metadata("DC","language")[0][0]

    def sujet(self):
        return None #selon le documentation y a pas de metadata pour le sujet

    def date(self):
        return self.ressource.get_metadata("DC","date")[0][0]
