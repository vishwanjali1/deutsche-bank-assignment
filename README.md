# deutsche-bank-assignment

 # Step1: python -m venv venv

 # Step2: Activate venv
       '''
        venv\Scripts\activate 
      '''

# Step3: Install dependencies
        '''
       pip install -r requirements-dev.txt  
       '''

# Step4: Run tests
       '''
       pytest -v
       '''
# Step5: Build docker image
    '''
    docker build -t trade-store-api .
    '''
# Step6: Run application locally
    '''
    uvicorn app.main:app --reload
    Access application using : http://127.0.0.1:8000/docs  
    '''