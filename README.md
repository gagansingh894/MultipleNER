# MultipleNER

## Objective
    The goal of this project is create NER system which is capable of identifying
    -> ORGANIZATION
    -> LOCATION
    -> ADDRESS
    -> PRODUCT
    -> SERIAL
    
    Once the NER is done, we have to also create cluster i.e group together similar text

## My Approach
### Design
    Since the goal is to identify different entities from text, my idea was to design
    a seperate system for each task and aggerate the result. Each system will perform the
    following tasks:
        -> ingest 
        -> preprocess data
        -> detect entity
        -> create/update cluster
     
     These methods are implemented with the help of an interface. For each system, individual class
     is created which implements the base interface. All these classes are encapsulated
     inside DetectorSystem class which acts as the entrypoint to the system. Please refer diagram below
     
###  Diagram
![alt text](https://github.com/gagansingh894/MultipleNER/blob/main/diagram_drawio.png)     
 
 ### Basic Idea
    For performing entity detection, pretrained model from Stanford was used. The input text was
    processed by removing unwanted punctuation, tokenized and then fed to the classifier. The output
    from the model was post processed based on the system and is defined below sections. Apart from this,
    for PRODUCT entity detection, a manual corpus was created using retail data set. In order to create clusters,
    different approaches were which are also defined in below sections.
    
  
 #### ORG Detector
    In order to extract ORG from text, the tags were predicted using the pretrained model. For each part/phrase,
    prediction with ORGANIZATION tags was filtered. The results were stored in the dictionary. Using the results, the cluster was
    created using jaro_winkler string distance function with a threshold of 55.
 #### LOC Detector
    The approach is similar as to ORG Detector but instead of ORGANIZATION, prediction with LOCATION tags was filtered. In order to create clusters,
    the longitude and latitude was extracted for each location ard grouped based on distance.
    
 #### ADDRESS Detector
    Not Implemented. 
    The approach was 
        -> check number of punctuation ","
        -> contains postal code
        -> use a address parser like libpostal
        -> custum trained NER model
        
 #### PRODUCT Detector
    For this, predictions with O tag were filtered. The corresponding text was then
    compared with product names corpus. This corpus was manually created using flipkart dataset from
    here - https://www.kaggle.com/PromptCloudHQ/flipkart-products. In order to create clusters,
    the text was grouped using cosine distance with a threshlod of 75.
 
 #### SERIAL Detector
    Same logic as PRODUCT detector but along with filtering predictions based on O tag, an additional token filter
    was also applied i,e text which has O tag and is a single word and can contain both numbers and characters.
    In order to create cluster, python's set was used.
    
  
 #### Detection System
    In order to replicate streaming data, loops were used and since each system is implemented
    using classes the state was also preserved i.e what was the previous texts and cluster. This
    assisted in updating when new text was input.
    
 ## How to use
    -> Download StanfordNER from https://nlp.stanford.edu/software/stanford-ner-4.2.0.zip
    -> Created a directory in resource folder - stanford-ner
    -> Extract the contents from downloaded zip into stanford-ner folder
    -> Update paths in config.py file under utils. Please use absolute paths. 
    -> pip install -r requirements.txt
    -> Since we use nltk, u will need to download the additonal resources. I suggest to download all using mnltk.download() command.
