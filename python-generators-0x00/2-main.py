import sys

processing = __import__('1-batch_processing')
##### print processed users in a batch of 50
try:
    for batch in processing.batch_processing(50):
        print("Filtered Batch:")
        for user in batch:
            print(user)
except BrokenPipeError:
    sys.stderr.close()