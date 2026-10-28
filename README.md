# BrightSmile Dental Clinic: Docker + Jenkins on AWS EC2

Flask + MySQL dental website: home page, services, online appointment booking, appointments list.

## Run locally (quick test)
    docker compose -f docker-compose-jenkins.yml up -d
    open http://localhost:8081

## Part I: Docker Hub + EC2
    docker login
    docker build -t YOUR_DOCKERHUB_USER/dental-clinic:1.0 .
    docker push YOUR_DOCKERHUB_USER/dental-clinic:1.0
On EC2 (Docker installed): copy docker-compose.yml, edit the image name, then:
    docker compose up -d      # site on http://<EC2_IP>
Persistence proof: `docker compose down && docker compose up -d` and your appointments remain.

## Part II: Jenkins
1. Push this folder to GitHub, edit the repo URL in `Jenkinsfile`.
2. Install Jenkins on EC2, add the jenkins user to the docker group, restart Jenkins.
3. Plugins: Git, Pipeline, Docker Pipeline.
4. New Item -> Pipeline -> "Pipeline script from SCM" -> your repo, script path `Jenkinsfile`.
5. Build Now. Site on http://<EC2_IP>:8081

Security group ports: 22, 80, 8080 (Jenkins), 8081.
