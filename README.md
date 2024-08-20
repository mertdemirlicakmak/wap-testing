# WAP testing (Twitch GUI Automation)

This script runs following steps:

1. go to Twitch
2. click in the search icon
3. input StarCraft II
4. scroll down 2 times
5. Select one streamer
6. on the streamer page wait until all is load and take a screenshot

## Prerequisites
- Create a virtual environment (Python 3.12)
- Install requirements via pip:
`pip install -r requirements.txt`
- Run test with: 
`python run_wap_test.py`