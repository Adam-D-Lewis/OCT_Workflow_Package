def writePause(file, delay_in_seconds):
    #writePause(file, delay_in_seconds):
    delay_in_microseconds = delay_in_seconds*10**6
    # file.write("<LongDelay>" + str(delay_in_microseconds) + "</LongDelay>\n") #wrong way to do it
    file.write("<LongDelay>{0:.0f}</LongDelay>\n".format(delay_in_microseconds))