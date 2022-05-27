import fiftyone as fo
import numpy as np
import os


# Creates YOLOV4 dataset
# Data split into train and test 
# train set in images/train_2022/ and test in /images/test_2022
# train files in ./data/train.txt and test files in ./data/test.txt

def create_yolo_dataset(dataset, train_test_split = 0.8, output_folder='./'):
    anno = [0, 0, 0, 0, 0]
    train_files = []
    test_files = []
       
    np.random.seed(42)
    
    train_image_path =  output_folder+'/data/obj'                   
    isExist = os.path.exists(train_image_path)                  
                    
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(train_image_path)    
                        
    test_image_path =  output_folder+'/images/test'                       
    isExist = os.path.exists(test_image_path)

    if not isExist:
        os.makedirs(test_image_path)                    

    for sample in dataset:  
        anno[1:] = sample['ground_truth']['detections'][0]['bounding_box']
        height = sample['metadata']['height']
        width = sample['metadata']['width']
        
        
        if anno[3] >=1.0:
            anno[3] = 1-1.0/width
            
        if anno[4] >=1.0:
            anno[4] = 1-1.0/height    

        anno[1] = anno[1]+0.5*anno[3]
        anno[2] = anno[2]+0.5*anno[4]       
       
       
            
        old_image_file = sample['filepath']
        train_image_file = 'data/obj/' + old_image_file.split("/")[-1]
        new_image_file = output_folder + '/images/test/' + old_image_file.split("/")[-1]                 
        
        if(np.random.random_sample() > train_test_split):        
            test_files.append(new_image_file+'\n')
        else:
            train_files.append(train_image_file+'\n')
            new_image_file =  output_folder+'/'+ train_image_file    
                        
        new_anno_file = new_image_file.replace("jpg", "txt")              
           
        copy_str = 'cp ' + old_image_file + ' ' + new_image_file
        os.system(copy_str)
        
        with open(new_anno_file, 'w') as fp:
            for item in anno:
            # write each item on a new line
                fp.write("%s " % item)
            fp.write("\n")  
    
   
    with open(output_folder+'/data/test.txt', 'w') as fp:
        fp.writelines(test_files)         
    with open(output_folder+'/data/train.txt', 'w') as fp:
        fp.writelines(train_files)  
        