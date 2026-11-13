# 577E Python Banking System
## Responsibilities of member A(Barish):Authentication,failed-attempts,60-second countdown,account blocking and password management.
## Member A ('auth.py'):login(usarnames and passwords),lockout and countdown(60-second waiting period after 3 incorrect attempts) ,  lockout(restarting the program doesnt change countdown or status)
### Permanent card blocking:Blocked account when failed attempts' count reachs 6
### Password management : pasword changing(demand current password and enforces strong password rules,rewriting ne password again)


## Member A ('users.json')
### Maintaining users' datas:Usernames,passwords,account numbers,failed attempts,transactions