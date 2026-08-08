from pathlib import Path


# ============================================================
# DIRECTORIES
# ============================================================

RESUME_DIR = Path("resumes")
JD_DIR = Path("job_descriptions")

RESUME_DIR.mkdir(exist_ok=True)
JD_DIR.mkdir(exist_ok=True)


# ============================================================
# RESUME DATA
# ============================================================

resumes = [
    {
        "filename": "resume_01_full_stack.txt",
        "name": "Rahul Sharma",
        "summary": "Full Stack Developer with 5 years of experience building scalable web applications.",
        "skills": "React, TypeScript, Node.js, Express.js, MongoDB, REST APIs, AWS, Docker, Git",
        "experience": "5 years of experience developing full stack web applications.",
        "education": "B.Tech Computer Science, Delhi Technical University",
        "work": "Built scalable React applications and Node.js REST APIs. Designed MongoDB databases and deployed applications on AWS. Implemented JWT authentication and role-based access control."
    },
    {
        "filename": "resume_02_backend.txt",
        "name": "Amit Verma",
        "summary": "Backend Developer with 6 years of experience designing high-performance APIs and distributed systems.",
        "skills": "Python, Django, FastAPI, PostgreSQL, Redis, REST APIs, Docker, AWS, Git",
        "experience": "6 years of backend development experience.",
        "education": "B.Tech Information Technology, Pune University",
        "work": "Developed Django and FastAPI services. Designed PostgreSQL databases and optimized complex queries. Built REST APIs and deployed microservices using Docker and AWS."
    },
    {
        "filename": "resume_03_frontend.txt",
        "name": "Priya Singh",
        "summary": "Frontend Developer specializing in modern React applications and responsive user interfaces.",
        "skills": "React, JavaScript, TypeScript, HTML, CSS, Tailwind CSS, Redux, Git",
        "experience": "4 years of frontend development experience.",
        "education": "B.Tech Computer Science, RGPV University",
        "work": "Developed responsive React applications using TypeScript and Tailwind CSS. Built reusable components and optimized frontend performance."
    },
    {
        "filename": "resume_04_nodejs.txt",
        "name": "Vikas Mehta",
        "summary": "Node.js Developer experienced in building scalable backend services.",
        "skills": "Node.js, Express.js, JavaScript, MongoDB, PostgreSQL, REST APIs, Redis, Docker",
        "experience": "5 years of Node.js development experience.",
        "education": "B.E. Computer Engineering, Mumbai University",
        "work": "Built RESTful APIs using Node.js and Express. Designed MongoDB schemas and implemented Redis caching for high traffic applications."
    },
    {
        "filename": "resume_05_python.txt",
        "name": "Neha Gupta",
        "summary": "Python Developer with strong experience in backend systems and automation.",
        "skills": "Python, Django, Flask, FastAPI, PostgreSQL, REST APIs, Celery, Docker",
        "experience": "4 years of Python development experience.",
        "education": "MCA, Bangalore University",
        "work": "Developed Python backend applications using Django and FastAPI. Created asynchronous tasks using Celery and integrated PostgreSQL databases."
    },
    {
        "filename": "resume_06_java.txt",
        "name": "Arjun Patel",
        "summary": "Java Developer with experience developing enterprise applications and microservices.",
        "skills": "Java, Spring Boot, Hibernate, REST APIs, MySQL, Kafka, Docker, AWS",
        "experience": "7 years of Java development experience.",
        "education": "B.Tech Computer Science, Gujarat Technological University",
        "work": "Built Spring Boot microservices and enterprise REST APIs. Worked with Kafka messaging and MySQL databases."
    },
    {
        "filename": "resume_07_dotnet.txt",
        "name": "Karan Malhotra",
        "summary": ".NET Developer experienced in enterprise web applications.",
        "skills": "C#, .NET, ASP.NET Core, SQL Server, Entity Framework, Azure, REST APIs",
        "experience": "6 years of .NET development experience.",
        "education": "B.Tech Computer Science, Amity University",
        "work": "Developed ASP.NET Core applications and REST APIs. Designed SQL Server databases and deployed services using Microsoft Azure."
    },
    {
        "filename": "resume_08_data_scientist.txt",
        "name": "Sneha Kapoor",
        "summary": "Data Scientist with experience in machine learning, statistical analysis and predictive modeling.",
        "skills": "Python, Pandas, NumPy, Scikit-learn, TensorFlow, SQL, Machine Learning, Statistics",
        "experience": "5 years of data science experience.",
        "education": "M.Tech Data Science, IIT Hyderabad",
        "work": "Built predictive machine learning models using Python and Scikit-learn. Performed statistical analysis and created data pipelines using SQL."
    },
    {
        "filename": "resume_09_data_analyst.txt",
        "name": "Rohit Jain",
        "summary": "Data Analyst experienced in business intelligence and data visualization.",
        "skills": "SQL, Python, Excel, Power BI, Tableau, Pandas, Statistics",
        "experience": "4 years of data analytics experience.",
        "education": "B.Sc Statistics, Delhi University",
        "work": "Created business dashboards using Power BI and Tableau. Analyzed large datasets using SQL and Python and delivered actionable business insights."
    },
    {
        "filename": "resume_10_data_engineer.txt",
        "name": "Anjali Rao",
        "summary": "Data Engineer experienced in building reliable data pipelines and processing systems.",
        "skills": "Python, SQL, Apache Spark, Kafka, Airflow, AWS, Snowflake, ETL",
        "experience": "6 years of data engineering experience.",
        "education": "B.Tech Computer Science, Anna University",
        "work": "Built ETL pipelines using Python and Airflow. Processed large datasets using Apache Spark and implemented streaming pipelines with Kafka."
    },
    {
        "filename": "resume_11_ml_engineer.txt",
        "name": "Saurabh Mishra",
        "summary": "Machine Learning Engineer specializing in production ML systems.",
        "skills": "Python, TensorFlow, PyTorch, Scikit-learn, MLflow, Docker, Kubernetes, AWS",
        "experience": "5 years of machine learning engineering experience.",
        "education": "M.Tech Artificial Intelligence, IIT Delhi",
        "work": "Developed and deployed machine learning models using PyTorch and TensorFlow. Built ML pipelines using MLflow and Kubernetes."
    },
    {
        "filename": "resume_12_ai_engineer.txt",
        "name": "Meera Nair",
        "summary": "AI Engineer focused on NLP, generative AI and intelligent applications.",
        "skills": "Python, NLP, Transformers, PyTorch, LangChain, LLMs, OpenAI APIs, Vector Databases",
        "experience": "4 years of AI engineering experience.",
        "education": "M.Tech Artificial Intelligence, NIT Trichy",
        "work": "Built NLP and LLM-powered applications. Developed retrieval augmented generation systems using vector databases and transformer models."
    },
    {
        "filename": "resume_13_devops.txt",
        "name": "Vivek Kumar",
        "summary": "DevOps Engineer experienced in CI/CD, cloud infrastructure and automation.",
        "skills": "AWS, Docker, Kubernetes, Jenkins, GitHub Actions, Terraform, Linux, CI/CD",
        "experience": "6 years of DevOps experience.",
        "education": "B.Tech Computer Science, VTU",
        "work": "Built CI/CD pipelines using Jenkins and GitHub Actions. Managed Kubernetes clusters and AWS infrastructure using Terraform."
    },
    {
        "filename": "resume_14_cloud.txt",
        "name": "Pooja Sharma",
        "summary": "Cloud Engineer specializing in AWS infrastructure and scalable cloud architecture.",
        "skills": "AWS, EC2, S3, Lambda, VPC, CloudFormation, Terraform, Docker, Kubernetes",
        "experience": "5 years of cloud engineering experience.",
        "education": "B.Tech IT, Rajasthan Technical University",
        "work": "Designed AWS cloud infrastructure using EC2, S3, Lambda and VPC. Automated infrastructure using Terraform and CloudFormation."
    },
    {
        "filename": "resume_15_aws.txt",
        "name": "Nitin Agarwal",
        "summary": "AWS Engineer experienced in cloud migration and infrastructure management.",
        "skills": "AWS, EC2, RDS, S3, IAM, CloudWatch, Terraform, Linux",
        "experience": "7 years of AWS experience.",
        "education": "B.Tech Computer Science, Kurukshetra University",
        "work": "Migrated enterprise applications to AWS. Managed EC2, RDS and S3 infrastructure and implemented monitoring using CloudWatch."
    },
    {
        "filename": "resume_16_cybersecurity.txt",
        "name": "Aditya Singh",
        "summary": "Cybersecurity Engineer focused on application and network security.",
        "skills": "Cybersecurity, Network Security, SIEM, Linux, Python, Penetration Testing, OWASP, Firewalls",
        "experience": "5 years of cybersecurity experience.",
        "education": "M.Tech Cybersecurity, Amity University",
        "work": "Performed security assessments and penetration testing. Implemented SIEM monitoring and investigated security incidents."
    },
    {
        "filename": "resume_17_qa.txt",
        "name": "Riya Shah",
        "summary": "QA Engineer experienced in software testing and quality assurance.",
        "skills": "Manual Testing, Selenium, Java, API Testing, Postman, SQL, Jira, Test Automation",
        "experience": "4 years of QA experience.",
        "education": "B.Tech Computer Science, Gujarat University",
        "work": "Created automated Selenium test suites and performed API testing using Postman. Managed test cases and defect tracking through Jira."
    },
    {
        "filename": "resume_18_automation.txt",
        "name": "Deepak Joshi",
        "summary": "Automation Test Engineer experienced in UI and API automation.",
        "skills": "Selenium, Python, Playwright, Cypress, API Testing, Jenkins, Git, SQL",
        "experience": "5 years of automation testing experience.",
        "education": "B.Tech Information Technology, RTU",
        "work": "Developed UI automation using Selenium and Playwright. Created API automation frameworks and integrated tests into Jenkins pipelines."
    },
    {
        "filename": "resume_19_android.txt",
        "name": "Akash Verma",
        "summary": "Android Developer experienced in building modern mobile applications.",
        "skills": "Kotlin, Java, Android SDK, Jetpack Compose, Firebase, REST APIs, Git",
        "experience": "4 years of Android development experience.",
        "education": "B.Tech Computer Science, LNCT Bhopal",
        "work": "Built Android applications using Kotlin and Jetpack Compose. Integrated Firebase services and REST APIs."
    },
    {
        "filename": "resume_20_ios.txt",
        "name": "Isha Kapoor",
        "summary": "iOS Developer experienced in native mobile application development.",
        "skills": "Swift, SwiftUI, iOS SDK, Xcode, REST APIs, Firebase, Core Data",
        "experience": "5 years of iOS development experience.",
        "education": "B.Tech Computer Science, Pune University",
        "work": "Developed native iOS applications using Swift and SwiftUI. Integrated REST APIs, Firebase and Core Data."
    },
    {
        "filename": "resume_21_uiux.txt",
        "name": "Simran Kaur",
        "summary": "UI/UX Designer specializing in user-centered digital experiences.",
        "skills": "Figma, Adobe XD, UI Design, UX Research, Prototyping, Wireframing, Design Systems",
        "experience": "5 years of UI/UX design experience.",
        "education": "Bachelor of Design, NIFT Delhi",
        "work": "Designed mobile and web interfaces using Figma. Conducted UX research, usability testing and created design systems."
    },
    {
        "filename": "resume_22_business_analyst.txt",
        "name": "Manish Tiwari",
        "summary": "Business Analyst experienced in requirements gathering and process improvement.",
        "skills": "Business Analysis, SQL, Excel, Power BI, Requirements Gathering, Agile, Jira",
        "experience": "6 years of business analysis experience.",
        "education": "MBA Business Analytics, IIM Indore",
        "work": "Gathered business requirements and translated them into technical specifications. Created Power BI dashboards and worked with Agile teams."
    },
    {
        "filename": "resume_23_product_manager.txt",
        "name": "Kavita Sharma",
        "summary": "Product Manager experienced in building and launching technology products.",
        "skills": "Product Management, Agile, Scrum, Jira, Roadmaps, User Research, Analytics, SQL",
        "experience": "7 years of product management experience.",
        "education": "MBA, IIM Bangalore",
        "work": "Managed product roadmaps and coordinated cross-functional engineering teams. Conducted user research and analyzed product metrics."
    },
    {
        "filename": "resume_24_project_manager.txt",
        "name": "Rajiv Bansal",
        "summary": "Project Manager experienced in managing software development projects.",
        "skills": "Project Management, Agile, Scrum, Jira, Risk Management, Stakeholder Management, MS Project",
        "experience": "8 years of project management experience.",
        "education": "MBA Project Management, Symbiosis University",
        "work": "Managed software projects from planning to delivery. Coordinated engineering teams and handled project risks, budgets and stakeholder communication."
    },
    {
        "filename": "resume_25_dba.txt",
        "name": "Mohit Saxena",
        "summary": "Database Administrator experienced in enterprise database systems.",
        "skills": "PostgreSQL, MySQL, Oracle, SQL Server, Database Administration, Performance Tuning, Backup, Linux",
        "experience": "7 years of database administration experience.",
        "education": "B.Tech Computer Science, RGPV University",
        "work": "Managed PostgreSQL, MySQL and Oracle databases. Performed database tuning, backups, recovery and high availability configuration."
    },
    {
        "filename": "resume_26_architect.txt",
        "name": "Tarun Mehta",
        "summary": "Solutions Architect experienced in designing scalable enterprise systems.",
        "skills": "AWS, Azure, Microservices, Kubernetes, Docker, Java, Node.js, System Design",
        "experience": "10 years of software architecture experience.",
        "education": "M.Tech Computer Science, IIT Bombay",
        "work": "Designed cloud-native microservice architectures. Led technical architecture decisions involving AWS, Kubernetes, Docker and distributed systems."
    },
    {
        "filename": "resume_27_tech_lead.txt",
        "name": "Rakesh Yadav",
        "summary": "Technical Lead with extensive experience leading software engineering teams.",
        "skills": "Java, Spring Boot, React, AWS, Microservices, System Design, Docker, Kubernetes, Leadership",
        "experience": "9 years of software engineering experience.",
        "education": "B.Tech Computer Science, NIT Bhopal",
        "work": "Led engineering teams building enterprise applications. Designed microservices and reviewed architecture, code and deployment strategies."
    },
    {
        "filename": "resume_28_software_engineer.txt",
        "name": "Varun Singh",
        "summary": "Software Engineer experienced in developing scalable backend and web applications.",
        "skills": "JavaScript, Python, React, Node.js, PostgreSQL, REST APIs, Git, Docker",
        "experience": "3 years of software engineering experience.",
        "education": "B.Tech Computer Science, MANIT Bhopal",
        "work": "Developed React and Node.js applications. Built REST APIs and worked with PostgreSQL databases and Docker."
    },
    {
        "filename": "resume_29_react_native.txt",
        "name": "Ayesha Khan",
        "summary": "React Native Developer experienced in cross-platform mobile applications.",
        "skills": "React Native, React, JavaScript, TypeScript, Redux, Firebase, REST APIs, Android, iOS",
        "experience": "4 years of React Native development experience.",
        "education": "B.Tech Computer Science, Jamia Millia Islamia",
        "work": "Developed cross-platform mobile applications using React Native and TypeScript. Integrated Firebase and REST APIs."
    },
    {
        "filename": "resume_30_mlops.txt",
        "name": "Harsh Vardhan",
        "summary": "MLOps Engineer specializing in production machine learning infrastructure.",
        "skills": "Python, MLflow, Kubernetes, Docker, AWS, CI/CD, Terraform, Airflow, Machine Learning",
        "experience": "6 years of MLOps and machine learning infrastructure experience.",
        "education": "M.Tech Machine Learning, IIT Kanpur",
        "work": "Built ML deployment pipelines using MLflow and Kubernetes. Automated infrastructure with Terraform and created CI/CD pipelines for machine learning models."
    },
]


