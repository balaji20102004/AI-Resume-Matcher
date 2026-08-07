import re

# Standardize different names for the same skill
ALIASES = {
    "github": "git",
    "gitlab": "git",
    "js": "javascript",
    "nodejs": "node.js",
    "node js": "node.js",
    "reactjs": "react",
    "react.js": "react",
    "oops": "oop",
    "object oriented programming": "oop",
    "object-oriented programming": "oop",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "mysql/sql": "mysql",
    "sql/mysql": "mysql"
}

SKILLS = {
    "python","java","c","c++","c#","javascript","typescript","php",
    "go","rust","kotlin","swift",

    "html","css","react","angular","vue",
    "node.js","express","django","flask",
    "spring","spring boot","bootstrap",

    "sql","mysql","postgresql","mongodb",
    "oracle","sqlite","firebase",

    "machine learning","deep learning",
    "artificial intelligence","nlp",
    "computer vision","tensorflow",
    "pytorch","keras","scikit-learn",
    "opencv",

    "numpy","pandas","matplotlib",
    "seaborn","statistics",
    "data visualization","power bi",
    "tableau","excel",

    "aws","azure","gcp",
    "docker","kubernetes",
    "jenkins","git","github",

    "rest api","graphql",

    "oop","problem solving",
    "communication","leadership",
    "teamwork","agile","scrum",

    "linux","postman","jira",
    "eclipse","intellij",
    "visual studio code","vscode"
}

def extract_skills(text):

    text = text.lower()

    # Replace aliases with standard names
    for alias, standard in ALIASES.items():
        text = text.replace(alias, standard)

    found = set()

    for skill in SKILLS:
        if re.search(r"\b" + re.escape(skill) + r"\b", text):
            found.add(skill)

    return found