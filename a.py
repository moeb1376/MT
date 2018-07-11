arabic = open('arabic.txt', 'w')
farsi = open('rahnama.txt', 'w')
with open('translate_dataset.txt', 'r') as f:
    for line in f:
        a = line.strip().split('|')
        print(a)
        if a[0].strip() != '':
            farsi.write(a[0])
            farsi.write('\n')
            arabic.write(a[1])
            arabic.write('\n')
arabic.close()
farsi.close()
