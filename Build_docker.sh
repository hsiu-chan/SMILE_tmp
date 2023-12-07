docker image build -t smile .
docker run -d -p 7777:8888 --name smile smile
