import xml.etree.ElementTree as etree
from .model import GraphRules, Rule
from PyQt5.QtGui import QImageReader, QPainter, QColor

class SymbologyReader:
    def read(self, path):
        tree = etree.parse(path)
        root = tree.getroot()
        node_rules = self.parseRule(
            root.findall(".//noderules/rule"))
        edge_rules = self.parseRule(
            root.findall(".//edgerules/rule"))
        return ({"node_rules": node_rules, "edge_rules": edge_rules})

    def rulesToXml(self, filename, rules):
        graph_render = etree.Element("graphrenderer")
        for key in rules:
            if (key == "node_rules"):
                node_rules = etree.Element(key)
            if (key == "edge_rules"):
                edge_rules = etree.Element(key)
        graph_render.append(node_rules)
        graph_render.append(edge_rules)
        for k, grules in rules.items():
            if k == "node_rules":
                for k, rule in grules.items():
                    attribute_name = rule.attr_name
                    interpol = rule.interpol
                    default_prop_value = rule.getDefaultProp().value()
                    rule_b = etree.SubElement(node_rules, "rule")
                    rule_b.set("property", k)
                    attr = etree.SubElement(rule_b, "attribute")
                    attr.text = attribute_name
                    interpol_r = etree.SubElement(rule_b, "interpol")
                    interpol_r.text = interpol
                    default_prop = etree.SubElement(rule_b, "default")
                    self.parseQVariant(default_prop, default_prop_value)
                    rulee = rule.getRule()
                    if (len(rulee) != []):
                        for i in range(len(rulee)):
                            rule_unit = etree.SubElement(rule_b, "ruleunit")
                            rule_unit.set("name", str(rulee[i].prop_name))
                            atr_val = etree.SubElement(rule_unit, "attr_val")
                            atr_value = rulee[i].attr_val.value()
                            self.parseQVariant(atr_val, atr_value)
                            prop_val = etree.SubElement(rule_unit, "prop_val")
                            prop_value = rulee[i].prop_val.value()
                            self.parseQVariant(prop_val, prop_value)
            elif(k == "edge_rules"):
                for k, rule in grules.items():
                    attribute_name = rule.attr_name
                    interpol = rule.interpol
                    default_prop_value = rule.getDefaultProp().value()
                    rule_b = etree.SubElement(edge_rules, "rule")
                    rule_b.set("property", k)
                    attr = etree.SubElement(edge_rules, "attribute")
                    attr.text = attribute_name
                    interpol_r = etree.SubElement(edge_rules, "interpol")
                    interpol_r.text = interpol
                    default_prop = etree.SubElement(edge_rules, "default")
                    self.parseQVariant(default_prop, default_prop_value)
                    rulee = rule.getRule()
                    if (len(rulee) != []):
                        for i in range(len(rulee)):
                            rule_unit = etree.SubElement(rule_b, "ruleunit")
                            rule_unit.set("name", str(rulee[i].prop_name))
                            atr_val = etree.SubElement(rule_unit, "attr_val")
                            atr_value = rulee[i].attr_val.value()
                            self.parseQVariant(atr_val, atr_value)
                            prop_val = etree.SubElement(rule_unit, "prop_val")
                            prop_value = rulee[i].prop_val.value()
                            self.parseQVariant(prop_val, prop_value)
        
        renderer = etree.ElementTree(graph_render)

        with open(filename, "wb") as sb:
            renderer.write(sb)

    def parseQVariant(self, default_prop, default_prop_value):
        if(type(default_prop_value) == QColor):
            default_prop.set('iscolor', '1')
            default_prop.set('r', 'r')
            default_prop.set('g', 'g')
            default_prop.set('b', 'b')
        elif(type(default_prop_value) == int):
            default_prop.set('iscolor', '0')
            default_prop.set('ival', str(default_prop_value))
        elif(type(default_prop_value) == float):
            default_prop.set('iscolor', '0')
            default_prop.set('dval', str(default_prop_value))
        elif(type(default_prop_value) == str):
            default_prop.set('iscolor', '0')
            default_prop.set('str', str(default_prop_value))

    def parseRule(self, sub_tree):
        rules = {}
        for rule in sub_tree:
            property = rule.get('property')
            childrens = rule.getchildren()
            attribut = childrens[0].text
            default = self.parseValue(childrens[1])
            interpol = childrens[2].text
            childrens.pop(0)
            childrens.pop(0)
            childrens.pop(0)
            graphRule = GraphRules(default, attribut, interpol)
            for child in childrens:
                liste = list(child)
                prop_name = child.get('name')
                attr_value = self.parseValue(liste[0])
                prop_value = self.parseValue(liste[1])
                graphRule.addRule(Rule(attr_value, prop_value, prop_name))
            rules[property] = graphRule
        return(rules)

    def parseValue(self, value):
        res = 0
        if(int(value.get('iscolor'))):
            r = int(value.get('r'))
            g = int(value.get('g'))
            b = int(value.get('b'))
            res = QColor(r, g, b)
        elif(value.get('ival') != None):
            res = int(value.get('ival'))
        elif(value.get('dval') != None):
            res = float(value.get('dval'))
        elif(value.get('str') != None):
            res = value.get('str')
        return res


def main():
    symbo_reader = SymbologyReader()
    rules = symbo_reader.read("render.xml")
    symbo_reader.rulesToXml("renderer_save.xml", rules)


if __name__ == "__main__":
    main()
