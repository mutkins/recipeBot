pipeline {
    agent any
    environment {
       tgBot_id = credentials('recipe_bot_id')
       postgres_pass = credentials('recipe_bot_postgres_pass')
       CHAT_ID = credentials('my_chat_id')
    }

    stages {
       stage('get dependencies'){
            steps {
                sh 'sudo python3 -m venv ./venv'
                sh '. venv/bin/activate'
                sh 'sudo apt install -y libpq-dev'
                sh 'pip install -r requirements.txt'
                   }
        }
       stage('runBot'){
            steps {
                sh 'python3 main.py'
                   }
        }
    }
        post {
    failure {
    sh  ("""
        curl -s -X POST https://api.telegram.org/bot${tgBot_id}/sendMessage -d chat_id=${CHAT_ID} -d parse_mode=markdown -d text="*${env.JOB_NAME}* FAILED ${env.BUILD_URL}"
    """)
    }
    aborted {
    sh  ("""
        curl -s -X POST https://api.telegram.org/bot${tgBot_id}/sendMessage -d chat_id=${CHAT_ID} -d parse_mode=markdown -d text="*${env.JOB_NAME}* ABORTED ${env.BUILD_URL}"
    """)
    }

        }

    }
