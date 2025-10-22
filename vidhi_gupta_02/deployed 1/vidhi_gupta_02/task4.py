import pandas as pd
import numpy as np

print("Task 4.1")
num = pd.Series(np.random.randint(1, 100, size=10))

print("Series:\n",num)
print("Starting 5 elements:\n",num.head())
print("Last 5 elements:\n",num.tail())
print(num.describe())
print("Series into List: ",num.to_list())

print("Task 4.2")

info = {
    "Name": ['Adi','Bobby','Candy','Dior','Ena'],
    "Age": [20,21,19,22,20],
    "Marks":[85,90,75,95,88]
}
df = pd.DataFrame(info)
print(df)
print("First 3 rows:\n", df.head(3))
print("Name column:\n",df['Name'])
print("Row for marks > 85:\n", df[df['Marks']>85])
df['Grade'] = ['B','A','C','A','B']
print("New Dataframe:\n", df)
df.drop(columns =['Age'], inplace=True)
print("Dataset after removing age:\n",df)

print("Task 4.3")

student = {
    'Name':['Mohan','Subh','Kirti','Shivam','Arpit','Alok','Megha','Lalita','Shiv','Radhika'],
    'Maths': np.random.randint(50, 100, size=10),
    'Science': np.random.randint(50, 100, size=10),
    'English': np.random.randint(50, 100, size=10)
}
imp = pd.DataFrame(student)
print(imp)
print("Average for Maths: ",imp["Maths"].mean())
print("Average for Science: ",imp["Science"].mean())
print("Average for English: ",imp["English"].mean())
imp["Total"] = imp.iloc[:, 1:].sum(axis=1)
print(imp)
print("Top student: ",imp.loc[imp["Total"].idxmax(), "Name"])
imp['Result'] = (imp["Total"] >= 150).map({True: "Pass", False: "Fail"})
sort = imp.sort_values(by="Total",ascending=False)
print(sort)