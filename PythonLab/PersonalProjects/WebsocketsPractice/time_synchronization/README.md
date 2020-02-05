# Explenations idea

to create a client-server softwer, where each client that is connected
to the server, will be able to sound and allert sound in the same time.

```JS
(new Date()).getTime();
//to get timestamp on local (client) machine.
```

JS: record time, send test request to server and wait for server
respond. Save this time as 2r. 

Now every time the server wants somthing to
start in the client side, the client know when actualy to start it.

Python: after getting a request to play something, and getting 
answer from all the clients are ready, send in multy process to all when to start.
(In next t time).