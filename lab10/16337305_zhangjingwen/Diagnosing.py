from pomegranate import *
import json
PatientAge = DiscreteDistribution({'0-30':0.10, '31-65':0.30, '65+':0.60})
CTScanResult = DiscreteDistribution({'Ischemic Stroke':0.7, 'Hemmorraghic Stroke':0.3})
MRIScanResult = DiscreteDistribution({'Ischemic Stroke':0.7, 'Hemmorraghic Stroke':0.3})
Anticoagulants = DiscreteDistribution({"Used":0.5, "Not used":0.5})

StrokeType = ConditionalProbabilityTable(
    [
        ["Ischemic Stroke", "Ischemic Stroke", "Ischemic Stroke", 0.8],
        ["Ischemic Stroke", "Hemmorraghic Stroke", "Ischemic Stroke", 0.5],
        ['Hemmorraghic Stroke', "Ischemic Stroke", "Ischemic Stroke", 0.5],
        ['Hemmorraghic Stroke', 'Hemmorraghic Stroke', 'Ischemic Stroke', 0],
        ['Ischemic Stroke', 'Ischemic Stroke', 'Hemmorraghic Stroke', 0],
        ["Ischemic Stroke", 'Hemmorraghic Stroke', 'Hemmorraghic Stroke', 0.4],
        ['Hemmorraghic Stroke', 'Ischemic Stroke', 'Hemmorraghic Stroke', 0.4],
        ['Hemmorraghic Stroke', 'Hemmorraghic Stroke', 'Hemmorraghic Stroke', 0.9],
        ['Ischemic Stroke', 'Ischemic Stroke', 'Stroke Mimic', 0.2],
        ['Ischemic Stroke', 'Hemmorraghic Stroke', 'Stroke Mimic', 0.1],
        ['Hemmorraghic Stroke', 'Ischemic Stroke', 'Stroke Mimic', 0.1],
        ['Hemmorraghic Stroke', 'Hemmorraghic Stroke', 'Stroke Mimic', 0.1]
    ],
    [CTScanResult, MRIScanResult]
)

Mortality = ConditionalProbabilityTable(
    [
        ['Ischemic Stroke', 'Used', 'False', 0.28],
        ['Hemmorraghic Stroke', 'Used', 'False', 0.99],
        ['Stroke Mimic', 'Used', 'False', 0.1],
        ['Ischemic Stroke', 'Not used', 'False', 0.56],
        ['Hemmorraghic Stroke', 'Not used', 'False', 0.58],
        ['Stroke Mimic', 'Not used', 'False', 0.05],
        
        ['Ischemic Stroke', 'Used', 'True', 0.72],
        ['Hemmorraghic Stroke', 'Used', 'True', 0.01],
        ['Stroke Mimic', 'Used', 'True', 0.9],
        ['Ischemic Stroke', 'Not used', 'True', 0.44],
        ['Hemmorraghic Stroke', 'Not used', 'True', 0.42],
        ['Stroke Mimic', 'Not used', 'True', 0.95],
    ],
    [StrokeType, Anticoagulants]
)

Disability = ConditionalProbabilityTable(
    [
        ['Ischemic Stroke', '0-30', 'Negligible', 0.80],
        ['Hemmorraghic Stroke', '0-30', 'Negligible', 0.70],
        ['Stroke Mimic', '0-30', 'Negligible', 0.9],
        ['Ischemic Stroke', '31-65', 'Negligible', 0.60],
        ['Hemmorraghic Stroke', '31-65', 'Negligible', 0.50],
        ['Stroke Mimic', '31-65', 'Negligible', 0.4],
        ['Ischemic Stroke', '65+', 'Negligible', 0.3],
        ['Hemmorraghic Stroke', '65+', 'Negligible', 0.2],
        ['Stroke Mimic', '65+', 'Negligible', 0.1],

        ['Ischemic Stroke', '0-30', 'Moderate', 0.1],
        ['Hemmorraghic Stroke', '0-30', 'Moderate', 0.2],
        ['Stroke Mimic', '0-30', 'Moderate', 0.05],
        ['Ischemic Stroke', '31-65', 'Moderate', 0.3],
        ['Hemmorraghic Stroke', '31-65', 'Moderate', 0.4],
        ['Stroke Mimic', '31-65', 'Moderate', 0.3],
        ['Ischemic Stroke', '65+', 'Moderate', 0.4],
        ['Hemmorraghic Stroke', '65+', 'Moderate', 0.2],
        ['Stroke Mimic', '65+', 'Moderate', 0.1],

        ['Ischemic Stroke', '0-30', 'Severe', 0.1],
        ['Hemmorraghic Stroke', '0-30', 'Severe', 0.1],
        ['Stroke Mimic', '0-30', 'Severe', 0.05],
        ['Ischemic Stroke', '31-65', 'Severe', 0.1],
        ['Hemmorraghic Stroke', '31-65', 'Severe', 0.1],
        ['Stroke Mimic', '31-65', 'Severe', 0.3],
        ['Ischemic Stroke', '65+', 'Severe', 0.3],
        ['Hemmorraghic Stroke', '65+', 'Severe', 0.6],
        ['Stroke Mimic', '65+', 'Severe', 0.8],
    ],
    [StrokeType, PatientAge]
)

s1 = State(PatientAge, name="PatientAge")
s2 = State(CTScanResult, name='CTScanResult')
s3 = State(MRIScanResult, name="MRIScanResult")
s4 = State(StrokeType, name="StrokeType")
s5 = State(Anticoagulants, name="Anticoagulants")
s6 = State(Mortality, name="Mortality")
s7 = State(Disability, name='Disability')

model = BayesianNetwork("Diagnosing")
model.add_states(s1, s2, s3, s4, s5, s6, s7)
model.add_transition(s2, s4)
model.add_transition(s3, s4)
model.add_transition(s4, s6)
model.add_transition(s4, s7)
model.add_transition(s5, s6)
model.add_transition(s1, s7)
model.bake()

#第一题
p1 = json.loads(str(model.predict_proba({'PatientAge':'0-30', 'CTScanResult':'Ischemic Stroke'})[-2]))['parameters'][0]['True']
print(p1)
#第二题
p2 = json.loads(str(model.predict_proba({'PatientAge':'65+', 'MRIScanResult':'Ischemic Stroke'})[-1]))['parameters'][0]['Severe']
print(p2)
#第三题
p3 = json.loads(str(model.predict_proba({'PatientAge':'65+', 'CTScanResult':'Hemmorraghic Stroke', 'MRIScanResult':'Ischemic Stroke'})[-4]))['parameters'][0]['Stroke Mimic']
print(p3)
#第四题
p4 = json.loads(str(model.predict_proba({'PatientAge':'0-30', 'Anticoagulants':'Used', 'StrokeType':'Stroke Mimic'})[-2]))['parameters'][0]['False']
print(p4)
#第五题
p5 = model.probability(['0-30', 'Ischemic Stroke', 'Hemmorraghic Stroke', 'Stroke Mimic', 'Used', 'False', 'Severe'])
print(p5)