import fiftyone as fo
import numpy as np
import os

# Creates YOLOV4 dataset
# Data split into train and test 
# train set in images/train_2022/ and test in /images/test_2022
# train files in ./data/train.txt and test files in ./data/test.txt

def create_yolo_dataset(dataset, train_test_split = 0.8, output_file_path='./data'):
    anno = [0, 0, 0, 0, 0]
    train_files = []
    test_files = []

    np.random.seed(42)
    new_base_path = os.getcwd()

    for sample in dataset:  
        old_image_file = sample['filepath']
        new_image_file = new_base_path + old_image_file.split("leopard_coco")[-1]
        
        new_anno_file = new_image_file.replace("jpg", "txt")
        if(np.random.random_sample() > train_test_split):
            new_image_file = new_image_file.replace("train", "test")
            test_files.append(new_anno_file+'\n')
        else:
            train_files.append(new_anno_file+'\n')
        
        new_path = '/'.join(new_image_file.split('/')[:-1])    
        isExist = os.path.exists(new_path)

        if not isExist:
            # Create a new directory because it does not exist 
            os.makedirs(new_path)    
         
        copy_str = 'cp ' + old_image_file + ' ' + new_image_file
        os.system(copy_str)
        
        anno[1:] = sample['ground_truth']['detections'][0]['bounding_box']
        with open(new_anno_file, 'w') as fp:
            for item in anno:
            # write each item on a new line
                fp.write("%s " % item)
            fp.write("\n")  
            
    isExist = os.path.exists(output_file_path)
    if not isExist:
            os.makedirs(output_file_path)      
            
    with open(output_file_path+'/test.txt', 'w') as fp:
        fp.writelines(test_files)         
    with open(output_file_path+'/train.txt', 'w') as fp:
        fp.writelines(train_files)         