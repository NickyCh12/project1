## Generate overall monthly trending (volume & avg rent & % change in rent)
  WITH summary AS (
    SELECT EXTRACT(YEAR FROM Transaction_Date) AS year, EXTRACT(MONTH FROM Transaction_Date) AS month, ROUND(AVG(Transaction_Rent),2) AS avg_rent, COUNT(*) AS total_transactions
    FROM table
    GROUP BY year, month
    ORDER BY year,month)

  SELECT year, month, avg_rent, ROUND(((avg_rent - (LAG(avg_rent,1) OVER(ORDER BY year, month)))/(LAG(avg_rent,1) OVER(ORDER BY year, month))*100),2) AS rent_percent_changes,      
  total_transactions
  FROM summary
  ORDER BY year, month
  
  
## Generate unit size (SFA) trend
  SELECT SFA_Range AS  unit_SFA_range, COUNT(*) AS total_transactions, ROUND(AVG(Transaction_Rent),2) AS avg_rent
  FROM table
  GROUP BY SFA_Range
  HAVING SFA_Range <> "N/A"
  ORDER BY total_transactions DESC
  
  
## Generate top 10 districts with highest volumes / average rent
  SELECT District, COUNT(*) AS total_transactions, ROUND(AVG(Transaction_Rent),2) AS avg_rent
  FROM table
  GROUP BY District
  ORDER BY total_transactions DESC
  LIMIT 10
  
  
## Generate total volume and average transaction rent for specific unit type in each district
  SELECT District, SFA_Range, COUNT(*) AS total_transactions, ROUND(AVG(Transaction_Rent),2) AS avg_rent
  FROM table
  GROUP BY District, SFA_Range
  HAVING SFA_Range = "400 - 800 sq.ft."
  ORDER BY total_transactions DESC
  
  
 ## Generate rental difference between different floor (upper/middle/lower)
  SELECT Floor, COUNT(*) AS total_transactions, ROUND(AVG(Transaction_Rent),2) AS avg_rent
  FROM table
  GROUP BY Floor
  HAVING Floor <> "N/A"
  ORDER BY avg_rent DESC
  
  
## Sample of using "IF" to replace values
  SELECT Transaction_Date AS Date, Building, Floor, Transaction_Rent AS Rent,
         if (GFA='N/A',"Unknown", GFA) AS GFA
  FROM table
  ORDER BY Date DESC


## Sample of using "SAFE_CAST" and "WHEN" to clean and categorize data
  ***the column "SFA" is auto-classified as "STRING" because there are certain values with commas. We need to covert them into numeric values in order to perform calculation. Usuing "WITH" to create a correctly formatted table for "SFA".
    
    WITH new_data AS (
                      SELECT SAFE_CAST(REPLACE(SFA,",","") AS INT64) AS new_SFA
                      FROM table)

 -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
  ***Inside "FROM" statement, we use "CASE" to categorize the SFA size into groups of ranges and deemed it as a temporary table. Then, we select from this table and perform the calculation.
    
    SELECT SFA_Range, COUNT(*) AS total_transactions
    FROM (
           SELECT new_SFA,
                  CASE 
                    WHEN new_SFA < 400 THEN "Less than 400 sq.ft."
                    WHEN new_SFA >= 400 AND new_SFA <= 800 THEN "400 - 800 sq.ft."
                    WHEN new_SFA >= 801 AND new_SFA <= 1200 THEN "801 - 1200 sq.ft."
                    WHEN new_SFA >= 1201 AND new_SFA <= 1500 THEN "1201 - 1500 sq.ft."
                    WHEN new_SFA >= 1501 AND new_SFA <= 2000 THEN "1501 - 2000 sq.ft."
                    WHEN new_SFA IS NULL THEN ""
                    ELSE  "More than 2000 sq.ft."
                  END AS SFA_Range
           FROM new_data) AS new2
     GROUP BY new2.SFA_Range
     ORDER BY total_transactions DESC
