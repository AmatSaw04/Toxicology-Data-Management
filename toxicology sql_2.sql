USE MyDatabase;
GO

DROP TABLE IF EXISTS Fact_Labs;
DROP TABLE IF EXISTS Fact_BodyWeights;
DROP TABLE IF EXISTS Dim_Animal;

-- Clean Animal Table 
CREATE TABLE Dim_Animal (
    AnimalID VARCHAR(50) PRIMARY KEY, 
    StudyID VARCHAR(50),
    Species VARCHAR(255),
    Sex VARCHAR(50),
    Age VARCHAR(50)
);

-- Clean Body Weight Table 
CREATE TABLE Fact_BodyWeights (
    WeightID INT IDENTITY(1,1) PRIMARY KEY,
    AnimalID VARCHAR(50), 
    StudyID VARCHAR(50),
    Day VARCHAR(50),
    Weight_g FLOAT
);

-- Clean Lab Results Table 
CREATE TABLE Fact_Labs (
    LabID INT IDENTITY(1,1) PRIMARY KEY,
    AnimalID VARCHAR(50), 
    TestName VARCHAR(50), 
    Value FLOAT
);
GO


-- LOAD ANIMALS 
WITH UniqueAnimals AS (
    SELECT 
        INDIVIDUAL_ID, 
        EXP_ID, 
        STRAIN_TYPE, 
        SEX_TYPE, 
        [ANIMAL_AGE(week)],
        ROW_NUMBER() OVER(PARTITION BY INDIVIDUAL_ID ORDER BY EXP_ID) as RowNum
    FROM Staging_Animals
    WHERE INDIVIDUAL_ID IS NOT NULL
)
INSERT INTO Dim_Animal (AnimalID, StudyID, Species, Sex, Age)
SELECT INDIVIDUAL_ID, EXP_ID, STRAIN_TYPE, SEX_TYPE, [ANIMAL_AGE(week)]
FROM UniqueAnimals
WHERE RowNum = 1;

print '✅ Animals Loaded Successfully';

-- B. LOAD BODY WEIGHTS
INSERT INTO Fact_BodyWeights (AnimalID, StudyID, Day, Weight_g)
SELECT 
    INDIVIDUAL_ID, 
    EXP_ID, 
    PROGRESS_TIME, 
    TRY_CAST(BODY_WEIGHT AS FLOAT)
FROM Staging_BodyWeights
WHERE 
    TRY_CAST(BODY_WEIGHT AS FLOAT) IS NOT NULL
    AND INDIVIDUAL_ID IN (SELECT AnimalID FROM Dim_Animal);

print 'Body Weights Loaded Successfully';

-- C. LOAD LABS
INSERT INTO Fact_Labs (AnimalID, TestName, Value)
-- 1. ALT (Liver)
SELECT INDIVIDUAL_ID, 'ALT', TRY_CAST([ALT(IU/L)] AS FLOAT) 
FROM Staging_Biochemistry WHERE TRY_CAST([ALT(IU/L)] AS FLOAT) IS NOT NULL
UNION ALL
-- 2. AST (Liver)
SELECT INDIVIDUAL_ID, 'AST', TRY_CAST([AST(IU/L)] AS FLOAT) 
FROM Staging_Biochemistry WHERE TRY_CAST([AST(IU/L)] AS FLOAT) IS NOT NULL
UNION ALL
-- 3. BUN (Kidney)
SELECT INDIVIDUAL_ID, 'BUN', TRY_CAST([BUN(mg/dL)] AS FLOAT) 
FROM Staging_Biochemistry WHERE TRY_CAST([BUN(mg/dL)] AS FLOAT) IS NOT NULL
UNION ALL
-- 4. TBIL (Bilirubin)
SELECT INDIVIDUAL_ID, 'TBIL', TRY_CAST([TBIL(mg/dL)] AS FLOAT) 
FROM Staging_Biochemistry WHERE TRY_CAST([TBIL(mg/dL)] AS FLOAT) IS NOT NULL;

print 'Lab Data Loaded Successfully';
GO