# kubernetes-test
Kubernetes-test repo provide a python script that uses pygithub lib to list all kubernetes org repo, sorted by number of stars, and inserted into postgresql database deployed on kubernetes using helm chart.

prerequisites:
1) kubectl installed.
2) helm installed on your machine.
3) Kubernetes cluster(either minikuber or any cloud provider/on-premises kubernetes cluster).
4) github user , you will need to generate access token, you can use github docs to see how to generate token.
      https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token


installation:
1)helm repo add github-repo https://awadmhamad.github.io/github-repo
2)helm repo update
3)helm install github-app github-repo/github-chart --set accessToken="$your_generated_token"

helm values.yaml:
1) you will have to provide access token to override the empty accessToken in values.yaml files in github-chart helm chart as shown in step 3 above(installation).
2) in values.yaml file there's a default values of postgres db that is installed by the helm chart:
  postgres:
    database: "postgresdb"
    user: "postgresadmin"
    password: "admin123"
    host: "postgres"
    port: "5432"
  you can change these values by overriding these values using --set option with the helm installation.

validation:
1) kubectl get pods will show you two new generated pods, one starts with github-job-XXXX and the other one starts with postgres-XXX
2) use 'kubectl logs -f github-job-XXXX' to see the logs of calculating the repos and the list of repos sorted in console.
3) use 'kubectl exec -it postgres-XXX bash' to connect to postgresql pod.
4) run 'psql -h localhost -U postgresadmin postgresdb' to connect to the database
5) run '\dt' to validate githu table exists.
6) run 'SELECT * FROM github;' to see the table of repos names, stars, and primary programming language.



