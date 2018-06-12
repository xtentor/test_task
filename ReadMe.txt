Добрый день. Высылаю вам ответ на тестовое задание, я сделал всё функциями и раздельно. 
Раскомментируйте нужную функцию и запустите скрипт. 
Результаты работы скрипта я сохраню в файл output.txt. т.к. я привязал домены к ипам, но любой старт/стоп меняет адреса, эластик я не цеплял.
Вот :)

    Create three A or CNAME records for the custom domain (like a.domain.com, b.domain.com, c.domain.com). If you don’t have one, please register free in pp.ua zone.

    functions.CreateMyInstances()


    Point them to three EC2 instances: 2xEC2 should be running, 1xEC2 should be in stopped state.

    functions.StopOneInstance()


    Determine the instance state using its DNS name (need at least 2 verifications: TCP and HTTP).

    functions.CheckStatus()


    Create an AMI of the stopped EC2 instance and add a descriptive tag based on the EC2 name along with the current date.

    functions.CreateAMI()


    Terminate stopped EC2 after AMI creation.

    functions.TerminateMyStopedInstance()


    Clean up AMIs older than 7 days.

    functions.DeleteAMIs()


    Print all instances in fine-grained output, INCLUDING terminated one, with highlighting their current state.

    functions.CheckStatus()


    Clean up all instances assigned to my name

    functions.AllMyStop()
    functions.AllMyTerminate()    

С ув. Алексей Колодка
