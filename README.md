# chat-sync

## Requirements 
The main directory should include a database_creds.json file where the credentials to the MongoDB Atlas cluster will be read by the server using the following format: 
```
{
   "username" : "user",
   "password" : "password"
}
```

The security directory should include a config.py file where the JWT Token Algorithm, secret key and token timeout limit is specified in the following format: 

```
SECRET_KEY = "some_super_secret"  
ALGORITHM = "some_algo"  
ACCESS_TOKEN_EXPIRE_MINUTES = 60 
```


## Getting Started 
Here's a streamlined guide to get you started with a clean development environment using Visual Studio Code's Remote Development Containers:

## Prerequisites 
- Visual Studio Code: Download and install the latest version of VS Code from the official website: https://code.visualstudio.com/download
- Docker Desktop: Install Docker Desktop for your operating system. Refer to the official Docker documentation for installation instructions: https://www.docker.com/products/docker-desktop/ 
- VS Code Remote Development Extension Pack: This extension pack provides the necessary functionality to work with remote development containers within VS Code. You can install it directly within VS Code by following these steps:

   1. Open VS Code.
   2. Go to the Extensions panel (usually on the left side).
   3. Search for "Remote Development" in the Extensions marketplace.
   4. Look for the "Remote Development Pack" by Microsoft (official extension). Install this extension pack.

## Setup Steps 
   1. Clone the Repository (Using VS Code): Use Git to clone the project repository to your local machine. You can use your preferred Git client or the command line
   2. Open VS Code and Use Remote Development:

      - Open the cloned project directory in VS Code.

      - In VS Code, locate the Remote Containers icon in the status bar (usually looks like a container symbol) and click on it. Select "Reopen in Container" from the menu.

      - VS Code will detect the presence of the .devcontainer.json file and use its configuration to build and launch the development container environment. This includes the base Docker image, volumes, ports, and any other configurations specified in the file.
   3. Install Project Dependencies (Inside the Container):
      - Once connected to the development container, you'll need to install the project's dependencies listed in the requirements.txt file. Open the integrated terminal within the container and run the following command:
      ```
      sudo apt-get update && sudo apt-get install pip
      pip install -r requirements.txt
      ```
   4. Congratulations! 
      - You've successfully connected to the development container for this project. 
      - The container environment is pre-configured with the necessary tools and dependencies based on the .devcontainer.json file. 
      - You can now start developing and testing the project efficiently.





