
Build aidoc-demo-base
------------------------
Only if conda env was changed

docker build -t aidoc-demo-base docker/demo-base -f docker/demo-base/Dockerfile      
docker tag aidoc-demo-base aidocdev/aidoc-demo-base 
 docker push aidocdev/aidoc-demo-base 


Build aidoc-demo:
------------------------------
In project root:

docker build -t aidoc-demo . -f docker/aidoc-demo/Dockerfile  
docker tag aidoc-demo aidocdev/demo
docker push aidocdev/demo


