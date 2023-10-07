# -*- coding: utf-8 -*-
import re #regex
import string 
from tinydb import TinyDB, where  
from pathlib import Path


class User:
    #attr de class
    DB=TinyDB(Path(__file__).resolve().parent / "db.json", indent = 4)
    
    def  __init__(self, first_name: str, last_name: str, phone_number: str="", address: str=""):
        self.first_name=first_name
        self.last_name=last_name
        self.phone_number=phone_number
        self.address=address

    def __str__(self):
        #return(f"{self.first_name}\n{self.last_name}\n{self.phone_number}\n{self.address}")
         return(f"{self.full_name}\n{self.phone_number}\n{self.address}\n")
   
     # ce decorateur permet de dynamiser la fonction
    @property
    def __attr__(self):
        return (f"{self.first_name} {self.last_name}")
    
  
    @property
    def full_name(self)->str:
       """donne le nom complet
         Arg: None
               Return: str
       """
       return(f"{self.first_name} {self.last_name}")

    
    @property
    def db_instance(self)->object:
        """retourne les donnes ayant le nom et prenom de l'objet courant l'instance present ds la bdd
        arg: None
        return: object
        """
        return User.DB.get((where('first_name')==self.first_name) & (where('last_name')==self.last_name))
        

    #methode pour avoir representation de classe
    def __repr__(self) :
        """indication sur comment recreer objet à partir des info
               Arg: None
               Return: object
         """
    
        return f"User({self.first_name}, {self.last_name})"
    
    

    def _check_phonenumber(self):
        """ netoyer pour extraire les caratere speciaux des num de tel, et verifier sa validite
            attr: None
        """
        phone_digit=re.sub(r"[+()\s]*","",self.phone_number)
        if len(phone_digit)<10 or not phone_digit.isdigit():
            raise ValueError(f"Numéro de telephone {self.phone_number} invalide.")
        
    def _check_names(self):
        """"Verifie la validite du nom et prenom
        arg: None
        """

        if not (self.first_name and self.last_name):
            raise ValueError("Le nom et le prenom  ne peuvent être vide")

        specialcharacter=string.punctuation+string.digits
        
        if  any(char in self.full_name for char in specialcharacter):
            raise ValueError(f"Nom: {self.full_name} invalide.")
       
    def _checks(self):
        """Pour lancer ts les checks"""
        self._check_phonenumber()
        self._check_names()

    def exists(self)->bool:
        """ retourne true si un user exist"""
        return bool(self.db_instance)

    def delete(self)->list[int]:
        """"pour supprimer un user ds la bdd s'il exist
        args: None
        return: list[int] # liste des id des users surprimé
        """ 
        if self.exists():
           User.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []
       
    def save(self, validate_data: bool=False) -> int :
        """verifier les donne si validate_data=true, enregistrer donnee ds une bdd  
        Arg: bool [optional] : 
        return: int, correspond au identifiant uniq des tuples inserer
        """

        if(validate_data):
           self._checks()

        if self.exists():
          return -1        
        return User.DB.insert(self.__dict__) 

def get_all_users()->list:
    """Recuperer les donnee des utilisateurs ds la bdd
    Arg:None
    return list liste de ts les  users 
    """

    #for user in User.DB.all():
        #print(user) # unpack pour recup cle et val de chaq dict (instance)
        #chaq_user=User(**user)
        #print(chaq_user.full_name)

    return [ User(**user) for user in User.DB.all()]
    

if __name__=="__main__":
    from faker  import Faker

    fake=Faker(locale="fr_FR") 
    for _ in range(10):
        user=User(
            first_name=fake.first_name(),
            last_name=fake.last_name(), 
            phone_number=fake.phone_number(),
            address= fake.address()
            )
        user._checks()
        print(user.full_name)
        print(user.save())
          
       
        #print(user.full_name)
        #print(repr(user))
       
        print()
        print("-"*10)
#Afficher ts les users        
print(get_all_users())    


#Verifier si une instance existe ds la bdd
utilisateur= User( "Pauline","Perrot")
print(utilisateur.db_instance) 

#print(utilisateur.db_instance.doc_id) 
# doc id permet d'acceder a l'id uniq de l'instance ou son objet ds la bdd) 

print(utilisateur.delete())