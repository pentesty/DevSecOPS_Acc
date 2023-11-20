
### This tool will parse the output of test and transform into json/csv, 
### Output would be further used for importing into other test/defect management tools (Ex -> Jira)

Below is the high level structure of this tool and its related files location. 

- a4mation 
  - docs
    - requirements.txt
  - src
    - lib
      - common.py
    - modules
      - devsecops_tool_parser
        - test_tools
          - zap_scan.py
          - truffle_hog3.py
          - dependency_check.py 
        - README.md
        - run_parser.py
    - testdata
      - devsecops_tool_parser
        - config.json
			

In addition to this, we will create logs and output_files folder in a4mation folder and 
add output csv/json and log file at the runtime.

To add any new tool, we need to add parser in <tool_name>.py format in test_tool directory 
and add condition in run_parser method to execute based on commandline input.

config.json file have configurable params like:
	csv_headers
	cwe_url
	log_filename
	log_level


You can use below steps to run this tool:
-----------------
1. Open cmd prompt/console
2. Go to src\modules\devsecops_tool_parser directory. 
cmd> cd src\modules\devsecops_tool_parser\

3. Run the tool
cmd> python run_parser.py -t <test> -p <test_output_file>

Example:
-----------------
Run below command to run the script and generate json output:
cmd> python run_parser.py -t "Trufflehog3 Scan" -p "D:\DevSecOps\truffelhog_output.json" 

Run below command to run the script to generate csv output:
cmd> python run_parser.py -t "Trufflehog3 Scan" -p "D:\DevSecOps\truffelhog_output.json" -o "consolidated_test_output.csv"

NOTE: This code is pending for review.
