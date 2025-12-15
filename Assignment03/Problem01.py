import pandas as pd
import pandasql as ps

filepath ="emp_hdr.csv"
df = pd. read_csv(filepath)
print("Dataframe Columns Types: ")
print(df.dtypes)
print("\nEmp Data:")
print(df)

query="SELECT job ,SUM(sal) total FROM data GROUP BY job"
result=ps.sqldf(query,{"data":df})
print("\nQuery Result for total salary for job :")
print(result)


query="SELECT * FROM data where sal<=5000"
result=ps.sqldf(query,{"data":df})
print("\nQuery Result for sal less than 5000:")
print(result)

query="SELECT empno, job, sal, deptno FROM data where job='SALESMAN'"
result=ps.sqldf(query,{"data":df})
print("\nQuery Result:")
print(result)
