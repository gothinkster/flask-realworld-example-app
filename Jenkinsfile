cat <<-'JENKINSFILE' > Jenkinsfile
pipeline {
    agent{
        docker {
            image 'python: 3.7.2'
        }
    stages{
        stage('build'){
            steps{
                sh 'python --version'
                sh 'pip install -r requirements/dev.txt'
            }
        }
        stage('test'){
            steps {
                sh flask test
            }
        }
        stage('Git merge'){
            steps {
                git checkout master
                git merge dev
                git checkout dev

            }
    }
    }
}
