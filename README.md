# Weather App Project

🚀 **Project Overview**:  
This project automates the deployment of a Python-based weather application using Docker 🐳, Ansible 🤖, GitHub 📦, Jenkins 🤖, and Vagrant 🖥️. The project started by developing the application, then Dockerizing it, uploading the Docker image to Docker Hub 🌐, and automating the deployment process across virtual machines using Ansible. Finally, we created a Jenkins pipeline 🔄 to fully automate the workflow.

## Steps Involved

### 1. Python Application Development 🐍
The weather application was developed by the development team. It's a Python application that retrieves weather data from a source and processes it.

### 2. Dockerizing the Application 🐋
A Dockerfile was created to containerize the Python application. The Dockerfile contains all the instructions to build the environment, install dependencies, and run the application inside a Docker container.

### 3. Pushing Docker Image to Docker Hub ⬆️
After successfully building the Docker image locally, we pushed the image to Docker Hub for easy access from any environment that needs it.

### 4. GitHub Repository Creation 🧑‍💻
A GitHub repository was created to store the source code of the application and all configuration files, including the Dockerfile.
The project was cloned to our local machine and connected to the GitHub repository.

### 5. Setting Up Vagrant Machines 🖥️
We created two Vagrant virtual machines with Ubuntu as the operating system. These machines were provisioned for testing and deploying the application.
The Vagrant machines were used as the target hosts where the Docker containers will run.

### 6. Using Ansible for Automation 🤖
We used Ansible to automate the deployment process:
- Ansible installs Docker on the Vagrant machines.
- It pulls the Docker image from Docker Hub.
- After pulling the image, Ansible runs a Docker container on each Vagrant machine.

### 7. Jenkins Pipeline 🔄
A Jenkins pipeline was created to automate the entire workflow, which includes:
- Pulling the latest code from the GitHub repository.
- Building the Docker image.
- Pushing the Docker image to Docker Hub.
- Provisioning Vagrant machines and running the Ansible playbook.
- After completing the deployment, Jenkins sends an email notification 📧.

## Technologies Used
- **Python 🐍**: The core language used for the weather application.
- **Docker 🐋**: Used for containerizing the Python application.
- **Docker Hub 🌐**: Public registry where the Docker image is stored.
- **Vagrant 🖥️**: Tool for creating virtual machine environments to deploy the application.
- **Ansible 🤖**: Automation tool for provisioning and deploying the Docker containers.
- **Jenkins 🤖**: Continuous Integration/Continuous Deployment (CI/CD) tool for automating the workflow.
- **GitHub 📦**: Version control system for managing project files.

##Setup Instructions

### 1. Clone the Repository
Clone the project repository to your local machine:

``` bash ###git clone https://github.com/amirelkhateeb/weather-app.git
 cd weather-app ```














