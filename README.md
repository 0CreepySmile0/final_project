# Final Project

---
- ## File included
|          Filename           | Description                                                                                                                                                                                                     |
|:---------------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|         database.py         | - Contain class Database which used for storing Table object </br>- class Table for storing data read from csv file </br>- Many _**"quality of life"**_ function included for easier work on project_manage.py  |
|      project_manage.py      | - Contain all class of each role and each class have their respective activities </br>- Including class Performance, this class use the value returned from login() function to perform activities of each role |
|         persons.csv         | - Contain information of all person                                                                                                                                                                             |
|          login.csv          | - Contain information necessary for login                                                                                                                                                                       |
|      Project_table.csv      | - Contain all project information _**(Initially empty, only header given)**_                                                                                                                                    |
| Member_pending_request.csv  | - Contain all history of request to be member _**(Initially empty, only header given)**_                                                                                                                        |
| Advisor_pending_request.csv | - Contain all history of request to be advisor _**(Initially empty, only header given)**_                                                                                                                       |

- ## How program work?
    It's simple, just run the program and follow this step!
    - login with you _**user**_ and _**password**_.
    - program will give you a _**set of choices**_ what you can do, simply enter _**index of choice**_ to do what you want. 
    - leave it empty by hitting Enter or input white space to exit the program.
    - all _**modified**_ data in the program will also _**re-write the csv file**_ so _**be careful!**_

- ## Action of each role
  - ### Admin
   | Action       | Method       | Class   | Completion in % |
   |--------------|--------------|---------|----------------:|
   | See Database | operation(1) | Admin   |            100% |
   | Create Table | operation(2) | Admin   |            100% |
   | Insert Data  | operation(3) | Admin   |            100% |
   | Update Table | operation(4) | Admin   |            100% |
   | Remove Table | operation(5) | Admin   |            100% |
   | Remove Row   | operation(6) | Admin   |            100% |

  - ### Student
   | Action          | Method       | Class   | Completion in % |
   |-----------------|--------------|---------|----------------:|
   | See Request     | operation(1) | Student |            100% |
   | Respond Request | operation(2) | Student |            100% |
   | Create Project  | operation(3) | Student |            100% |

  - ### Lead
   | Action              | Method       | Class | Completion in % |
   |---------------------|--------------|-------|----------------:|
   | See Project Status  | operation(1) | Lead  |            100% |
   | Modify Project Info | operation(2) | Lead  |            100% |
   | See Pending Request | operation(3) | Lead  |            100% |
   | Send Request        | operation(4) | Lead  |            100% |

  - ### Member
   | Action              | Method       | Class  | Completion in % |
   |---------------------|--------------|--------|----------------:|
   | See Project Status  | operation(1) | Member |            100% |
   | Modify Project Info | operation(2) | Member |            100% |
   | See Pending Request | operation(3) | Member |            100% |

  - ### Faculty
   | Action                | Method       |  Class  | Completion in % |
   |-----------------------|--------------|---------|----------------:|
   | See Request           | operation(1) | Faculty |            100% |
   | Respond Request       | operation(2) | Faculty |            100% |
   | See Project table     | operation(3) | Faculty |            100% |
   | Evaluate Project [^1] | operation(4) | Faculty |            100% |

  - ### Advisor
   | Action                                               | Method       | Class   | Completion in % |
   |------------------------------------------------------|--------------|---------|----------------:|
   | See Project table                                    | operation(1) | Advisor |            100% |
   | Approve Project you are advising [^1]                | operation(2) | Advisor |            100% |
   | Approve Project's final report you are advising [^1] | operation(3) | Advisor |            100% |

- ## Missing Features
    [^1] : I assume these activities done outside the program, so these action only update the csv file.

- ## Bug
    Currently, I haven't found the little or outstanding one yet. I already debug most little one for now.

