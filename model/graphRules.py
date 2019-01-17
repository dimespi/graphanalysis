from PyQt5.QtCore import QVariant

class GraphRules:

    def __init__(self, default_prop_value, attr_name, interpol):
        #QVariant peut prendre les valeurs suivantes: int, double, String ou QColor
        self.default_prop_value = QVariant(default_prop_value)
        self.attr_name = attr_name
        self.rule_set = []
        self.interpol = interpol
    
    def getDefaultProp(self):
        return self.default_prop_value    
    
    def getName(self):
        return self.attr_name
    
    def getRule(self):
        res = self.rule_set.copy()
        return res

    def addRule(self, rule):
        self.rule_set.append(rule)

    def isInterpol(self):
        return self.interpol

class Rule:
    
    def __init__(self,attr_val, prop_val, prop_name):
        #QVariant peut prendre les valeurs suivantes: int, double, String ou QColor
        self.attr_val = QVariant(attr_val)
        self.prop_val =QVariant(prop_val)
        self.prop_name = prop_name
