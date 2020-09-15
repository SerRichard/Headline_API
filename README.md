# **Sky news headline API**

An automated read only API, connects with a Stateful Cassandra Ring.

## Installation and preparation: Linux users

Prepare your working environment
```
sudo pacman -Syu python3-pip
sudo pacman -Syu minikube
sudo pacman -Syu kubectl
sudo mkdir newsApi
cd newsApi
```

Grab the relevant files!
```
sudo wget -O requirements.txt https://raw.githubusercontent.com/SerRichard/Headline_API/Version-2/requirements.txt
sudo wget -O temp.csv https://raw.githubusercontent.com/SerRichard/Headline_API/Version-2/temp.csv
sudo wget -O scraped_articles.csv https://raw.githubusercontent.com/SerRichard/Headline_API/Version-2/scraped_articles.csv
sudo wget -O modified_articles.csv https://raw.githubusercontent.com/SerRichard/Headline_API/Version-2/modified_articles.csv
sudo wget -O sky_api.py https://raw.githubusercontent.com/SerRichard/Headline_API/Version-2/sky_api.py
sudo wget -O sky_scraping.py https://raw.githubusercontent.com/SerRichard/Headline_API/Version-2/sky_scraping.py
sudo wget -O cassandra-nodeport.yaml https://raw.githubusercontent.com/SerRichard/Headline_API/Version-2/cassandra-nodeport.yaml
sudo wget -O cassandra-service.yaml https://raw.githubusercontent.com/SerRichard/Headline_API/Version-2/cassandra-service.yaml
sudo wget -O cassandra-statefulset.yaml https://raw.githubusercontent.com/SerRichard/Headline_API/Version-2/casandra-statefulset.yaml
```

Install Requirements
```
pip3 install -r requirements.txt
```

Set up your minikube environment
```
minikube start --memory 5120 --cpus=4
```

Set up the kubectl
```
kubectl apply -f ./cassandra/cassandra-nodeport.yaml
kubectl apply -f ./cassandra/cassandra-service.yaml
kubectl apply -f ./cassandra/cassandra-statefulset.yaml
```

Check the pods, wait till they are running.
```
kubectl get pods -l='app=cassandra' 
```

Copy our starting articles into cassandra node & exec cqlsh:
```
kubectl cp modified_articles.csv default/cassandra-0:/home/modified_articles.csv
kubectl exec -it cassandra-0 -- cqlsh
```

Once in the CQL temrinal
```
CREATE NAMESPACE news;
CREATE TABLE news.daily (uid uuid, title text, date text, trending text, brexit int, covid int, PRIMARY KEY(uid, date)) WITH CLUSTERING ORDER BY (date ASC);
COPY news.daily (uid, title, date, trending, brexit, covid) FROM '/home/modified_articles.csv' WITH DELIMITER=',' AND HEADER=TRUE;
QUIT
```

Check the IP address of your cluster
```
kubectl get nodes -o wide
```

The resulting IP needs to be set in the sky_api.py
```
cluster = Cluster(contact_points=['RESULTING IP HERE'],port=30036)
```

Now you can run the API!
```
sudo python3 sky_api.py
```

## Interact with API

/
```
curl -i 0.0.0.0:80/                                           
```
Returns welcome statement

/articles
```
curl -i 0.0.0.0:80/articles                                              
```
Returns all current articles held in the API

/today
```
curl -i 0.0.0.0:80/today                                             
```
Returns all articles with todays date

/brexit
```
curl -i 0.0.0.0:80/brexit
```
Returns all articles relevant to brexit

/covid
```
curl -i 0.0.0.0:80/covid
```
Returns all articles relevant to covid

## Future Updates

Intended updates to this API will be the addition of the links to each articles.
