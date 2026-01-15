# devops-demo-app
git clone https://github.com/Shub0705/devops-demo-app.git
bash '''
apt install docker.io
'''
bash '''
systemctl start docker 
systemctl enable docker
systemctl status docker
sudo usermod -aG docker jenkins
sudo chmod 666 /var/run/docker.sock
sudo systemctl restart docker
sudo systemctl restart jenkins
'''
docker login -u shubhamdec0705
install Jenkins
java --version 
install java 
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install jenkins
edit inbound
TCP 8080 0.0.0.0/0
TCP 9000 0.0.0.0/0
docker run -d --name sonarqube -p 9000:9000 sonarqube:lst
docker ps
in SonarQube
click Administration
click Projects
click Management
click create project
AFTER THAT 
Administrator ----->(TOP right corner "A")
click my Acount
click Security
Generate Tokens
copy token
Goto the Jenkins---> Manage Jenkins--->Plugins (install plugins :- SonarQube Scner)
Goto the Jenkins---> Manage Jenkins----->Credentials---->System---->Global credentials----> kind:- secret text ---->past token
Goto the Jenkins ---> manage jenkins ----> system ----> SonarQube installations





pipeline {
    agent any 
    environment{
        DOCKER_NAME = "shubhamdoc0705/my-simple"
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CRED = credentials('Docker-creds')
        SONAR_HOST_URL = "http://57.182.251.103:9000/"
    }
    
    stages{
        stage('Git checkout') {
            steps{
                git branch: 'main', credentialsId: 'GIT-hub', url: 'https://github.com/Shub0705/devops-demo-app.git'
            }
        }
        stage('SonarQube Analysis'){
            steps{
                withSonarQubeEnv('sonarqube-server') {
                sh """
                    sonar-scanner \
                    -Dsonar.projectKey=devops-demo-app \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=${SONAR_HOST_URL} \
                    """
                }
            }
        }
        stage('build'){
            steps{
                sh'''
                docker build -t ${DOCKER_NAME}:${DOCKER_TAG} .
                '''
            }
        }
        stage('Push to Docker'){
            steps{
                withCredentials([usernamePassword(
            credentialsId: 'Docker-creds',
            usernameVariable: 'DOCKER_USER',
            passwordVariable: 'DOCKER_PASS'
            )]) {
                sh'''
                echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                docker push ${DOCKER_NAME}:${DOCKER_TAG}
                '''
              }
            }
        }
    }
    post{
        success {
            echo "shubham pipeline done"
        }
        failure {
            echo "lawade lagale"
        }
    }
}
