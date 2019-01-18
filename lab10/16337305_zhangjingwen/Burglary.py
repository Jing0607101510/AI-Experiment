from pomegranate import *
from matplotlib import pyplot as plt
import json


burglary = DiscreteDistribution({"True":0.001, "False":0.999})
earthquake = DiscreteDistribution({"True":0.002, "False":0.998})
alarm = ConditionalProbabilityTable(
    [
        ["True", "True", "True", 0.95],
        ["True", "True", "False", 0.05],
        ["True", 'False', 'True', 0.94],
        ["True", "False", "False", 0.06],
        ["False", "True", 'True', 0.29],
        ["False", "True", "False", 0.71],
        ["False", 'False', 'True', 0.001],
        ["False", "False", "False", 0.999]
    ],
    [burglary, earthquake]
)

johnCalls = ConditionalProbabilityTable(
    [
        ["True", "True", 0.90],
        ["True", "False", 0.10],
        ["False", "True", 0.05],
        ["False", "False", 0.95]
    ],
    [alarm]
)

maryCalls = ConditionalProbabilityTable(
    [
        ["True", "True", 0.70],
        ["True", "False", 0.30],
        ["False", "True", 0.01],
        ["False", "False", 0.99]
    ],
    [alarm]
)

s1 = State(burglary, name="burglary")
s2 = State(earthquake, name="earthquake")
s3 = State(alarm, name="alarm")
s4 = State(johnCalls, name="johnCalls")
s5 = State(maryCalls, name="maryCalls")

model = BayesianNetwork("Burglary")
model.add_states(s1, s2, s3, s4, s5)
model.add_transition(s1, s3)
model.add_transition(s2, s3)
model.add_transition(s3, s4)
model.add_transition(s3, s5)
model.bake()

#第1题
m_is_true = json.loads(str(model.predict_proba({})[-1]))['parameters'][0]['True']
j_is_true = json.loads(str(model.predict_proba({'maryCalls':"True"})[-2]))['parameters'][0]['True']
p_j_and_m = m_is_true * j_is_true
print(p_j_and_m)

#第2题
print(model.probability(['True', "True", "True", 'True', 'True']))

#第3题
print(model.predict_proba([None, None, None, "True", 'True']))

#第4题
p_not_b = json.loads(str(model.predict_proba({})[0]))['parameters'][0]['False']
p_not_m_not_b = json.loads(str(model.predict_proba({'burglary':"False"})[-1]))['parameters'][0]['False']
p_j_not_m_not_b = json.loads(str(model.predict_proba({'burglary':"False", 'maryCalls':"False"})[-2]))['parameters'][0]["True"]
numerator = p_not_b * p_not_m_not_b * p_j_not_m_not_b
denominator = json.loads(str(model.predict_proba({})[0]))['parameters'][0]['False']
probability = numerator / denominator
print(probability)
