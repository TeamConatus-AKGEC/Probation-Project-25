import pandas as pd
import numpy as np
#Task1
pq=np.random.randint(1,101,10)
ser=pd.Series(pq)
print(ser)
print(ser.head())
print(ser.tail())
print(ser.max())
print(ser.min())
print(ser.mean())


#Task2
student={
    "Name":['Adi','Bobby','Candy','Dior','Ena'],"Age":[20,21,19,22,20],"Marks":[85,90,75,95,88]
}
e=pd.DataFrame(student)
print(e.to_string(index=False))
print(e['Name'])
d=e.query("Marks>85")
print(d)
e["Grade"]=["A","A","B","A","B"]
print(e.to_string(index=False))
e.drop("Age",axis=1,inplace=True)
print(e)

#Task3
a=np.random.randint(50,101,10)
b=np.random.randint(50,101,10)
c=np.random.randint(50,101,10)
Student2={
    "Name":['Adi','Bobby','Candy','Dior','Ena','Aki','Ali','Ritu','Sakshi','Tani'],"Maths":a, 'Science':b , "English":c

}
l=pd.DataFrame(Student2)
print(l.to_string(index=False))

w=l["Maths"].mean()
z=l["Science"].mean()
x=l["English"].mean()
print(f"Maths:{w},Science:{z},English:{x}")
q=l.sum(axis=1,numeric_only=True)
l['Total']=q
print(l)
s=l['Total'].max()
print(s)
qw=l.query("Total==@s")['Name']
print(qw)
l['Result'] = l['Total'].apply(lambda x: 'pass' if x >= 150 else 'fail')
print(l)
l=l.sort_values("Total",ascending=False)
print(l)