@Library('hostel-lib') _  // Apne Jenkins mein jo library naam rakha hai wohi use karein

pipeline {
    agent any
    environment {
        MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
        EMAIL_TO            = '70155033@student.uol.edu.pk'
    }
    stages {
        stage('Setup Environment') {
            steps { 
                setupEnv() 
            }
        }

        // ---------- DEV: dev branch par push ----------
        stage('DEV Pipeline') {
            when { branch 'dev' }
            stages {
                stage('Data Ingest')   { steps { ingestData() } }
                stage('Model Train + Register (Challenger)') { steps { trainModel() } }
                stage('Model Deploy')  { steps { deployModel('Challenger', 5001) } }
                stage('Model Test')    { steps { testModel('Challenger') } }
            }
        }

        // ---------- PRE-PROD: main branch par merge ----------
        stage('PRE-PROD Pipeline') {
            when { branch 'main' }
            stages {
                stage('Data Ingest') { steps { ingestData() } }
                stage('Load Challenger, Register as Challenger-pre-test') {
                    steps { registerModel('Challenger', 'Challenger-pre-test') }
                }
                stage('Model Deploy') { steps { deployModel('Challenger-pre-test', 5002) } }
                stage('Model Test')   { steps { testModel('Challenger-pre-test') } }
                stage('Update alias to Challenger-post-test') {
                    steps { setAlias('Challenger-pre-test', 'Challenger-post-test') }
                }
            }
        }

        // ---------- PROD: release tag lagane par ----------
        stage('PROD Pipeline') {
            when { buildingTag() }
            stages {
                stage('Load Challenger-post-test, Register as Champion') {
                    steps { registerModel('Challenger-post-test', 'Champion') }
                }
                stage('Model Deploy (Champion)') { 
                    steps { deployModel('Champion', 5003) } 
                }
                stage('Model Test (Champion)') { 
                    steps { testModel('Champion') } 
                }
                stage('Promote to Champion Alias') {
                    steps { setAlias('Champion', 'Champion') }
                }
            }
        }
    }
    
    post {
        always {
            // Har build status par automatic aapko email notify karega
            notifyEmail()
        }
    }
}

