import nso_ds_classes.nso_tif_kernel as nso_tif_kernel
import nso_ds_classes.nso_ds_models as nso_ds_models
import glob
from nso_ds_classes.nso_ds_models import cluster_annotations_stats_model 
from nso_ds_classes.nso_ds_normalize_scaler import normalize_scaler_class_BNDVIH 
import nso_ds_classes.nso_ds_cluster as nso_ds_cluster 
from os.path import exists


if __name__ == '__main__':

    # Set a kernel generator.
    x_kernel_width = 32
    y_kernel_height = 32


    for file in glob.glob("E:/data/coepelduynen/2022*ndvi_height.tif"):

        path_to_tif_file = file.replace("\\","/")
        print(path_to_tif_file)
        out_path = "E:/output/Coepelduynen_segmentations/"+path_to_tif_file.split("/")[-1].replace(".tif","_normalised_cluster_model.shp")
        tif_kernel_generator = nso_tif_kernel.nso_tif_kernel_generator(path_to_tif_file, x_kernel_width , y_kernel_height)
        cluster_centers_file = "./cluster_centers/normalized_5_BHNDVI_cluster_centers.csv"

               
        # Make clusters if a cluster file does not yet exist
        if exists(cluster_centers_file) is False:
            a_nso_cluster_break = nso_ds_cluster.nso_cluster_break(tif_kernel_generator)
            a_nso_cluster_break.get_stepped_pixel_df(output_name = path_to_tif_file.split("/")[-1], parts=2, begin_part=1, multiprocessing= True)
            
            a_nso_cluster_break.make_clusters_centers(cluster_centers_file)
        else:
            print("Previous cluster centers found")
            
        a_cluster_annotations_stats_model = cluster_annotations_stats_model(cluster_centers_file)

        # This model needs scalers in order to be useful.
        if exists("./scalers/"+path_to_tif_file.split("/")[-1]+"_band3.save") is False:
                print("No scalers found making scalers")
                a_nso_cluster_break = nso_ds_cluster.nso_cluster_break(tif_kernel_generator)
                a_nso_cluster_break.make_scaler_stepped_pixel_df(output_name = path_to_tif_file.split("/")[-1], parts=2, begin_part=1, multiprocessing= True)


        a_normalize_scaler_class_BNDVIH = normalize_scaler_class_BNDVIH( "./scalers/"+path_to_tif_file.split("/")[-1]+"_band3.save", \
                                                                            scaler_file_band5 = "./scalers/"+path_to_tif_file.split("/")[-1]+"_band5.save", \
                                                                            scaler_file_band6 = "./scalers/ahn4.save")



            
        tif_kernel_generator.predict_all_output_multiprocessing(a_cluster_annotations_stats_model, out_path , parts = 3, pixel_values=True, normalize= a_normalize_scaler_class_BNDVIH )