# ============================================================
# JOB DESCRIPTIONS
# ============================================================

job_descriptions = {
    "jd_01_full_stack.txt": """
JOB TITLE: Full Stack Developer

We are looking for a Full Stack Developer to build scalable web applications.

MUST HAVE:
- 3+ years of software development experience
- React
- Node.js
- JavaScript or TypeScript
- REST APIs
- MongoDB

NICE TO HAVE:
- AWS
- Docker
- CI/CD
- Git

RESPONSIBILITIES:
- Build responsive frontend applications.
- Develop scalable backend APIs.
- Design and maintain databases.
- Collaborate with engineering and product teams.
""",

    "jd_02_data_scientist.txt": """
JOB TITLE: Data Scientist

We are looking for a Data Scientist to develop machine learning and analytics solutions.

MUST HAVE:
- 3+ years of experience
- Python
- Machine Learning
- SQL
- Pandas
- Scikit-learn

NICE TO HAVE:
- TensorFlow
- PyTorch
- Statistics
- Data visualization

RESPONSIBILITIES:
- Build predictive models.
- Analyze large datasets.
- Develop machine learning solutions.
- Communicate insights to stakeholders.
""",

    "jd_03_backend_developer.txt": """
JOB TITLE: Backend Developer

We are looking for a Backend Developer to build scalable APIs and distributed services.

MUST HAVE:
- 5+ years of backend development
- Python
- Django or FastAPI
- PostgreSQL
- REST APIs

NICE TO HAVE:
- Docker
- AWS
- Redis
- Microservices

RESPONSIBILITIES:
- Design backend services.
- Develop REST APIs.
- Optimize database performance.
- Build scalable backend systems.
""",

    "jd_04_ml_engineer.txt": """
JOB TITLE: Machine Learning Engineer

We are looking for a Machine Learning Engineer to build and deploy production ML systems.

MUST HAVE:
- 4+ years of experience
- Python
- Machine Learning
- TensorFlow or PyTorch
- Docker

NICE TO HAVE:
- Kubernetes
- MLflow
- AWS
- CI/CD

RESPONSIBILITIES:
- Train machine learning models.
- Deploy models into production.
- Build ML pipelines.
- Monitor model performance.
""",

    "jd_05_frontend_developer.txt": """
JOB TITLE: Frontend React Developer

We are looking for a Frontend Developer to build modern web interfaces.

MUST HAVE:
- 3+ years of frontend development
- React
- JavaScript
- TypeScript
- HTML
- CSS

NICE TO HAVE:
- Redux
- Tailwind CSS
- Git
- UI/UX experience

RESPONSIBILITIES:
- Build reusable React components.
- Develop responsive interfaces.
- Optimize frontend performance.
- Work with backend engineers.
"""
}


# ============================================================
# CREATE RESUME FILES
# ============================================================

print("=" * 70)
print("CREATING RESUME DATASET")
print("=" * 70)

for resume in resumes:

    content = f"""\
{resume['name']}

SUMMARY

{resume['summary']}

SKILLS

{resume['skills']}

EXPERIENCE

{resume['experience']}

{resume['work']}

EDUCATION

{resume['education']}
"""

    path = RESUME_DIR / resume["filename"]

    path.write_text(
        content,
        encoding="utf-8"
    )

    print(f"Created: {path}")


# ============================================================
# CREATE JOB DESCRIPTION FILES
# ============================================================

print("\n" + "=" * 70)
print("CREATING JOB DESCRIPTIONS")
print("=" * 70)

for filename, content in job_descriptions.items():

    path = JD_DIR / filename

    path.write_text(
        content.strip(),
        encoding="utf-8"
    )

    print(f"Created: {path}")


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("DATASET CREATED")
print("=" * 70)

print(f"Resumes created       : {len(resumes)}")
print(f"Job descriptions      : {len(job_descriptions)}")

print("\nDataset is ready!")