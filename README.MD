Please make a python virtual environment using conda or pyenv or anything else and insert an API key from openweather into the environment

following this command (if using conda )

conda create -m "Environment-name" (Without quotes)

conda activate "Environment-name" (Without quotes)

conda env config vars set "Environment-varriable-name"="Your API key" (Without quotes)
example:
conda env config vars set API_KEY=RANDOM_API_KEY (Without quotes)

conda deactivate "Environment-name" (Without quotes)

conda update "Environment-name" (Without quotes)

conda activate "Environment-name" (Without quotes)

In the code (API_KEY) is the name of the environment variable .. change it accordingly to the key name that would be given 

I meant that it in place of API_KEY there should be Environment-name .

then print the key using os module

import os

api_key = os.getenv('API_KEY')
print(api_key)

or, in terminal use 

echo $API_KEY