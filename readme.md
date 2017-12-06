# Logs Analysis
This programme analyzes the logs from the database and answers the following three questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Requirements:
1. Install git on your system. [Download here](https://git-scm.com/downloads)
2. This programme uses Linux-based virtual machine. Using git bash install the virtual machine. Instructions to install the virtual machine is 
[here](https://www.sitepoint.com/getting-started-vagrant-windows/)
3. Install Python language on the virtual machine.
4. Install PostgreSQL management system and psycopg2 connector on the virtual machine.

## How to use:
1. Open git bash and use the command `cd [DIRECTORY NAME]` to enter your shared vagrant directory.
2. Clone this repository into your shared vagrant directory using the command `git clone [URL]`.
3. Now use the command `vagrant up` to start your virtual machine.
4. Then use `vagrant ssh` to log in into the virtual machine.
5. Use `cd [DIRECTORY NAME]` to change your directory to **Logs-Analysis**.
6. Now run the command `python logs.py`
7. The output of the programme will be printed on your terminal window.
