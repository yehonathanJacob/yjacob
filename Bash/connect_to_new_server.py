connect to the server:
ssh -i ".ssh/yjacob_try.pem" ubuntu@ec2-3-17-36-43.us-east-2.compute.amazonaws.com
OR
ssh -i ".ssh/yjacob_try.pem" ubuntu@3.17.36.43
#####################################################
create new user with root permition:
https://coderwall.com/p/j5nk9w/access-ec2-linux-box-over-ssh-without-pem-file

#######################################################
create an option to connect to server without password:
http://www.linuxproblem.org/art_9.html
a@A:~> ssh-keygen -t rsa
a@A:~> ssh b@B mkdir -p .ssh
a@A:~> cat .ssh/id_rsa.pub | ssh b@B 'cat >> .ssh/authorized_keys'
a@A:~> ssh b@B
#######################################################
create an option to essy connect to server:
https://www.cyberciti.biz/faq/create-ssh-config-file-on-linux-unix/
https://serverfault.com/questions/253313/ssh-returns-bad-owner-or-permissions-on-ssh-config
vi ~/.ssh/config
(in the file)
Host server1
HostName 3.17.36.43
User yonathan
(exit)
chmod 600 ~/.ssh/config
ssh server1
#######################################################