pipeline {
    agent { label 'master' }

    stages {

        stage('unit-tests') {

            agent { label 'master' }

            steps {
                sh '''
                    if [ ! -d "../venv" ]
                    then
                      virtualenv -p python3 ../venv
                    fi
                '''
                sh '''
                    PATH="$WORKSPACE/../venv/bin":/usr/local/bin:$PATH
                    . "$WORKSPACE/../venv/bin/activate"
                    cd python_package
                    pip install .
                    python -m unittest discover
                '''
            }
        }

        stage('kitchen-tests') {
            agent { label 'dice_worker' }

            steps {
                sh 'bash run-kitchen-tests.sh'
            }
        }
    }
}