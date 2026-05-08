import config
import services.dataset_indexer as di
import services.eda_service as eda

print("test")

test_data_frame = di.DatasetIndexer().build_dataframe()
print("test")
eda_service = eda.EDAService(test_data_frame, config.EDA_OUTPUT_DIR)
print("test")
print(eda_service)
print("test")
eda_service.save_class_distribution()
print("test")
eda_service.save_image_size_distribution()
print("test")
print(eda_service.build_summary())
