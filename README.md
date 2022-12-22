# cava-tiler

Home of the CAVA Lambda Tiler powered by [TiTiler](https://developmentseed.org/titiler/).

## Deployment

The Lambda stack is also deployed by the [AWS CDK](https://aws.amazon.com/cdk/) utility. Under the hood, CDK will create the deployment package required for AWS Lambda, upload it to AWS, and handle the creation of the Lambda and API Gateway resources.

1. Assuming that conda is installed, create a new environment with `python=3.8`.

    ```bash
    conda create -n cava-tiler -c conda-forge python=3.8
    ```

2. Activate and install `nodejs=14` into the conda environment.

    ```bash
    conda activate cava-tiler
    conda install -c conda-forge nodejs=14
    ```

3. Install CDK and connect to your AWS account.

    ```bash
    # install package
    pip install -e .

    # install cdk dependencies
    pip install -r deployment/requirements.txt
    npm install

    # Deploys the CDK toolkit stack into an AWS environment
    npm run cdk bootstrap
    ```

4. Pre-Generate CFN template

    ```bash
    # Synthesizes and prints the CloudFormation template for this stack
    npm run cdk synth
    ```

5. Update settings in a `.env` file.

    ```env
    TITILER_STACK_STAGE=production
    TITILER_STACK_NAME=titiler
    TITILER_STACK_MEMORY=6016
    ```

6. Deploy

    ```bash
    # Deploys the stack(s) titiler-lambda-production in deployment/app.py
    npm run cdk deploy
    ```
