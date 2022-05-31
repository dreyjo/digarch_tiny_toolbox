#this small program creates "fake packages"
#that look like what we create
#from file transfers


#needed libraries:
import os



#get the collection number
coll = input('please give the collection number beginning with M: ')
#get destination path
dest = input('please give path to destination of fake packages: ')
#get the range of numbers
start = int(input('please give first number of media carrier range: '))
end = int(input('please give last number of media carrier range:  '))

def make_fake_packages(coll=coll, dest=dest, start=start, end=end):
    media = []
    subdirs = ['metadata', 'objects']
    media_range = ["%.4d" % i for i in range(start, (end+1))]
    for item in media_range:
        path = os.path.join(dest, coll)
        name = f'{coll}_{item}_bag'
        mpath = os.path.join(path,name)
        media.append(mpath)
        print(mpath)


    for item in media:
        for dir in subdirs:
            try:
                os.makedirs(os.path.join(item, dir))
            except FileExistsError:
                pass


        # meta = os.path.join(item, 'metadata')
        # obj = os.path.join(item, 'objects')
        # if not os.path.exists(meta):
        #     os.makedirs(meta)
        # if not os.path.exists(obj):
        #     os.makedirs(obj)
        # for dir in subdirs:
        #     os.makedirs(os.path.join(item, dir), exist_ok=True)
        # #os.makedirs(os.path.join(item, 'objects'))





def main():
    make_fake_packages()


if __name__ == '__main__':
    main()
    exit(0)
