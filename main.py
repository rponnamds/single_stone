from data_python_engine.config import config
from data_python_engine.dependencies.spark_setup import start_spark
from data_python_engine.elt_scripts.file_handler import FileHandler
from data_python_engine.elt_scripts.spark_functions import join_dfs
from data_python_engine.elt_scripts.transform import DataTransformer
from utils.plugins.custom_logger import ensure_basic_logging
import logging


LOG_FORMAT = " %(asctime)s %(levelname)-8s : %(name)s %(message)s"
logger = logging.getLogger("spark_init")

@ensure_basic_logging(level=logging.INFO, format=LOG_FORMAT)
def main():
    student_file = config.input['student_file']
    teacher_file = config.input['teacher_file']
    report_file_path = config.output['report_file']
    schema_path = config.output['schema_json']
    print(student_file)
    print("-----------")
    run(student_file, teacher_file, report_file_path, schema_path)


def run(student_file, teacher_file, report_file_path, schema_path):
    """ Main driver function of data processor application """
    spark_session = start_spark()
    spark_session.conf.set("mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")
    file_handler = FileHandler(spark_session)
    try:
        student_df = file_handler.spark_read_file(student_file, delimiter='_')
        logger.info("Successfully loaded student file from %s", student_file)
        teacher_df = file_handler.spark_read_file(teacher_file)
        logger.info("Successfully loaded teacher file from %s", teacher_file)
    except FileNotFoundError as error_message:
        logger.error('Caught error: ' + repr(error))
        raise Exception

    joined_df = join_dfs(student_df, teacher_df, 'cid')
    logger.info("Finished joining dataframes")

    transformer = DataTransformer(spark_session, schema_path)
    output_df = transformer.fit_output_schema(joined_df)
    logger.info("Fit data to output schema:")
    output_df.show()

    print('report_file_path', report_file_path)
    file_handler.write_report(output_df, 'json', report_file_path)
    logger.info("Processing completed")

if __name__ == "__main__":
    main()
