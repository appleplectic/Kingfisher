# Setup(for will/levin)

1. Create a folder "sar-dataset" in the root directory. 
2. Add the "images" and "labels" folders into the sar-dataset folder.
3. In both of those folders, add a "train" and a "val" folder.
4. Ask daniel for a client_secrets.json file. Add that to the project.
5. Run gen_label_files.py, then download_images.py. Finally, run test_model.py and see the results.

NOTE: The pics used for download_images.py are randomly taken from the google drive;
so you guys will have to save a shared sar-dataset folder in order to do proper testing.
I think its prob too big to store on github but idk