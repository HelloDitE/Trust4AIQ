from dataclasses import dataclass

@dataclass
class Patient:
    id: str
    age: int
    gender: str
    respiratory: str
    bmi: float
    cardio: str
    immune: str
    post_op: str
    smoking: str
    pregnancy: str
    vuln_score: float
    
    # On pourra ajouter des méthodes ici plus tard si besoin