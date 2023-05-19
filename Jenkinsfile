import java.text.SimpleDateFormat
pipeline {
  agent any 
  parameters {
    string defaultValue: '', description: '', name: 'INPUT_LOCATION', trim: true
    }
  tools {
    maven 'Maven'
  }
  stages {
//     stage ('Initialize') {
//       steps {
//         sh '''
//                 echo "PATH = ${PATH}"
//                 echo "M2_HOME = ${M2_HOME}"
//             ''' 
//       }
//     }
    {
        stage('Clone Repo') {
            steps {
                // Get some code from a GitHub repository
                git url: 'https://github.com/dineshshetty/Android-InsecureBankv2.git', branch: 'master'
            }
        }
    
    stage ('Check secrets') {
      steps {
      sh 'trufflehog3 https://github.com/dineshshetty/Android-InsecureBankv2.git -f json -o truffelhog_output.json || true'
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
                sh 'scp -o StrictHostKeyChecking=no /var/lib/jenkins/workspace/DemoProject-Mob/webgoat-server/target/webgoat-server-v8.2.0-SNAPSHOT.jar ubuntu@43.205.194.48:/WebGoat'
		sh 'ssh -o  StrictHostKeyChecking=no ubuntu@43.205.194.48 "nohup java -jar /WebGoat/webgoat-server-v8.2.0-SNAPSHOT.jar &"'
              }      
           }     
    }
    stage('Binary Analysis') {
            steps {
                script {
                    dir(INPUT_LOCATION) {
                        files = findFiles(glob: '*.apk')
                    }
                    echo 'Test Script files'
                    files.each { f ->
                        def TASK_COLLECTION = [:]
                        TASK_COLLECTION["MOBSF"] =  {
                            def AUTH_KEY = 'ce368c2a03dac6cb30e6afb7421dc7c345dcfb97368953238dbb709c5a8ec64a'
                            upload_cmd = "curl -F 'file=@${env.INPUT_LOCATION}${f}' http://localhost:8000/api/v1/upload -H 'Authorization:${AUTH_KEY}'"
                            upload_result = sh label: 'Upload Binary', returnStdout: true, script: upload_cmd

                            def response_map = readJSON text: upload_result
                            def app_type = response_map["scan_type"]
                            sh "echo  $app_type"
                            def app_hash = response_map["hash"]
                            sh "echo  $app_hash"
                            def app_name = response_map["file_name"]
                            sh "echo  $app_name"

                            scan_start_cmd = "curl -X POST --url http://localhost:8000/api/v1/scan --data 'scan_type=${app_type}&file_name=${app_name}&hash=${app_hash}' -H 'Authorization:${AUTH_KEY}'"
                            sh label: 'Start Scan of Binary', returnStdout: true, script: scan_start_cmd

                            def dateFormat = new SimpleDateFormat("yyyy_MM_dd_HH:mm")
                            def date = new Date()
                            def time =dateFormat.format(date)


                            scan_download_report="curl -# -o ${env.INPUT_LOCATION}/MobSF_Report_${time}.pdf -X POST --url http://localhost:8000/api/v1/download_pdf --data 'hash=${app_hash}' -H 'Authorization:${AUTH_KEY}'"
                            report_text = sh label: 'Start Scan of Download Report', returnStdout: true, script: scan_download_report
                            sh "echo $report_text"
                        }
                        parallel(TASK_COLLECTION)
                    }
                }
            }
        }
    stage ('Dynamic analysis') {
            steps {
           sshagent(['application_server']) {
                sh 'ssh -o  StrictHostKeyChecking=no ubuntu@65.0.76.237 "sudo docker run --rm -v /home/ubuntu:/zap/wrk/:rw -t owasp/zap2docker-stable zap-full-scan.py -t http://43.205.194.48/WebGoat -x zap_report || true" '
		sh 'ssh -o  StrictHostKeyChecking=no ubuntu@65.0.76.237 "sudo ./zap_report.sh"'
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
}
