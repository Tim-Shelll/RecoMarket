import joblib

path_to_model = 'models/model_LightFM.joblib'

def model(path_to_model: str):
    """
    Returns load model
    :param path_to_model str: path to file with model
    :return model_LightFM LightFM: model ML
    """
    model_LightFM = joblib.load(path_to_model)

    return model_LightFM

model_LightFM = model(path_to_model=path_to_model)