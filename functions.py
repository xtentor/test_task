import boto3, shlex,socket,subprocess, datetime
from datetime import datetime, timedelta
import requests

#Working
def CreateMyInstances():
    ec2 = boto3.resource('ec2')
    ids = []
    instances = ec2.create_instances(ImageId='ami-ca0135b3', InstanceType='t2.micro', MinCount=3, MaxCount=3, TagSpecifications=[{'ResourceType': 'instance','Tags': [{'Key': 'testinstance','Value': 'alexey-k'}]}])
    for instance in instances:
        ids.append(instance.id)
        print(instance.id, instance.instance_type)

    ec2.create_tags(
        Resources=ids,
        Tags=[
            {
                'Key': 'Name',
                'Value': 'alexey-k',
            },
        ],
    )

#Working
def StopOneInstance():
    ec2 = boto3.resource('ec2')
    ids = []
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['alexey*']}])
    for instance in instances:
        print(instance.id, instance.instance_type)
    ids.append(instance.id)
    print(ids)
    ec2.instances.filter(InstanceIds=ids).stop()

#Working
def TerminateMyStopedInstance():
    ec2 = boto3.resource('ec2')
    ids = []
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['alexey*']}, {'Name': 'instance-state-name', 'Values': ['stopped']}])
    for instance in instances:
        ids.append(instance.id)
    print(ids)
    ec2.instances.filter(InstanceIds=ids).terminate()

#Working
def AllMyStop():
    ec2 = boto3.resource('ec2')
    ids = []
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['alexey*']}])
    for instance in instances:
        ids.append(instance.id)
    print(ids)
    ec2.instances.filter(InstanceIds=ids).stop()

#Working
def AllMyTerminate():
    ec2 = boto3.resource('ec2')
    ids = []
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['alexey*']}])
    for instance in instances:
        ids.append(instance.id)
    print(ids)
    ec2.instances.filter(InstanceIds=ids).terminate()

def url_ok(url):
    try:
        r = requests.head(url, timeout=1, verify=False)
        return r.status_code == 200
    except requests.exceptions.RequestException as e:
        site=0

#Working
def CheckStatus():
    ec2 = boto3.resource('ec2')
    #domains=['google.com','yahoo.com','microsoft.com']
    domains=['a.crymea.ru','b.crymea.ru','c.crymea.ru']
    fakeaddr=['34.247.190.164', '34.243.28.28', '34.240.135.18']
    ids = []
    ips = []
    tcp_stat = []
    http_stat = []
    aws_stat = []
    curr_id = []
    curr_ip = []
    curr_aws = []
    c1=0
    c2=0
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['alexey*']}])
    for instance in instances:
        ids.append(instance.id)
        ips.append(instance.public_ip_address)
        aws_stat.append(instance.state['Name'])

    for domain in domains:
        address = socket.gethostbyname(domain)      #Uncomment to work with real domains
#        address=fakeaddr[c1]        #Comment to work with fake IPs
        command = 'ping -c 1 ' +address
        args = shlex.split(command)
        response_tcp = subprocess.Popen(args,stdout=subprocess.PIPE)
        response_tcp.wait()
        response_http = url_ok("http://" + domain)
        c2=0

        if response_tcp.poll():
            tcp_stat.append(0)
        else:
            tcp_stat.append(1)
        if response_http == 0:
            http_stat.append(1)
        else:
            http_stat.append(0)
        c1 += 1

        c2 = 0
        for ip in ips:
            if address == ip:
                id = ids[c2]
                aws = aws_stat[c2]
                curr_id.append(id)
                curr_ip.append(ip)
                curr_aws.append(aws)
            c2 += 1
    print
    print('Instance ID        | Status | Checked |  IP address   ')
    print
    for instance in instances:
        c1=0
        for curr in curr_id:
            if instance.id == curr:
                if (tcp_stat[c1] == 1) and (http_stat[c1] == 1):
                    print curr, curr_aws[c1], '  Online   ', curr_ip[c1]
                else:
                    print curr, curr_aws[c1], '  Offline  ', curr_ip[c1]
            c1 += 1


def CreateSnapshot():
    ec2 = boto3.resource('ec2')
    ids = []
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['alexey*']}])
    for instance in instances:
        ids.append(instance.id)
    instance = ec2.Instance(ids[2])
    for device in instance.block_device_mappings:
        volume = device.get('Ebs')
        volume_id=volume.get('VolumeId')
    now = datetime.datetime.now()
    date_formated = now.strftime("%Y-%m-%d_%H-%M")
    description='-'.join((ids[2],date_formated))
    snapshot = ec2.create_snapshot(VolumeId=volume_id, Description=description)

#Working
def CreateAMI():
    ec2 = boto3.resource('ec2')
    ec = boto3.client('ec2')
    ids = []
    now = datetime.datetime.now()
    date_formated = now.strftime("%Y-%m-%d_%H-%M")
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['alexey*']}])
    for instance in instances:
        ids.append(instance.id)
    AMIid = ec.create_image(InstanceId=ids[2], Name=ids[2] + "_" + date_formated, Description="AMI of instance " + ids[2], NoReboot=True, DryRun=False)

#Working
def DeleteAMIs():
    ec2 = boto3.resource('ec2')
    myAccount = boto3.client('sts').get_caller_identity()['Account']
    images = ec2.images.filter(Owners=["self"])

    #for image in images:
        #print(image.creation_date)
    for image in images:
        created_at = datetime.strptime(
            image.creation_date, "%Y-%m-%dT%H:%M:%S.000Z")
        if created_at > datetime.now() - timedelta(7):
            print 'Actual -' + image.id
        else:
            print 'Delete - ' + image.id
            #This is real delete part:
            #amiResponse = ec.deregister_image(
            #    DryRun=False,
            #    ImageId=image.id,
            #)