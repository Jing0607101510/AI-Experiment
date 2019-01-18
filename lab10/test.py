from pomegranate import *
from matplotlib import pyplot as plt



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

s1 = State(burglary, name="burglary")
s2 = State(earthquake, name="earthquake")
s3 = State(alarm, name="alarm")


model = BayesianNetwork("Burglary")
model.add_states(s1, s2, s3)
model.add_transition(s1, s3)
model.add_transition(s2, s3)
model.bake()


print(model.probability({'burglary':"True", 'earthquake':'True'}))
#求得是条件概率
# print(model.predict_proba({}))

# print(model.probability({'johnCalls':'True', 'maryCalls':"True"}))
# print(model.probability(["True", "True", "True", "True", "True"]))
# print(model.predict_proba([None, None, None, "True", "True"]))

# #适用条件概率公式计算P（j，-M|-B）
# numerator = model.probability(['False', None, None, 'True', 'False'])
# denominator = model.probability(["False", None, None, None, None])
# probability = numerator / denominator
# print(probability)