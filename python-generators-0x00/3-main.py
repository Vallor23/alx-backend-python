#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_paginate


try:
    page_num = 1
    for page in lazy_paginator(100):
        print(f"Page {page_num}:")
        for user in page:
            print(user)
        print("--------")
        page_num += 1
except BrokenPipeError:
    sys.stderr.close()