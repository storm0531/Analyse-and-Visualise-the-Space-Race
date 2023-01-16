import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv("Space_Corrected.csv")

print(data.shape)
print(data.tail())

print(data.isna().values.any())
print(data.duplicated().values.any())

clean_data = data
clean_data.shape

clean_data.drop(columns=['Unnamed: 0', 'Unnamed: 0.1'],axis=1,inplace=True)
clean_data.head()

clean_data.info()

clean_data['Rocket_cost'] = clean_data[' Rocket'].str.replace(',','')
clean_data.drop(columns=" Rocket",inplace=True)

clean_data['Rocket_cost'] = pd.to_numeric(clean_data['Rocket_cost'])
clean_data.rename(columns = {'Status Rocket': 'Status_Rocket', 'Status Mission': 'Status_Mission', 'Company Name': 'Company_Name'}, inplace = True)

clean_data.info()

clean_data.sample()

clean_data["year"] = clean_data['Datum'].astype(str).str.split(",",1,expand=True)[1].str.split(" ",expand=True)[1]
clean_data["year"] = pd.DatetimeIndex(clean_data["year"]).year
clean_data.sample()

clean_data.shape

clean_data.fillna(0,inplace=True)

clean_data.sample()

clean_data["Status_Mission"].value_counts()

clean_data["Company_Name"].nunique()

clean_data.Status_Rocket.value_counts()

#rate of success over the years
sns.jointplot(data=clean_data, x = "year", y="Status_Mission")

plt.show()

#comparing cost of rocket in decades
sns.scatterplot(data=clean_data,x='year',y='Rocket_cost')

plt.show()

#TOP 10 COUNTRIES
clean_data.Company_Name.value_counts().head(10)

successes_count = clean_data[ clean_data["Status_Mission"] == "Success" ].groupby("year").count()["Status_Mission"]

bar = px.bar(x=successes_count.index,y=successes_count.values)
bar.show()

top_companies = clean_data[clean_data["Status_Mission"] == "Success"].groupby("Company_Name").count()["Status_Mission"]
top_companies = top_companies.sort_values(ascending=False)
top_companies.head()

plt.figure(figsize=(20,15))
plt.title("Top 10 company base on rocket lunched number",fontsize=30)
plt.xticks(fontsize=20,rotation=45)
plt.yticks(fontsize=15)

sns.barplot(x=top_companies[:10].index,y=top_companies[:10].values)
plt.ylabel("number of rocket lunches",fontsize=25)
plt.xlabel("company name",fontsize=25)

plt.show()

failure_count = clean_data.query('Status_Mission != "Success"')["Status_Mission"].value_counts()

bar_x = px.bar(x=failure_count.index,
               y=failure_count.values,
               color=failure_count.values,
               title="failure Count from begaining")

bar_x.update_layout(xaxis_title="COUNT",
                    yaxis_title="Type",
                    coloraxis_showscale=False,
                  )
bar_x.show()

plt.figure(figsize=(20,15))
plt.title("cost of making rocket in one year",fontsize=30)
plt.xticks(fontsize=10,rotation=45)
plt.yticks(fontsize=15)

sns.barplot(data=clean_data,x='year',y='Rocket_cost')
plt.ylabel("rocket cost m(million)",fontsize=25)
plt.xlabel("year",fontsize=25)

plt.show()

clean_data.head(2)

active_status = clean_data[clean_data["Status_Rocket"] == "StatusActive" ].groupby("Company_Name").count()["year"]
active_status = active_status.sort_values(ascending=False)

plt.figure(figsize=(20,15))
plt.title("companies with active rockets over the year",fontsize=30)
plt.xticks(fontsize=15,rotation=45)
plt.yticks(fontsize=15)

sns.barplot(x=active_status.index,y=active_status.values)
plt.ylabel("rocket number",fontsize=25)
plt.xlabel("company name",fontsize=25)

plt.show()

clean_data.describe()
