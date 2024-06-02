pipeline {
    agent any
	
    
    stages {
        stage('Start') {
            steps {
                echo 'Lab_2: nginx/custom'
            } 
        }
        
        stage('Image Build') {
            steps {
                sh "docker-compose build mqtt2prometheus mosquitto prometheus_mqtt grafana_mqtt node_exporter_mqtt" 
            } 
        }
        stage('Stop previous artifact'){
		    steps {
                sh "docker-compose down mqtt2prometheus mosquitto prometheus_mqtt grafana_mqtt node_exporter_mqtt"
            } 
		}
        stage('Deploy new artifact'){
            steps{
                sh "docker-compose up -d --build mqtt2prometheus mosquitto prometheus_mqtt grafana_mqtt node_exporter_mqtt"
            } 
        } 

        
    } 

}