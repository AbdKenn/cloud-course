import json
import mass_price_regression.MASS_23_12.predict as predict

import time


def test_price_predict():
    with open("unit_test_mass_price_regression.json") as f:
        json_content = json.load(f)
    start = time.time()
    predicted_dict, x = predict.predict(predict.model, json_content, predict.out_data, predict.entite)
    print(predicted_dict)
    end = time.time()
    time_taken = round((end - start), 2)
    print("Time taken : ", time_taken, " seconds")

    # assert predicted == 27.16
    # assert predicted_dict == {'min': 29.163357, 'mean': 64.248344, 'max': 92.38669}


test_price_predict()
