# Phishing-Detection
## Extracting Emails &amp; Header Information from Outlook in Order to Detect Phishing Attacks using Python

#### Note: You can find a comprehensive article on this project at https://ghafoorazhar.medium.com/ 
#### Constrainst: Python3, Windows OS, Outlook Account

### Steps To Follow:
1. Clone this git repository: https://github.com/AzharGhafoor/Phishing-Detection
2. In ```main.py``` file find ```imap_password, imap_username```
3. Replace the values with your own outlook email and respective password
4. Run the script using: ```python main.py``` 
5. if you are interested in Jupyter Notebook then Run ```phishing_detection.ipynb```
6. I believe you already have installed the python modules used in this code, if not then go ahead and install them.
7. Sample Output:
```
+        It could be Phishing
Sender: gophish
Sent From: https://higee.net
Origional Sender:  ['bilal@higee.net']
Pretender Sender:  ['hiddenuser@company.com'] # dummy data

Sent From: https://emkei.cz
Origional Sender:  ['235@emkei.cz']
Pretender Sender:  ['hiddenuser@company.com'] # dummy data
```
