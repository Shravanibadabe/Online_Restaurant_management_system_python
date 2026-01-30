import pandas as pd
# Sample Employee DataFrame
employee_data = {
    'EmployeeID': [101, 102, 103, 104],
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'DepartmentID': [1, 2, 1, 3]
}
df_employees = pd.DataFrame(employee_data)
# Sample Department DataFrame
department_data = {
    'DepartmentID': [1, 2, 3],
    'DepartmentName': ['HR', 'Engineering', 'Marketing']
}
df_departments = pd.DataFrame(department_data)
# Merge the DataFrames on DepartmentID
merged_df = pd.merge(df_employees, df_departments, on='DepartmentID')
# Display the merged DataFrame
print("Merged DataFrame:")
print(merged_df)