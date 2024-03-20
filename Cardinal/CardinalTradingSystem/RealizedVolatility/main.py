from polygon import RESTClient
import pickle
# uAZtAwym4JxD3U9wTJfvlW3fx12XScLM
client = RESTClient(api_key="gjwnimbmBf2p465awj1DI3ln4JkeJ6Re")

ticker = "META"

aggs = []
for a in client.list_aggs(ticker=ticker, multiplier=5, timespan="minute", from_="2022-10-01", to="2023-10-01", limit=50000):
    aggs.append(a)
    
print(len(aggs))

with open(f"{ticker}", "wb") as fp:   #Pickling
    pickle.dump(aggs, fp)

print("Done!")