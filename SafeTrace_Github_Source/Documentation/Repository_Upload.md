# Upload the repository
The connected GitHub account has pull=true and push=false for SbGit05/Tata_Techpulse. No files were pushed.

Use the repo owner's account or obtain collaborator write access. With GitHub Desktop: sign into the account with write access, clone this repository, copy the **contents** of the supplied submission folder into the clone, review the changed files, commit, and push main. Keep private signatures and the confidential case-study source document out of a public repository.

Alternatively from the parent directory in PowerShell:
```powershell
git clone https://github.com/SbGit05/Tata_Techpulse.git
Copy-Item -Path .\PCCOE_ShreedharBargaje_123B1F006_CS2_AIML\* -Destination .\Tata_Techpulse\ -Recurse -Force
cd Tata_Techpulse
git add .
git commit -m "Add CS2 SafeTrace HARA implementation and evaluation"
git push -u origin main
```
A separate repository-ready source archive is provided with unsigned documents and no confidential supplied case-study PDF. Verify the actual online Code directory and README after pushing.
