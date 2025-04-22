1.1 In my project, I am triggering a pythin code from a Unix shell script.
That unix shell script is scheduled via Tidal scheduler which captures the error based on exit status.
show me sample unix script which will set properly the exit status if my python code raises any exception

2.1 if i want to add " sys.exit(1)  or
    sys.exit(0) " should i add before tracemalloc.stop()  or after?
2.2 show me sample code