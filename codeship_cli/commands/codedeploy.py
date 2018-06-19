# -*- coding: utf-8 -*-
import boto3
import sys
import time
import datetime

codedeploy = boto3.client('codedeploy')

def format_time(diff):
    return str(diff).split('.')[0]

def deployment_error(deployment_id):
    try:
        response = codedeploy.get_deployment(
            deploymentId=deployment_id
        )
        return response['deploymentInfo']['errorInformation']['message']
    except:
        return ""

def deployment_status(deployment_id):
    try:
        response = codedeploy.get_deployment(
            deploymentId=deployment_id
        )
        return response['deploymentInfo']['status']
    except:
        return ""

def deployments_going_on(args):
    deployments = []
    print("\nChecking if has deployments going on...")
    for deployment_group in args.deployment_groups:
        application_name, deployment_group = deployment_group.split(':')

        response = codedeploy.list_deployments(
            applicationName=application_name,
            deploymentGroupName=deployment_group,
            includeOnlyStatuses=['InProgress', 'Created', 'Queued']
        )

        if not response['deployments']:
            print("-> OK: (no deployments %s/%s)" % (application_name, deployment_group))
            continue

        deployments.append((application_name, deployment_group, response['deployments'][0]))
    return deployments

def create_deployments(args):
    deployments = []
    for deployment_group in args.deployment_groups:
        application_name, deployment_group = deployment_group.split(':')
        if not deployment_group:
            raise "Can not find deployment_group name"

        res = codedeploy.create_deployment(
            applicationName=application_name,
            description="Deploy created by custom script",
            deploymentGroupName=deployment_group,
            deploymentConfigName=args.deployment_config_name,
            autoRollbackConfiguration={
                "enabled": args.enable_rollback,
                "events": [ "DEPLOYMENT_FAILURE" ]
            },
            revision={
                "revisionType": "S3",
                "s3Location": {
                    "bucket": args.s3_bucket,
                    "key": args.s3_bucket_key,
                    "bundleType": args.bundle_type
                }
            }
        )

        started_time = datetime.datetime.now()
        deployments.append((application_name, deployment_group, res['deploymentId'], started_time))
    return deployments

def command(args=None):

    started_time = datetime.datetime.now()

    deployments = deployments_going_on(args)

    # if has some deployments, exit with error
    if len(deployments) > 0:
        print("Error: Deployments going on at moment on Codedeploy")
        for deployment in deployments:
            print("-> Application: %s DeploymentGroup: %s Id: %s" % deployment)
            print('CodeDeploy: https://console.aws.amazon.com/codedeploy/home?region=us-east-1#/deployments/%s' % deployment[2])
        sys.exit(1)

    # if no deployments and action equal test, exit with success
    if args.codedeploy_action == 'test':
        print("\nNice! Codedeploy is ready to deploy!")
        sys.exit(0)

    print("\nPreparing to deploy release file s3://%s/%s" % (args.s3_bucket, args.s3_bucket_key))
    created_deployments = create_deployments(args)

    for deploy in created_deployments:
        print(' * Created: %s/%s #%s at %s'.decode('utf-8') % deploy)
        print('  -> CodeDeploy: https://console.aws.amazon.com/codedeploy/home?region=us-east-1#/deployments/%s\n' % deploy[2])

    deploy_finished = {}
    while True:
        deploy_success=True
        diff = datetime.datetime.now() - started_time
        print("============= %s =============" % format_time(diff))

        for deploy in created_deployments:

            application = deploy[0]
            deployment_group = deploy[1]
            deployment_id = deploy[2]
            deployment_group_started_time = deploy[3]

            status = deployment_status(deployment_id)

            if 'Succeeded' in status:
                if not deploy_finished.has_key(deployment_group):
                    deploy_finished[deployment_group] = datetime.datetime.now()

                diff = deploy_finished[deployment_group] - deployment_group_started_time
                print("Succeeded: %s | duration time: %s" % (deployment_group, format_time(diff)))
                continue

            if 'InProgress' in status:
                print("InProgress: %s" % deployment_group)
                deploy_success=False
                continue

            if 'Stopped' in status:
                print("DeployError: %s %s status=Stopped" % (deployment_group, deployment_id))
                sys.exit(1)
                continue

            if 'Failed' in status:
                print("DeployError: %s %s status=Failed" % (deployment_group, deployment_id))
                print(deployment_error(deployment_id))
                sys.exit(1)
                continue

            print("Waiting... %s deploy: %s %s" % (status, deployment_group, deployment_id))
            deploy_success=False
            time.sleep(2)

        if deploy_success:
            print("Finished!")
            sys.exit(0)

        time.sleep(args.log_refresh_time)
        print("\n")
