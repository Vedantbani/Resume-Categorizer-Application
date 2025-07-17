import pandas as pd
import random

# Job role detailed information
job_role_details = {
    'Data Scientist': {
        'Skills': 'Python, Machine Learning, SQL, Pandas, TensorFlow, Data Visualization',
        'Salary': '₹8-18 LPA',
        'Companies': 'Google, Amazon, Microsoft, TCS, Infosys',
        'Industry': 'IT Services, AI Startups, Product Companies',
        'Growth': 'Data Scientist → Senior Data Scientist → ML Engineer → Data Science Manager'
    },
    'Web Developer': {
        'Skills': 'HTML, CSS, JavaScript, React, Node.js, Express',
        'Salary': '₹4-12 LPA',
        'Companies': 'Wipro, Cognizant, Accenture, Infosys, Mindtree',
        'Industry': 'IT Services, Web Agencies, Product Companies',
        'Growth': 'Web Developer → Senior Web Developer → Tech Lead → Frontend/Backend Architect'
    },
    'Java Developer': {
        'Skills': 'Java, Spring Boot, REST API, Microservices, Hibernate',
        'Salary': '₹5-14 LPA',
        'Companies': 'TCS, Infosys, Capgemini, Cognizant, Accenture',
        'Industry': 'IT Services, Banking Software, Enterprise Solutions',
        'Growth': 'Java Developer → Senior Java Developer → Technical Lead → Software Architect'
    },
    'Android Developer': {
        'Skills': 'Kotlin, Android Studio, Firebase, Jetpack Compose',
        'Salary': '₹4-10 LPA',
        'Companies': 'Swiggy, Zomato, Ola, Paytm, Byju’s',
        'Industry': 'App Development, Startups, Product Companies',
        'Growth': 'Android Developer → Senior Android Developer → Mobile Tech Lead → Product Manager'
    },
    'UI/UX Designer': {
        'Skills': 'Figma, Adobe XD, Prototyping, Wireframing, User Research',
        'Salary': '₹3-8 LPA',
        'Companies': 'Zoho, Freshworks, Practo, Startups',
        'Industry': 'Design Agencies, Product Startups, Consulting',
        'Growth': 'UI/UX Designer → Senior Designer → Design Lead → Product Designer'
    },
    'DevOps Engineer': {
        'Skills': 'Docker, Kubernetes, AWS, Jenkins, CI/CD, Linux',
        'Salary': '₹6-16 LPA',
        'Companies': 'Amazon, Flipkart, ThoughtWorks, Accenture',
        'Industry': 'Cloud Services, DevOps Consulting, Product Companies',
        'Growth': 'DevOps Engineer → Senior DevOps → DevOps Lead → Cloud Architect'
    },
    'Software Engineer': {
        'Skills': 'C++, Java, System Design, SDLC, Algorithms, Data Structures',
        'Salary': '₹5-15 LPA',
        'Companies': 'Google, Microsoft, Oracle, IBM, Infosys',
        'Industry': 'IT Services, Product Companies, MNCs',
        'Growth': 'Software Engineer → Senior Software Engineer → Lead Engineer → Engineering Manager'
    },
    'Python Developer': {
        'Skills': 'Python, Django, Flask, REST API, PostgreSQL',
        'Salary': '₹5-13 LPA',
        'Companies': 'Startups, Tech Mahindra, Capgemini, Mphasis',
        'Industry': 'Backend Development, SaaS Companies',
        'Growth': 'Python Developer → Senior Python Developer → Backend Lead → Technical Architect'
    }
}

# Dataset generation
data = {
    'Resume': [],
    'Job Role': [],
    'Skills Required': [],
    'Salary Estimate': [],
    'Top Companies': [],
    'Industry': [],
    'Growth Path': []
}

# Generate 200 samples
for _ in range(200):
    role = random.choice(list(job_role_details.keys()))
    details = job_role_details[role]
    skills_list = details['Skills'].split(', ')
    selected_skills = ', '.join(random.sample(skills_list, k=min(4, len(skills_list))))
    resume_text = f"Experienced in {selected_skills} and other related tools."

    data['Resume'].append(resume_text)
    data['Job Role'].append(role)
    data['Skills Required'].append(details['Skills'])
    data['Salary Estimate'].append(details['Salary'])
    data['Top Companies'].append(details['Companies'])
    data['Industry'].append(details['Industry'])
    data['Growth Path'].append(details['Growth'])

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("IT_Job_Details_Dataset.csv", index=False)
print("Dataset Generated and Saved as IT_Job_Details_Dataset.csv")
