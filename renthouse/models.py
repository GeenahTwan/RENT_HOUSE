from django.conf import settings
from django.db import models


class Sexe(models.TextChoices):
    MASCULIN = "M", "Masculin"
    FEMININ = "F", "Féminin"


class EtatCivil(models.TextChoices):
    CELIBATAIRE = "Célibataire"
    MARIE = "Marié(e)"
    DIVORCE = "Divorcé(e)"
    VEUF = "Veuf/Veuve"


class Quartier(models.Model):
    id_quart = models.AutoField(primary_key=True)
    nom_quart = models.CharField(max_length=100)
    commune_quart = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom_quart} ({self.commune_quart})"


class Commissionnaire(models.Model):
    id_com = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="commissionnaire",
    )
    nom_com = models.CharField(max_length=100)
    prenom_com = models.CharField(max_length=100)
    sex_com = models.CharField(max_length=1, choices=Sexe.choices)
    adr_com = models.CharField(max_length=255)
    matricule_com = models.CharField(max_length=100, unique=True)
    nationalite_com = models.CharField(max_length=100)
    tel_com = models.CharField(max_length=20)
    email_com = models.EmailField(unique=True)
    profile_com = models.ImageField(upload_to="commissionnaires/", blank=True)

    def __str__(self):
        return f"{self.nom_com} {self.prenom_com}"


class Maison(models.Model):
    id_maison = models.AutoField(primary_key=True)
    profil_maison = models.ImageField(upload_to="maisons/profil/")
    nbrpiece_maison = models.PositiveIntegerField()
    description = models.TextField()
    quartier = models.ForeignKey(
        Quartier, on_delete=models.PROTECT, related_name="maisons"
    )
    loyer = models.DecimalField(
        max_digits=12, decimal_places=2,
    )
    garantie = models.DecimalField(
        max_digits=12, decimal_places=2,
    )
    commissionnaire = models.ForeignKey(
        Commissionnaire, on_delete=models.CASCADE, related_name="maisons"
    )

    def __str__(self):
        return f"Maison {self.id_maison} - {self.quartier}"


class PhotoMaison(models.Model):
    id_photo = models.AutoField(primary_key=True)
    maison = models.ForeignKey(
        Maison, on_delete=models.CASCADE, related_name="photos"
    )
    img_maison = models.ImageField(upload_to="maisons/photos/")

    def __str__(self):
        return f"Photo {self.id_photo} - Maison {self.maison_id}"


class DataLocation(models.Model):
    id_loc = models.AutoField(primary_key=True)
    nom_loc = models.CharField(max_length=100)
    prenom_loc = models.CharField(max_length=100)
    tel_loc = models.CharField(max_length=20)
    email_loc = models.EmailField()
    etatcivil_loc = models.CharField(max_length=20, choices=EtatCivil.choices, default=EtatCivil.CELIBATAIRE)
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

    def __str__(self):
        return f"{self.nom_loc} {self.prenom_loc}"


class ComLoc(models.Model):
    loc = models.ForeignKey(DataLocation, on_delete=models.CASCADE)
    com = models.ForeignKey(Commissionnaire, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("loc", "com")

    def __str__(self):
        return f"{self.com} - {self.loc}"


class Administration(models.Model):
    id_admin = models.AutoField(primary_key=True)
    com = models.ForeignKey(
        Commissionnaire, on_delete=models.CASCADE, related_name="administrations"
    )
    data = models.ForeignKey(
        DataLocation, on_delete=models.CASCADE, related_name="administrations"
    )

    def __str__(self):
        return f"Administration {self.id_admin}" 