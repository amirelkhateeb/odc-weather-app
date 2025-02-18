# Weather App Project

🚀 **Project Overview**:  
This project automates the deployment of a Python-based weather application using Docker 🐳, Ansible 🤖, GitHub 📦, Jenkins 🤖, and Vagrant 🖥️. The project started by developing the application, then Dockerizing it, uploading the Docker image to Docker Hub 🌐, and automating the deployment process across virtual machines using Ansible. Finally, we created a Jenkins pipeline 🔄 to fully automate the workflow.
![217443148-60aa77bc-3a6c-45f1-a457-ba178b19a8dc](https://github.com/user-attachments/assets/304c5b89-6ac1-4c04-97f5-308fb306c329)
### What do we cover
Build and
 deploy on tomcat server
Setup CI/CD with github, jenkins, Maven and tomcat

- Setup Jenkins
- Setup and configure maven and git
- Setup jenkins 
- Integrate github, maven,server with jenkins
Create a CI and CD job
Test the deployment


## Technologies Used
- **Python 🐍**: The core language used for the weather application.
- **Docker 🐋**: Used for containerizing the Python application.
- **Docker Hub 🌐**: Public registry where the Docker image is stored.
- **Vagrant 🖥️**: Tool for creating virtual machine environments to deploy the application.
- **Ansible 🤖**: Automation tool for provisioning and deploying the Docker containers.
- **Jenkins 🤖**: Continuous Integration/Continuous Deployment (CI/CD) tool for automating the workflow.
- **GitHub 📦**: Version control system for managing project files.


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


##Setup Instructions

### 1. Clone the Repository
Clone the project repository to your local machine:

``` bash
 git clone https://github.com/amirelkhateeb/weather-app.git
 cd weather-app
```
### 2. Build and Push Docker Image
If you need to build the Docker image locally before pushing to Docker Hub, use these commands
``` bash
docker build -t weather-app .
docker push weather-app:latest
```
### 3. Set Up Vagrant Machines
in vagrantfile locate Create and start the Vagrant virtual machines:
``` bash
vagrant up
```
![Screenshot from 2025-02-18 17-51-07](https://github.com/user-attachments/assets/cbf63694-3410-40fc-a0b9-8192b962d9e6)

### 4. Run Ansible Playbook
![Screenshot from 2025-02-18 17-49-49](https://github.com/user-attachments/assets/6d9daa8a-1219-46f0-b083-139dae55ecf9)

Use Ansible to install Docker and deploy the application on the Vagrant machines
``` bash
ansible-playbook -i inventory playbook.yml
```



### 5. Run the Jenkins Pipeline
![Screenshot from 2025-02-18 16-33-28](https://github.com/user-attachments/assets/eec9fba7-926f-438d-8d2b-d3a2043b6355)

The Jenkins pipeline automates the entire process:

Pulls the latest code from GitHub.
Builds and pushes the Docker image to Docker Hub.
Deploys the application on the Vagrant machines using Ansible.
Sends an email notification once the process completes.
To trigger the Jenkins pipeline, ensure your Jenkins instance is set up with the relevant configurations and then run the pipeline.
### Running the Application on Vagrant Machines 🖥️🐳
![Screenshot from 2025-02-18 16-11-10](https://github.com/user-attachments/assets/573bd8df-6b86-4187-b53c-4fe6beb529e6)
![Screenshot from 2025-02-18 16-10-54](https://github.com/user-attachments/assets/f0c87cf0-8a57-4543-a5b0-052d3947cbf4)

- After successfully setting up and deploying the application, the weather app is now running on both Vagrant machines. Here's a quick 
  summary of what happened during the process:

### Docker Containers on Vagrant Machines:

The application Docker image was pulled from Docker Hub.
A Docker container was created and started on each machine.
Both containers are now running the weather application smoothly.
Application Output:
ذذذ
ذذ
```bash
# SSH into the first Vagrant machine
vagrant ssh ubuntu01

# Check running Docker containers
docker ps

# Access the application logs inside the container
docker logs <container-id>
```
Each Vagrant machine produces the expected weather data output.
Logs and application behavior can be monitored directly inside the running containers using Docker commands.
How to Verify: You can log in to each machine and verify the application is running properly by executing the following commands:


### Conclusion
This project demonstrates how to automate the full deployment cycle of a Python weather application using modern DevOps tools like Docker 🐋, Ansible 🤖, Jenkins 🔄, Vagrant 🖥️, and GitHub 📦. By using automation, we ensure that the deployment process is fast, reliable, and reproducible across multiple environments.

Note:
Replace the GitHub URL and Docker image references with the correct ones for your project.
If you have any specific configurations or files you want to highlight, feel free to modify the sections above.












