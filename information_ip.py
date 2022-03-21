# import library
import requests
import pandas
# end import library

# function getting information of the ip
def ip_information(ip):
    while True:
        try:
            API = f"http://ip-api.com/json/{ip}"
            request = requests.get(API)
            data = request.json()
    
            return (data["country"], data["city"], data["lat"], data["lon"])
        except:
            pass
# end function getting information of the ip

# set data frame
df = pandas.DataFrame(pandas.read_csv("database/visitor_original.tsv", sep = "\t"))
# end data frame

# set variables
country = []
city = []
lat = []
lon = []
browser = []
date = []
n = 0   # variable for number of IPs
nb = 0  # variable for number browser
# end set

# loop for working with IPs
print("receiving information ip")

for ip in df["IP"]:

    # set informations ip to ip data
    ip_data = ip_information(ip)
    # end set

    # append informations to variables 
    try:
        country.append(ip_data[0])
    except:
        country.append("EROR IP")
    try:
        city.append(ip_data[1])
    except:
        city.append("EROR IP")
    try:
        lat.append(f"{ip_data[2]}")
    except:
        lat.append("EROR IP")
    try:
        lon.append(f"{ip_data[3]}")
    except:
        lat.append("EROR IP")
    # end append

    # print number and IP
    n += 1
    print(n, ip)
    # end print

print("full")
# end loop

# loop for set browsers to variable
print("set browsers to variable")

for device in df["LOGIN DEVICE"]:
    browser.append(str(device).split()[-1])

    # print number adn device
    nb += 1
    print(nb, str(device).split()[-1])
    # end print

print("end set")
# end loop

# set date to variable
print("set date to variable")

for dt in df["DATE TIME LOGIN"]:
    date.append(dt.split(" ")[0])

print("end set")
# set informations to data frame
print("set informations to data frame")

df["COUNTRY"] = country
df["CITY"] = city
df["LAT"] = lat
df["LON"] = lon
df["BROWSER"] = browser
df["DATE"] = date

print("end set")
# end set

# data frame to csv
print("data frame to csv")

df.to_csv("database/visitor.tsv", sep = "\t")

print("full")
# end data frame to csv

# show data frame
print("show data frame")
print(df)