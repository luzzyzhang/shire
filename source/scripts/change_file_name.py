import os


target_dir = os.path.realpath('./chapters/')


for name in os.listdir(target_dir):
    print(name)
    if name.endswith('.rst'):
        name = os.path.join(target_dir, name)
        new_name = os.path.join(target_dir, name.replace('_', '-'))
        os.rename(name, new_name)

