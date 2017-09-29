#### CheckRBL - A python application to check an IP against a list of RBLs (Realtime Blackhole lists) - *WIP*
  
##### Requirements

- Python 3.x
- dnspython

Install the requirements using `pip install -r requirements.txt`

##### Usage

```
# python checkrbl.py <ip-address>
```

##### Limitations

- Takes only 1 IP as input
- Python3 only
- Currently takes about ~3 to 4 minutes to query 236 RBLs 

##### TODO

- Tests
- Faster execution using either multithreading/multiprocessing or using another (better) approach
