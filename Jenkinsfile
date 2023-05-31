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
    
    stage ('Check secrets') {
      steps {
      sh 'trufflehog3 https://github.com/pentesty/DevSecOps_Acc.git -f json -o truffelhog_output.json || true'
      sh './truffelhog_report.sh'
      }
    }
    
    stage ('Software composition analysis') {
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
    
    stage ('Static analysis - SonarQube') {
      steps {
        withSonarQubeEnv('sonar') {
          sh 'mvn sonar:sonar'
	  //sh 'sudo python3 sonarqube.py'
	  sh './sonarqube_report.sh'
        }
      }
    }
	  
//       stage ('SAST-SemGrep') {
// 	      steps {
		      
// 		   //sh 'sudo docker run --rm -v "${PWD}:/src" returntocorp/semgrep semgrep --config=auto --output semgrep_output.json --json'
// 		   sh './semgrep_report.sh'



		      //sshagent(['semgrep-server']) {
//	        sh '''
//			ifconfig
//		'''
//			     //		ssh -o  StrictHostKeyChecking=no ubuntu@52.66.29.170 'sudo git clone https://github.com/pentesty/DevSecOps_Acc.git && sudo cd DevSecOps_Acc && sudo docker run --rm -v "${PWD}:/src" returntocorp/semgrep semgrep --config auto  --output scan_results.json --json'
// //		     }
		      
//         	}
//       	}
    
    stage ('Generate build') {
      steps {
        sh 'mvn clean install -DskipTests'
      }
    }  
	  
    stage ('Deploy to server') {
            steps {
           sshagent(['application_server']) {
                sh 'scp -o StrictHostKeyChecking=no /var/lib/jenkins/workspace/DemoProject/webgoat-server/target/webgoat-server-v8.2.0-SNAPSHOT.jar ubuntu@43.204.29.113:/WebGoat'
		sh 'ssh -o  StrictHostKeyChecking=no ubuntu@43.204.29.113 "nohup java -jar /WebGoat/webgoat-server-v8.2.0-SNAPSHOT.jar &"'
              }      
           }     
    }
   
    stage ('Dynamic analysis') {
            steps {
           sshagent(['application_server']) {
                //sh 'ssh -o  StrictHostKeyChecking=no ubuntu@13.233.123.52 "sudo docker run --rm -v /home/ubuntu:/zap/wrk/:rw -t owasp/zap2docker-stable zap-full-scan.py -t http://43.204.29.113/WebGoat -x zap_report || true" '
		sh 'ssh -o  StrictHostKeyChecking=no ubuntu@13.233.123.52 "sudo docker run --rm -v /home/ubuntu:/zap/wrk/:rw -t owasp/zap2docker-stable zap-full-scan.py -t http://43.204.29.113:8081/WebGoat -x zap_report -n defaultcontext.context || true" '
		sh 'ssh -o  StrictHostKeyChecking=no ubuntu@13.233.123.52 "sudo ./zap_report.sh"'
              }      
           }       
    }
  
//    stage ('Host vulnerability assessment') {
//        steps {
//             sh 'echo "In-Progress"'
//            }
//    }

  // stage ('Security monitoring and misconfigurations') {
  //      steps {
	 //		sh 'echo "AWS misconfiguration"'
   //          sh './securityhub.sh'
   //         }
   // }
	  
	
   stage ('Incidents report') {
        steps {
	sh 'echo "Final Report"'
         sh './final_report.sh'
        }
    }	  
	  
   }  
}
