USE MyDatabase;
GO

-- You should see ~66,376 rows for BodyWeights and ~23,868 for Animals
SELECT 'Staging_BodyWeights' AS Tab, COUNT(*) AS Count FROM Staging_BodyWeights
UNION ALL
SELECT 'Staging_Animals', COUNT(*) FROM Staging_Animals;