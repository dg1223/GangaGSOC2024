#!/usr/bin/env python3

j = Job(name='hello', backend=Local())
j.submit()

print(f"\nTo check the job's stdout, run the command: jobs({j.id}).peek('stdout')")
