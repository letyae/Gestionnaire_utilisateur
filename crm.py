# -*- coding: utf-8 -*-
import re #regex
import string 
class User:

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



if __name__=="__main__":
    from faker  import Faker

    fake=Faker(locale="fr_FR") 
    for _ in range(3):
        user=User(
            first_name=fake.first_name(),
            last_name=fake.last_name(), 
            phone_number=fake.phone_number(),
            address= fake.address()
            )
        user._checks()
        print(user.full_name)
        print(user)
        #print(repr(user))
        print("-"*10,"\n")
