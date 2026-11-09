from django.db import models


class Sexe(models.TextChoices):
    MASCULIN = "M", "Masculin"
    FEMININ = "F", "Féminin"


class Quartier(models.Model):
    id_quart = models.AutoField(primary_key=True)
    nom_quart = models.CharField(max_length=100)
    commune_quart = models.CharField(max_length=100)

    class Meta:
        db_table = "quartier"

    def __str__(self):
        return f"{self.nom_quart} ({self.commune_quart})"


class Commissionnaire(models.Model):

    """le modele commissionnaire qui gere les donnees du commissionnaire depuis leurs bureau"""

    id_com = models.AutoField(primary_key=True)
    nom_com = models.CharField(max_length=100)
    prenom_com = models.CharField(max_length=100)
    sexe_com = models.CharField(max_length=1, choices=Sexe.choices)
    adr_com = models.CharField(max_length=255)
    matricule = models.CharField(max_length=100, unique=True)
    nationalite_com = models.CharField(max_length=100)
    tel_com = models.CharField(max_length=20)
    email_com = models.EmailField(unique=True)
    profile_com = models.ImageField (upload_to="commissionnaire_profiles/", null=True, blank=True)

    class Meta:
        db_table = "commissionnaire"
        ordering=["nom_com","prenom_com"]

    def __str__(self):
        return f"{self.nom_com} {self.prenom_com}"

class User_com(models.Model):

    """le modele user commissionnaire qui gere les donnees du commissionnaire qui se s'inscrit dans l'application"""

    id_user_com = models.AutoField(primary_key=True)
    nom_user_com = models.CharField (max_length=100)
    prenom_user_com = models.CharField(max_length=100)
    matricule_user_com = models.CharField(max_length=100, unique=True)
    sex_user_com = models.CharField(max_length=1, choices=Sexe.choices)
    email_user_com = models.EmailField(unique=True)
    tel_user_com = models.CharField(max_length=20)
    password_user_com = models.CharField(max_length=100)

    class Meta:
        db_table = "user_com"
        ordering=["nom_user_com","prenom_user_com"]

    def __str__(self):
        return f"{self.nom_user_com} - {self.prenom_user_com}"

class PhotoMaison(models.Model):

    """le modele photo maison qui gere les photos de la maison publiee"""

    id_photo = models.AutoField(primary_key=True)
    img_maison = models.ImageField(upload_to="maison_photos/", null=True, blank=True)

    class Meta:
        db_table = "photo_maison"

    def __str__(self):
        return f"Photo {self.id_photo} - Maison {self.maison_id}"

class Maison(models.Model):

    """le modele maison qui gere les donnees de la maison publiee"""

    id_maison = models.AutoField(primary_key=True)
    profil_maison = models.ImageField
    photo_maison = models.ForeignKey(
        PhotoMaison, on_delete=models.SET_NULL, null=True, blank=True, related_name="maisons")
    nbrpiece_maison = models.PositiveIntegerField()
    description = models.TextField()
    quartier = models.ForeignKey(
        Quartier, on_delete=models.PROTECT, related_name="maisons"
    )
    loyer = models.DecimalField(max_digits=12, decimal_places=2,)
    garantie = models.DecimalField(max_digits=12, decimal_places=2,)
    user_com_id= models.ForeignKey(
        User_com, on_delete=models.CASCADE, related_name="maisons"
    )

    class Meta:
        db_table = "maison"

    def __str__(self):
        return f"Maison {self.id_maison} - {self.quartier}"





class DataLocation(models.Model):

    """donnees pour la demande de location """

    class EtatCivil(models.TextChoices):

        """Le choix d'etat civil pour le locataire"""

        CELIBATAIRE = "Célibataire"
        MARIE = "Marié(e)"
        DIVORCE = "Divorcé(e)"
        VEUF = "Veuf/Veuve"

    id_loc = models.AutoField(primary_key=True)
    nom_loc = models.CharField(max_length=100)
    prenom_loc = models.CharField(max_length=100)
    tel_loc = models.CharField(max_length=20)
    email_loc = models.EmailField()
    etatcivil_loc = models.CharField(max_length=20, choices=EtatCivil.choices)
    nombre_enfant_loc = models.PositiveIntegerField(default=0)
    sexe_loc = models.CharField(max_length=1, choices=Sexe.choices)
    adr_loc = models.CharField(max_length=255)
    nationalite_loc = models.CharField(max_length=100)
    maison = models.ForeignKey(
        Maison,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="locations",
    )

    class Meta:
        db_table = "data_location"

    def __str__(self):
        return f"{self.nom_loc} - {self.prenom_loc}"



class Administration(models.Model):

    """le modele administration qui gere les donnees(statistiques) de l'application"""

    id_admin = models.AutoField(primary_key=True)
    user_com_id= models.ForeignKey(User_com, on_delete=models.CASCADE, related_name="administration")
    data_id = models.ForeignKey(DataLocation, on_delete=models.CASCADE, related_name="administration")

    class Meta:
        db_table = "administration"


class Auth_admin(models.Model):

    

    id_auth = id_auth = models.AutoField(primary_key=True)
    email_auth = models.EmailField(unique=True)
    password_auth = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.email_auth}"

    class Meta:
        db_table="auth_admin"