import re

class EntityExtractor:
    def __init__(self):
        self.entities = [
            #Label, Patterns
            ["color", [
               ["black", "black"],
               ["blue", "blue"],
               ["brown", "brown"],
               ["beige", "beige"],
               ["gray", "gr(a|e)y"],
               ["green", "green"],
               ["orange", "orange"],
               ["pink", "pink"],
               ["purple", "purple"],
               ["red", "(red)"],
               ["white", "white"],
               ["yellow", "yellow"],
            ]],
            ["fabric", [
                ["denim", "(denim|jean(s)?)"],
                ["knitted", "(knit(ted)?|whool)"],
                ["laced", "(lac(e|y|ed)|jacquard)"],
                ["glossy", "(leather|glossy)"],
                ["velvet", "(velvet|plushy)"],
                ["general", "(cotton|jersey|silk|satin)"],
            ]],
            ["pattern", [
                ["animal_print", "animal([\ -]+print)?"],
                ["geometric", "(geometric|argyle)"],
                ["camouflage", "camouflage"],
                ["checked", "(checked|plaid)"],
                ["floral", "flo(ral|wer)"],
                ["paisley", "paisley"],
                ["plain", "plain"],
                ["dots", "dot(s|ted)?"],
                ["striped", "stripe(s|d)?"],
                ["tie_dyed", "tie[\ -]+dye(d)?"],
            ]],
            ["size", [
                ["maxi", "(max(i)?|long(er)?)"],
                ["midi", "(mid(i)?)"],
                ["mini", "(mini|short)"],
            ]],
            ["type", [
                ["straight", "(pencil|straight|bubble|tulip)"],
                ["pleated", "((pleat(s|es|ed)?)|a[\ -]+line|yoke|panel|tiered|gathered|godet)"],
                ["skewed", "(skewed|wrap|hankerchief|sarong|assymetric)"],
            ]],
        ]
    def extract(self, text):
        ents = []
        for label, ent in self.entities:
            for key, pattern in ent:
                x = re.search(r'\b{}\b'.format(pattern), text.lower())
                if x:
                    ents.append([key , label])
        return ents