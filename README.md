# Street View Cabinet Detection

## Installing the requirements for main.py

```bash
pip install googlemaps matplotlib numpy1~pip install googlemaps matplotlib numpy
```

## Training the model on AWS

To train the model on AWS, you need to have an EC2 instance with a GPU. The following steps are required to train the model:

1. Select an EC2 instance with a GPU. I used the `g4ad.2xlarge` instance with the Deep Learning AMI GPU PyTorch 2.0.0 (Amazon Linux 2). The AMI comes with most of the necessary packages pre-installed.

2. Since pip installation on root is not recommended (can cause issues with the speed of installation), create a new user and install the packages there. To create a new user, run the following commands:

```bash
sudo adduser <username>
sudo su - <username>
```

3. Creating new Conda environment:

```bash
conda create -n <env_name> python=3.7   # To create new env
conda init                              # To initialize conda (need a shell restart)
conda activate <env_name>               # Use this to activate the created env
```

4. Clone the YoloV7 repository on the EC2 instance:

```bash
git clone https://github.com/WongKinYiu/yolov7.git
```

5. Install the required packages:

```bash
pip install -r yolov7/requirments.txt
```

6. Edit the default coco.yaml file
    
The file you need to modify is the `yolov7/data/coco.yaml` file. Remove first four lines, define number of classes (1), remove the test folder line because we do not have tests and write correct paths to the train and validation folders.

7. Edit the default yoolv7.yaml file

For file `yolov7/models/yolov7.yaml` change the number of classes to 1.

8. TODO: Edit the last configuration file

TODO

9. Download the dataset

TODO - add link to the dataset

10. Start the training

```bash
python train.py --workers 1 --batch-size 8 --epochs 100 --img 640 640 --data data/coco.yaml --hyp data/hyp.scratch.custom.yaml --cfg cfg/training/custom.yaml --name swcd0 --weights yolov7.pt
```