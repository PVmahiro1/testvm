pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'vulchakpavlo/prikm'
    }
    
    stages {
        stage('Start') {
            steps {
                echo 'Lab_5: start for monitoring'
            }
        }

        stage('Image build') {
            steps {
                dir("Telegrambot") {
                    sh "pwd"
                    sh 'docker-compose build'
                    sh 'docker tag $DOCKER_IMAGE:latest $DOCKER_IMAGE:$BUILD_NUMBER'
                }
            }
            post{
                failure {
                    script {
                    // Send Telegram notification on success
                        telegramSend message: "Job Name: ${env.JOB_NAME}\n Branch: ${env.GIT_BRANCH}\nBuild #${env.BUILD_NUMBER}: ${currentBuild.currentResult}\n Failure stage: '${env.STAGE_NAME}'"
                    }
                }
            }
            
        }

        stage('Push to registry') {
            steps {
                withDockerRegistry([ credentialsId: "dockerhub_token", url: "" ])
                {
                    sh "docker push $DOCKER_IMAGE:latest"
                    sh "docker push $DOCKER_IMAGE:$BUILD_NUMBER"
                }
            }
            post{
                failure {
                    script {
                    // Send Telegram notification on success
                        telegramSend message: "Job Name: ${env.JOB_NAME}\nBranch: ${env.GIT_BRANCH}\nBuild #${env.BUILD_NUMBER}: ${currentBuild.currentResult}\nFailure stage: '${env.STAGE_NAME}'"
                    }
                }
            }
        }

        stage('Deploy image'){
            steps{
                dir("Telegrambot") {
                    sh "pwd"
                    sh "docker-compose down"
                    sh "docker container prune --force"
                    sh "docker image prune --force"
                    //sh "docker rmi \$(docker images -q) || true"
                    sh "docker-compose up -d"
                }
            }
            post{
                failure {
                    script {
                    // Send Telegram notification on success
                        telegramSend message: "Job Name: ${env.JOB_NAME}\nBranch: ${env.GIT_BRANCH}\nBuild #${env.BUILD_NUMBER}: ${currentBuild.currentResult}\nFailure stage: '${env.STAGE_NAME}'"
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                // Send Telegram notification on success
                telegramSend message: "Job Name: ${env.JOB_NAME}\n Branch: ${env.GIT_BRANCH}\nBuild #${env.BUILD_NUMBER}: ${currentBuild.currentResult}"
            }
        }
    }
}