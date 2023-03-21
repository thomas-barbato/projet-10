LOW = "faible"
AVERAGE = "moyenne"
HIGH = "élevée"
PRIORITY_CHOICES = [(LOW, "low"), (AVERAGE, "average"), (HIGH, "high")]

TO_DO = "à faire"
IN_PROGRESS = "en cours"
DONE = "terminée"
TASK_STATUS_CHOICES = [(TO_DO, "to do"), (IN_PROGRESS, "in progress"), (DONE, "done")]

BUG = "bug"
IMPROVEMENT = "amélioration"
TASK = "tâche"
TAG_CHOICES = [
    (BUG, "bug"),
    (IMPROVEMENT, "improvement"),
    (TASK, "task"),
]

PROJECT = "projet"
PRODUCT = "produit"
APPLICATION = "application"
PROJECT_TYPE = [
    (PROJECT, "project"),
    (PRODUCT, "product"),
    (APPLICATION, "application"),
]

CREATOR = "createur"
ADMIN = "administrateur"
TECHNICIAN = "technician"
CONTRIBUTOR_CHOICES = [
    (CREATOR, "creator"),
    (ADMIN, "admin"),
    (TECHNICIAN, "technician")
]
