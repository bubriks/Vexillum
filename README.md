[![Build Status](https://travis-ci.com/bubriks/Vexillum.svg?token=y4NB5cZzss8tCyNyKNzz&branch=master)](https://travis-ci.com/bubriks/Vexillum)

QUICK COMMANDS FOR VEXILLUM:
RabbitMq:
- to start rabbitmq on gcp:
-- sudo systemctl enable rabbitmq-server
-- sudo systemctl start rabbitmq-server
-- sudo rabbitmq-plugins enable rabbitmq_management

Java:
- to compile java files:
-- javac -cp '.:/home/ubuntu/Downloads/rabbitmq java client/lib/*' Send.java Recv.java

- to run the compiled java files:
-- java -cp '.:/home/ubuntu/Downloads/rabbitmq java client/lib/*' Send.java Recv.java

Smart contracts:
- to compile smart contrats:
-- solcjs ContractName.sol --bin --abi --optimize -o ./
- to wrap smart contracts to java: 
-- web3j solidity generate -a ContractName.abi -b ContractName.bin -o . -p SomeFileName
