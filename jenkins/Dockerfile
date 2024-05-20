FROM jenkins/jenkins

ENV JENKINS_USER admin
ENV JENKINS_PASS admin

USER jenkins

# Skip initial setup
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
COPY plugins.txt /usr/share/jenkins/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/plugins.txt
COPY config.xml /usr/share/jenkins/ref/jobs/hello_world/config.xml

# Create credentials
COPY --chown=jenkins:jenkins credentials.groovy /usr/share/jenkins/ref/init.groovy.d/credentials.groovy
#COPY .env /usr/share/jenkins/ref/init.groovy.d/.env

USER root

RUN apt-get update \
    && apt-get install -qqy apt-transport-https ca-certificates curl gnupg2 software-properties-common
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"

RUN apt-get update -qq \
    && apt-get install docker-ce -y \
    && apt-get clean

RUN usermod -aG docker jenkins

RUN curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose

USER jenkins