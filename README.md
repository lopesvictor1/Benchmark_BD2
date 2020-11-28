# Benchmark_BD2
## Requirements
### InfluxDB
- Install Python 3.7: "sudo apt install python3.7"
- Install library InfluxDBClient: "sudo python3.7 -m pip install influxdb"
- Install InfluxDB latest version:
    "sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -"  
    "sudo echo "deb https://repos.influxdata.com/ubuntu bionic stable" | sudo tee /etc/apt/sources.list.d/influxdb.list"  
    "sudo apt-get update"  
    "sudo apt-get install influxdb"  
    "sudo service influxdb start"  
    "influx"  

###PostgreSQL
- Install Python 3.7: "sudo apt install python3.7"  
- Install PostgreSQL 11:  
    "wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -"  
    "sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'"  
    "sudo apt-get update"  
    "sudo apt-get install postgresql-11"  
- Install Psycopg2: "sudo python3.7 -m pip install psycopg2-binary"  
- Set up PostgreSQL:
	"sudo su -l postgres"
	"psql"
	"\password postgres"
	"123"
	"CREATE DATABASE stock;"
	"exit"
	"exit"


##Usage
- Go to Benchmark_BD2 folder
- Turn "orquestrador.sh" executable: "chmod +x orquestrador.sh"
- Execute "orquestrador.sh": "./orquestrador.sh"
- Note that this execution could take from 2 to 4 hours.
	
