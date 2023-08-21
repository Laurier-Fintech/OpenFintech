from AlphavantageLFT import Alphavantage

myclient = pymongo.MongoClient()
mydb = myclient["openfintech"]
mycol = mydb["price"]

sample_data = {
    "2023-06-02": {
            "1. open": "129.5600",
            "2. high": "133.1200",
            "3. low": "127.4600",
            "4. close": "132.4200",
            "5. volume": "24339245"
        },
    "2023-05-26": {
        "1. open": "127.5000",
        "2. high": "129.6600",
        "3. low": "125.0100",
        "4. close": "128.8900",
        "5. volume": "21029979"
    }
}


data = []
for key in sample_data: 
    sample_data[key].update({"0. date": key})
    data.append(sample_data[key])
print(data)
mycol.insert_many(data)

