SELECT TOP 20 
    A.Species, 
    A.Sex, 
    W.Day AS Study_Day, 
    W.Weight_g,
    L.TestName,
    L.Value AS Lab_Result
FROM Dim_Animal A
JOIN Fact_BodyWeights W ON A.AnimalID = W.AnimalID
JOIN Fact_Labs L ON A.AnimalID = L.AnimalID
ORDER BY W.Weight_g DESC;