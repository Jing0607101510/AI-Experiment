import pandas as pd
class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.var_list = var_list
    
    def set_cpt(self, cpt):
        self.cpt = cpt

class Net():
    def __init__(self, nodes):
        self.nodes = nodes
        self.form()
    
    def form(self):
        if len(self.nodes) >= 1:
            node_can_visited = []

            data = {self.nodes[0].var_list[i]: [key[i] for key in self.nodes[0].cpt.keys()] for i in range(len(self.nodes[0].var_list))}
            data['probability'] = list(self.nodes[0].cpt.values())
            df = pd.DataFrame(data=data, columns=(self.nodes[0].var_list+['probability']))

            node_can_visited.extend(self.nodes[0].var_list)

            flag = [0] * len(self.nodes)
            flag[0] = 1
            k = 1
            while k < len(self.nodes):
                for i in range(len(self.nodes)):
                    if flag[i] == 0:
                        for name in self.nodes[i].var_list:
                            if name in node_can_visited:
                                flag[i] = 1
                                break
                        if flag[i] == 1:
                            break
                data = {self.nodes[i].var_list[j]:[key[j] for key in self.nodes[i].cpt.keys()] for j in range(len(self.nodes[i].var_list))}
                data['probability1'] = list(self.nodes[i].cpt.values())
                new_df = pd.DataFrame(data=data, columns=(self.nodes[i].var_list+['probability1']))
                df = pd.merge(df, new_df)
                df['probability'] = df['probability'] * df['probability1']
                df.drop(['probability1'],axis=1,inplace=True)

                node_can_visited.extend(self.nodes[i].var_list)
                k += 1

            self.total_joint_probability = df


    def calc_joint_probability(self, partial_var):
        data = {key : [partial_var[key]] for key in partial_var}
        df = pd.DataFrame(data=data, columns=list(partial_var.keys()))
        result = pd.merge(self.total_joint_probability, df)
        return sum(result['probability'])

