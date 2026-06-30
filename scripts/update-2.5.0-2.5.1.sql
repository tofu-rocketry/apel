-- ============================================================================
-- APEL UPDATE SCRIPT FOR CLIENT SCHEMA
-- APEL version 2.5.0 databases of the following types to 2.5.1:
-- Run this script against the ??
--
-- This script will:
--  - Add new column InfrastructureDescription to:
--      SuperSummaries
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
