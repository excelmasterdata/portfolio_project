# portfolio/models.py
from django.db import models
from django.utils.text import slugify
from django.core.validators import EmailValidator
import uuid

class Profile(models.Model):
    """Profil principal de l'utilisateur"""
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    pseudo = models.CharField(max_length=50, unique=True, verbose_name="Pseudo")
    titre_professionnel = models.CharField(max_length=200, verbose_name="Titre professionnel")
    bio = models.TextField(verbose_name="Biographie")
    photo_profil = models.ImageField(
        upload_to='profile/', 
        verbose_name="Photo de profil",
        help_text="Recommandé : 400x400px"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class Project(models.Model):
    """Projets du portfolio"""
    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('lance', 'Lancé'),
        ('beta', 'Beta'),
        ('termine', 'Terminé'),
        ('pause', 'En pause'),
    ]

    STATUS_COLORS = {
        'en_cours': 'bg-orange-500',
        'lance': 'bg-green-500', 
        'beta': 'bg-blue-500',
        'termine': 'bg-gray-500',
        'pause': 'bg-red-500',
    }

    titre = models.CharField(max_length=200, verbose_name="Titre du projet")
    description_courte = models.TextField(
        max_length=300, 
        verbose_name="Description courte",
        help_text="Résumé en 300 caractères max"
    )
    description_detaillee = models.TextField(
        verbose_name="Description détaillée",
        help_text="Description complète pour la page détail"
    )
    image = models.ImageField(
        upload_to='projects/', 
        verbose_name="Image du projet",
        help_text="Recommandé : 800x600px"
    )
    statut = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='en_cours',
        verbose_name="Statut"
    )
    technologies = models.JSONField(
        default=list, 
        verbose_name="Technologies utilisées",
        help_text="Ex: [\"React\", \"Django\", \"PostgreSQL\"]"
    )
    slug = models.SlugField(unique=True, blank=True)
    ordre_affichage = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    featured = models.BooleanField(default=False, verbose_name="Projet mis en avant")
    url_demo = models.URLField(blank=True, null=True, verbose_name="URL de démo")
    url_github = models.URLField(blank=True, null=True, verbose_name="URL GitHub")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['ordre_affichage', '-created_at']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titre)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def status_color(self):
        return self.STATUS_COLORS.get(self.statut, 'bg-gray-500')

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('portfolio:projet_detail', kwargs={'slug': self.slug})


class Skill(models.Model):
    """Compétences professionnelles"""
    nom_competence = models.CharField(max_length=100, verbose_name="Nom de la compétence")
    description = models.TextField(verbose_name="Description détaillée")
    icone_class = models.CharField(
        max_length=50, 
        verbose_name="Classe d'icône",
        help_text="Ex: fas fa-code, fas fa-brain"
    )
    ordre_affichage = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"
        ordering = ['ordre_affichage', 'nom_competence']

    def __str__(self):
        return self.nom_competence


class News(models.Model):
    """Fil d'actualités"""
    PLATEFORME_CHOICES = [
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('blog', 'Blog'),
        ('youtube', 'YouTube'),
    ]

    PLATEFORME_COLORS = {
        'facebook': 'bg-blue-600',
        'linkedin': 'bg-blue-700',
        'twitter': 'bg-blue-400',
        'instagram': 'bg-pink-500',
        'blog': 'bg-gray-600',
        'youtube': 'bg-red-600',
    }

    titre = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(
        upload_to='news/', 
        verbose_name="Image",
        help_text="Recommandé : 600x400px"
    )
    lien_externe = models.URLField(verbose_name="Lien externe")
    plateforme = models.CharField(
        max_length=50, 
        choices=PLATEFORME_CHOICES,
        verbose_name="Plateforme"
    )
    date_publication = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de publication"
    )
    ordre_affichage = models.IntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ['ordre_affichage', '-date_publication']

    def __str__(self):
        return self.titre

    @property
    def plateforme_color(self):
        return self.PLATEFORME_COLORS.get(self.plateforme, 'bg-gray-500')


class Partner(models.Model):
    """Partenaires"""
    nom_partenaire = models.CharField(max_length=100, verbose_name="Nom du partenaire")
    logo = models.ImageField(
        upload_to='partners/', 
        verbose_name="Logo",
        help_text="Recommandé : format carré 200x200px, fond transparent"
    )
    url_site = models.URLField(blank=True, null=True, verbose_name="Site web")
    description = models.TextField(blank=True, verbose_name="Description")
    ordre_affichage = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ['ordre_affichage', 'nom_partenaire']

    def __str__(self):
        return self.nom_partenaire


class SocialGallery(models.Model):
    """Galerie sociale"""
    image = models.ImageField(
        upload_to='gallery/', 
        verbose_name="Image",
        help_text="Recommandé : 600x600px"
    )
    titre = models.CharField(max_length=200, verbose_name="Titre")
    description_courte = models.TextField(
        max_length=300, 
        verbose_name="Description courte",
        help_text="Résumé en 300 caractères max"
    )
    contenu_detaille = models.TextField(
        verbose_name="Contenu détaillé",
        help_text="Contenu complet pour la page détail"
    )
    slug = models.SlugField(unique=True, blank=True)
    ordre_affichage = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Galerie sociale"
        verbose_name_plural = "Galerie sociale"
        ordering = ['ordre_affichage', '-created_at']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titre)
            slug = base_slug
            counter = 1
            while SocialGallery.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('portfolio:galerie_detail', kwargs={'slug': self.slug})


class Feed(models.Model):
    """Feed d'images"""
    image = models.ImageField(
        upload_to='feed/', 
        verbose_name="Image",
        help_text="Images pour le feed principal"
    )
    alt_text = models.CharField(
        max_length=200, 
        verbose_name="Texte alternatif",
        help_text="Description de l'image pour l'accessibilité"
    )
    ordre_affichage = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feed"
        verbose_name_plural = "Feed"
        ordering = ['ordre_affichage', '-created_at']

    def __str__(self):
        return f"Feed image {self.id}"


class Newsletter(models.Model):
    """Abonnés newsletter"""
    email = models.EmailField(
        unique=True, 
        validators=[EmailValidator()],
        verbose_name="Email"
    )
    date_inscription = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'inscription"
    )
    actif = models.BooleanField(default=True, verbose_name="Actif")
    token_desabonnement = models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        verbose_name="Token de désabonnement"
    )

    class Meta:
        verbose_name = "Abonné newsletter"
        verbose_name_plural = "Abonnés newsletter"
        ordering = ['-date_inscription']

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    """Messages de contact"""
    nom = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    sujet = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    date_envoi = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    lu = models.BooleanField(default=False, verbose_name="Lu")
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"{self.nom} - {self.sujet}"