if __name__ == "__main__":
    guest = Node('guest', ['guest'])
    prize = Node('prize', ['prize'])
    monty = Node('monty', ['monty', 'guest', 'prize'])

    guest.set_cpt({('A',):1/3, ('B',):1/3, ('C',):1/3})
    prize.set_cpt({('A',):1/3, ('B',):1/3, ('C',):1/3})
    monty.set_cpt({
        ('A', 'A', 'A'):0,
        ('B', 'A', 'A'):0.5,
        ('C', 'A', 'A'):0.5,
        ('A','A', 'B'):0,
        ('B','A', 'B'):0,
        ('C','A', 'B'):1,
        ('A','A', 'C'):0,
        ('B','A', 'C'):1,
        ('C','A', 'C'):0,
        ('A','B', 'A'):0,
        ('B','B', 'A'):0,
        ('C','B', 'A'):1,
        ('A','B', 'B'):0.5,
        ('B','B', 'B'):0,
        ('C','B', 'B'):0.5,
        ('A','B', 'C'):1,
        ('B','B', 'C'):0,
        ('C','B', 'C'):0,
        ('A','C', 'A'):0,
        ('B','C', 'A'):1,
        ('C','C', 'A'):0,
        ('A','C', 'B'):1,
        ('B','C', 'B'):0,
        ('C','C', 'B'):0,
        ('A','C', 'C'):0.5,
        ('B','C', 'C'):0.5,
        ('C','C', 'C'):0
    })

    nodes = [guest, prize, monty]
    net = Net(nodes)
    #第一题
    print(net.calc_joint_probability({'guest':'A', 'prize':'C','monty':'B'}))
    #第二题
    print(net.calc_joint_probability({'guest':'A', 'prize':'C', 'monty':'A'}))



    burglary = Node('burglary', ['burglary'])
    earthquake = Node('earthquake', ['earthquake'])
    alarm = Node('alarm', ['alarm', 'burglary', 'earthquake'])
    johnCalls = Node('johnCalls', ['johnCalls', 'alarm'])
    maryCalls = Node('maryCalls', ['maryCalls', 'alarm'])

    burglary.set_cpt({("True",):0.001, ("False",):0.999})
    earthquake.set_cpt({("True",):0.002, ("False",):0.998})
    alarm.set_cpt(
        {
            ("True", "True", "True") : 0.95,
            ("False", "True", "True") : 0.05,
            ('True', "True", 'False') : 0.94,
            ("False", "True", "False") :0.06,
            ('True', "False", "True") :0.29,
            ("False", "False", "True") :0.71,
            ('True', "False", 'False') :0.001,
            ("False", "False", "False") :0.999
        }
    )
    johnCalls.set_cpt(
        {
            ("True", "True") : 0.90,
            ("False", "True") : 0.10,
            ("True", "False") : 0.05,
            ("False", "False") : 0.95
        }
    )
    maryCalls.set_cpt(
        {
            ("True", "True") : .70,
            ("False", "True") : .30,
            ("True", "False") : .01,
            ("False", "False") : 0.99
        }
    )

    nodes = [burglary, earthquake, alarm, johnCalls, maryCalls]
    net = Net(nodes)

    #第一题
    print(net.calc_joint_probability({'johnCalls':'True', 'maryCalls':'True'}))
    #第二题
    print(net.calc_joint_probability({'burglary':"True", 'earthquake':"True", 'alarm':"True", 'johnCalls':'True', 'maryCalls':"True"}))
    #第三题
    print(net.calc_joint_probability({'alarm':"True", 'johnCalls':"True", 'maryCalls':"True"}) / net.calc_joint_probability({'johnCalls':"True", 'maryCalls':"True"}))
    #第四题
    print(net.calc_joint_probability({'johnCalls':'True', 'maryCalls':'False', 'burglary':'False'}) / net.calc_joint_probability({'burglary':"False"}))



    PatientAge = Node('PatientAge', ['PatientAge'])
    CTScanResult = Node('CTScanResult', ['CTScanResult'])
    MRIScanResult = Node('MRIScanResult', ['MRIScanResult'])
    Anticoagulants = Node('Anticoagulants', ['Anticoagulants'])
    StrokeType = Node('StrokeType', ['CTScanResult', 'MRIScanResult','StrokeType'])
    Mortality = Node('Mortality', ['StrokeType', 'Anticoagulants', 'Mortality'])
    Disability = Node('Disability', ['StrokeType', 'PatientAge', 'Disability'])
    PatientAge.set_cpt(
        {('0-30',):0.10, ('31-65',):0.30, ('65+',):0.60}
    )
    CTScanResult.set_cpt(
        {('Ischemic Stroke',):0.7, ('Hemmorraghic Stroke',):0.3}
    )
    MRIScanResult.set_cpt(
        {('Ischemic Stroke',):0.7, ('Hemmorraghic Stroke',):0.3}
    )
    Anticoagulants.set_cpt(
        {("Used",):0.5, ("Not used",):0.5}
    )
    StrokeType.set_cpt(
        {
            ("Ischemic Stroke", "Ischemic Stroke", "Ischemic Stroke") : .8,
            ("Ischemic Stroke", "Hemmorraghic Stroke", "Ischemic Stroke") : .5,
            ('Hemmorraghic Stroke', "Ischemic Stroke", "Ischemic Stroke") : .5,
            ('Hemmorraghic Stroke', 'Hemmorraghic Stroke', 'Ischemic Stroke') : 0,
            ('Ischemic Stroke', 'Ischemic Stroke', 'Hemmorraghic Stroke') : 0,
            ("Ischemic Stroke", 'Hemmorraghic Stroke', 'Hemmorraghic Stroke') : .4,
            ('Hemmorraghic Stroke', 'Ischemic Stroke', 'Hemmorraghic Stroke') : .4,
            ('Hemmorraghic Stroke', 'Hemmorraghic Stroke', 'Hemmorraghic Stroke') : .9,
            ('Ischemic Stroke', 'Ischemic Stroke', 'Stroke Mimic') : .2,
            ('Ischemic Stroke', 'Hemmorraghic Stroke', 'Stroke Mimic') : .1,
            ('Hemmorraghic Stroke', 'Ischemic Stroke', 'Stroke Mimic') : .1,
            ('Hemmorraghic Stroke', 'Hemmorraghic Stroke', 'Stroke Mimic') : .1,
        }
    )
    Mortality.set_cpt(
        {
            ('Ischemic Stroke', 'Used', 'False') : .28,
            ('Hemmorraghic Stroke', 'Used', 'False') : .99,
            ('Stroke Mimic', 'Used', 'False') : .1,
            ('Ischemic Stroke', 'Not used', 'False') : .56,
            ('Hemmorraghic Stroke', 'Not used', 'False') : .58,
            ('Stroke Mimic', 'Not used', 'False') : .05,
            
            ('Ischemic Stroke', 'Used', 'True') : .72,
            ('Hemmorraghic Stroke', 'Used', 'True') : .01,
            ('Stroke Mimic', 'Used', 'True') : .9,
            ('Ischemic Stroke', 'Not used', 'True') : .44,
            ('Hemmorraghic Stroke', 'Not used', 'True') : .42,
            ('Stroke Mimic', 'Not used', 'True') : .95,
        }
    )
    Disability.set_cpt(
        {
            ('Ischemic Stroke', '0-30', 'Negligible') : 0.80,
            ('Hemmorraghic Stroke', '0-30', 'Negligible') : 0.70,
            ('Stroke Mimic', '0-30', 'Negligible') : 0.9,
            ('Ischemic Stroke', '31-65', 'Negligible') : 0.60,
            ('Hemmorraghic Stroke', '31-65', 'Negligible') : 0.50,
            ('Stroke Mimic', '31-65', 'Negligible') : 0.4,
            ('Ischemic Stroke', '65+', 'Negligible') : 0.3,
            ('Hemmorraghic Stroke', '65+', 'Negligible') : 0.2,
            ('Stroke Mimic', '65+', 'Negligible') : 0.1,

            ('Ischemic Stroke', '0-30', 'Moderate') : 0.1,
            ('Hemmorraghic Stroke', '0-30', 'Moderate') : 0.2,
            ('Stroke Mimic', '0-30', 'Moderate') : 0.05,
            ('Ischemic Stroke', '31-65', 'Moderate') : 0.3,
            ('Hemmorraghic Stroke', '31-65', 'Moderate') : 0.4,
            ('Stroke Mimic', '31-65', 'Moderate') : 0.3,
            ('Ischemic Stroke', '65+', 'Moderate') : 0.4,
            ('Hemmorraghic Stroke', '65+', 'Moderate') : 0.2,
            ('Stroke Mimic', '65+', 'Moderate') : 0.1,

            ('Ischemic Stroke', '0-30', 'Severe') : 0.1,
            ('Hemmorraghic Stroke', '0-30', 'Severe') : 0.1,
            ('Stroke Mimic', '0-30', 'Severe') : 0.05,
            ('Ischemic Stroke', '31-65', 'Severe') : 0.1,
            ('Hemmorraghic Stroke', '31-65', 'Severe') : 0.1,
            ('Stroke Mimic', '31-65', 'Severe') : 0.3,
            ('Ischemic Stroke', '65+', 'Severe') : 0.3,
            ('Hemmorraghic Stroke', '65+', 'Severe') : 0.6,
            ('Stroke Mimic', '65+', 'Severe') : 0.8,
        }
    )

    nodes = [PatientAge, CTScanResult, MRIScanResult, StrokeType, Anticoagulants, Mortality, Disability]
    net = Net(nodes)

    #第一题
    print(net.calc_joint_probability({'Mortality':'True', 'PatientAge':'0-30', 'CTScanResult':'Ischemic Stroke'}) / net.calc_joint_probability({'PatientAge':'0-30', 'CTScanResult':'Ischemic Stroke'}))
    #第二题
    print(net.calc_joint_probability({'Disability':'Severe', 'PatientAge':'65+' , 'MRIScanResul':'Ischemic Stroke'}) / net.calc_joint_probability({'PatientAge':'65+' , 'MRIScanResul':'Ischemic Stroke'}))
    #第三题
    print(net.calc_joint_probability({'StrokeType': 'Stroke Mimic' ,'PatientAge':'65+', 'CTScanResult':'Hemmorraghic Stroke', 'MRIScanResult':'Ischemic Stroke'}) / net.calc_joint_probability({'PatientAge':'65+', 'CTScanResult':'Hemmorraghic Stroke', 'MRIScanResult':'Ischemic Stroke'}))
    #第四题
    print(net.calc_joint_probability({ 'Mortality':'False' ,'PatientAge':'0-30', 'Anticoagulants':'Used', 'StrokeType':'Stroke Mimic'}) / net.calc_joint_probability({'PatientAge':'0-30', 'Anticoagulants':'Used', 'StrokeType':'Stroke Mimic'}))
    #第五题
    print(net.calc_joint_probability({"PatientAge":'0-30', 'CTScanResult':'Ischemic Stroke', 'MRIScanResult':'Hemmorraghic Stroke', 'StrokeType':'Stroke Mimic','Anticoagulants': 'Used', 'Mortality': 'False', 'Disability':'Severe'}))

        