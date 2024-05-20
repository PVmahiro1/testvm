import com.cloudbees.plugins.credentials.domains.*
import com.cloudbees.plugins.credentials.impl.*
import com.cloudbees.plugins.credentials.*
import jenkins.model.*
import hudson.util.Secret

import java.io.File
import groovy.xml.XmlUtil
import groovy.xml.*
import hudson.model.*

// Функція для отримання змінних середовища
def getEnvVariable(String name) {
    return System.getenv(name)
}

def newtelegramBotToken = getEnvVariable('TELEGRAM_BOT_TOKEN')
def newtelegramBotName = getEnvVariable('TELEGRAM_BOT_NAME')
def dockerUserName = getEnvVariable('DOCKERHUB_USERNAME')
def dockerPassword = getEnvVariable('DOCKERHUB_PASSWORD')

def domain = Domain.global()
def store = Jenkins.instance.getExtensionList('com.cloudbees.plugins.credentials.SystemCredentialsProvider')[0].getStore()
def creds = new UsernamePasswordCredentialsImpl(CredentialsScope.GLOBAL, "dockerhub_token", "Description", dockerUserName, dockerPassword)

store.addCredentials(domain, creds)

// Налаштування плагіну Telegram Bot
def jenkinsHome = Jenkins.instance.getRootDir()
def telegramConfigFile = ""
try{
    telegramConfigFile = new File(jenkinsHome, "jenkinsci.plugins.telegrambot.TelegramBotGlobalConfiguration.xml")
    def xml = new XmlSlurper().parse(telegramConfigFile)
    
    // Читання поточних значень
    println "Current Bot Token: ${xml.botToken}"
    println "Current Bot Name: ${xml.botName}"
    
    xml.botToken.replaceNode { botToken(newtelegramBotToken) }
    xml.botName.replaceNode { botName(newtelegramBotName) }
    
    // Збереження змін
    def writer = new StringWriter()
    XmlUtil.serialize(xml, writer)
    
    telegramConfigFile.text = writer.toString()
    
    println "Updated Bot Token: ${newtelegramBotToken}"
    println "Updated Bot Name: ${newtelegramBotName}"
    
}catch(FileNotFoundException ex) {
    println "Configuration file not found, creating a new one!"
    
    // Створення нової конфігурації
    def xmlContent = """
    <jenkinsci.plugins.telegrambot.TelegramBotGlobalConfiguration plugin="telegram-notifications@1.4.0">
        <botToken>${newtelegramBotToken}</botToken>
        <botName>${newtelegramBotName}</botName>
        <approvalType>ALL</approvalType>
    </jenkinsci.plugins.telegrambot.TelegramBotGlobalConfiguration>
    """
    println "New configuration file created with Bot Token:  and Chat ID: "
    telegramConfigFile.text = xmlContent
}
