from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd

# Start Selenium
# mac #driver = webdriver.Chrome("/Users/brett.olmstead/Downloads/chromedriver 2")
driver = webdriver.Chrome("C:\\Users\\Brett\\Downloads\\chromedriver.exe")

# Go to the Tupperware page and login
driver.get("https://my.tupperware.ca/")

username = driver.find_element_by_name("user[login]")
username.clear()
username.send_keys("93000499897")
password = driver.find_element_by_name("user[password]")
password.clear()
password.send_keys("Easton1")
password.send_keys(Keys.RETURN)

# Navigate to the item search
driver.get(
    "https://my.tupperware.ca/pyr_core/seamless/default?path=https%3A%2F%2Forder.tupperware.ca%2Fsf%2Fapp%2F%21nsf_session_ctl.p_link%3Fpv_source%3DMYTUP%26pv_url%3Dtup_btp%24personal_sales_recruit.p_show_current")
driver.find_element_by_id("s4").click()
driver.find_element_by_id("ax_64").click()
driver.switch_to.window(driver.window_handles[-1])

# Search for Regular items, value 01
driver.find_element_by_xpath("//input[@value='01']").click()
driver.find_element_by_xpath("//input[contains(@onclick,'return check_selection()')]").click()

# Get the regular items as a table df
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find_all('table')[1].tbody
table = str(table).replace("value=", "/><div>")  # Fixes an issue with the item column showing up as nan
table = table.replace("/></td>", "</div></td>")  # Fixes an issue with the item column showing up as nan
df = pd.read_html(str(table), flavor="bs4")  # Get the table as Pandas
df = df[1]
df.columns = ["Item Number", "Description", "Item Type", "Retail Price", "Cost Price"]

# Back to search. Search for Specials, value 08
driver.find_element_by_xpath("//input[contains(@value,'Retry Search')]").click()
driver.find_element_by_xpath("//input[@value='08']").click()
driver.find_element_by_xpath("//input[contains(@onclick,'return check_selection()')]").click()

# Get the sales specials items as a table df2
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find_all('table')[1].tbody
table = str(table).replace("value=", "/><div>")  # Fixes an issue with the item column showing up as nan
table = table.replace("/></td>", "</div></td>")  # Fixes an issue with the item column showing up as nan
df2 = pd.read_html(str(table), flavor="bs4")  # Get the table as Pandas
df2 = df2[1]
df2.columns = ["Item Number", "Description", "Item Type", "Retail Price", "Cost Price"]

# Back to search. Search for PWP, value 88
driver.find_element_by_xpath("//input[contains(@value,'Retry Search')]").click()
driver.find_element_by_xpath("//input[@value='88']").click()
driver.find_element_by_xpath("//input[contains(@onclick,'return check_selection()')]").click()

# Get the PWP items as a table df3
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find_all('table')[1].tbody
table = str(table).replace("value=", "/><div>")  # Fixes an issue with the item column showing up as nan
table = table.replace("/></td>", "</div></td>")  # Fixes an issue with the item column showing up as nan
df3 = pd.read_html(str(table), flavor="bs4")  # Get the table as Pandas
df3 = df3[1]
df3.columns = ["Item Number", "Description", "Item Type", "Retail Price", "Cost Price"]

# Back to search. Search for Samples, value 05
driver.find_element_by_xpath("//input[contains(@value,'Retry Search')]").click()
driver.find_element_by_xpath("//input[@value='05']").click()
driver.find_element_by_xpath("//input[contains(@onclick,'return check_selection()')]").click()

# Get the Sample items as a table df4
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find_all('table')[1].tbody
table = str(table).replace("value=", "/><div>")  # Fixes an issue with the item column showing up as nan
table = table.replace("/></td>", "</div></td>")  # Fixes an issue with the item column showing up as nan
df4 = pd.read_html(str(table), flavor="bs4")  # Get the table as Pandas
df4 = df4[1]
df4.columns = ["Item Number", "Description", "Item Type", "Retail Price", "Cost Price"]

# Back to search. Search for Exclusive Host Gofts, value 04
driver.find_element_by_xpath("//input[contains(@value,'Retry Search')]").click()
driver.find_element_by_xpath("//input[@value='04']").click()
driver.find_element_by_xpath("//input[contains(@onclick,'return check_selection()')]").click()

# Get the Sample items as a table df5
soup = BeautifulSoup(driver.page_source, 'html.parser')
table = soup.find_all('table')[1].tbody
table = str(table).replace("value=", "/><div>")  # Fixes an issue with the item column showing up as nan
table = table.replace("/></td>", "</div></td>")  # Fixes an issue with the item column showing up as nan
df5 = pd.read_html(str(table), flavor="bs4")  # Get the table as Pandas
df5 = df5[1]
df5.columns = ["Item Number", "Description", "Item Type", "Retail Price", "Cost Price"]

driver.close()

# Put all the items together
df = pd.concat([df, df2, df3, df4, df5])
df.reset_index(inplace=True, drop=True)
df.dropna(axis="index", inplace=True)
df = df[["Description", "Item Number", "Item Type", "Retail Price", "Cost Price"]]
df["Item Number"] = df["Item Number"].str.replace('"', '')
df.sort_values(by="Description", inplace=True)

# Write the catalog of items to a file
df.to_csv("/Users/brett.olmstead/Downloads/partyTracker/catalog.csv", index=False)

# upload the file to s3 bucket
import boto3

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)

data = open('/Users/brett.olmstead/Downloads/partyTracker/catalog.csv', 'rb')
s3.Bucket('partytracker').put_object(Key='catalog.csv', Body=data)
object_acl = s3.ObjectAcl('partytracker', 'catalog.csv')
response = object_acl.put(ACL='public-read')
