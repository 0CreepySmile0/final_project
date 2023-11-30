# Describe what each role does

---
## Admin

---
- Managing the database
  - Can create table
  - Can update all tables
  - Can remove table
## Student

---
- See if there are pending requests to become members of already created projects
- Accept or deny the requests
  - Login table needs to be updated
  - Member_pending_request table needs to be updated
  - Project table needs to be updated
- Create a project and become a lead; must deny all member requests first
  - Project table needs to be updated
  - Login table needs to be updated
  - If more members needed, send out requests and update the Member_pending_request table; requests can only go to those whose role is student, i.e., not yet become a member or a lead
## Lead Student

---
- See project status (pending member, pending advisor, or ready to solicit an advisor)
- See and modify project information
  - Project table needs to be updated
- See who has responded to the requests sent out
- Send out requests to potential members
  - Member_pending_request table needs to be updated	
- Send out requests to a potential advisor; can only do one at a time and after all potential members have accepted or denied the requests
  - Advisor_pending_request table needs to be updated
## Member Student

---
- See project status (like pending member or advisor)
- See and modify project information
  - Project table needs to be updated
- See who has responded to the requests sent out
## Normal Faculty

---
- See request to be an advisor
- Accept or deny the requests
  - Login table needs to be updated
  - Advisor_pending_request table needs to be updated
  - Project table needs to be updated
- See details of all the project
- Evaluate projects
## Advising Faculty

---
- See request to be an advisor
- Accept or deny the requests
  - Login table needs to be updated
  - Accept for projects eventually serving as an advisor
  - Deny for projects not eventually serving as an advisor
- See details of all the project
- Approve the project
- Approve the final report