pipeline {
    agent any
    environment {
       tgBot_id = credentials('recipe_bot_id')
       postgres_pass = credentials('recipe_bot_postgres_pass')
    }

    stages {
       stage('get dependencies'){
            steps {
                sh 'sudo python3 -m venv ./venv'
                sh '. venv/bin/activate'
                sh 'sudo apt get install libpq-dev'
                sh 'pip install -r requirements.txt'
                   }
        }
       stage('runBot'){
            steps {
                sh 'python3 main.py'
                   }
        }
    }
    }