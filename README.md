# nordcloud-tech-assignment

## Requirements 

## Run locally 


1. Install docker.
2. Clone the repository.
3. Run `docker build -t api -f Dockerfile_api .` in the root directory
to build the container, then run it with `docker run -p 8000:5001 api`.
4. The API should become available at `http://localhost:8000`. 
5. Send a HTTP GET request to check the optimal station for query parameters `x`, `y` and `solution`. The final parameter defaults to `numpy` and can also be set to `simple`. For example `http://localhost:5001?x=2.0&y=5.0&solution=simple`. 
6. The response should be plaintext with status code `200`, for example `Best network station for point x,y is x,y with speed z` or `No network station within reach for point x,y`. If something goes wrong it may also return an error with status code `400` (Bad request) or `500` (Internal server error).

## Run tests 
1. Ensure that the app is running locally.
2. Run `docker build -t test -f Dockerfile_test .` in the root directory
to build the container, then run the tests with `docker run --network="host" test`.


## Deployment

1. Install Azure CLI

2. Create an image registry in Azure. Only do this once.

`az group create --name ncassignment --location westeurope`
`az acr create --name ncassignmentregistry --resource-group ncassignment --sku Basic --admin-enabled true`
`az acr credential show --resource-group ncassignment --name ncassignmentregistry`

The last command should show you credentials for the registry, needed in the next step.

3. Push the docker image to the registry. Remember to build the Docker image first.

`docker login ncassignmentregistry.azurecr.io --username ncassignmentregistry`
`docker tag api ncassignmentregistry.azurecr.io/api:latest`
`docker push ncassignmentregistry.azurecr.io/api:latest`

4. Create the App Service 

`az appservice plan create --name ncassignmentplan --resource-group ncassignment --sku S1 --is-linux`
`az webapp create --resource-group ncassignment --plan ncassignmentplan --name ncassignmentapp --deployment-container-image-name ncassignmentregistry.azurecr.io/api:latest`
`az webapp config appsettings set --resource-group ncassignment --name ncassignmentapp --settings WEBSITES_PORT=8000`

5. Get your principal id and subscription id 

`az webapp identity assign --resource-group ncassignment --name ncassignmentapp --query principalId --output tsv`
az account show --query id --output tsv

6. Run this command with the id's from previous step

az role assignment create --assignee <principal-id> --scope /subscriptions/<subscription-id>/resourceGroups/ncassignment/providers/Microsoft.ContainerRegistry/registries/ncassignmentregistry --role "AcrPull"

az resource update --ids /subscriptions/<subscription-id>/resourceGroups/ncassignment/providers/Microsoft.Web/sites/ncassignmentapp/config/web --set properties.acrUseManagedIdentityCreds=True

az webapp config container set --name ncassignmentapp --resource-group ncassignment --docker-custom-image-name ncassignmentregistry.azurecr.io/api:latest --docker-registry-server-url https://ncassignmentregistry.azurecr.io

## Limitations

The solution in `src/solutions/simple.py` can handle a dataset of any size, however the execution time scales linearly in terms of data points which quickly becomes unfeasible to use in a production environment.

The alternative in `src/solutions/numpy.py` takes advantage of optimized matrix operations to arrive at the solution much faster. This can serve as a good basis for a highly available system if the entire dataset can be held in memory. 

If the dataset is larger than available memory, both options are **not viable** for a highly available system. In this case my approach would be to use a database that supports **spatial indexing** (An example of this is PostGIS).  In theory this would allow a logarithmic lookup time for stations that can reach the given point while storing the data on disk. I deemed this to be overly involved for this exercise.

In addition to the points above, the solution needs **data backups** to ensure reliability in a production setting. This can be solved by moving to Azure File Storage or a database with automated backups. In addition, I would add detailed **logging** to ensure that errors can be monitored. Finally, the production app may not **scale** very well to handle spikes in traffic unless the Azure App Service is configured appropriately.
