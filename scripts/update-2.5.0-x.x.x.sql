-- ============================================================================
-- APEL UPDATE SCRIPT FOR CLIENT SCHEMA
-- APEL version 2.5.0 databases of the following types to x.x.x:
-- Run this script against the grid client database
--
-- This script will:
--  - Add new column InfrastructureDescription to:
--      SuperSummaries
--      VSuperSummaries
--  - Recreate procedures:
--      SummariseJobs
-- ============================================================================

-- -----------------------------
-- Add columns
-- -----------------------------
ALTER TABLE SuperSummaries
  ADD InfrastructureDescription VARCHAR(100)
  AFTER InfrastructureType;

-- -----------------------------
-- Add column InfrastructureDescription
-- -----------------------------
-- Update view on SuperSummaries
DROP VIEW IF EXISTS VSuperSummaries;
CREATE VIEW VSuperSummaries AS
    SELECT
        UpdateTime,
        site.name Site,
        Month,
        Year,
        userdn.name GlobalUserName,
        vos.name VO,
        vogroup.name VOGroup,
        vorole.name VORole,
        submithost.name SubmitHost,
        InfrastructureType,
        InfrastructureDescription,
        ServiceLevelType,
        ServiceLevel,
        NodeCount,
        Processors,
        EarliestEndTime,
        LatestEndTime,
        WallDuration,
        CpuDuration,
        NumberOfJobs
    FROM SuperSummaries,
         Sites site,
         DNs userdn,
         VORoles vorole,
         VOs vos,
         VOGroups vogroup,
         SubmitHosts submithost
    WHERE
        SiteID = site.id
        AND GlobalUserNameID = userdn.id
        AND VORoleID = vorole.id
        AND VOID = vos.id
        AND VOGroupID = vogroup.id
        AND SubmitHostID = submithost.id;

-- -----------------------------
-- Procedures
-- -----------------------------
-- Update SummariseJobs procedure
DROP PROCEDURE IF EXISTS SummariseJobs;
DELIMITER //
CREATE PROCEDURE SummariseJobs()
BEGIN
    REPLACE INTO SuperSummaries(SiteID, Month, Year, GlobalUserNameID, VOID,
        VOGroupID, VORoleID, SubmitHostID, InfrastructureType, InfrastructureDescription,
        ServiceLevelType, ServiceLevel, NodeCount, Processors, EarliestEndTime,
        LatestEndTime, WallDuration, CpuDuration, NumberOfJobs)
    SELECT SiteID,
    EndMonth AS Month, EndYear AS Year,
        GlobalUserNameID, VOID, VOGroupID, VORoleID, SubmitHostID, InfrastructureType,
        InfrastructureDescription, ServiceLevelType, ServiceLevel, NodeCount, Processors,
    MIN(EndTime) AS EarliestEndTime,
    MAX(EndTime) AS LatestEndTime,
    SUM(WallDuration) AS SumWCT,
    SUM(CpuDuration) AS SumCPU,
    COUNT(*) AS Njobs
    FROM JobRecords
    GROUP BY SiteID, VOID, GlobalUserNameID, VOGroupID, VORoleID, EndYear, EndMonth, InfrastructureType,
             SubmitHostID, ServiceLevelType, ServiceLevel, NodeCount, Processors
    ORDER BY NULL;
END //
DELIMITER ;
