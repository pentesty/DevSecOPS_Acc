pipeline {
  agent any 
  tools {
    maven 'Maven'
  }
  stages {
    stage ('Initialize') {
      steps {
        sh '''
                echo "PATH = ${PATH}"
                echo "M2_HOME = ${M2_HOME}"
            ''' 
      }
     }
    
    stage ('Secrets Scanner') {
      steps {
          sh 'trufflehog3 https://github.com/pentesty/DevSecOps_Acc.git -f json -o truffelhog_output.json || true'
          sh './truffelhog_report.sh'
      }
    }
    
    stage ('Software Composition Analysis') {
            steps {
                dependencyCheck additionalArguments: ''' 
                    -o "./" 
                    -s "./"
                    -f "ALL" 
                    --prettyPrint''', odcInstallation: 'OWASP-DC'

                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
		        sh './dependency_check_report.sh'
            }
        }
    
    stage ('Static Code Analysis') {
      steps {
        withSonarQubeEnv('sonar') {
            sh 'mvn sonar:sonar'
	        sh './sonarqube_report.sh'
        }
      }
    }
    
    stage ('Generate build') {
      steps {
        sh 'mvn clean install -DskipTests'
      }
    }  
	  
    stage ('Deploy to server') {
            steps {
           sshagent(['application_server']) {
                sh 'scp -o StrictHostKeyChecking=no /var/lib/jenkins/workspace/DemoProject/webgoat-server/target/webgoat-server-v8.2.0-SNAPSHOT.jar ubuntu@3.110.132.150:/WebGoat'
		        sh 'ssh -o  StrictHostKeyChecking=no ubuntu@3.110.132.150 "sudo nohup java -Dfile.encoding=UTF-8 -Dserver.port=8080 -Dserver.address=0.0.0.0 -Dhsqldb.port=9001 -jar webgoat-server-v8.2.0-SNAPSHOT.jar &"'
              }      
           }     
    }
   
    stage ('Dynamic Code Analysis') {
            steps {
           sshagent(['application_server']) {

                sh 'ssh -o  StrictHostKeyChecking=no ubuntu@65.0.92.62 "sudo docker run --rm -v /home/ubuntu:/zap/wrk/:rw -t owasp/zap2docker-stable zap-full-scan.py -t http://3.110.132.150:8080/WebGoat -x zap_report -n defaultcontext.context || true" '
                sh 'ssh -o  StrictHostKeyChecking=no ubuntu@65.0.92.62 "sudo ./zap_report.sh"'
              }      
           }       
    }
  
   stage ('Host Vulnerability Assessment') {
       steps {
                sh 'echo "CIS Host vulnerability assessment"'
                sh 'cd src && ansible-playbook -i modules/cis_audit/environment/hosts modules/cis_audit/run_cis_tool.yml --verbose'
                sh 'cd src/modules/devsecops_tool_parser/ && python3 run_parser.py -t "CIS-Audit" -p "../cis_audit/CIS_Audit/CIS_10.0.0.82_Ubuntu18_cis_audit.json" -o "consolidated_test_output.csv"'
           }
   }

  stage ('Cloud Security') {
       steps {
                sh 'echo "AWS misconfiguration"'
                sh 'docker run --cpus="1.5" --memory="1.5g" --memory-swap="2.5g" -v `pwd`/aws:/root/.aws -v `pwd`/reports:/app/reports securityftw/cs-suite -env aws'
                sh 'cd src/modules/devsecops_tool_parser/ && python3 run_parser.py -t "awscisaudit" -p "../../../reports/AWS/aws_audit/390618173518/20231123-120259/final_report/final_json" -o "consolidated_test_output.csv"'
           }
   }
	  
	
   stage ('Incidents report') {
        steps {
	        sh 'echo "Consolidated Final Report"'
	        sh 'cd src/modules/devsecops_tool_parser/ && python3 run_parser.py -t "Trufflehog3 Scan" -p "../../../truffelhog_output.json" -o "consolidated_test_output.csv"'
	        sh 'cd src/modules/devsecops_tool_parser/ && python3 run_parser.py -t "DependencyCheck Scan" -p "../../../dependency-check-report.xml" -o "consolidated_test_output.csv"'
	        sh 'cd src/modules/devsecops_tool_parser/ && python3 run_parser.py -t "ZAP Scan" -p "../../../zap_report" -o "consolidated_test_output.csv"'
	        sh ''
            sh './final_report.sh'
        }
    }	  
	  
   }  
}
