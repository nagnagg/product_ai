import os
import pandas
main_dir = 'VOCDevkit/VOC2007/ImageSets/Main'
os.chdir(main_dir)
pwd = os.getcwd()
print(pwd)


def make_train_files():
    suffixs = ['_train','_val','_test']

    for suffix in suffixs:
        print('suffix',suffix)
        new_file = open('{}.txt'.format(suffix.replace('_','')),'w')
        text = ""
        for file in os.listdir():
            if file.find(suffix) == -1:continue
            with open(file) as f:
                if text == "":text = f.read()
                text =text +'\n'+ f.read()
        new_file.write(text)

def split_val_test(rate:float):
    val = pandas.read_csv('val.txt')
    val = val.sample(frac=1)
    print('len',len(val))
    split = int(len(val) * rate)
    test = val.values
    val[:split].to_csv('val.txt',index=False)
    val[split:].to_csv('test.txt',index=False)
    print('val.txt',split)
    print('test.txt',len(val) - split)

if __name__ == '__main__':
    val_rate = 0.33
    make_train_files()
    split_val_test(val_rate)
