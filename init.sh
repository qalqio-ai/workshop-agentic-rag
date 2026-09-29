#!/bin/bash
##eval "(ssh-agent -c)"
##ssh-add ~/.ssh/id_ed25519

#cd ~/Downloads
#chmod +x init-git-repo.sh
#git@github.com:qalqio-ai/workshop-agentic-rag.git

#…or create a new repository on the command line
#echo "# workshop-agentic-rag" >> README.md
#git init
#git add README.md
#git commit -m "first commit"
#git branch -M main
#git remote add origin git@github.com:qalqio-ai/workshop-agentic-rag.git
#git push -u origin main
#…or push an existing repository from the command line
#git remote add origin git@github.com:qalqio-ai/workshop-agentic-rag.git
#git branch -M main
#git push -u origin main

git clone git@github.com:qalqio-ai/workshop-agentic-rag.git
./init-git-repo.sh git@github.com:qalqio-ai/workshop-agentic-rag.git "$HOME/Projects/workshop-agentic-rag"
