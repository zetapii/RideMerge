## Architecture Decision Record 003

### Title 
Decision regarding the Database Selection for Microservices

### Created By 
Aman Raj  

### Date 
27th March 2024

### Decision Makers 
Team 19


### Status: <span style="color:green">ACCEPTED</span>


### Chosen: MongoDB for subscription microservices, SQL Based Database for other microservices

### Reason:
In subscription microservice, there are more READs than WRITEs so MongoDB was chosen as it was very efficient for reads. 

In other services, there is equal proportion of READs and WRITEs, if not more WRITEs than READs so we have SQL databases for other microservices. 

### Options
- MongoDB
- SQL Based database 
