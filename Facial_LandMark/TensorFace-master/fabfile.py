import os,sys,logging,time
from fabric.api import env,local,run,sudo,put,cd,lcd,puts,task,get
from fabric.operations import local as lrun, run
from fabric.state import env
from settings import BUCKET_NAME
import data
import cv2
fileDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fileDir, "./openface/"))
from settings import USER,private_key,HOST
env.user = USER
env.key_filename = private_key
env.hosts = [HOST,]


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logs/fab.log',
                    filemode='a')

@task
def process_server(process_count=2):
    """
    :param process_count:
    :return:
    """
    with cd("workspace"):
        try:
            run("rm -rf fabfile.py")
            run("rm -rf output")
        except:
            pass
        put("fabfile.py","fabfile.py")
        run("mkdir output")
        for code in range(process_count):
            run("screen -S face_process_{} -d -m /home/ubuntu/anaconda/bin/fab process:{},{};sleep 5  ".format(code,code,process_count))


@task
def process(code,div):
    import openface
    import openface.helper
    import dlib
    from openface.alignment import NaiveDlib  # Depends on dlib.
    code = int(code)
    div = int(div)
    dlibModelDir = os.path.join(fileDir, "./openface/models/dlib")
    dlibFaceMean = os.path.join(dlibModelDir, "mean.csv")
    dlibFacePredictor = os.path.join(dlibModelDir,"shape_predictor_68_face_landmarks.dat")
    align = NaiveDlib(dlibFaceMean,dlibFacePredictor)
    dataset = data.Dataset()
    last = time.time()
    count = 0
    for model,key,img in dataset.get_images(BUCKET_NAME):
        if hash(key) % div == code:
            bb = align.getLargestFaceBoundingBox(img)
            aligned  = align.alignImg("affine", 224, img, bb)
            # print time.time() - last
            last = time.time()
            count += 1
            if not aligned is None:
                # print model,key,img.shape,bb,aligned.shape
                cv2.imwrite("output/face_{}".format(key.replace('/','_').replace('models','')),aligned)
                # cv2.imshow("test",aligned)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                # break
        if count % 20 == 0 and code == 0:
            local('aws s3 mv output/ s3://aub3data/output/ --recursive --storage-class "REDUCED_REDUNDANCY"  --region "us-east-1"')

@task
def notebook_server():
    """
    Run IPython notebook on an AWS server
    run("openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.key -out mycert.pem")
    c = get_config()
    c.NotebookApp.open_browser = False
    c.NotebookApp.ip = '0.0.0.0'
    c.NotebookApp.port = 8888
    c.NotebookApp.certfile = u'/home/ubuntu/mycert.pem'
    c.NotebookApp.enable_mathjax = False
    c.NotebookApp.password = u'{}'
    :return:
    """
    from IPython.lib.security import passwd
    sudo("/home/ubuntu/anaconda/bin/ipython notebook --ip=0.0.0.0  --NotebookApp.password={} --no-browser".format(passwd())) #--certfile=mycert.pem


@task
def notebook():
    """
    deactivate
    pip freeze > requirements.txt
    local("sudo port select --set python python27")
    local("sudo port select --set ipython ipython27")
    local("sudo port select --set pip pip27")
    local("sudo port select --set virtualenv virtualenv27")
    :return:
    """
    local("ipython-2.7 notebook")


@task
def setup():
    """
        install Tensorflow
        /Users/aub3/.ssh/cs5356
    """
    run("/home/ubuntu/anaconda/bin/pip install https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.6.0-cp27-none-linux_x86_64.whl")
    run("/home/ubuntu/anaconda/bin/pip install --upgrade fabric")
    run("/home/ubuntu/anaconda/bin/pip install --upgrade boto3")
    run("/home/ubuntu/anaconda/bin/pip install --upgrade dlib")
    run("/home/ubuntu/torch/install/bin/luarocks install dpnn")
    run("/home/ubuntu/torch/install/bin/luarocks install nn")
    run("/home/ubuntu/torch/install/bin/luarocks install image")
    run("/home/ubuntu/torch/install/bin/luarocks install torch")
    sudo("apt-get update")
    sudo("apt-get install -y awscli")
    upload()


@task
def download():
    get("/home/ubuntu/crfasrnn/","crfasrnn")

@task
def freeze():
    local("source ~/portenv/bin/activate;pip freeze >> requirements.txt")


@task
def connect():
    """
    Creates connect.sh for the current host
    :return:
    """
    fh = open("connect.sh",'w')
    fh.write("#!/bin/bash\n"+"ssh -i "+env.key_filename+" "+"ubuntu"+"@"+HOST+"\n")
    fh.close()

@task
def backup():
    get("/tmp/*.png",".")

@task
def upload():
    try:
        sudo("rm -rf workspace")
        run("mkdir workspace")
    except:
        pass
    put("*.py","workspace/")
    put("*.md","workspace/")
    put("*.ipynb","workspace/")
    put("*.sh","workspace/")
    for d in filter(os.path.isdir, os.listdir('.')):
        if not d.startswith('.'):
            put("{}".format(d),"workspace/")


"""
mogrify -resize '500x500' *.jpg

"""
