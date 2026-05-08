import config
import services.dataset_indexer as di
import services.eda_service as eda

test_data_frame = di.DatasetIndexer().build_dataframe()

eda_service = eda.EDAService(test_data_frame, config.EDA_OUTPUT_DIR)
print(eda_service)
eda_service.save_class_distribution()
eda_service.save_image_size_distribution()
print(eda_service.build_summary())
