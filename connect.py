import boto3
import functions

#Hello, to check any of required functions just uncomment them and run script.

#functions.CreateMyInstances()
#This function will create 3 instances and assign them on my name

#functions.StopOneInstance()
#This function will stop last instance from instances assigned to y name

#functions.TerminateMyStopedInstance()
#This function will terminate stopped instance

#functions.CheckStatus()
#This function checking status of instances assigned to my name

#functions.CreateSnapshot()
#This function create a snapshot of stopped instance(but I selected one of the instances because I didn't use elastic IPs and every instance start/stop changes IP address)

#functions.CreateAMI()
#This function create an AMI of stopped instance(but I selected one of the instances because I didn't use elastic IPs and every instance start/stop changes IP address)

#functions.DeleteAMIs()
#This function will delete AMIs older than 7 days(delete part is commented and replaced with "print")

#functions.AllMyStop()
#functions.AllMyTerminate()
#Those functions will clean up all my instances created for this task



