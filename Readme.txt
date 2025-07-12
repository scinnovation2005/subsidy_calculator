project-root/
├── frontend/                
│   ├── index.html (Common feilds : State and Enterprise Size ) 
                    Enterprise size is asked since in some state(i.e. UP, Gujarat, Policies are based on Enterprise Size)
│   ├── main.js     (pdf_path and url for pdf gnerated to frontend )
│   ├── /state/.js (State specific inputs)
│   └── assets/              # Images, fonts, etc. (optional)
│
├── backend/                 # Flask API code
│   ├── subsidy_api.py (API to call process_/state/ function after selecting state)
│   ├── report_/state/.py (Latex code for report format. Separate format for each state.)
│   ├── subsidy_/state/.py (Calculation Logic for each state)
│   ├── requirements.txt        
