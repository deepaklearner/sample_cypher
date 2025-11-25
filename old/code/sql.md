WITH aethusers_clone AS (

    SELECT 
        'FWaris2' AS samaccountname,
        '2017328' AS E_EmployeeID,
        'CLOUD' AS extensionattribute3,
        'Enabled' AS accountdisabled,
        'CORP.CVS' AS domain,
        'abc' AS admin_description,
        '' AS user_oneid,
        'N' AS to_be_included,
        NULL AS lastuseraccountoneid,
        '2024-01-18 09:24:45' AS lastlogontimestamp
    UNION ALL

    SELECT
        'Fwaris' AS samaccountname,
        '2017328' AS E_EmployeeID,
        'CLOUD' AS extensionattribute3,
        'Enabled' AS accountdisabled,
        'CORP.CVS' AS domain,
        'abc' AS admin_description,
        '' AS user_oneid,
        'N' AS to_be_included,
        NULL AS lastuseraccountoneid,
        '2024-01-18 09:24:45' AS lastlogontimestamp
SELECT 
    samaccountname,
    E_EmployeeID,
    COALESCE(extensionattribute3, 'DNE') AS extensionattribute,
    accountdisabled,
    domain,
    COALESCE(admin_description, 'DNE') AS admin_description,
    '' AS user_oneid,
    'N' AS to_be_included,
    NULL AS lastuseraccountoneid,
    COALESCE(lastlogontimestamp, '2099-12-12 00:00:00') AS lastlogontimestamp,

    CONCAT(E_EmployeeID, '|', samaccountname, '|', domain) AS concat_attr_col,

    CONCAT(
        E_EmployeeID, '|', samaccountname, '|', domain, '|',
        COALESCE(extensionattribute3, 'DNE'), '|',
        COALESCE(admin_description, 'DNE')
    ) AS concat_attr_col1,

    CONCAT(E_EmployeeID, '|', samaccountname, '|', domain, '|ASSIGNED') AS concat_attr_col2

FROM aethusers_clone
WHERE E_EmployeeID IS NOT NULL
  AND E_EmployeeID IN ('$$users');
